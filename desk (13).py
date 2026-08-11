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


def qkey(q):
    """Sortable integer for a quarter string like '2026Q1'. Matches app.py."""
    try:
        return int(q[:4]) * 10 + int(q[-1])
    except (ValueError, IndexError, TypeError):
        return 0


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


# ==========================================================================
# Bank detail — the call-prep brief as a page, not a PDF download
#
# Rationale: exporting straight to PDF from the ledger spends the slowest
# operation in the app (the LLM call) BEFORE the desk can tell whether the bank
# is worth a call. This page shows every scored fact for free and generates the
# narrative only on request, so qualifying a bank costs nothing.
# ==========================================================================

# Metrics shown in the trend table, in display order.
# (label, facts-path, formatter)  — path is (section, key).
TREND_METRICS = [
    ("Total assets ($000)",     ("balance_sheet", "total_assets_$000"),        "int"),
    ("Idle liquidity ($000)",   ("signal_facts_A", "cash_est_$000"),           "int"),
    ("Idle liquidity / assets", ("signal_facts_A", "cash_pct_assets"),         "pct"),
    ("Loans / deposits",        ("signal_facts_A", "loans_deposits_pct"),      "pct"),
    ("FV / amortized cost",     ("signal_facts_B", "fv_over_cost_pct"),        "pct"),
    ("Unrealized loss ($000)",  ("signal_facts_B", "est_unrealized_loss_$000"), "negint"),
    ("Securities yield",        ("signal_facts_B", "securities_yield_pct"),    "pct2"),
    ("Net income ($000)",       ("signal_facts_C", "net_income_now_$000"),     "int"),
    ("Net interest margin",     ("margin_funding", "nim_pct"),                 "pct2"),
]


_QUARTER_RE = None


def _blk(d, *path):
    """
    Walk nested dicts safely. Any non-dict along the way yields {} rather than
    raising — get_bank_facts' exact nesting is not guaranteed.
    """
    cur = d
    for p in path:
        if not isinstance(cur, dict):
            return {}
        cur = cur.get(p)
    return cur if isinstance(cur, dict) else {}


def _is_quarter(s):
    global _QUARTER_RE
    import re
    if _QUARTER_RE is None:
        _QUARTER_RE = re.compile(r"^\d{4}Q[1-4]$")
    return bool(_QUARTER_RE.match(str(s).strip()))


def _dig(facts, section, key):
    """Read a value out of a facts dict, including the signal_facts_X paths."""
    if not isinstance(facts, dict):
        return None
    if section.startswith("signal_facts_"):
        block = _blk(facts, "signal_facts", section[-1])
    else:
        block = _blk(facts, section)
    return _num(block.get(key))


def _fmt(v, kind):
    if v is None:
        return "—"
    if kind == "int":
        return "{:,.0f}".format(v)
    if kind == "negint":
        return "-{:,.0f}".format(abs(v))
    if kind == "pct":
        return "%.1f%%" % v
    if kind == "pct2":
        return "%.2f%%" % v
    return str(v)


def _trend_from_facts(quarters, series):
    """quarters + one facts dict per quarter -> table rows."""
    rows = []
    for label, (section, key), kind in TREND_METRICS:
        vals = [_dig(f, section, key) for f in series]
        if all(v is None for v in vals):
            continue
        rows.append({
            "label": label,
            "display": [_fmt(v, kind) for v in vals],
            "spark": _spark_points(vals),
        })
    return rows


def _trend_from_series(quarters, mapping):
    """
    {label: [v, v, ...]} -> table rows, in the mapping's own order.

    Used when get_bank_trend has already chosen the metrics (it reads
    settings.TREND_FIELDS), in which case we display its labels rather than
    imposing TREND_METRICS.
    """
    rows = []
    for label, vals in mapping.items():
        if not isinstance(vals, (list, tuple)):
            continue
        nums = [_num(v) for v in vals]
        if all(v is None for v in nums):
            display = [("—" if v in (None, "") else str(v)) for v in vals]
            spark = ""
        else:
            display = []
            for raw, n in zip(vals, nums):
                if n is None:
                    display.append("—" if raw in (None, "") else str(raw))
                elif abs(n) >= 1000:
                    display.append("{:,.0f}".format(n))
                elif abs(n) < 100 and n != int(n):
                    display.append("%.2f" % n)
                else:
                    display.append("{:,.2f}".format(n).rstrip("0").rstrip("."))
            spark = _spark_points(nums)
        rows.append({"label": str(label), "display": display, "spark": spark})
    return rows


