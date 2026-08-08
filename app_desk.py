"""
Bank Universe — landing view (reference implementation)

DROP-IN STATUS: this is a *reference*, not copy-paste-ready. The three seams
marked `# >>> WIRE:` must be connected to the scoring code that already exists
in this app (the same code the /analyze POST path uses today). Everything else
— shaping, filtering, movers, entrants, caching — is complete.

The design intent: the landing page is the screen ALREADY RUN. No form gates
it. Filters refine a live result; the bank/quarter picker survives only as an
on-demand "Custom screen" drawer that still POSTs to /analyze exactly as before.
"""

from dataclasses import dataclass
from flask import render_template, request

# How many top-composite banks the landing ledger shows. The desk reads this
# list top-down; beyond ~30 rows nobody scrolls. Tune, don't remove.
PRESCREEN_N = 25

# A bank is "in the top decile" at or above this rank. Recomputed per quarter
# from the real universe size rather than hardcoded.
TOP_DECILE_FRACTION = 0.10

ASSET_BANDS = [
    ("0-250000",            "Under $250M",   0,          250_000),
    ("250000-500000",       "$250M – $500M", 250_000,    500_000),
    ("500000-1000000",      "$500M – $1B",   500_000,    1_000_000),
    ("1000000-3000000",     "$1B – $3B",     1_000_000,  3_000_000),
    ("3000000-10000000",    "$3B – $10B",    3_000_000,  10_000_000),
    ("10000000-",           "Over $10B",     10_000_000, None),
]


def band_of(assets_raw):
    """Asset-size band key for a raw asset figure (thousands, as in the workbook)."""
    if assets_raw is None:
        return None
    for key, _label, lo, hi in ASSET_BANDS:
        if assets_raw >= lo and (hi is None or assets_raw < hi):
            return key
    return None


# ---------------------------------------------------------------------------
# Cached full-universe screen
# ---------------------------------------------------------------------------

_universe_cache = {}  # (as_of, settings_fingerprint) -> list[row]


def screen_universe(as_of, settings):
    """
    Score every bank in `as_of` against the full universe and return rows in the
    same shape results.html already consumes, plus prior-quarter fields.

    Scoring 4,500+ banks is not free — memoize on (as_of, settings fingerprint)
    and invalidate from the same place /refresh clears the workbook cache.
    """
    key = (as_of, settings.fingerprint())
    if key in _universe_cache:
        return _universe_cache[key]

    # >>> WIRE 1: run the existing scorer over the whole universe, not a
    # selection. This is the same call /analyze makes, with banks=None.
    rows = score_banks(as_of=as_of, banks=None, settings=settings)  # noqa: F821

    prior = prior_quarter(as_of)  # noqa: F821  # >>> WIRE 2: existing helper
    prior_rows = {}
    if prior:
        try:
            prior_rows = {r["key"]: r for r in score_banks(as_of=prior, banks=None, settings=settings)}  # noqa: F821
        except Exception:
            prior_rows = {}  # a missing back-quarter must never break the landing page

    for r in rows:
        p = prior_rows.get(r["key"])
        r["prev_composite"] = p["composite"] if p else None
        r["prev_rank"] = p["universe_rank"] if p else None
        r["delta"] = (
            round(r["composite"] - p["composite"])
            if p and r["composite"] is not None and p["composite"] is not None
            else None
        )

    _universe_cache[key] = rows
    return rows


def invalidate_universe_cache():
    """Call from the /refresh handler, next to the workbook cache clear."""
    _universe_cache.clear()


# ---------------------------------------------------------------------------
# What changed — the question the old landing page could not answer
# ---------------------------------------------------------------------------

def build_movers(rows, limit=5):
    scored = [r for r in rows if r.get("delta") is not None]
    scored.sort(key=lambda r: abs(r["delta"]), reverse=True)
    out = []
    for r in scored[:limit]:
        out.append({
            "key": r["key"],
            "bank": r["bank"],
            "delta": r["delta"],
            "composite": r["composite"],
            "prev_composite": r["prev_composite"],
            "driver": describe_driver(r),
        })
    return out


def describe_driver(r):
    """
    One short clause naming the signal that moved most. Deterministic — this is
    a scan aid on a dense page, not narrative copy, so it must not call the LLM.
    """
    moves = []
    for letter, field in (("A", "signal_a"), ("B", "signal_b"), ("C", "signal_c")):
        sig = r.get(field) or {}
        prev = (r.get("prev_" + field) or {}).get("score")
        if sig.get("score") is not None and prev is not None:
            moves.append((abs(sig["score"] - prev), letter, sig["score"] - prev, sig))
    if not moves:
        return "Composite re-ranked q/q"
    _, letter, change, sig = max(moves, key=lambda m: m[0])
    name = {"A": "Idle liquidity", "B": "Underwater book", "C": "Net income q/q"}[letter]
    return "%s %s %d pts" % (name, "up" if change > 0 else "down", abs(round(change)))


