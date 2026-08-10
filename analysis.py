"""analysis.py - read/clean/cache SNL workbooks, score universe, attach reps."""

import os, re, glob, threading
import config, schema, signals, fields, reps

try:
    import pandas as pd
except ImportError:
    pd = None

_QUARTER_RE = re.compile(
    re.escape(config.FILENAME_PREFIX) + r"(\d{4}Q[1-4])", re.IGNORECASE
)
_MAX_HEADER_SCAN = 30
_LOCK = threading.RLock()
_WORKBOOK_CACHE = {}
_QUARTER_CACHE = {}
_SCORE_CACHE = {}
_OPTIONS_CACHE = {}


def refresh_cache():
    with _LOCK:
        n = len(_WORKBOOK_CACHE)
        _WORKBOOK_CACHE.clear()
        _QUARTER_CACHE.clear()
        _SCORE_CACHE.clear()
        _OPTIONS_CACHE.clear()
    reps.refresh()
    return (
        f"Cache cleared ({n} workbook(s) released). Next screen reloads from the share."
    )


def cache_status():
    with _LOCK:
        return {
            "enabled": bool(getattr(config, "CACHE_ENABLED", True)),
            "workbooks_cached": len(_WORKBOOK_CACHE),
            "quarters_scored": len(_SCORE_CACHE),
        }


def _list_workbooks(data_dir):
    out = []
    for path in glob.glob(os.path.join(data_dir, config.FILENAME_PREFIX + "*.xlsx")):
        name = os.path.basename(path)
        if name.startswith("~$"):
            continue
        m = _QUARTER_RE.search(name)
        if m:
            out.append((m.group(1).upper(), path))
    out.sort(key=lambda t: int(t[0][:4]) * 10 + int(t[0][-1]), reverse=True)
    return out


def _quarter_before(q):
    y, qq = int(q[:4]), int(q[-1])
    qq -= 1
    if qq < 1:
        qq, y = 4, y - 1
    return f"{y}Q{qq}"


def _dedup(names):
    c, out = {}, []
    for n in names:
        if n in c:
            c[n] += 1
            out.append(f"{n}.{c[n]}")
        else:
            c[n] = 0
            out.append(n)
    return out


def _row_has_bank(vals):
    t = config.BANK_NAME_COLUMN.strip().lower()
    return t in [str(v).strip().lower() for v in vals]


def _locate(path):
    xls = pd.ExcelFile(path)
    for sh in xls.sheet_names:
        raw = pd.read_excel(xls, sheet_name=sh, header=None)
        for i in range(min(_MAX_HEADER_SCAN, raw.shape[0])):
            if _row_has_bank(raw.iloc[i].tolist()):
                return raw, i
    return (
        pd.read_excel(xls, sheet_name=xls.sheet_names[0], header=None),
        config.HEADER_ROW,
    )


def _clean_headers(vals):
    keep, names = [], []
    for i, h in enumerate(vals):
        if pd.isna(h):
            continue
        s = str(h).strip()
        if s == "" or s.lower() == "nan" or s.startswith("Unnamed"):
            continue
        keep.append(i)
        names.append(s)
    return keep, _dedup(names)


def _build(raw, hidx):
    keep, names = _clean_headers(raw.iloc[hidx].tolist())
    data = raw.iloc[hidx + 1 :, keep].copy()
    data.columns = names
    nc = config.BANK_NAME_COLUMN
    if nc in data.columns:
        nm = data[nc].astype(str).str.strip()
        data = data[
            data[nc].notna()
            & (nm != "")
            & (nm.str.lower() != "nan")
            & ~nm.str.match(r"^\d+(\.\d+)?$")
            & ~nm.str.match(r"^\d{4}Q[1-4]$", case=False)
        ]
    return data.reset_index(drop=True)


def _read_workbook(path):
    if pd is None:
        return None
    uc = bool(getattr(config, "CACHE_ENABLED", True))
    if uc:
        with _LOCK:
            if path in _WORKBOOK_CACHE:
                return _WORKBOOK_CACHE[path]
    raw, hidx = _locate(path)
    df = None if raw.shape[0] <= hidx else _build(raw, hidx)
    if uc and df is not None:
        with _LOCK:
            _WORKBOOK_CACHE[path] = df
    return df


