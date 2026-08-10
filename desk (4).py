"""
desk.py — Bank Universe landing page.

Renders templates/index.html: the screen already run. Full universe scored for
the newest quarter, ranked by composite, with a band showing what moved since
the prior quarter. The bank/quarter picker survives as a "Custom screen" drawer
that still POSTs to /analyze unchanged.

HOW IT GETS ITS DATA
analysis._score_as_of(q) already scores and ranks the entire universe for a
quarter and caches the result in analysis._SCORE_CACHE — the same cache
/refresh clears. So this module does NOT re-score anything: it reads that
DataFrame, filters it in plain Python, and calls analysis.run_analysis() for
only the ~40 rows the ledger actually shows (to pick up the signal rationales
in their template-ready shape).

That means the landing page costs one universe scoring per quarter — the same
work /analyze already does — and filter changes cost nothing.

It does reach into two private analysis helpers (_score_as_of and _keys_for_df).
That is deliberate: the public run_analysis() only returns rows for a bank list
you already know, and the whole point of this page is not knowing yet.
"""

import analysis
import config
import reps
import schema

try:
    import pandas as pd
except ImportError:
    pd = None

# How many top-composite banks the ledger shows after filtering.
PRESCREEN_N = 40

# A bank is "in the top decile" at or above this fraction of the universe.
TOP_DECILE_FRACTION = 0.10

# Require a securities portfolio to appear on this screen.
#
# Trust companies, credit-card banks and other special-purpose charters carry no
# bond book, so signal B scores null. The composite is then computed from the
# signals that DO exist, which floats them to the top of the ranking — the
# screen's first page fills with institutions that cannot be sold a bond idea.
# Requiring a B score removes them. Set False to see the raw ranking.
REQUIRE_BOND_BOOK = True

# Signal C (net income q/q) is percentile-ranked, so a small bank swinging from
# a tiny loss to a tiny profit can move ~100 points on noise. A bank whose ONLY
# meaningful move is C is not a real mover; require a balance-sheet signal (A or
# B) to have moved at least this much to qualify for the band.
MOVER_MIN_BALANCE_SHEET_MOVE = 4

# Quarters of composite history behind each row's sparkline.
#
# COST: each quarter here is one full-universe scoring on first load (cached
# after, and cleared by /refresh). The page already scores 2 — current and
# prior — so the default of 5 adds 3. Set to 0 to switch sparklines off.
SPARK_QUARTERS = 5

ASSET_BANDS = [
    ("0-250000",         "Under $250M",   0,          250_000),
    ("250000-500000",    "$250M – $500M", 250_000,    500_000),
    ("500000-1000000",   "$500M – $1B",   500_000,    1_000_000),
    ("1000000-3000000",  "$1B – $3B",     1_000_000,  3_000_000),
    ("3000000-10000000", "$3B – $10B",    3_000_000,  10_000_000),
    ("10000000-",        "Over $10B",     10_000_000, None),
]

SIGNAL_NAMES = {"a": "Idle liquidity", "b": "Underwater book", "c": "Net income q/q"}


def band_of(assets_raw):
    if assets_raw is None:
        return None
    try:
        a = float(assets_raw)
    except (TypeError, ValueError):
        return None
    for key, _label, lo, hi in ASSET_BANDS:
        if a >= lo and (hi is None or a < hi):
            return key
    return None


def fmt_assets(raw):
    """Workbook assets are in $000 — render as $85M / $1.1B / $2.67T."""
    a = _num(raw)
    if a is None:
        return None
    if a >= 1_000_000_000:
        return "$%.2fT" % (a / 1_000_000_000)
    if a >= 1_000_000:
        return "$%.1fB" % (a / 1_000_000)
    return "$%dM" % round(a / 1_000)


def _num(v):
    if v is None:
        return None
    try:
        if pd is not None and pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _col(df, name, n):
    """Column as a plain list of floats-or-None, without touching iloc per row."""
    if name not in df.columns:
        return [None] * n
    if pd is None:
        return [None] * n
    return [_num(x) for x in pd.to_numeric(df[name], errors="coerce").tolist()]


def _text_col(df, name, n):
    if name not in df.columns:
        return [""] * n
    vals = df[name].astype(str).str.strip().tolist()
    return ["" if v.lower() == "nan" else v for v in vals]


# --------------------------------------------------------------------------
# one flat snapshot of a scored quarter, keyed by bank key
# --------------------------------------------------------------------------

_snapshots = {}