def build_trend(bank_key, as_of, n=5):
    """
    Reshape whatever analysis.get_bank_trend returns into
    {quarters: [...], rows: [{label, display, spark}]}.

    The return shape is not pinned down anywhere, so every plausible one is
    handled and anything unrecognized yields None — the trend section then
    hides and the rest of the page is unaffected. This must never raise: a
    formatting problem in an optional table is not worth a 500 on the brief.
    """
    try:
        raw = analysis.get_bank_trend(bank_key, as_of, n=n)
    except TypeError:
        try:
            raw = analysis.get_bank_trend(bank_key, as_of, n)
        except Exception:
            return None
    except Exception:
        return None
    if not raw:
        return None

    try:
        # ---- list of facts dicts -----------------------------------------
        if isinstance(raw, (list, tuple)):
            series = [f for f in raw if isinstance(f, dict)]
            if not series:
                return None
            quarters = [f.get("as_of") or f.get("quarter") for f in series]
            if any(q is None for q in quarters):
                return None
            order = sorted(range(len(quarters)), key=lambda i: qkey(quarters[i]))
            quarters = [quarters[i] for i in order]
            series = [series[i] for i in order]
            rows = _trend_from_facts(quarters, series)
            return {"quarters": quarters, "rows": rows} if rows else None

        if not isinstance(raw, dict):
            return None

        # ---- already-shaped: {"quarters": [...], "rows"/"fields": ...} ----
        if "quarters" in raw:
            quarters = list(raw.get("quarters") or [])
            if len(quarters) < 2:
                return None

            body = None
            for cand in ("rows", "fields", "metrics", "data", "series", "values"):
                if cand in raw and raw[cand]:
                    body = raw[cand]
                    break
            if body is None:
                return None

            # rows as a list of dicts
            if isinstance(body, (list, tuple)):
                rows = []
                for r in body:
                    if not isinstance(r, dict):
                        continue
                    label = r.get("label") or r.get("name") or r.get("field") or ""
                    vals = r.get("values") or r.get("display") or r.get("data") or []
                    if not isinstance(vals, (list, tuple)):
                        continue
                    nums = [_num(v) for v in vals]
                    rows.append({
                        "label": str(label),
                        "display": [
                            ("—" if v in (None, "") else str(v)) for v in vals
                        ] if all(x is None for x in nums) else [
                            ("—" if x is None else "{:,.2f}".format(x)
                             .rstrip("0").rstrip("."))
                            for x in nums
                        ],
                        "spark": _spark_points(nums),
                    })
                return {"quarters": quarters, "rows": rows} if rows else None

            # rows as {label: [values]}
            if isinstance(body, dict):
                rows = _trend_from_series(quarters, body)
                return {"quarters": quarters, "rows": rows} if rows else None
            return None

        keys = list(raw.keys())

        # ---- {quarter: facts} --------------------------------------------
        if all(_is_quarter(k) for k in keys):
            quarters = sorted(keys, key=qkey)
            if len(quarters) < 2:
                return None
            series = [raw[q] for q in quarters]
            if not all(isinstance(f, dict) for f in series):
                return None
            rows = _trend_from_facts(quarters, series)
            return {"quarters": quarters, "rows": rows} if rows else None

        # ---- {label: [values]} with quarters unnamed ----------------------
        lists = {k: v for k, v in raw.items() if isinstance(v, (list, tuple))}
        if lists:
            width = max(len(v) for v in lists.values())
            if width < 2:
                return None
            quarters = _back_quarters(as_of, width)
            rows = _trend_from_series(quarters, lists)
            return {"quarters": quarters, "rows": rows} if rows else None

        return None
    except Exception:
        return None


def _back_quarters(as_of, n):
    """[as_of-n+1 ... as_of], oldest first — for shapes that omit the labels."""
    try:
        y, q = int(as_of[:4]), int(as_of[-1])
    except (ValueError, IndexError, TypeError):
        return [""] * n
    out = []
    for _ in range(n):
        out.append("%dQ%d" % (y, q))
        q -= 1
        if q == 0:
            q = 4
            y -= 1
    return list(reversed(out))