def _read_quarter(q):
    q = q.upper()
    uc = bool(getattr(config, "CACHE_ENABLED", True))
    if uc:
        with _LOCK:
            if q in _QUARTER_CACHE:
                return _QUARTER_CACHE[q]
    df = None
    for qq, p in _list_workbooks(config.DATA_DIR):
        if qq == q:
            df = _read_workbook(p)
            break
    if uc and df is not None:
        with _LOCK:
            _QUARTER_CACHE[q] = df
    return df


def validate_schema(path):
    if pd is None:
        return {
            "ok": False,
            "error": "pandas not installed",
            "file": os.path.basename(path),
            "missing": [],
            "unexpected": [],
            "count_expected": len(schema.EXPECTED_COLUMNS),
            "count_found": 0,
        }
    raw, hidx = _locate(path)
    if raw.shape[0] <= hidx:
        return {
            "ok": False,
            "file": os.path.basename(path),
            "missing": [],
            "unexpected": [],
            "count_expected": len(schema.EXPECTED_COLUMNS),
            "count_found": 0,
            "note": "header not found",
        }
    _, found = _clean_headers(raw.iloc[hidx].tolist())
    exp = schema.EXPECTED_COLUMNS
    return {
        "ok": (
            not [c for c in exp if c not in found]
            and not [c for c in found if c not in exp]
        ),
        "file": os.path.basename(path),
        "missing": [c for c in exp if c not in found],
        "unexpected": [c for c in found if c not in exp],
        "count_expected": len(exp),
        "count_found": len(found),
    }


def validate_all():
    return [validate_schema(p) for _, p in _list_workbooks(config.DATA_DIR)]


def _snl_of(row):
    return (
        str(row[schema.COL_INST_KEY]).strip()
        if schema.COL_INST_KEY in row.index and pd.notna(row[schema.COL_INST_KEY])
        else None
    )


# --- Vectorized helpers -----------------------------------------------------
def _col_list(df, col, n):
    if col in df.columns:
        return df[col].astype(str).str.strip().tolist()
    return [""] * n


def _num_list(df, col, n):
    if col in df.columns:
        s = pd.to_numeric(df[col], errors="coerce")
        return [None if pd.isna(x) else float(x) for x in s.tolist()]
    return [None] * n


def _snl_list(df, n):
    if schema.COL_INST_KEY in df.columns:
        raw = df[schema.COL_INST_KEY].tolist()
        out = []
        for v in raw:
            if v is None or (isinstance(v, float) and pd.isna(v)):
                out.append(None)
                continue
            s = str(v).strip()
            if s.endswith(".0"):
                s = s[:-2]
            out.append(s or None)
        return out
    return [None] * n


def _fmt_assets(v):
    """v is Total Assets in $000. Show $XXXm under $1B, $X.XB at/above."""
    if v is None:
        return ""
    if v >= 1_000_000:  # >= $1B (since v is in $000)
        return f"${v/1_000_000:.1f}B"
    return f"${v/1_000:.0f}M"