def build_entrants(rows, universe_total, limit=4):
    cutoff = max(1, int(universe_total * TOP_DECILE_FRACTION))
    out = [
        r for r in rows
        if r.get("universe_rank") and r["universe_rank"] <= cutoff
        and r.get("prev_rank") and r["prev_rank"] > cutoff
    ]
    out.sort(key=lambda r: r["universe_rank"])
    return out[:limit], cutoff


# ---------------------------------------------------------------------------
# The view
# ---------------------------------------------------------------------------

def home():
    settings = load_settings()          # noqa: F821  # >>> WIRE 3: existing loader
    quarters = detect_quarters()        # noqa: F821
    as_of = quarters[0] if quarters else None
    prior = prior_quarter(as_of) if as_of else None  # noqa: F821

    rows = screen_universe(as_of, settings) if as_of else []
    universe_total = len(rows)

    movers = build_movers(rows)
    entrants, top_decile_rank = build_entrants(rows, universe_total)

    # The ledger shows the top of the book, then filters refine THAT list.
    prescreen = sorted(
        [r for r in rows if r.get("composite") is not None],
        key=lambda r: r["composite"], reverse=True,
    )[:PRESCREEN_N]

    q = (request.args.get("q") or "").strip().lower()
    rep_filter = request.args.get("rep_filter") or "__all__"
    band = request.args.get("band") or "__all__"

    def matches(r):
        if rep_filter != "__all__":
            rep = r.get("rep")
            name = "__unassigned__" if (not rep or rep.get("unassigned")) else rep.get("name")
            if name != rep_filter:
                return False
        if band != "__all__" and band_of(r.get("assets_raw")) != band:
            return False
        if q and q not in ("%s %s" % (r.get("bank", ""), r.get("location", ""))).lower():
            return False
        return True

    visible = [r for r in prescreen if matches(r)]

    # Co-filtered option lists: each dropdown's counts reflect the OTHER's
    # current selection, so the desk never picks a combination that returns zero.
    def rep_key(r):
        rep = r.get("rep")
        return "__unassigned__" if (not rep or rep.get("unassigned")) else rep["name"]

    rep_pool = [r for r in prescreen if (band == "__all__" or band_of(r.get("assets_raw")) == band)]
    rep_counts = {}
    for r in rep_pool:
        rep_counts[rep_key(r)] = rep_counts.get(rep_key(r), 0) + 1
    rep_options = [{"value": "__all__", "label": "All reps"}] + [
        {"value": k, "label": "%s (%d)" % ("Unassigned" if k == "__unassigned__" else k, v)}
        for k, v in sorted(rep_counts.items())
        if v > 0 or k == rep_filter
    ]

    band_pool = [r for r in prescreen if (rep_filter == "__all__" or rep_key(r) == rep_filter)]
    band_counts = {}
    for r in band_pool:
        b = band_of(r.get("assets_raw"))
        if b:
            band_counts[b] = band_counts.get(b, 0) + 1
    band_options = [{"value": "__all__", "label": "All sizes"}] + [
        {"value": key, "label": "%s (%d)" % (label, band_counts.get(key, 0))}
        for key, label, _lo, _hi in ASSET_BANDS
        if band_counts.get(key, 0) > 0 or key == band
    ]

    return render_template(
        "index.html",
        active_nav="home",
        as_of=as_of,
        prior=prior,
        quarters=quarters,
        banks=list_banks(as_of),                # noqa: F821  # drawer cohort picker
        universe=visible,
        universe_total=universe_total,
        prescreen_total=len(prescreen),
        movers=movers,
        entrants=entrants,
        top_decile_rank=top_decile_rank,
        threshold=settings.threshold,
        above_count=sum(1 for r in prescreen if (r.get("composite") or 0) >= settings.threshold),
        rep_options=rep_options,
        band_options=band_options,
        rep_filter=rep_filter,
        band=band,
        q=request.args.get("q") or "",
        data_dir=current_data_dir(),            # noqa: F821
        cache=cache_status(),                   # noqa: F821
        rep_status=rep_status(),                # noqa: F821
        freshness=freshness_label(),            # noqa: F821  # e.g. "fresh" / "stale — refresh"
    )