def _headline_reason(facts):
    """One clause naming the strongest signal — shown before any LLM call."""
    sc = _blk(facts, "scores")
    named = {
        "A": "Idle liquidity is the lead: cash is %s of assets with no organic outlet.",
        "B": "The bond book carries the case: it is %s below cost at today's yields.",
        "C": "Earnings are the opening: net income moved %s quarter over quarter.",
    }
    best, bestv = None, -1
    for k in ("A", "B", "C"):
        v = _num(sc.get(k))
        if v is not None and v > bestv:
            best, bestv = k, v
    if best is None:
        return "Scores are material but no single signal dominates."

    if best == "A":
        v = _num(_blk(facts, "signal_facts", "A").get("cash_pct_assets"))
        return named["A"] % (("%.1f%%" % v) if v is not None else "an outsized share")
    if best == "B":
        v = _num(_blk(facts, "signal_facts", "B").get("underwater_pct_of_cost"))
        return named["B"] % (("%.1f%%" % v) if v is not None else "materially")
    cblk = _blk(facts, "signal_facts", "C")
    now = _num(cblk.get("net_income_now_$000"))
    was = _num(cblk.get("net_income_prior_$000"))
    if now is not None and was:
        return named["C"] % ("%.1f%%" % ((now - was) / abs(was) * 100.0))
    return named["C"] % "materially"


def _neighbours(bank_key, as_of):
    """Previous/next by composite rank, so a rep can work down the list."""
    now, _total = _snapshot(as_of)
    keys = [k for k, v in now.items()
            if v.get("composite") is not None and _eligible(v)]
    keys.sort(key=lambda k: now[k]["composite"], reverse=True)
    if bank_key not in keys:
        return None, None
    i = keys.index(bank_key)
    prev = keys[i - 1] if i > 0 else None
    nxt = keys[i + 1] if i < len(keys) - 1 else None
    mk = lambda k: {"key": k, "bank": now[k]["bank"]} if k else None
    return mk(prev), mk(nxt)


def render_bank():
    from flask import render_template, request, abort

    bank_key = (request.args.get("bank") or "").strip()
    as_of = (request.args.get("as_of") or "").strip()
    if not bank_key:
        abort(400, "bank is required")

    if not as_of:
        _opts, quarters = analysis.get_available_options()
        quarters = sorted(quarters or [], key=qkey, reverse=True)
        as_of = quarters[0] if quarters else None
    if not as_of:
        abort(404, "no quarters available")

    facts = analysis.get_bank_facts(bank_key, as_of)
    if facts is None:
        abort(404, "No data for %s in %s" % (bank_key, as_of))
    facts.setdefault("key", bank_key)

    settings = config.load_settings() or {}

    # q/q move, from the same cached snapshots the ledger uses
    now, _t = _snapshot(as_of)
    prior_q = _quarter_before(as_of)
    was, _t2 = _snapshot(prior_q) if prior_q else ({}, 0)
    delta = None
    if bank_key in now and bank_key in was:
        a, b = now[bank_key].get("composite"), was[bank_key].get("composite")
        if a is not None and b is not None:
            delta = round(a - b)

    # Location: the scored snapshot already resolved "City, ST" from
    # schema.COL_CITY / COL_STATE — that is what the ledger prints, so use the
    # same source rather than hoping get_bank_facts carries it.
    location = (now.get(bank_key) or {}).get("location") or facts.get("location")

    rep = None
    try:
        options, _q = analysis.get_available_options()
        for o in options or []:
            if o.get("key") == bank_key:
                rep = o.get("rep")
                if not location:
                    location = o.get("location") or o.get("city_state")
                break
    except Exception:
        pass

    # last resort: pull the columns directly off the current quarter's frame
    if not location:
        try:
            df = analysis._read_quarter(as_of)
            if df is not None and len(df):
                keys = analysis._keys_for_df(df)
                if bank_key in list(keys):
                    i = list(keys).index(bank_key)
                    city = str(df.iloc[i].get(schema.COL_CITY, "") or "").strip()
                    state = str(df.iloc[i].get(schema.COL_STATE, "") or "").strip()
                    parts = [p for p in (city, state) if p and p.lower() != "nan"]
                    location = ", ".join(parts)
        except Exception:
            pass

    facts["location"] = location or ""

    cblk = _blk(facts, "signal_facts", "C")
    cnow = _num(cblk.get("net_income_now_$000"))
    cwas = _num(cblk.get("net_income_prior_$000"))
    ni_change_pct = ((cnow - cwas) / abs(cwas) * 100.0) if (cnow is not None and cwas) else None

    rationales = {}
    for k in ("A", "B", "C"):
        r = _blk(facts, "signal_facts", k).get("rationale")
        if r:
            rationales[k] = r

    # The template reads facts.signal_facts.A/B/C and the four figure blocks
    # directly. Normalize them to dicts here so a missing or oddly-typed block
    # renders as em-dashes instead of raising inside Jinja.
    facts["scores"] = _blk(facts, "scores")
    sfn = {}
    for k in ("A", "B", "C"):
        sfn[k] = _blk(facts, "signal_facts", k)
    facts["signal_facts"] = sfn
    for block in ("balance_sheet", "margin_funding", "securities_detail", "credit"):
        facts[block] = _blk(facts, block)
    facts.setdefault("universe_rank", 0)
    facts.setdefault("universe_total", 0)
    facts.setdefault("materiality_threshold", settings.get("MATERIALITY_PERCENTILE", 70))

    try:
        trend = build_trend(
            bank_key, as_of, n=settings.get("PDF_TREND_QUARTERS", 5)
        )
    except Exception:
        trend = None

    try:
        prev_bank, next_bank = _neighbours(bank_key, as_of)
    except Exception:
        prev_bank, next_bank = None, None

    return render_template(
        "bank.html",
        facts=facts,
        rep=rep,
        delta=delta,
        ni_change_pct=ni_change_pct,
        rationales=rationales,
        headline_reason=_headline_reason(facts),
        trend=trend,
        default_voice=settings.get("NARRATIVE_TONE", "conversational"),
        prev_bank=prev_bank,
        next_bank=next_bank,
    )


