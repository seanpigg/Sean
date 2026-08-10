"""
reps.py
-------
Loads the sales-rep assignment file (BankAssignments_*.xlsx) and maps each bank
(by its unique SNL ID) to a rep. Read IN-PLACE from the network share; never
copied.

ROBUST header detection: scans EVERY sheet in the workbook, and matches the
'SNL ID' header tolerantly (normalizes whitespace/case, and also accepts a cell
that merely contains 'snl' + 'id'). Other columns are matched the same way, so
extra spaces or a second data sheet can't break the load.

Rep code "UNA" (or a bank not present in the file) = UNASSIGNED. Unassigned
banks are SHOWN and clearly flagged - never hidden.

PERFORMANCE: read ONCE in a BACKGROUND thread with a bounded wait, so a slow
UNC network path can never freeze the page. Cleared by refresh().
"""
import os
import threading
import config

try:
    import pandas as pd
except ImportError:
    pd = None

UNASSIGNED_CODE = "UNA"
UNASSIGNED_LABEL = "Unassigned"

_LOCK = threading.RLock()
_CACHE = {}
_THREAD = None
_MAX_HEADER_SCAN = 40


def _norm(v):
    """Normalize a cell/header to lowercase, single-spaced text."""
    if v is None:
        return ""
    s = str(v).replace("\xa0", " ").strip().lower()
    return " ".join(s.split())  # collapse multiple/odd whitespace


def _norm_key(v):
    if v is None:
        return None
    s = str(v).strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s or None


def _is_snl_header(cell):
    n = _norm(cell)
    if n in ("snl id", "snl institution key", "snlid"):
        return True
    return ("snl" in n) and ("id" in n or "key" in n)


def _find_header_in(raw):
    """Return header row index in a sheet whose row contains an SNL-ID header."""
    for i in range(min(_MAX_HEADER_SCAN, raw.shape[0])):
        for cell in raw.iloc[i].tolist():
            if _is_snl_header(cell):
                return i
    return None


def _match_col(header_norms, *candidates):
    """Return the index of the first header matching any candidate (normalized)."""
    for cand in candidates:
        c = _norm(cand)
        if c in header_norms:
            return header_norms.index(c)
    return None


def _match_col_contains(header_norms, must_all):
    """Find a header index that contains ALL the given substrings (normalized)."""
    for idx, h in enumerate(header_norms):
        if all(tok in h for tok in must_all):
            return idx
    return None


