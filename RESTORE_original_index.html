# Handoff: Bank Universe (landing page redesign)

## Overview

Replaces the landing page of the Bond-Portfolio Opportunity Screen. The old
`index.html` was a setup form — pick banks, pick quarters, run analysis. That
puts a configuration step in front of a strategy desk that arrives wanting to
know where opportunity moved this quarter across the whole universe.

The new page lands on the screen **already run**: the full universe scored for
the newest detected quarter, ranked by composite, with a band showing what
changed since last quarter. Bank/quarter selection survives as an on-demand
"Custom screen" drawer that still POSTs to `/analyze` unchanged.

## About the design files

The files in this bundle are **design references created in HTML** — they show
intended look and behavior. `templates/` and `static/desk.css` are shaped for
this Flask/Jinja app and can be adopted close to as-is. `app_desk.py` cannot: it
names functions that may not exist under those names in `app.py`, and marks three
integration seams (`# >>> WIRE:`) that must be bound to the scoring code the
`/analyze` path already uses.

`Opportunity Screen.dc.html` is the interactive prototype. Open it in a browser
for spacing, both themes, and interaction behavior. It is not production code.

## Fidelity

**High-fidelity.** Colors, typography, spacing, and interaction states are final.
Recreate them exactly. Every token in the design already exists in `desk.css`.

## Screens / views

### Bank Universe — `/`

**Purpose:** the desk's arrival view. Answer "what moved and who should we call"
before any interaction.

**Layout:** two-column CSS grid, `212px minmax(0,1fr)`. Left rail is
`position:sticky; top:0; height:100vh`. Right column is a vertical stack:

1. **Header** — `padding:16px 22px 13px`, `border-bottom:1px solid var(--line)`,
   `background:var(--panel)`. `h1` "Bank Universe" at 19px/600/-0.01em. Below it a
   fact row: QUARTER LOADED / UNIVERSE SCREENED / Q/Q BASIS / ABOVE THRESHOLD,
   each a 9.5px 0.13em-tracked uppercase key over a 15px mono value, separated by
   1px × 26px vertical rules. Right side: Dark/Light toggle, Export CSV, and the
   gold "Custom screen" button.

2. **Status strip** — 7px/22px, `background:var(--panel2)`, 10.5px `var(--faint)`.
   Data dir (mono), workbook/quarter counts, rep-file status, a green freshness
   dot; right-aligned Refresh and "Run data QC →" (gold, underlined).

3. **Custom screen drawer** — hidden by default. Two columns
   (`minmax(0,1fr) 300px`): scrollable bank cohort checklist with its own search
   and live selected-count, and a 3-up grid of quarter chips (checked chips take
   the amber border and `#17222B` fill). Submits to `/analyze`.

4. **What-changed band** — grid `minmax(0,1fr) 1px minmax(0,340px)`, collapsing to
   one column under 1100px.
   - *Moved this quarter*: `repeat(auto-fit,minmax(154px,1fr))` cards. Each card:
     bank name 11.5px/500 truncated, delta at 19px mono/600 (amber-red `#E2653F`
     up, `#5A7186` down), `prev→now` pair at 10.5px mono, driver clause at 10px.
     **The auto-fit minimum matters** — a fixed 5-column track crushed the cards
     below their content width and overflowed the borders at desk widths.
   - *New to the top decile*: rows with a 3px × 20px `#E2653F` tick, bank name,
     rep line, and `prevRank → rank` in mono.

5. **Refine toolbar** — 10px/22px, hairline bottom. REFINE label, 246px text
   input, rep select, band select, conditional gold "clear", right-aligned count
   in mono.

6. **Ledger** — grid `88px minmax(150px,1fr) 96px 84px 84px 84px 74px 78px`,
   `min-width:800px` inside an `overflow-x:auto` wrapper. Header row 30px on
   `var(--panel2)` with 9.5px/0.12em keys. Body rows 46px, `border-bottom:1px
   solid var(--line2)`, hover `var(--hover)`, and a 2px left border in amber when
   the composite clears the threshold. Rank cell carries a 64px × 5px position
   track. Signal cells pair a 19px-wide mono percentile with a 46px × 4px bar in
   the heat color. Δ Q/Q and COMPOSITE are right-aligned; composite is 15px/600.