def get_available_options(upload_folder=None):
    uc = bool(getattr(config, "CACHE_ENABLED", True))
    if uc:
        with _LOCK:
            if "opts" in _OPTIONS_CACHE:
                return _OPTIONS_CACHE["opts"]
    wbs = _list_workbooks(config.DATA_DIR)
    if not wbs:
        return (
            [
                {
                    "key": "__err__",
                    "label": "(data folder not found - check config.DATA_DIR)",
                    "name": "",
                    "snl": None,
                    "rep": None,
                    "assets_raw": None,
                    "assets_fmt": "",
                }
            ],
            _expected_quarters("2023Q1", "2026Q1"),
        )
    quarters = [q for q, _ in wbs]
    options = []
    if pd is not None:
        newest = wbs[0][1]
        try:
            df = _read_workbook(newest)
            if df is None or config.BANK_NAME_COLUMN not in df.columns:
                raw, h = _locate(newest)
                seen = [
                    str(v).strip()
                    for v in raw.iloc[h].tolist()
                    if str(v).strip() and str(v).strip().lower() != "nan"
                ][:8]
                return (
                    [
                        {
                            "key": "__err__",
                            "label": f"('{config.BANK_NAME_COLUMN}' not found. Header seen: {seen})",
                            "name": "",
                            "snl": None,
                            "rep": None,
                            "assets_raw": None,
                            "assets_fmt": "",
                        }
                    ],
                    quarters,
                )
            reps.ensure_loaded(timeout=12)
            rep_map = reps.get_map()
            n = len(df)
            names = _col_list(df, config.BANK_NAME_COLUMN, n)
            cities = _col_list(df, schema.COL_CITY, n)
            states = _col_list(df, schema.COL_STATE, n)
            snls = _snl_list(df, n)
            assets = _num_list(df, schema.COL_ASSETS, n)  # Total Assets ($000)
            seen = set()
            for i in range(n):
                name = names[i]
                if not name or name.lower() == "nan":
                    continue
                city = cities[i] if cities[i] and cities[i].lower() != "nan" else ""
                state = states[i] if states[i] and states[i].lower() != "nan" else ""
                snl = snls[i]
                key = f"K:{snl}" if snl else "N:" + "|".join([name, city, state])
                if key in seen:
                    continue
                seen.add(key)
                loc = ", ".join([p for p in [city, state] if p])
                rep = rep_map.get(snl) if snl else None
                if rep is None:
                    rep = {"code": "", "name": "Unassigned", "unassigned": True}
                av = assets[i]
                options.append(
                    {
                        "key": key,
                        "label": f"{name} \u2014 {loc}" if loc else name,
                        "name": name,
                        "snl": snl,
                        "rep": rep,
                        "assets_raw": av,
                        "assets_fmt": _fmt_assets(av),
                    }
                )
            options.sort(key=lambda o: o["label"].lower())
        except Exception as e:
            options = [
                {
                    "key": "__err__",
                    "label": f"(could not read {os.path.basename(newest)}: {e})",
                    "name": "",
                    "snl": None,
                    "rep": None,
                    "assets_raw": None,
                    "assets_fmt": "",
                }
            ]
    result = (options, quarters)
    if uc:
        with _LOCK:
            _OPTIONS_CACHE["opts"] = result
    return result


def _expected_quarters(start, end):
    out, (y, q) = [], (int(start[:4]), int(start[-1]))
    ey, eq = int(end[:4]), int(end[-1])
    while (y, q) <= (ey, eq):
        out.append(f"{y}Q{q}")
        q += 1
        if q > 4:
            q, y = 1, y + 1
    return list(reversed(out))


def _row_key(row):
    snl = _snl_of(row)
    if snl:
        return f"K:{snl}"
    name = str(row[schema.COL_BANK]).strip()
    city = (
        str(row[schema.COL_CITY]).strip()
        if schema.COL_CITY in row.index and pd.notna(row[schema.COL_CITY])
        else ""
    )
    state = (
        str(row[schema.COL_STATE]).strip()
        if schema.COL_STATE in row.index and pd.notna(row[schema.COL_STATE])
        else ""
    )
    return "N:" + "|".join([name, city, state])


def _keys_for_df(df):
    n = len(df)
    names = _col_list(df, schema.COL_BANK, n)
    cities = _col_list(df, schema.COL_CITY, n)
    states = _col_list(df, schema.COL_STATE, n)
    snls = _snl_list(df, n)
    keys = []
    for i in range(n):
        if snls[i]:
            keys.append(f"K:{snls[i]}")
        else:
            c = cities[i] if cities[i].lower() != "nan" else ""
            st = states[i] if states[i].lower() != "nan" else ""
            keys.append("N:" + "|".join([names[i], c, st]))
    return keys


def _match_rows_by_keys(scored, keys):
    if not keys:
        return scored.iloc[0:0]
    kset = {k.strip() for k in keys}
    allkeys = _keys_for_df(scored)
    mask = [k in kset for k in allkeys]
    return scored[pd.Series(mask, index=scored.index)]


def _match_one_row(scored, key):
    sub = _match_rows_by_keys(scored, [key])
    return None if sub.empty else sub.iloc[0]


def _score_as_of(as_of):
    as_of = as_of.upper()
    uc = bool(getattr(config, "CACHE_ENABLED", True))
    if uc:
        with _LOCK:
            if as_of in _SCORE_CACHE:
                return _SCORE_CACHE[as_of]
    prior = _quarter_before(as_of)
    cur = _read_quarter(as_of)
    if cur is None or config.BANK_NAME_COLUMN not in cur.columns:
        return None, None
    pdf = _read_quarter(prior)
    scored = signals.score_universe(cur, pdf)
    scored = scored.sort_values("composite", ascending=False).reset_index(drop=True)
    scored["universe_rank"] = scored.index + 1
    result = (scored, (prior if pdf is not None else None))
    if uc:
        with _LOCK:
            _SCORE_CACHE[as_of] = result
    return result


