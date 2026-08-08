# Copilot prompt — implement the Bank Universe landing page

Paste everything below the line into Copilot Chat with this folder open in the
workspace. It assumes Opus, so it is written as a brief rather than a
step-by-step script — state the goal and the constraints, let it plan.

---

You are working in an internal Flask app for the SouthState Securities strategy
desk. It screens depository call-report data (SNL / Capital IQ Pro workbooks) and
scores each bank 0–100 on three signals — A idle liquidity, B underwater bond
book, C net income q/q — plus a weighted composite, all as percentiles against
the full universe of ~4,530 banks. It produces a per-bank PDF call-prep hand-off.

Current structure: `app.py`, `templates/{base,index,results,settings,validate}.html`,
`static/style.css`. `index.html` is the landing page and today it is a *setup
form*: choose banks, choose quarters, POST to `/analyze`, then read `results.html`.

## The task

Replace the landing page with a screen that is **already run**. The desk does not
arrive knowing which bank it wants; it arrives wanting to know where opportunity
moved this quarter across the whole universe. Selection becomes refinement, not a
gate.

A design reference has been built and approved. In this folder:

- `templates/base_desk.html` — new chrome-free base with the left rail and theme toggle
- `templates/index.html` — the new landing template
- `static/desk.css` — all styles, scoped under `.desk`
- `app_desk.py` — reference view logic, with three seams marked `# >>> WIRE:`
- `Opportunity Screen.dc.html` — the full interactive design prototype; open it in
  a browser to see intended behavior, spacing, and both themes

Treat these as **design references to implement against**, not code to paste
blindly. The CSS and templates are production-shaped and can be adopted close to
as-is; `app_desk.py` cannot — it names functions that may not exist under those
names in `app.py`.

## What the page must do

1. **Land on the ranked ledger.** Full universe, newest detected quarter, sorted
   by composite descending, top `PRESCREEN_N` (25) rows shown. No form in front
   of it.

2. **A "what changed" band above the ledger.** Two parts: the five largest
   composite moves vs the prior quarter (with a one-clause driver naming the
   signal that moved most), and the banks that newly crossed into the top decile
   (rank ≤ 10% of universe) since last quarter. This requires scoring the prior
   quarter too — see caching below.

3. **Refine, don't gate.** Rep filter, asset-size band, and free-text search sit
   above the ledger as GET params on `/`. Both dropdowns are *co-filtered*: each
   one's option counts reflect the other's current selection, so the desk can
   never pick a combination that returns nothing. Carry the asset bands over from
   the old `index.html` verbatim.

4. **Desk header, not a data-source card.** Lead with quarter loaded, universe
   size, q/q basis, and how many banks clear the scoring threshold. Demote
   `data_dir`, workbook cache count, rep-file status, refresh, and the Data QC
   link into a thin status strip below it.

5. **Keep the picker as a drawer.** The bank/quarter selection UI survives as an
   on-demand "Custom screen" panel that still POSTs to `/analyze` with the same
   `banks` / `quarters` field names. Nothing about `/analyze` or `results.html`
   changes.

## Wiring you must do

`app_desk.py` marks three seams:

- **WIRE 1** — call the existing scorer over the whole universe (`banks=None`),
  the same path `/analyze` uses.
- **WIRE 2** — resolve the prior quarter and score it too, for the q/q deltas.
  Wrap it in `try/except`: a missing or malformed back-quarter must degrade the
  movers band to an empty state, never 500 the landing page.
- **WIRE 3** — settings, quarter detection, bank list, cache/rep status, data dir.

Fold these into `app.py`'s existing `home()` route rather than adding a new
route. Keep the function names and row shape that `results.html` already
consumes (`r.key`, `r.bank`, `r.location`, `r.rep.name`, `r.rep.unassigned`,
`r.universe_rank`, `r.universe_total`, `r.signal_a.score`, `r.signal_a.rationale`,
`r.composite`) and add only `prev_composite`, `prev_rank`, `delta`, `assets_raw`,
`assets_fmt`.

## Non-negotiables

- **Performance.** Scoring ~4,530 banks twice (current + prior quarter) on every
  page load is unacceptable. Memoize on `(as_of, settings_fingerprint)` and clear
  it from the same place `/refresh` clears the workbook cache. If a cold load
  still exceeds ~2s, render the header and status strip immediately and load the
  band + ledger via a second request — but measure first.
- **`describe_driver` must stay deterministic.** No LLM call. It is a scan aid on
  a dense page; it has to be instant and identical across reloads.
- **Do not touch** `results.html`, `settings.html`, `validate.html`, the `/analyze`
  POST contract, the PDF generation path, or `static/style.css`. `desk.css` is
  additive and fully scoped under `.desk`.
- **`base_desk.html` is deliberately separate** from `base.html`. The landing page
  is full-bleed with its own left rail and must not inherit the topbar, container
  width, or footer. Leave `base.html` alone for the other pages.
- **Empty states are required, not optional.** No prior quarter → movers band
  shows its empty line. Filters match nothing → ledger shows a clear-filters
  message. Rep file missing → status strip says so.
- **Accessibility.** Ledger rows are links, not click-handlers on divs. The drawer
  toggle carries `aria-expanded` / `aria-controls`. Nothing smaller than 9.5px.

## Definition of done

`/` renders the ranked ledger with no interaction. Changing any filter re-renders
in under a second. The movers band and top-decile entrants reflect real prior-quarter
data. "Custom screen" opens, selects a cohort, and lands on the unchanged results
page. `/refresh` invalidates the new cache. Dark and light themes both render, and
the choice persists across requests.

Before you write code: read `app.py` and tell me which existing functions you are
binding each of the three WIRE seams to, and flag anything in the row shape above
that does not already exist. Then implement.