# --------------------------------------------------------------------------
# Narrative hand-off cache
#
# The detail page generates a narrative, the user reads it, then exports. The
# PDF must carry THAT text — regenerating on export would spend a second call
# and could return different words than the ones just approved.
#
# Deliberately small and short-lived: this is a hand-off between two requests
# seconds apart, not a persistence layer. Keyed by bank+quarter+voice so a
# rewrite in the other voice does not collide with the first.
# --------------------------------------------------------------------------

NARRATIVE_TTL = 1800     # seconds — long enough to read and export, not to go stale
NARRATIVE_MAX = 64       # entries; oldest evicted first

_narratives = {}


def _nkey(bank_key, as_of, voice):
    return (bank_key, as_of, voice)


def cache_narrative(bank_key, as_of, voice, data, model):
    import time
    if len(_narratives) >= NARRATIVE_MAX:
        for k in sorted(_narratives, key=lambda k: _narratives[k]["at"])[:8]:
            _narratives.pop(k, None)
    _narratives[_nkey(bank_key, as_of, voice)] = {
        "at": time.time(), "data": data, "model": model,
    }


def take_narrative(bank_key, as_of, voice):
    """
    Return a cached narrative if one was generated recently, else None.

    Non-destructive: the desk may export the same brief twice, and the second
    export should not silently produce different words than the first.
    """
    import time
    entry = _narratives.get(_nkey(bank_key, as_of, voice))
    if not entry:
        return None
    if time.time() - entry["at"] > NARRATIVE_TTL:
        _narratives.pop(_nkey(bank_key, as_of, voice), None)
        return None
    return entry["data"]


def narrative_json():
    """
    POST {bank, as_of, voice} -> the written narrative as JSON.

    Separate from the page render on purpose: the page must be free, and this
    is the only call that costs money and seconds.
    """
    from flask import request, jsonify
    import insight

    payload = request.get_json(silent=True) or {}
    bank_key = (payload.get("bank") or "").strip()
    as_of = (payload.get("as_of") or "").strip()
    voice = payload.get("voice") or "conversational"
    if voice not in ("conversational", "analyst"):
        voice = "conversational"
    if not bank_key or not as_of:
        return jsonify({"error": "bank and as_of are required."}), 400

    facts = analysis.get_bank_facts(bank_key, as_of)
    if facts is None:
        return jsonify({"error": "No data for that bank and quarter."}), 404

    try:
        result = insight.generate_insight(facts, voice)
    except TypeError:
        # older signature: voice comes from settings
        result = insight.generate_insight(facts)
    except Exception as e:
        return jsonify({"error": "%s: %s" % (type(e).__name__, e)}), 502

    data, model = (result if isinstance(result, tuple) else (result, None))
    data = data or {}
    cache_narrative(bank_key, as_of, voice, data, model)
    return jsonify({
        "headline": data.get("headline") or "",
        "body": data.get("body") or data.get("narrative") or "",
        "objection": data.get("objection") or "",
        "objection_answer": data.get("objection_answer") or data.get("answer") or "",
        "model": model or data.get("model") or "built-in",
        "voice": voice,
    })