def _read_file():
    path = getattr(config, "REP_FILE", "") or ""
    result = {"map": {}, "reps": [], "path": path, "ok": False, "note": ""}
    if pd is None:
        result["note"] = "pandas not installed"; return result
    if not path or not os.path.exists(path):
        result["note"] = "assignment file not found"; return result
    try:
        xls = pd.ExcelFile(path)
        raw = None; hidx = None; used_sheet = None
        for sh in xls.sheet_names:                       # <-- scan ALL sheets
            cand = pd.read_excel(xls, sheet_name=sh, header=None)
            h = _find_header_in(cand)
            if h is not None:
                raw, hidx, used_sheet = cand, h, sh
                break
        if raw is None:
            # helpful note: show what the first sheet's early rows looked like
            first = pd.read_excel(xls, sheet_name=xls.sheet_names[0], header=None)
            preview = []
            for i in range(min(5, first.shape[0])):
                preview += [str(v).strip() for v in first.iloc[i].tolist() if str(v).strip() and str(v).strip().lower() != "nan"]
            result["note"] = f"'SNL ID' header not found in any sheet {xls.sheet_names}. Saw: {preview[:10]}"
            return result

        header_norms = [_norm(v) for v in raw.iloc[hidx].tolist()]
        ci_snl = None
        for idx, cell in enumerate(raw.iloc[hidx].tolist()):
            if _is_snl_header(cell):
                ci_snl = idx; break
        ci_code = _match_col(header_norms, "rep assigned", "rep code", "assigned") \
            or _match_col_contains(header_norms, ["rep", "assign"])
        ci_nice = _match_col(header_norms, "nice rep name", "rep name") \
            or _match_col_contains(header_norms, ["rep", "name"])
        ci_city = _match_col(header_norms, "city")
        ci_state = _match_col(header_norms, "state")

        body = raw.iloc[hidx + 1:]
        def colvals(ci):
            return body.iloc[:, ci].tolist() if ci is not None else [None] * len(body)
        snl_list = colvals(ci_snl)
        code_list = colvals(ci_code); nice_list = colvals(ci_nice)
        city_list = colvals(ci_city); state_list = colvals(ci_state)

        def clean(v):
            return "" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v).strip()

        mapping = {}; rep_names = {}
        for i in range(len(body)):
            key = _norm_key(snl_list[i])
            if not key:
                continue
            code = clean(code_list[i]); nice = clean(nice_list[i])
            city = clean(city_list[i]); state = clean(state_list[i])
            is_un = (not code) or code.upper() == UNASSIGNED_CODE
            display = UNASSIGNED_LABEL if is_un else (nice or code)
            mapping[key] = {"code": code, "name": display, "unassigned": is_un, "city": city, "state": state}
            if not is_un and display:
                rep_names[display] = True

        note = f"{len(mapping)} banks, {len(rep_names)} reps"
        if used_sheet != xls.sheet_names[0]:
            note += f" (sheet '{used_sheet}')"
        return {"map": mapping, "reps": sorted(rep_names.keys(), key=lambda s: s.lower()),
                "path": path, "ok": True, "note": note}
    except Exception as e:  # noqa: BLE001
        result["note"] = f"read error: {type(e).__name__}: {e}"
        return result


def _bg_load():
    data = _read_file()
    with _LOCK:
        _CACHE["data"] = data


def _start_bg():
    global _THREAD
    with _LOCK:
        if _CACHE.get("data") is not None:
            return
        if _THREAD is not None and _THREAD.is_alive():
            return
        _THREAD = threading.Thread(target=_bg_load, daemon=True)
        _THREAD.start()


def ensure_loaded(timeout=12):
    with _LOCK:
        if _CACHE.get("data") is not None:
            return
    _start_bg()
    t = _THREAD
    if t is not None:
        t.join(timeout)


def _data():
    with _LOCK:
        return _CACHE.get("data")


def refresh():
    global _THREAD
    with _LOCK:
        _CACHE.clear()
        _THREAD = None


def status():
    d = _data()
    if d is None:
        return {"ok": False, "note": "loading… (reading assignment file)", "path": getattr(config, "REP_FILE", ""),
                "bank_count": 0, "rep_count": 0, "loading": True}
    return {"ok": d["ok"], "note": d["note"], "path": d["path"],
            "bank_count": len(d["map"]), "rep_count": len(d["reps"]), "loading": False}


def get_map():
    d = _data()
    return d["map"] if d else {}


def rep_for(snl_id):
    d = _data()
    if d is None:
        _start_bg()
        return {"code": "", "name": UNASSIGNED_LABEL, "unassigned": True}
    info = d["map"].get(_norm_key(snl_id))
    return info if info is not None else {"code": "", "name": UNASSIGNED_LABEL, "unassigned": True}


def rep_options():
    d = _data() or {"reps": []}
    opts = [{"value": "__all__", "label": "All reps"}]
    for r in d.get("reps", []):
        opts.append({"value": r, "label": r})
    opts.append({"value": "__unassigned__", "label": f"\u26aa {UNASSIGNED_LABEL}"})
    return opts


def matches_filter(snl_id, rep_filter):
    if not rep_filter or rep_filter == "__all__":
        return True
    info = rep_for(snl_id)
    if rep_filter == "__unassigned__":
        return info["unassigned"]
    return (not info["unassigned"]) and info["name"] == rep_filter