def _snapshot(q):
    """
    {key: {composite, rank, a, b, c, bank, location}} for quarter q, plus the
    universe total. Built off analysis._score_as_of, so it inherits that cache;
    memoized here too because _keys_for_df is the only real cost.
    """
    if q in _snapshots:
        return _snapshots[q]

    empty = ({}, 0)
    if pd is None:
        return empty
    try:
        scored, _prior = analysis._score_as_of(q)
    except Exception:
        return empty
    if scored is None or len(scored) == 0:
        return empty

    n = len(scored)
    keys = analysis._keys_for_df(scored)
    comps = _col(scored, "composite", n)
    ranks = _col(scored, "universe_rank", n)
    sa = _col(scored, "signal_a", n)
    sb = _col(scored, "signal_b", n)
    sc = _col(scored, "signal_c", n)
    names = _text_col(scored, schema.COL_BANK, n)
    cities = _text_col(scored, schema.COL_CITY, n)
    states = _text_col(scored, schema.COL_STATE, n)

    out = {}
    for i in range(n):
        loc = ", ".join([p for p in (cities[i], states[i]) if p])
        out[keys[i]] = {
            "composite": comps[i],
            "rank": int(ranks[i]) if ranks[i] is not None else None,
            "a": sa[i], "b": sb[i], "c": sc[i],
            "bank": names[i],
            "location": loc,
        }

    result = (out, n)
    _snapshots[q] = result
    return result


def invalidate():
    """Called from /refresh and after a settings save."""
    _snapshots.clear()


# --------------------------------------------------------------------------
# what changed since last quarter
# --------------------------------------------------------------------------

def _spark_points(vals, w=34, h=16, min_span=20):
    """
    Polyline points for a composite series, oldest first.

    Normalized to the series' own range so the shape is legible, but with a
    floor on that range — otherwise a bank drifting 88→90 draws the same
    dramatic climb as one going 40→90.
    """
    present = [v for v in vals if v is not None]
    if len(present) < 2:
        return ""
    lo, hi = min(present), max(present)
    if hi - lo < min_span:
        mid = (hi + lo) / 2.0
        lo, hi = mid - min_span / 2.0, mid + min_span / 2.0
    span = (hi - lo) or 1.0
    n = len(vals)
    out = []
    for i, v in enumerate(vals):
        if v is None:
            continue
        x = (i / (n - 1.0)) * w if n > 1 else 0.0
        y = h - ((v - lo) / span) * h
        out.append("%.1f,%.1f" % (x, max(0.0, min(h, y))))
    return " ".join(out) if len(out) >= 2 else ""


def _eligible(rec):
    """Whether a scored row belongs on a bond-portfolio screen at all."""
    if not REQUIRE_BOND_BOOK:
        return True
    return rec.get("b") is not None


def _describe_driver(now, was):
    """
    One short clause naming the signal that moved most. Deterministic — this is
    a scan aid on a dense page, so no LLM call.
    """
    moves = {}
    for letter in ("a", "b", "c"):
        n, w = now.get(letter), was.get(letter)
        if n is not None and w is not None:
            moves[letter] = n - w

    # Name a balance-sheet driver when there is one — that is what the desk
    # sells against. Fall back to C only when A and B are both flat.
    balance = [(l, v) for l, v in moves.items() if l in ("a", "b")]
    best = None
    if balance:
        cand = max(balance, key=lambda t: abs(t[1]))
        if abs(cand[1]) >= 2:
            best = cand
    if best is None and moves:
        best = max(moves.items(), key=lambda t: abs(t[1]))
    if not best or round(abs(best[1])) == 0:
        return "Composite re-ranked q/q"
    letter, change = best
    return "%s %s %d pts" % (
        SIGNAL_NAMES[letter], "up" if change > 0 else "down", round(abs(change))
    )


def _quarter_before(q):
    try:
        return analysis._quarter_before(q)
    except Exception:
        return None


# --------------------------------------------------------------------------
# the view
# --------------------------------------------------------------------------