# ==========================================================================
# Printed call-prep brief
#
# The PDF is rendered from templates/pdf.html by WeasyPrint, so it shares its
# design with the app instead of being rebuilt in a drawing API. One layout,
# one set of colours, one place to fix things.
#
# If WeasyPrint is not installed, build_call_pdf returns None and the /pdf
# route falls back to the original pdf_report module — the export keeps working,
# it just looks like the old one.
# ==========================================================================

def _split_paragraphs(text):
    if not text:
        return []
    parts = [p.strip() for p in str(text).split("\n\n")]
    return [p for p in parts if p]


def _fallback_narrative(facts, ni_change_pct):
    """
    Deterministic call copy, written from the scored figures.

    This is not a placeholder for the model — it is what prints whenever the
    model is unavailable, so it has to stand on its own. It names dollar
    amounts and ratios rather than describing them, and it never asserts
    anything the figures do not show.
    """
    sc = _blk(facts, "scores")
    a = _blk(facts, "signal_facts", "A")
    b = _blk(facts, "signal_facts", "B")
    c = _blk(facts, "signal_facts", "C")
    bs = _blk(facts, "balance_sheet")
    mf = _blk(facts, "margin_funding")

    def m(v):
        v = _num(v)
        if v is None:
            return None
        if abs(v) >= 1_000_000:
            return "$%.2fB" % (v / 1_000_000)
        if abs(v) >= 1000:
            return "$%.1fM" % (v / 1000)
        return "$%dK" % round(v)

    def p1(v):
        v = _num(v)
        return None if v is None else "%.1f%%" % v

    cash, cash_pct = m(a.get("cash_est_$000")), p1(a.get("cash_pct_assets"))
    ld = p1(a.get("loans_deposits_pct"))
    ea = _num(a.get("yield_earning_assets_pct"))
    fv = p1(b.get("fv_over_cost_pct"))
    loss = m(b.get("est_unrealized_loss_$000"))
    sy = _num(b.get("securities_yield_pct"))
    secs = m(bs.get("total_securities_amort_cost_$000"))
    assets, loans, deps = m(bs.get("total_assets_$000")), m(bs.get("total_loans_$000")), m(bs.get("total_deposits_$000"))
    ni_now, ni_prev = m(c.get("net_income_now_$000")), m(c.get("net_income_prior_$000"))
    nim = _num(mf.get("nim_pct"))
    cof = _num(mf.get("cost_of_funds_pct"))

    # lead with whichever signal actually scores highest
    ranked = sorted(
        [(k, _num(sc.get(k)) or 0) for k in ("A", "B", "C")],
        key=lambda t: t[1], reverse=True,
    )
    lead = ranked[0][0]

    if lead == "A" and cash and cash_pct:
        headline = (
            "A large share of this balance sheet is sitting in cash — %s, or %s of assets — "
            "with a %s loan/deposit ratio and no organic outlet for it."
            % (cash, cash_pct, ld or "a low")
        )
    elif lead == "B" and loss and fv:
        headline = (
            "The securities book is marked at %s of amortized cost, an unrealized loss of about %s, "
            "while yielding %s." % (fv, loss, ("%.2f%%" % sy) if sy is not None else "well below market")
        )
    else:
        headline = (
            "Earnings moved sharply quarter over quarter, from %s to %s, and the drag is showing up in margin."
            % (ni_prev or "the prior quarter", ni_now or "this quarter")
        )

    paras = []
    if cash and assets and loans and deps:
        paras.append(
            "%s holds roughly %s in idle liquidity against %s of assets. The loan book is %s against %s "
            "of deposits, a %s loan/deposit ratio. Whatever the reason — local loan demand, credit appetite, "
            "or a deliberate posture — a meaningful share of the balance sheet is earning less than it could."
            % (facts.get("bank", "The bank"), cash, assets, loans, deps, ld or "low")
        )
    if secs and sy is not None and fv and loss:
        gap = ("a %d basis point gap" % round((ea - sy) * 100)) if ea is not None else "a wide gap"
        paras.append(
            "The securities book compounds it: %s at a %.2f%% yield against a %s earning-asset yield — %s — "
            "and marked at %s of amortized cost, an unrealized loss of about %s. That mark is worth understanding "
            "before the call, because it sets what is actually on the table."
            % (secs, sy, ("%.2f%%" % ea) if ea is not None else "higher", gap, fv, loss)
        )
    if ni_now and ni_prev and ni_change_pct is not None:
        margin_note = ""
        if nim is not None:
            margin_note = " Net interest margin stands at %.2f%%" % nim
            if cof is not None:
                margin_note += ", with cost of funds at %.2f%% — the compression is on the asset side" % cof
            margin_note += "."
        paras.append(
            "The timing argument is in the earnings. Net income moved from %s to %s, a change of %.1f%%.%s"
            % (ni_prev, ni_now, ni_change_pct, margin_note)
        )

    if lead == "A":
        opener = ("You're carrying a lot of cash relative to the loan book — how are you thinking about "
                  "putting it to work, and what's holding it back?")
        objection = "We're holding that cash deliberately."
        answer = ("Reasonable — and nothing here requires locking it up. A short ladder keeps liquidity "
                  "available on a defined schedule while closing part of the yield gap.")
    elif lead == "B":
        opener = ("As the low-coupon paper rolls down, are you reinvesting, letting cash build, "
                  "or funding loan growth?")
        objection = "We don't want to realize a loss."
        answer = ("Understood — and the question isn't the loss, it's the earn-back. The relevant number is how "
                  "quickly the higher reinvestment yield recovers it, and whether the capital position can carry it.")
    else:
        opener = ("Margin gave up ground this quarter — how are you thinking about the asset side from here?")
        objection = "One quarter doesn't make a trend."
        answer = ("Agreed, and the trend table here covers five. The point isn't the single quarter, it's that "
                  "the balance-sheet mix is what's driving it.")

    return {
        "headline": headline,
        "paragraphs": paras,
        "opener": opener,
        "objection": objection,
        "objection_answer": answer,
        "byline": "Written by the built-in engine from the verified figures on this document.",
    }


