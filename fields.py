"""fields.py - curated ~31 selectable metrics for the two PDF tables."""

import pandas as pd, schema


def _num(row, col):
    if col not in row.index:
        return None
    v = pd.to_numeric(row[col], errors="coerce")
    return None if pd.isna(v) else float(v)


def _derived(name, row):
    a = _num(row, schema.COL_ASSETS)
    l = _num(row, schema.COL_LOANS)
    s = _num(row, schema.COL_SECURITIES)
    fv = _num(row, schema.COL_FV_COST)
    if name == "idle_liquidity":
        return None if None in (a, l, s) else a - l - s
    if name == "cash_pct_assets":
        return None if None in (a, l, s) or a == 0 else (a - l - s) / a * 100.0
    if name == "est_unrealized_loss":
        return None if None in (s, fv) else s * (1.0 - fv / 100.0)
    if name == "underwater_pct":
        return None if fv is None else 100.0 - fv
    return None


FIELDS = {
    "total_assets": {"label": "Total assets", "fmt": "money", "col": schema.COL_ASSETS},
    "total_loans": {"label": "Total loans", "fmt": "money", "col": schema.COL_LOANS},
    "total_deposits": {
        "label": "Total deposits",
        "fmt": "money",
        "col": schema.COL_DEPOSITS,
    },
    "total_securities": {
        "label": "Securities (amort cost)",
        "fmt": "money",
        "col": schema.COL_SECURITIES,
    },
    "loans_deposits": {
        "label": "Loans / deposits",
        "fmt": "pct1",
        "col": schema.COL_LOANS_DEP,
    },
    "equity_assets": {
        "label": "Equity / assets",
        "fmt": "pct1",
        "col": schema.COL_EQ_ASSETS,
    },
    "leverage": {"label": "Leverage ratio", "fmt": "pct1", "col": schema.COL_LEVERAGE},
    "idle_liquidity": {
        "label": "Est. idle liquidity",
        "fmt": "money",
        "derived": "idle_liquidity",
    },
    "cash_pct_assets": {
        "label": "Idle liquidity / assets",
        "fmt": "pct1",
        "derived": "cash_pct_assets",
    },
    "liquidity_ratio": {
        "label": "Liquidity ratio",
        "fmt": "pct1",
        "col": schema.COL_LIQUIDITY,
    },
    "yield_earning": {
        "label": "Yield on earning assets",
        "fmt": "pct2",
        "col": schema.COL_YIELD_EA,
    },
    "fv_cost": {
        "label": "Securities FV / cost",
        "fmt": "pct1",
        "col": schema.COL_FV_COST,
    },
    "underwater": {
        "label": "Underwater (% of cost)",
        "fmt": "pct1",
        "derived": "underwater_pct",
    },
    "unrealized_loss": {
        "label": "Est. unrealized loss",
        "fmt": "money",
        "derived": "est_unrealized_loss",
    },
    "securities_yield": {
        "label": "Securities yield",
        "fmt": "pct2",
        "col": schema.COL_YIELD_SEC,
    },
    "pledged": {
        "label": "Pledged / securities",
        "fmt": "pct1",
        "col": schema.COL_PLEDGED,
    },
    "net_income": {
        "label": "Net income (qtr)",
        "fmt": "money",
        "col": schema.COL_NET_INCOME,
    },
    "roaa": {"label": "ROAA", "fmt": "pct2", "col": "ROAA (%)"},
    "roae": {"label": "ROAE", "fmt": "pct2", "col": "ROAE (%)"},
    "nim": {"label": "Net interest margin", "fmt": "pct2", "col": schema.COL_NIM},
    "cost_of_funds": {
        "label": "Cost of funds",
        "fmt": "pct2",
        "col": schema.COL_COST_FUNDS,
    },
    "yield_on_loans": {
        "label": "Yield on loans",
        "fmt": "pct2",
        "col": schema.COL_YIELD_LOANS,
    },
    "noninterest_dep": {
        "label": "Noninterest-bear. dep.",
        "fmt": "pct1",
        "col": schema.COL_NONINT_DEP,
    },
    "brokered_dep": {
        "label": "Brokered / deposits",
        "fmt": "pct1",
        "col": schema.COL_BROKERED,
    },
    "npas_assets": {"label": "NPAs / assets", "fmt": "pct2", "col": schema.COL_NPAS},
    "npls_loans": {"label": "NPLs / loans", "fmt": "pct2", "col": "NPLs/ Loans (%)"},
    "net_chargeoffs": {
        "label": "Net charge-offs / loans",
        "fmt": "pct2",
        "col": "Net Chargeoffs/ Avg Loans (%)",
    },
    "reserves_loans": {
        "label": "Reserves / gross loans",
        "fmt": "pct2",
        "col": "Loan Loss Reserves/ Gross Loans (%)",
    },
    "asset_growth": {
        "label": "Asset growth rate",
        "fmt": "pct1",
        "col": "Asset Growth Rate (%)",
    },
    "loan_growth": {
        "label": "Loan growth rate",
        "fmt": "pct1",
        "col": "Loan Growth Rate (%)",
    },
    "deposit_growth": {
        "label": "Deposit growth rate",
        "fmt": "pct1",
        "col": "Deposit Growth Rate (%)",
    },
}
GROUPS = [
    (
        "Size & balance sheet",
        [
            "total_assets",
            "total_loans",
            "total_deposits",
            "total_securities",
            "loans_deposits",
            "equity_assets",
            "leverage",
        ],
    ),
    (
        "Liquidity (Signal A)",
        ["idle_liquidity", "cash_pct_assets", "liquidity_ratio", "yield_earning"],
    ),
    (
        "Bond book (Signal B)",
        ["fv_cost", "underwater", "unrealized_loss", "securities_yield", "pledged"],
    ),
    ("Earnings (Signal C)", ["net_income", "roaa", "roae"]),
    (
        "Margin & funding",
        ["nim", "cost_of_funds", "yield_on_loans", "noninterest_dep", "brokered_dep"],
    ),
    (
        "Credit quality",
        ["npas_assets", "npls_loans", "net_chargeoffs", "reserves_loans"],
    ),
    ("Growth", ["asset_growth", "loan_growth", "deposit_growth"]),
]
DEFAULT_SNAPSHOT = [
    "total_assets",
    "nim",
    "total_loans",
    "cost_of_funds",
    "total_deposits",
    "yield_on_loans",
    "total_securities",
    "securities_yield",
    "idle_liquidity",
    "loans_deposits",
    "unrealized_loss",
    "fv_cost",
    "equity_assets",
    "leverage",
    "liquidity_ratio",
    "npas_assets",
]
DEFAULT_TREND = [
    "nim",
    "cost_of_funds",
    "fv_cost",
    "securities_yield",
    "liquidity_ratio",
    "net_income",
]
TREND_MAX = 8


def raw_value(fid, row):
    f = FIELDS.get(fid)
    if not f:
        return None
    return _derived(f["derived"], row) if "derived" in f else _num(row, f["col"])


def fmt_value(fid, row):
    f = FIELDS.get(fid)
    if not f:
        return "n/a"
    v = raw_value(fid, row)
    if v is None:
        return "n/a"
    if f["fmt"] == "money":
        return f"${v:,.0f}K"
    if f["fmt"] == "pct2":
        return f"{v:.2f}%"
    return f"{v:.1f}%"


def label(fid):
    f = FIELDS.get(fid)
    return f["label"] if f else fid


def sanitize(ids, default):
    out = [i for i in (ids or []) if i in FIELDS]
    return out or list(default)