def render_home():
    from flask import render_template, request

    settings = config.load_settings() or {}
    threshold = settings.get(
        "MATERIALITY_PERCENTILE", getattr(config, "MATERIALITY_PERCENTILE", 70)
    )

    options, quarters = analysis.get_available_options()
    options = options or []
    quarters = quarters or []
    broken = len(options) == 1 and options[0].get("key") == "__err__"

    as_of = quarters[0] if quarters else None
    prior_q = _quarter_before(as_of) if as_of else None

    # key -> rep / assets, straight off the option list analysis already built
    meta = {}
    banks = []
    for o in options:
        if o.get("key") == "__err__":
            continue
        meta[o["key"]] = {
            "rep": o.get("rep"),
            "assets_raw": o.get("assets_raw"),
            "assets_fmt": o.get("assets_fmt"),
        }
        banks.append({
            "key": o["key"],
            "label": o.get("label") or o.get("name") or o["key"],
            "assets_fmt": o.get("assets_fmt"),
        })

    now, universe_total = _snapshot(as_of) if (as_of and not broken) else ({}, 0)
    was, _ = _snapshot(prior_q) if (prior_q and not broken) else ({}, 0)

    # If the universe came back empty, say why rather than render a blank page.
    diagnostic = None
    if not broken and not now:
        if pd is None:
            diagnostic = "pandas is not installed — the workbooks cannot be read."
        elif not quarters:
            diagnostic = "No quarterly workbooks found in %s." % config.DATA_DIR
        else:
            diagnostic = _why_empty(as_of)

    def rep_key_of(key):
        rep = meta.get(key, {}).get("rep")
        if not rep or rep.get("unassigned"):
            return "__unassigned__"
        return rep.get("name") or "__unassigned__"

    # ---- filters (GET params; they refine the run, they never gate it) ----
    q_text = (request.args.get("q") or "").strip().lower()
    rep_filter = request.args.get("rep_filter") or "__all__"
    band = request.args.get("band") or "__all__"

    def matches(key, rec):
        if rep_filter != "__all__" and rep_key_of(key) != rep_filter:
            return False
        if band != "__all__" and band_of(meta.get(key, {}).get("assets_raw")) != band:
            return False
        if q_text:
            hay = "%s %s" % (rec.get("bank") or "", rec.get("location") or "")
            if q_text not in hay.lower():
                return False
        return True

    scored_keys = [
        k for k, v in now.items()
        if v.get("composite") is not None and _eligible(v)
    ]
    scored_keys.sort(key=lambda k: now[k]["composite"], reverse=True)

    no_book = sum(
        1 for v in now.values()
        if v.get("composite") is not None and v.get("b") is None
    )

    matching = [k for k in scored_keys if matches(k, now[k])]
    shown_keys = matching[:PRESCREEN_N]

    # Full template-shaped rows (with rationales) for just the visible slice.
    universe = []
    if shown_keys:
        rows = analysis.run_analysis(
            banks=shown_keys, quarters=[as_of], rep_filter="__all__"
        ) or []
        for r in rows:
            k = r.get("key")
            w = was.get(k)
            pc = w["composite"] if w else None
            cc = r.get("composite")
            r["prev_composite"] = pc
            r["prev_rank"] = w["rank"] if w else None
            r["delta"] = (
                round(cc - pc) if (pc is not None and cc is not None) else None
            )
            r["assets_raw"] = meta.get(k, {}).get("assets_raw")
            r["assets_fmt"] = (
                fmt_assets(meta.get(k, {}).get("assets_raw"))
                or meta.get(k, {}).get("assets_fmt")
            )
            universe.append(r)
        universe.sort(key=lambda r: (r.get("composite") is None,
                                     -(r.get("composite") or 0)))

        # Composite history for the visible rows only. The snapshots are
        # universe-wide and cached, so this costs nothing after first load.
        if SPARK_QUARTERS > 1 and quarters:
            hist_qs = list(reversed(quarters[:SPARK_QUARTERS]))  # oldest first
            snaps = [_snapshot(hq)[0] for hq in hist_qs]
            for r in universe:
                series = [s.get(r["key"], {}).get("composite") for s in snaps]
                r["spark"] = _spark_points(series)

    # ---- moved this quarter ----
    movers = []
    if was:
        deltas = []
        for k, rec in now.items():
            w = was.get(k)
            if not w or rec["composite"] is None or w["composite"] is None:
                continue
            if not _eligible(rec):
                continue
            d = round(rec["composite"] - w["composite"])
            if d == 0:
                continue
            bs = max(
                (abs(rec[l] - w[l]) for l in ("a", "b")
                 if rec.get(l) is not None and w.get(l) is not None),
                default=0,
            )
            if bs < MOVER_MIN_BALANCE_SHEET_MOVE:
                continue
            deltas.append((abs(d), d, k, rec, w))
        deltas.sort(key=lambda t: t[0], reverse=True)
        for _mag, d, k, rec, w in deltas[:5]:
            movers.append({
                "key": k,
                "bank": rec["bank"],
                "delta": d,
                "composite": rec["composite"],
                "prev_composite": w["composite"],
                "driver": _describe_driver(rec, w),
            })

    # ---- new to the top decile ----
    top_decile_rank = max(1, int(universe_total * TOP_DECILE_FRACTION))
    entrants = []
    if was:
        crossed = []
        for k, rec in now.items():
            w = was.get(k)
            if not w or not rec["rank"] or not w["rank"]:
                continue
            if not _eligible(rec):
                continue
            if rec["rank"] <= top_decile_rank < w["rank"]:
                crossed.append((rec["rank"], k, rec, w))
        crossed.sort(key=lambda t: t[0])
        for _r, k, rec, w in crossed[:4]:
            entrants.append({
                "key": k,
                "bank": rec["bank"],
                "rep": meta.get(k, {}).get("rep"),
                "universe_rank": rec["rank"],
                "prev_rank": w["rank"],
            })

    # ---- co-filtered dropdowns: each reflects the other's selection ----
    rep_pool = [
        k for k in matching_or_all(scored_keys, band, meta)
    ]
    rep_counts = {}
    for k in rep_pool:
        rk = rep_key_of(k)
        rep_counts[rk] = rep_counts.get(rk, 0) + 1
    label_for = {o["value"]: o["label"] for o in reps.rep_options()}
    rep_options = [{"value": "__all__", "label": "All reps"}]
    for k in sorted(rep_counts, key=lambda x: (x == "__unassigned__", x.lower())):
        base = label_for.get(k, "Unassigned" if k == "__unassigned__" else k)
        rep_options.append({"value": k, "label": "%s (%d)" % (base, rep_counts[k])})
    if rep_filter != "__all__" and rep_filter not in rep_counts:
        rep_options.append({
            "value": rep_filter,
            "label": "%s (0)" % label_for.get(rep_filter, rep_filter),
        })

    band_counts = {}
    for k in scored_keys:
        if rep_filter != "__all__" and rep_key_of(k) != rep_filter:
            continue
        b = band_of(meta.get(k, {}).get("assets_raw"))
        if b:
            band_counts[b] = band_counts.get(b, 0) + 1
    band_options = [{"value": "__all__", "label": "All sizes"}]
    for key, label, _lo, _hi in ASSET_BANDS:
        c = band_counts.get(key, 0)
        if c > 0 or key == band:
            band_options.append({"value": key, "label": "%s (%d)" % (label, c)})

    cache = analysis.cache_status() or {}
    rep_st = reps.status() or {}
    if broken:
        freshness = "data folder unreadable"
    elif not cache.get("workbooks_cached"):
        freshness = "no workbook cached"
    else:
        freshness = "fresh"

    return render_template(
        "index.html",
        active_nav="home",
        as_of=as_of or "—",
        prior=prior_q if was else None,
        quarters=quarters,
        banks=banks,
        universe=universe,
        universe_total=universe_total,
        prescreen_total=len(matching),
        movers=movers,
        entrants=entrants,
        top_decile_rank=top_decile_rank,
        threshold=threshold,
        above_count=sum(
            1 for k in matching if (now[k]["composite"] or 0) >= threshold
        ),
        rep_options=rep_options,
        band_options=band_options,
        rep_filter=rep_filter,
        band=band,
        q=request.args.get("q") or "",
        data_dir=config.DATA_DIR,
        cache=cache,
        rep_status=rep_st,
        freshness=freshness,
        load_error=options[0]["label"] if broken else None,
        diagnostic=diagnostic,
        no_book=no_book if REQUIRE_BOND_BOOK else 0,
    )


def _why_empty(as_of):
    """Best available explanation for a quarter that scored nothing."""
    try:
        df = analysis._read_quarter(as_of)
    except Exception as e:
        return "Could not read the %s workbook: %s: %s" % (
            as_of, type(e).__name__, e
        )
    if df is None:
        return "No workbook found for %s in %s." % (as_of, config.DATA_DIR)
    if config.BANK_NAME_COLUMN not in df.columns:
        cols = list(df.columns)[:8]
        return (
            "The %s workbook has no '%s' column. First columns seen: %s"
            % (as_of, config.BANK_NAME_COLUMN, ", ".join(str(c) for c in cols))
        )
    try:
        scored, _p = analysis._score_as_of(as_of)
    except Exception as e:
        return "Scoring %s failed: %s: %s" % (as_of, type(e).__name__, e)
    if scored is None or len(scored) == 0:
        return "Scoring %s produced no rows." % as_of
    return "Scored %d rows for %s but none carried a composite score." % (
        len(scored), as_of
    )


def matching_or_all(keys, band, meta):
    """Keys narrowed by the asset band only — used to count rep options."""
    if band == "__all__":
        return keys
    return [k for k in keys if band_of(meta.get(k, {}).get("assets_raw")) == band]