def run_analysis(
    upload_folder=None, banks=None, quarters=None, weights=None, rep_filter=None
):
    if pd is None or not quarters:
        return []
    as_of = sorted(quarters, key=lambda q: int(q[:4]) * 10 + int(q[-1]))[-1]
    scored, prior = _score_as_of(as_of)
    if scored is None:
        return []
    total = len(scored)
    picked = _match_rows_by_keys(scored, banks or [])
    reps.ensure_loaded(timeout=8)
    rep_map = reps.get_map()
    res = []
    for _, r in picked.iterrows():
        snl = _snl_of(r)
        rep = rep_map.get(snl) if snl else None
        if rep is None:
            rep = {"code": "", "name": "Unassigned", "unassigned": True}
        if rep_filter and rep_filter != "__all__":
            if rep_filter == "__unassigned__":
                if not rep["unassigned"]:
                    continue
            elif rep["unassigned"] or rep["name"] != rep_filter:
                continue
        name = str(r[schema.COL_BANK]).strip()
        city = (
            str(r[schema.COL_CITY]).strip()
            if schema.COL_CITY in r.index and pd.notna(r[schema.COL_CITY])
            else ""
        )
        state = (
            str(r[schema.COL_STATE]).strip()
            if schema.COL_STATE in r.index and pd.notna(r[schema.COL_STATE])
            else ""
        )
        loc = ", ".join([p for p in [city, state] if p])
        res.append(
            {
                "bank": name,
                "location": loc,
                "key": _row_key(r),
                "snl": snl,
                "rep": rep,
                "as_of": as_of,
                "prior": prior,
                "signal_a": {
                    "score": (
                        round(float(r["signal_a"]), 0)
                        if pd.notna(r["signal_a"])
                        else None
                    ),
                    "rationale": signals.rationale_a(r),
                },
                "signal_b": {
                    "score": (
                        round(float(r["signal_b"]), 0)
                        if pd.notna(r["signal_b"])
                        else None
                    ),
                    "rationale": signals.rationale_b(r),
                },
                "signal_c": {
                    "score": (
                        round(float(r["signal_c"]), 0)
                        if pd.notna(r["signal_c"])
                        else None
                    ),
                    "rationale": signals.rationale_c(r),
                },
                "composite": (
                    round(float(r["composite"]), 0)
                    if pd.notna(r["composite"])
                    else None
                ),
                "universe_rank": int(r["universe_rank"]),
                "universe_total": total,
            }
        )
    res.sort(key=lambda x: (x["composite"] is None, -(x["composite"] or 0)))
    return res


def _g(row, col):
    if col not in row.index:
        return None
    v = pd.to_numeric(row[col], errors="coerce")
    return None if pd.isna(v) else float(v)