def _shape_narrative(data, model, voice, facts, ni_change_pct):
    """Model output if there is any, deterministic copy if not."""
    if not data or not (data.get("headline") or data.get("body") or data.get("narrative")):
        return _fallback_narrative(facts, ni_change_pct)

    body = data.get("body") or data.get("narrative") or ""
    return {
        "headline": data.get("headline") or "",
        "paragraphs": _split_paragraphs(body),
        "opener": data.get("opener") or data.get("conversation_starter") or "",
        "objection": data.get("objection") or "",
        "objection_answer": data.get("objection_answer") or data.get("answer") or "",
        "byline": "Written by %s · %s voice · every figure cited appears in the tables on this document."
                  % (model or "the built-in engine", voice),
    }


def _logo_data_uri():
    """
    Inline the lockup so the renderer never depends on a URL resolving.
    Returns None if the file is missing — the header falls back to type.
    """
    import base64
    import os
    for name in ("sss-lockup.png", "southstate_logo.png"):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", name)
        if os.path.exists(path):
            try:
                with open(path, "rb") as fh:
                    return "data:image/png;base64," + base64.b64encode(fh.read()).decode("ascii")
            except Exception:
                continue
    return None


PDF_ENGINE_ERROR = None


# Browsers Playwright can drive, in preference order.
#
# msedge and chrome are ALREADY INSTALLED on a managed Windows machine, so they
# need no download and no admin rights — which matters when a corporate TLS
# proxy blocks Playwright's CDN. None means Playwright's own bundled build,
# used only if it happens to be present.
BROWSER_CHANNELS = ["msedge", "chrome", None]


def _launch_browser(pw):
    """First channel that actually launches. Returns (browser, name)."""
    errs = []
    for ch in BROWSER_CHANNELS:
        try:
            b = pw.chromium.launch(channel=ch) if ch else pw.chromium.launch()
            return b, (ch or "bundled chromium"), None
        except Exception as e:
            errs.append("%s: %s" % (ch or "bundled", type(e).__name__))
    return None, None, "; ".join(errs)


def _chromium_ok():
    """Playwright installed AND some Chromium-family browser it can drive."""
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        return False, "%s: %s" % (type(e).__name__, e)
    try:
        with sync_playwright() as pw:
            b, name, err = _launch_browser(pw)
            if not b:
                return False, "no usable browser (%s)" % err
            b.close()
        return True, None
    except Exception as e:
        return False, "%s: %s" % (type(e).__name__, e)