## Interactions & behavior

- Rep and band selects submit the GET form on change. The text input submits
  420ms after the last keystroke.
- Dropdowns are co-filtered: each one's counts reflect the other's selection, so
  no combination returns zero.
- Ledger rows, mover cards, and entrant rows are `<a>` elements opening the PDF
  hand-off in a new tab.
- Custom screen button toggles the drawer, flips to an outline style, and swaps
  its label to "Custom screen ✕". `aria-expanded` / `aria-controls` are set.
- Theme toggle writes `sss.desk.theme` to localStorage and applies `.theme-light`
  on the `.desk` root and `<body>`.
- Empty states: no prior quarter → movers band shows an empty line; no filter
  matches → ledger shows a clear-filters message; rep file missing → status strip
  reports it.

## State

Server-rendered; all filter state lives in query params on `/` (`q`,
`rep_filter`, `band`). Client state is only the drawer's open/closed flag and the
theme preference.

Data fetching: `screen_universe(as_of, settings)` scores the full universe for the
current and prior quarters, memoized on `(as_of, settings_fingerprint)`. It must
be invalidated wherever `/refresh` clears the workbook cache.

## Design tokens

Dark (default) → light:

| token | dark | light |
| --- | --- | --- |
| `--bg` | `#0A1420` | `#EFF2F7` |
| `--panel` | `#0B1826` | `#FFFFFF` |
| `--panel2` | `#0C1A2A` | `#F6F8FC` |
| `--line` | `#1B2C42` | `#D9E0EA` |
| `--line2` | `#14263A` | `#E9EEF4` |
| `--border` | `#24384F` | `#CBD5E2` |
| `--borderHi` | `#3A5470` | `#9AAABF` |
| `--text` | `#E9EEF6` | `#0B2545` |
| `--text2` | `#B7C7DA` | `#3B5375` |
| `--muted` | `#7E93AE` | `#5C7189` |
| `--dim` | `#5D7391` | `#6B7F99` |
| `--faint` | `#4E637F` | `#8DA0B6` |
| `--hover` | `#101F31` | `#F3F6FB` |
| `--track` | `#1D3149` | `#DCE4EE` |
| `--gold` | `#C9A227` | `#9A7412` |
| `--rail` | `#0B1826` | `#002F6C` |
| `--railSel` | `#14283E` | `#0B4192` |

Fixed across themes: amber action `#E9A93C`; percentile heat ramp `#E2653F` (80+),
`#C08243` (60–79), `#7E8B9C` (40–59), `#5A7186` (20–39), `#3F6584` (0–19); status
green `#4E9A6A`.

Type: IBM Plex Sans for UI, IBM Plex Mono for every numeral, always with
`font-variant-numeric: tabular-nums`. Scale in use: 19 / 15 / 13.5 / 13 / 12.5 /
11.5 / 11 / 10.5 / 10 / 9.5px. **Nothing below 9.5px.** Section labels are 9.5px,
600 weight, 0.12–0.16em tracking, uppercase.

Geometry: no border radius anywhere — every edge is square. Borders are 1px
hairlines. No shadows except the PDF preview card.

## Assets

- `static/southstate_logo.png` — existing, reused in the rail at 152px wide
- IBM Plex Sans + Mono via Google Fonts (linked in `base_desk.html`)

No new imagery.

## Files

| file | role |
| --- | --- |
| `templates/base_desk.html` | chrome-free base: left rail, theme toggle. **Do not merge into `base.html`** — the other pages keep the topbar. |
| `templates/index.html` | the landing template |
| `static/desk.css` | all styles, scoped under `.desk` |
| `app_desk.py` | reference view logic; three `# >>> WIRE:` seams |
| `COPILOT_PROMPT.md` | the brief to hand Copilot |
| `Opportunity Screen.dc.html` | interactive prototype — open in a browser |

## Not in scope

`results.html`, `settings.html`, `validate.html`, the `/analyze` POST contract,
PDF generation, and `static/style.css` are all untouched.