def get_bank_facts(bank_key, as_of):
    scored, prior = _score_as_of(as_of)
    if scored is None:
        return None
    r = _match_one_row(scored, bank_key)
    if r is None:
        m = scored[
            scored[schema.COL_BANK].astype(str).str.strip() == str(bank_key).strip()
        ]
        if m.empty:
            return None
        r = m.iloc[0]
    bank = str(r[schema.COL_BANK]).strip()
    snl = _snl_of(r)

    def s(col):
        return str(r[col]).strip() if col in r.index and pd.notna(r[col]) else None

    facts = {
        "bank": bank,
        "as_of": as_of,
        "prior": prior,
        "city": s(schema.COL_CITY),
        "state": s(schema.COL_STATE),
        "cert": s(schema.COL_CERT),
        "inst_key": s(schema.COL_INST_KEY),
        "rep": reps.rep_for(snl),
        "universe_rank": int(r["universe_rank"]),
        "universe_total": int(len(scored)),
        "scores": {
            "A": None if pd.isna(r["signal_a"]) else round(float(r["signal_a"])),
            "B": None if pd.isna(r["signal_b"]) else round(float(r["signal_b"])),
            "C": None if pd.isna(r["signal_c"]) else round(float(r["signal_c"])),
            "composite": (
                None if pd.isna(r["composite"]) else round(float(r["composite"]))
            ),
        },
        "signal_facts": {
            "A": {
                "cash_est_$000": _g(r, "_cash_est"),
                "cash_pct_assets": _g(r, "_cash_ratio"),
                "loans_deposits_pct": _g(r, "_loans_dep"),
                "liquidity_pct": _g(r, "_liq"),
                "yield_earning_assets_pct": _g(r, "_yld_ea"),
            },
            "B": {
                "fv_over_cost_pct": _g(r, "_fv_cost"),
                "underwater_pct_of_cost": _g(r, "_underwater"),
                "est_unrealized_loss_$000": _g(r, "_est_loss"),
                "securities_yield_pct": _g(r, "_yld_sec"),
            },
            "C": {
                "net_income_now_$000": _g(r, "_ni_curr"),
                "net_income_prior_$000": _g(r, "_ni_prior"),
                "net_income_change_$000": _g(r, "_ni_change"),
            },
        },
        "balance_sheet": {
            "total_assets_$000": _g(r, schema.COL_ASSETS),
            "total_loans_$000": _g(r, schema.COL_LOANS),
            "total_deposits_$000": _g(r, schema.COL_DEPOSITS),
            "total_securities_amort_cost_$000": _g(r, schema.COL_SECURITIES),
            "equity_over_assets_pct": _g(r, schema.COL_EQ_ASSETS),
            "leverage_ratio_pct": _g(r, schema.COL_LEVERAGE),
        },
        "margin_funding": {
            "nim_pct": _g(r, schema.COL_NIM),
            "cost_of_funds_pct": _g(r, schema.COL_COST_FUNDS),
            "yield_on_loans_pct": _g(r, schema.COL_YIELD_LOANS),
            "noninterest_bearing_dep_pct": _g(r, schema.COL_NONINT_DEP),
            "brokered_dep_pct": _g(r, schema.COL_BROKERED),
        },
        "securities_detail": {"pledged_pct_of_secs": _g(r, schema.COL_PLEDGED)},
        "credit": {"npas_over_assets_pct": _g(r, schema.COL_NPAS)},
        "materiality_threshold": config.MATERIALITY_PERCENTILE,
    }
    top = max(
        [
            v
            for v in [facts["scores"]["A"], facts["scores"]["B"], facts["scores"]["C"]]
            if v is not None
        ]
        or [0]
    )
    facts["has_material_opportunity"] = top >= config.MATERIALITY_PERCENTILE
    facts["snapshot_table"] = [
        {"label": fields.label(fid), "value": fields.fmt_value(fid, r)}
        for fid in config.SNAPSHOT_FIELDS
    ]
    return facts


def get_bank_trend(bank_key, as_of, n=5):
    if pd is None:
        return None
    wbs = _list_workbooks(config.DATA_DIR)
    ordered = [q for q, _ in wbs]
    if as_of.upper() in ordered:
        st = ordered.index(as_of.upper())
        ordered = ordered[st : st + n]
    else:
        ordered = ordered[:n]
    cur = _read_quarter(as_of)
    if cur is None or config.BANK_NAME_COLUMN not in cur.columns:
        return None
    anchor = _match_one_row(cur, bank_key)
    if anchor is None:
        m = cur[cur[schema.COL_BANK].astype(str).str.strip() == str(bank_key).strip()]
        if m.empty:
            return None
        anchor = m.iloc[0]
    key_col = (
        schema.COL_INST_KEY
        if schema.COL_INST_KEY in cur.columns and pd.notna(anchor[schema.COL_INST_KEY])
        else schema.COL_BANK
    )
    key_val = str(anchor[key_col]).strip()
    tfids = list(config.TREND_FIELDS)[: fields.TREND_MAX]
    per_q = {}
    for q in ordered:
        df = _read_quarter(q)
        if df is None or key_col not in df.columns:
            per_q[q] = None
            continue
        m = df[df[key_col].astype(str).str.strip() == key_val]
        per_q[q] = m.iloc[0] if not m.empty else None
    quarters = [q for q in ordered if per_q.get(q) is not None]
    rows = []
    for fid in tfids:
        if fid not in fields.FIELDS:
            continue
        rows.append(
            {
                "label": fields.label(fid),
                "values": [fields.fmt_value(fid, per_q[q]) for q in quarters],
            }
        )
    return {"quarters": quarters, "rows": rows}