def pdf_engine_status():
    """
    Which HTML renderer will be used, and why the others are unavailable.

    Chromium is preferred: it is the same engine the app is designed in, so the
    PDF matches the screen exactly. WeasyPrint is the fallback for environments
    where a browser cannot be downloaded.
    """
    chrome_ok, chrome_err = _chromium_ok()
    if chrome_ok:
        name = None
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as pw:
                b, name, _e = _launch_browser(pw)
                if b:
                    b.close()
        except Exception:
            pass
        return {
            "ok": True,
            "engine": "chromium",
            "browser": name,
            "note": "The redesigned PDF is in use, rendered by %s." % (name or "Chromium"),
        }

    try:
        import weasyprint
        return {
            "ok": True,
            "engine": "weasyprint",
            "version": getattr(weasyprint, "__version__", "unknown"),
            "note": "The redesigned PDF is in use, rendered by WeasyPrint.",
            "chromium_error": chrome_err,
        }
    except Exception as e:
        return {
            "ok": False,
            "engine": None,
            "chromium_error": chrome_err,
            "weasyprint_error": "%s: %s" % (type(e).__name__, e),
            "note": ("Neither renderer is available, so /pdf is falling back to the "
                     "original generator. Chromium needs no admin rights: "
                     "pip install playwright, then python -m playwright install chromium."),
        }


def build_call_pdf(bank_key, as_of, voice=None, narrative_data=None, model=None):
    """
    Render the call-prep brief to PDF bytes.

    Returns None when WeasyPrint is unavailable, so the caller can fall back to
    the original generator rather than failing the download.
    """
    from flask import render_template

    facts = analysis.get_bank_facts(bank_key, as_of)
    if facts is None:
        return None
    facts.setdefault("key", bank_key)

    settings = config.load_settings() or {}
    voice = voice or settings.get("NARRATIVE_TONE", "conversational")

    # same normalization the detail page uses, so both read identically
    facts["scores"] = _blk(facts, "scores")
    facts["signal_facts"] = {k: _blk(facts, "signal_facts", k) for k in ("A", "B", "C")}
    for block in ("balance_sheet", "margin_funding", "securities_detail", "credit"):
        facts[block] = _blk(facts, block)
    facts.setdefault("universe_rank", 0)
    facts.setdefault("universe_total", 0)
    facts.setdefault("materiality_threshold", settings.get("MATERIALITY_PERCENTILE", 70))

    now, _t = _snapshot(as_of)
    facts["location"] = (now.get(bank_key) or {}).get("location") or facts.get("location") or ""

    prior_q = _quarter_before(as_of)
    was, _t2 = _snapshot(prior_q) if prior_q else ({}, 0)
    delta = None
    if bank_key in now and bank_key in was:
        x, y = now[bank_key].get("composite"), was[bank_key].get("composite")
        if x is not None and y is not None:
            delta = round(x - y)

    cblk = facts["signal_facts"]["C"]
    cnow, cwas = _num(cblk.get("net_income_now_$000")), _num(cblk.get("net_income_prior_$000"))
    ni_change_pct = ((cnow - cwas) / abs(cwas) * 100.0) if (cnow is not None and cwas) else None

    rep = None
    try:
        options, _q = analysis.get_available_options()
        for o in options or []:
            if o.get("key") == bank_key:
                rep = o.get("rep")
                break
    except Exception:
        pass

    rationales = {}
    for k in ("A", "B", "C"):
        r = facts["signal_facts"][k].get("rationale")
        if r:
            rationales[k] = r

    try:
        trend = build_trend(bank_key, as_of, n=settings.get("PDF_TREND_QUARTERS", 5))
    except Exception:
        trend = None

    engine = _pdf_engine_name()
    html = render_template(
        "pdf.html",
        engine=engine,
        facts=facts,
        rep=rep if settings.get("PDF_SHOW_REP", True) else None,
        delta=delta,
        ni_change_pct=ni_change_pct,
        rationales=rationales,
        headline_reason=_headline_reason(facts),
        trend=trend if settings.get("PDF_INCLUDE_TREND", True) else None,
        narrative=_shape_narrative(narrative_data, model, voice, facts, ni_change_pct),
        logo_src=_logo_data_uri(),
    )
    return _html_to_pdf(
        html,
        header_html=_running_header(facts, _logo_data_uri()),
        footer_html=_running_footer(facts),
    )


