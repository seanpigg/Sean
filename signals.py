"""signals.py - Signal A/B/C engine."""

import numpy as np, pandas as pd, schema, config


def _num(s):
    return pd.to_numeric(s, errors="coerce")


def _pctl(series, invert=False):
    r = _num(series).rank(pct=True)
    return (1.0 - r) if invert else r


def _mean_ignore_nan(cols):
    mat = np.vstack([c.to_numpy(dtype=float) for c in cols])
    with np.errstate(invalid="ignore"):
        return np.nanmean(mat, axis=0)


def _prior_net_income(cur, prior):
    key = (
        schema.COL_INST_KEY
        if schema.COL_INST_KEY in cur.columns and schema.COL_INST_KEY in prior.columns
        else schema.COL_BANK
    )
    pni = _num(prior[schema.COL_NET_INCOME])
    pk = prior[key].astype(str).str.strip()
    lookup = (
        pd.DataFrame({"k": pk, "ni": pni.values})
        .dropna(subset=["k"])
        .drop_duplicates(subset="k", keep="first")
        .set_index("k")["ni"]
    )
    ck = cur[key].astype(str).str.strip()
    mapped = ck.map(lookup)
    mapped.index = cur.index
    return _num(mapped)


def _f0(x):
    return "n/a" if pd.isna(x) else f"${x:,.0f}k"


def _fp(x, dp=1):
    return "n/a" if pd.isna(x) else f"{x:.{dp}f}%"


def score_universe(cur, prior=None):
    df = cur.copy()
    assets = _num(df[schema.COL_ASSETS])
    loans = _num(df[schema.COL_LOANS])
    secs = _num(df[schema.COL_SECURITIES])
    ld = _num(df[schema.COL_LOANS_DEP])
    liq = _num(df[schema.COL_LIQUIDITY])
    ye = _num(df[schema.COL_YIELD_EA])
    fv = _num(df[schema.COL_FV_COST])
    ys = _num(df[schema.COL_YIELD_SEC])
    nic = _num(df[schema.COL_NET_INCOME])
    cash = assets - loans - secs
    cr = cash / assets
    sa = (
        _mean_ignore_nan(
            [_pctl(cr), _pctl(ld, invert=True), _pctl(liq), _pctl(ye, invert=True)]
        )
        * 100
    )
    uw = 100.0 - fv
    el = secs * (1.0 - fv / 100.0)
    lr = el / assets
    sb = _mean_ignore_nan([_pctl(uw), _pctl(lr), _pctl(ys, invert=True)]) * 100
    if prior is not None:
        npi = _prior_net_income(df, prior)
        nch = nic - npi
        sc = _pctl(nch, invert=config.SIGNAL_C_REWARD_DECLINE).to_numpy(float) * 100
    else:
        npi = pd.Series([np.nan] * len(df), index=df.index)
        nch = pd.Series([np.nan] * len(df), index=df.index)
        sc = np.full(len(df), np.nan)
    w = config.SIGNAL_WEIGHTS
    parts = []
    wts = []
    for s, k in [(sa, "A"), (sb, "B"), (sc, "C")]:
        parts.append(np.where(np.isnan(s), 0.0, s) * w[k])
        wts.append(np.where(np.isnan(s), 0.0, w[k]))
    den = np.sum(wts, axis=0)
    comp = np.where(den > 0, np.sum(parts, axis=0) / den, np.nan)
    out = cur.copy()
    out["_cash_est"] = cash.values
    out["_cash_ratio"] = (cr * 100).values
    out["_loans_dep"] = ld.values
    out["_liq"] = liq.values
    out["_yld_ea"] = ye.values
    out["_fv_cost"] = fv.values
    out["_underwater"] = uw.values
    out["_est_loss"] = el.values
    out["_yld_sec"] = ys.values
    out["_ni_curr"] = nic.values
    out["_ni_prior"] = npi.values
    out["_ni_change"] = nch.values
    out["signal_a"] = sa
    out["signal_b"] = sb
    out["signal_c"] = sc
    out["composite"] = comp
    return out


def rationale_a(r):
    return f"Idle liquidity ~{_f0(r['_cash_est'])} ({_fp(r['_cash_ratio'])} of assets); Loans/Deposits {_fp(r['_loans_dep'])}, Liquidity {_fp(r['_liq'])}, Earning-asset yield {_fp(r['_yld_ea'],2)}."


def rationale_b(r):
    return f"Securities FV/Cost {_fp(r['_fv_cost'])} (underwater {_fp(r['_underwater'])} of cost); est. unrealized loss ~{_f0(r['_est_loss'])}; securities yield {_fp(r['_yld_sec'],2)}."


def rationale_c(r):
    d = "decline" if config.SIGNAL_C_REWARD_DECLINE else "improvement"
    return f"Net income {_f0(r['_ni_prior'])} -> {_f0(r['_ni_curr'])} (QoQ change {_f0(r['_ni_change'])}). Score = universe percentile of earnings {d}."