def _running_header(facts, logo):
    """
    Masthead for Chromium's per-page header slot.

    These templates are rendered in isolation — no page stylesheet, no custom
    properties, no external CSS — so every value is inline and literal, and
    lengths are px because Chrome scales this box at 96dpi.
    """
    brand = ('<img src="%s" style="width:118px;height:auto;display:block;">' % logo) if logo else (
        '<div style="font-size:14px;font-weight:700;">SouthState'
        '<span style="font-weight:400;color:#9DB3D0;"> Securities</span></div>')
    return (
        '<div style="width:100%;margin:0;padding:0;'
        '-webkit-print-color-adjust:exact;print-color-adjust:exact;">'
        '<div style="background:#0B2545;color:#ffffff;padding:10px 48px 9px;'
        'display:flex;align-items:center;justify-content:space-between;'
        "font-family:'IBM Plex Sans',Segoe UI,sans-serif;">"
        + brand +
        '<div style="text-align:right;">'
        '<div style="font-size:12px;font-weight:600;letter-spacing:-.01em;">%s</div>'
        '<div style="font-size:8px;letter-spacing:1.5px;text-transform:uppercase;'
        'color:#9DB3D0;margin-top:2px;">Fixed-Income Call Prep &middot; '
        '<b style="color:#C9A227;font-weight:600;">%s</b></div>'
        '</div></div></div>'
    ) % (facts.get("bank", ""), facts.get("as_of", ""))


def _running_footer(facts):
    """Disclaimer + page counter, repeated on every sheet."""
    total = facts.get("universe_total") or 0
    return (
        '<div style="width:100%;padding:0 48px;box-sizing:border-box;'
        "font-family:'IBM Plex Sans',Segoe UI,sans-serif;font-size:7px;"
        'line-height:1.5;color:#54687F;">'
        '<div style="border-top:1px solid #D3DBE5;padding-top:6px;display:flex;'
        'align-items:flex-start;gap:14px;">'
        '<div style="flex:1;text-align:left;">'
        '<b>Internal analytical aid &mdash; not investment advice or a solicitation.</b> '
        'Any idea should fit the institution&rsquo;s objectives and pass suitability review '
        'before action. Figures are SNL / Capital IQ call-report data, traceable to the FFIEC '
        'filing via the identifiers on page 1. Percentiles are ranked against all '
        '{:,} depositories filing for {}. For internal SouthState Securities use.'
        '</div>'
        "<div style="flex:0 0 auto;font-family:'IBM Plex Mono',Consolas,monospace;"
        'font-size:7px;font-weight:600;color:#7488A0;white-space:nowrap;padding-top:1px;">'
        '<span class="pageNumber"></span> of <span class="totalPages"></span>'
        '</div></div></div>'
    ).format(total, facts.get("as_of", ""))


def _pdf_engine_name():
    """
    Which engine will render — the template needs to know, because Chromium
    ignores CSS @page margin boxes and gets its page numbers from the print
    API instead.
    """
    ok, _e = _chromium_ok()
    if ok:
        return "chromium"
    try:
        import weasyprint  # noqa: F401
        return "weasyprint"
    except Exception:
        return None


def _html_to_pdf(html, header_html=None, footer_html=None):
    """
    Chromium first — it is the engine this design was built in, so the PDF is
    the design rather than an approximation of it. WeasyPrint second. None if
    neither is available, which makes the caller fall back to the old generator.
    """
    global PDF_ENGINE_ERROR

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser, _name, err = _launch_browser(pw)
            if not browser:
                raise RuntimeError("no usable browser (%s)" % err)
            try:
                page = browser.new_page()
                page.set_content(html, wait_until="networkidle")
                # Margins reserve the bands: 0.86in of top margin holds the
                # masthead, 0.92in of bottom margin holds the disclaimer.
                pdf = page.pdf(
                    format="Letter",
                    print_background=True,
                    margin={"top": "0.86in", "right": "0.5in",
                            "bottom": "0.92in", "left": "0.5in"},
                    display_header_footer=True,
                    header_template=header_html or "<div></div>",
                    footer_template=footer_html or "<div></div>",
                )
                PDF_ENGINE_ERROR = None
                return pdf
            finally:
                browser.close()
    except Exception as e:
        PDF_ENGINE_ERROR = "chromium: %s: %s" % (type(e).__name__, e)

    try:
        from weasyprint import HTML
        pdf = HTML(string=html).write_pdf()
        PDF_ENGINE_ERROR = None
        return pdf
    except Exception as e:
        PDF_ENGINE_ERROR = (PDF_ENGINE_ERROR or "") + " | weasyprint: %s: %s" % (type(e).__name__, e)
        return None
