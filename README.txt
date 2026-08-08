<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  html,body{margin:0;padding:0;background:#0A1420;}
  *{box-sizing:border-box;}
  a{color:#C9A227;text-decoration:none;}
  a:hover{color:#E4C257;}
  select{appearance:none;-webkit-appearance:none;}
</style>
</helmet>
<div style="{{ themeStyle }}">
<div style="font-family:'IBM Plex Sans',system-ui,sans-serif;background:var(--bg,#0A1420);color:var(--text,#E9EEF6);min-height:100vh;display:grid;grid-template-columns:212px minmax(0,1fr);">

  <aside style="border-right:1px solid var(--railLine,#1B2C42);background:var(--rail,#0B1826);display:flex;flex-direction:column;position:sticky;top:0;height:100vh;">
    <div style="padding:20px 18px 16px;border-bottom:1px solid var(--railLine,#1B2C42);display:flex;flex-direction:column;gap:11px;">
      <img src="assets/sss-lockup.png" alt="SouthState Securities" style="width:152px;height:auto;display:block;">
      <div style="font-size:11px;color:var(--railDim,#5D7391);letter-spacing:0.04em;">Bank Portfolio Screen</div>
    </div>

    <nav style="display:flex;flex-direction:column;gap:2px;padding:12px 10px;">
      <div style="font-size:9.5px;letter-spacing:0.16em;color:var(--railFaint,#4E637F);padding:6px 8px 8px;font-weight:600;">WORKSPACE</div>
      <div onClick="{{ goDesk }}" style="{{ navAnalyze }}"><span style="{{ navAnalyzeNum }}">01</span> Bank Universe</div>
      <div style="display:flex;align-items:center;gap:9px;padding:7px 9px;font-size:13px;color:var(--railMuted,#8AA0BC);border-left:2px solid transparent;cursor:pointer;" style-hover="color:var(--railText,#E9EEF6);background:var(--railHover,#0F2135);"><span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--railFaint,#4E637F);">02</span> Data QC</div>
      <div onClick="{{ goSettings }}" style="{{ navSettings }}"><span style="{{ navSettingsNum }}">03</span> Settings</div>
    </nav>

    <div style="margin-top:auto;padding:14px 16px;border-top:1px solid var(--railLine,#1B2C42);display:flex;flex-direction:column;gap:7px;">
      <div style="display:flex;justify-content:space-between;align-items:baseline;">
        <span style="font-size:10px;color:var(--railDim,#5D7391);letter-spacing:0.08em;">UNIVERSE</span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--railMuted,#B7C7DA);">4,530</span>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:baseline;">
        <span style="font-size:10px;color:var(--railDim,#5D7391);letter-spacing:0.08em;">QUARTERS</span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--railMuted,#B7C7DA);">13</span>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:baseline;">
        <span style="font-size:10px;color:var(--railDim,#5D7391);letter-spacing:0.08em;">REPS</span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--railMuted,#B7C7DA);">38</span>
      </div>
      <div style="display:flex;align-items:center;gap:6px;margin-top:3px;">
        <div style="width:5px;height:5px;border-radius:50%;background:#4E9A6A;"></div>
        <span style="font-size:10px;color:var(--railDim,#5D7391);">SNL cache · 1 workbook</span>
      </div>
    </div>
  </aside>

  <div style="display:flex;flex-direction:column;min-width:0;">

    <sc-if value="{{ isDesk }}" hint-placeholder-val="{{ true }}">
      <div style="display:flex;flex-direction:column;min-width:0;">

        <header style="border-bottom:1px solid var(--line,#1B2C42);padding:16px 22px 13px;display:flex;align-items:flex-start;justify-content:space-between;gap:24px;background:var(--panel,#0B1826);">
          <div style="display:flex;flex-direction:column;gap:9px;min-width:0;">
            <h1 style="margin:0;font-size:19px;font-weight:600;letter-spacing:-0.01em;color:var(--text,#E9EEF6);">Bank Universe</h1>
            <div style="display:flex;align-items:baseline;gap:22px;flex-wrap:wrap;">
              <div style="display:flex;flex-direction:column;gap:1px;">
                <span style="font-size:9.5px;letter-spacing:0.13em;color:var(--dim,#5D7391);font-weight:600;">QUARTER LOADED</span>
                <span style="font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:600;color:var(--text,#E9EEF6);font-variant-numeric:tabular-nums;">2026Q1</span>
              </div>
              <div style="width:1px;height:26px;background:var(--line,#1B2C42);"></div>
              <div style="display:flex;flex-direction:column;gap:1px;">
                <span style="font-size:9.5px;letter-spacing:0.13em;color:var(--dim,#5D7391);font-weight:600;">UNIVERSE SCREENED</span>
                <span style="font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:600;color:var(--text,#E9EEF6);font-variant-numeric:tabular-nums;">4,530</span>
              </div>
              <div style="width:1px;height:26px;background:var(--line,#1B2C42);"></div>
              <div style="display:flex;flex-direction:column;gap:1px;">
                <span style="font-size:9.5px;letter-spacing:0.13em;color:var(--dim,#5D7391);font-weight:600;">Q/Q BASIS</span>
                <span style="font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:500;color:var(--text2,#B7C7DA);font-variant-numeric:tabular-nums;">vs 2025Q4</span>
              </div>
              <div style="width:1px;height:26px;background:var(--line,#1B2C42);"></div>
              <div style="display:flex;flex-direction:column;gap:1px;">
                <span style="font-size:9.5px;letter-spacing:0.13em;color:var(--dim,#5D7391);font-weight:600;">ABOVE THRESHOLD</span>
                <span style="font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:600;color:#E2653F;font-variant-numeric:tabular-nums;">{{ aboveLabel }}</span>
              </div>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:8px;flex:0 0 auto;">
            <div style="display:flex;border:1px solid var(--border,#24384F);">
              <button onClick="{{ setDark }}" style="{{ darkBtn }}">Dark</button>
              <button onClick="{{ setLight }}" style="{{ lightBtn }}">Light</button>
            </div>
            <button style="font-family:inherit;font-size:12px;padding:6px 11px;background:transparent;color:var(--muted,#8AA0BC);border:1px solid var(--border,#24384F);cursor:pointer;" style-hover="color:var(--text,#E9EEF6);border-color:var(--borderHi,#3A5470);">Export CSV</button>
            <button onClick="{{ toggleCustom }}" style="{{ customBtn }}">{{ customLabel }}</button>
          </div>
        </header>

        <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:7px 22px;border-bottom:1px solid var(--line,#1B2C42);background:var(--panel2,#0C1A2A);font-size:10.5px;color:var(--faint,#4E637F);">
          <span style="font-family:'IBM Plex Mono',monospace;">~/snl_exports/quarterly</span>
          <span style="color:var(--line,#1B2C42);">|</span>
          <span>1 workbook cached · 13 quarters detected</span>
          <span style="color:var(--line,#1B2C42);">|</span>
          <span>rep file loaded · 4,276 of 4,530 banks mapped across 38 reps</span>
          <span style="display:flex;align-items:center;gap:5px;"><span style="width:5px;height:5px;border-radius:50%;background:#4E9A6A;display:inline-block;"></span>fresh</span>
          <span style="margin-left:auto;display:flex;align-items:center;gap:14px;">
            <span onClick="{{ noop }}" style="color:var(--muted,#7E93AE);cursor:pointer;" style-hover="color:var(--text,#E9EEF6);">↻ Refresh data</span>
            <span onClick="{{ noop }}" style="color:var(--gold,#C9A227);cursor:pointer;border-bottom:1px solid var(--goldLine,#43391A);">Run data QC →</span>
          </span>
        </div>

        <sc-if value="{{ customOpen }}" hint-placeholder-val="{{ false }}">
          <div style="border-bottom:1px solid var(--line,#1B2C42);background:var(--panel,#0B1826);padding:16px 22px 18px;display:flex;flex-direction:column;gap:13px;">
            <div style="display:flex;align-items:baseline;justify-content:space-between;gap:16px;">
              <div style="display:flex;flex-direction:column;gap:2px;">
                <div style="font-size:13.5px;font-weight:600;color:var(--text,#E9EEF6);">Custom screen</div>
                <div style="font-size:11.5px;color:var(--muted,#7E93AE);">Pick a cohort or a back-quarter comparison. Scores stay relative to the full universe for the most recent quarter selected.</div>
              </div>
              <span onClick="{{ toggleCustom }}" style="font-size:11.5px;color:var(--muted,#7E93AE);cursor:pointer;flex:0 0 auto;" style-hover="color:var(--text,#E9EEF6);">Close ✕</span>
            </div>
            <div style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:18px;align-items:start;">
              <div style="display:flex;flex-direction:column;gap:7px;min-width:0;">
                <div style="display:flex;align-items:center;justify-content:space-between;">
                  <span style="font-size:9.5px;letter-spacing:0.13em;color:var(--dim,#5D7391);font-weight:600;">BANK COHORT</span>
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:10.5px;color:var(--gold,#C9A227);">{{ pickedLabel }}</span>
                </div>
                <div style="border:1px solid var(--border,#24384F);max-height:196px;overflow-y:auto;background:var(--panel2,#0C1A2A);">
                  <sc-for list="{{ pickRows }}" as="p" hint-placeholder-count="8">
                    <div onClick="{{ p.toggle }}" style="display:flex;align-items:center;gap:9px;padding:6px 11px;cursor:pointer;border-bottom:1px solid var(--line2,#14263A);" style-hover="background:var(--hover,#101F31);">
                      <div style="{{ p.box }}"></div>
                      <span style="font-size:12px;color:var(--text2,#B7C7DA);">{{ p.bank }}</span>
                      <span style="font-family:'IBM Plex Mono',monospace;font-size:10.5px;color:var(--faint,#4E637F);margin-left:auto;font-variant-numeric:tabular-nums;">{{ p.assets }}</span>
                    </div>
                  </sc-for>
                </div>
              </div>
              <div style="display:flex;flex-direction:column;gap:7px;">
                <div style="font-size:9.5px;letter-spacing:0.13em;color:var(--dim,#5D7391);font-weight:600;">QUARTERS</div>
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5px;">
                  <sc-for list="{{ quarterRows }}" as="q" hint-placeholder-count="13">
                    <div onClick="{{ q.toggle }}" style="{{ q.style }}">{{ q.label }}</div>
                  </sc-for>
                </div>
              </div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;">
              <button onClick="{{ runCustom }}" style="font-family:inherit;font-size:12.5px;font-weight:600;padding:8px 14px;background:#E9A93C;color:#0A1420;border:none;cursor:pointer;">Run custom screen</button>
              <span onClick="{{ clearPicks }}" style="font-size:11.5px;color:var(--muted,#7E93AE);cursor:pointer;" style-hover="color:var(--text,#E9EEF6);">Clear selection</span>
            </div>
          </div>
        </sc-if>

        <div style="display:grid;grid-template-columns:minmax(0,1fr) 1px minmax(0,340px);border-bottom:1px solid var(--line,#1B2C42);background:var(--panel,#0B1826);">
          <div style="padding:13px 22px 14px;display:flex;flex-direction:column;gap:9px;min-width:0;">
            <div style="display:flex;align-items:center;gap:10px;">
              <span style="font-size:9.5px;letter-spacing:0.14em;color:var(--dim,#5D7391);font-weight:600;">MOVED THIS QUARTER</span>
              <span style="font-size:10.5px;color:var(--faint,#4E637F);">largest composite change vs 2025Q4</span>
            </div>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(154px,1fr));gap:8px;">
              <sc-for list="{{ movers }}" as="m" hint-placeholder-count="5">
                <div onClick="{{ m.open }}" style="border:1px solid var(--border,#24384F);background:var(--panel2,#0C1A2A);padding:9px 10px 10px;display:flex;flex-direction:column;gap:6px;cursor:pointer;min-width:0;" style-hover="border-color:var(--borderHi,#3A5470);">
                  <div style="font-size:11.5px;font-weight:500;color:var(--text,#E9EEF6);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{ m.bank }}</div>
                  <div style="display:flex;align-items:baseline;gap:7px;flex-wrap:wrap;min-width:0;">
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:19px;font-weight:600;line-height:1;color:{{ m.color }};font-variant-numeric:tabular-nums;">{{ m.delta }}</span>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:10.5px;color:var(--faint,#4E637F);font-variant-numeric:tabular-nums;white-space:nowrap;">{{ m.from }}→{{ m.to }}</span>
                  </div>
                  <div style="font-size:10px;color:var(--dim,#5D7391);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{ m.driver }}</div>
                </div>
              </sc-for>
            </div>
          </div>
          <div style="background:var(--line,#1B2C42);"></div>
          <div style="padding:13px 22px 14px;display:flex;flex-direction:column;gap:9px;min-width:0;">
            <div style="display:flex;align-items:center;gap:10px;">
              <span style="font-size:9.5px;letter-spacing:0.14em;color:var(--dim,#5D7391);font-weight:600;">NEW TO THE TOP DECILE</span>
              <span style="font-family:'IBM Plex Mono',monospace;font-size:10.5px;color:var(--faint,#4E637F);">rank ≤ 453</span>
            </div>
            <div style="display:flex;flex-direction:column;">
              <sc-for list="{{ entrants }}" as="e" hint-placeholder-count="3">
                <div onClick="{{ e.open }}" style="display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:1px solid var(--line2,#14263A);cursor:pointer;min-width:0;" style-hover="background:var(--hover,#101F31);">
                  <div style="width:3px;height:20px;background:#E2653F;flex:0 0 auto;"></div>
                  <div style="display:flex;flex-direction:column;gap:1px;min-width:0;flex:1;">
                    <span style="font-size:11.5px;font-weight:500;color:var(--text,#E9EEF6);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{ e.bank }}</span>
                    <span style="font-size:10px;color:var(--dim,#5D7391);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{ e.rep }}</span>
                  </div>
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--muted,#7E93AE);font-variant-numeric:tabular-nums;white-space:nowrap;">{{ e.prevRank }} → {{ e.rank }}</span>
                </div>
              </sc-for>
            </div>
          </div>
        </div>

        <div style="display:flex;align-items:center;gap:9px;flex-wrap:wrap;padding:10px 22px;border-bottom:1px solid var(--line,#1B2C42);">
          <span style="font-size:9.5px;letter-spacing:0.14em;color:var(--dim,#5D7391);font-weight:600;">REFINE</span>
          <input value="{{ q }}" onChange="{{ onQ }}" placeholder="Filter 4,530 banks by name or city…" style="font-family:inherit;font-size:11.5px;padding:5px 9px;width:246px;background:var(--panel2,#0C1A2A);color:var(--text,#E9EEF6);border:1px solid var(--border,#24384F);">
          <select value="{{ rep }}" onChange="{{ onRep }}" style="{{ selectStyle }}">
            <sc-for list="{{ deskRepOptions }}" as="o" hint-placeholder-count="5">
              <option value="{{ o.v }}">{{ o.label }}</option>
            </sc-for>
          </select>
          <select value="{{ band }}" onChange="{{ onBand }}" style="{{ selectStyle }}">
            <sc-for list="{{ bandOptions }}" as="o" hint-placeholder-count="7">
              <option value="{{ o.v }}">{{ o.label }}</option>
            </sc-for>
          </select>
          <sc-if value="{{ anyFilter }}" hint-placeholder-val="{{ false }}">
            <span onClick="{{ clearFilters }}" style="font-size:11px;color:var(--gold,#C9A227);cursor:pointer;border-bottom:1px solid var(--goldLine,#43391A);">clear</span>
          </sc-if>
          <span style="margin-left:auto;font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--muted,#7E93AE);font-variant-numeric:tabular-nums;">{{ deskCount }}</span>
        </div>

        <div style="overflow-x:auto;">
          <div style="display:grid;grid-template-columns:88px minmax(150px,1fr) 96px 84px 84px 84px 74px 78px;padding:0 22px;height:30px;align-items:center;border-bottom:1px solid var(--line,#1B2C42);background:var(--panel2,#0C1A2A);min-width:800px;">
            <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;">RANK</div>
            <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;">BANK</div>
            <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;">REP</div>
            <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;">A <span style="color:var(--faint,#3E5673);font-weight:400;">liq</span></div>
            <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;">B <span style="color:var(--faint,#3E5673);font-weight:400;">book</span></div>
            <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;">C <span style="color:var(--faint,#3E5673);font-weight:400;">n/i</span></div>
            <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;text-align:right;">Δ Q/Q</div>
            <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;text-align:right;">COMPOSITE</div>
          </div>

          <sc-for list="{{ deskRows }}" as="row" hint-placeholder-count="14">
            <div onClick="{{ row.open }}" style="display:grid;grid-template-columns:88px minmax(150px,1fr) 96px 84px 84px 84px 74px 78px;padding:0 22px;height:46px;align-items:center;border-bottom:1px solid var(--line2,#14263A);cursor:pointer;border-left:2px solid {{ row.mark }};min-width:800px;" style-hover="background:var(--hover,#101F31);">
              <div style="display:flex;flex-direction:column;gap:2px;">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:13px;font-weight:500;color:var(--text,#E9EEF6);font-variant-numeric:tabular-nums;">{{ row.rankStr }}</div>
                <svg width="64" height="5" viewBox="0 0 64 5">
                  <rect x="0" y="1.5" width="64" height="2" fill="var(--track,#1D3149)"></rect>
                  <rect x="{{ row.rankX }}" y="0" width="2" height="5" fill="var(--muted,#8AA0BC)"></rect>
                </svg>
              </div>
              <div style="display:flex;flex-direction:column;gap:1px;min-width:0;padding-right:12px;">
                <div style="font-size:13px;font-weight:500;color:var(--text,#E9EEF6);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{ row.bank }}</div>
                <div style="font-size:10.5px;color:var(--dim,#5D7391);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{ row.loc }} · {{ row.assets }}</div>
              </div>
              <div style="min-width:0;padding-right:10px;">
                <span style="font-size:11px;color:var(--text2,#9FB2C8);border:1px solid var(--border,#2C4560);padding:2px 6px;white-space:nowrap;">{{ row.rep }}</span>
              </div>
              <div style="display:flex;align-items:center;gap:7px;">
                <span style="font-family:'IBM Plex Mono',monospace;font-size:12.5px;color:{{ row.a.color }};width:19px;font-variant-numeric:tabular-nums;">{{ row.a.v }}</span>
                <svg width="46" height="14" viewBox="0 0 46 14">
                  <rect x="0" y="5" width="46" height="4" fill="var(--track,#1D3149)"></rect>
                  <rect x="0" y="5" width="{{ row.a.w }}" height="4" fill="{{ row.a.color }}"></rect>
                </svg>
              </div>
              <div style="display:flex;align-items:center;gap:7px;">
                <span style="font-family:'IBM Plex Mono',monospace;font-size:12.5px;color:{{ row.b.color }};width:19px;font-variant-numeric:tabular-nums;">{{ row.b.v }}</span>
                <svg width="46" height="14" viewBox="0 0 46 14">
                  <rect x="0" y="5" width="46" height="4" fill="var(--track,#1D3149)"></rect>
                  <rect x="0" y="5" width="{{ row.b.w }}" height="4" fill="{{ row.b.color }}"></rect>
                </svg>
              </div>
              <div style="display:flex;align-items:center;gap:7px;">
                <span style="font-family:'IBM Plex Mono',monospace;font-size:12.5px;color:{{ row.c.color }};width:19px;font-variant-numeric:tabular-nums;">{{ row.c.v }}</span>
                <svg width="46" height="14" viewBox="0 0 46 14">
                  <rect x="0" y="5" width="46" height="4" fill="var(--track,#1D3149)"></rect>
                  <rect x="0" y="5" width="{{ row.c.w }}" height="4" fill="{{ row.c.color }}"></rect>
                </svg>
              </div>
              <div style="text-align:right;font-family:'IBM Plex Mono',monospace;font-size:12.5px;color:{{ row.dColor }};font-variant-numeric:tabular-nums;">{{ row.delta }}</div>
              <div style="display:flex;align-items:center;justify-content:flex-end;gap:8px;">
                <svg width="34" height="16" viewBox="0 0 34 16">
                  <polyline points="{{ row.spark }}" fill="none" stroke="var(--faint,#3E5673)" stroke-width="1.25"></polyline>
                </svg>
                <span style="font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:600;color:{{ row.comp.color }};font-variant-numeric:tabular-nums;">{{ row.comp.v }}</span>
              </div>
            </div>
          </sc-for>

          <div style="padding:11px 22px 22px;font-size:11px;color:var(--faint,#4E637F);min-width:800px;">{{ deskFoot }}</div>
        </div>
      </div>
    </sc-if>

    <sc-if value="{{ isResults }}" hint-placeholder-val="{{ false }}">
      <div style="display:flex;flex-direction:column;min-width:0;">
        <header style="border-bottom:1px solid var(--line,#1B2C42);padding:16px 22px 14px;display:flex;align-items:flex-start;justify-content:space-between;gap:24px;background:var(--panel,#0B1826);">
          <div style="display:flex;flex-direction:column;gap:7px;min-width:0;">
            <h1 style="margin:0;font-size:19px;font-weight:600;letter-spacing:-0.01em;color:var(--text,#E9EEF6);">Opportunity Screen — Results</h1>
            <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;font-size:11.5px;color:var(--muted,#7E93AE);">
              <span>As-of <b style="color:var(--text,#E9EEF6);font-family:'IBM Plex Mono',monospace;font-weight:500;">2026Q1</b></span>
              <span style="color:var(--faint,#2A4059);">/</span>
              <span>q/q vs <span style="font-family:'IBM Plex Mono',monospace;color:var(--text2,#B7C7DA);">2025Q4</span></span>
              <span style="color:var(--faint,#2A4059);">/</span>
              <span>vs. universe of <span style="font-family:'IBM Plex Mono',monospace;color:var(--text2,#B7C7DA);">4,530</span></span>
              <span style="color:var(--faint,#2A4059);">/</span>
              <span style="display:flex;align-items:center;gap:7px;">
                <span>Rep filter</span>
                <select value="{{ rep }}" onChange="{{ onRep }}" style="{{ selectStyle }}">
                  <sc-for list="{{ repOptions }}" as="o" hint-placeholder-count="5">
                    <option value="{{ o.v }}">{{ o.label }}</option>
                  </sc-for>
                </select>
                <sc-if value="{{ repActive }}" hint-placeholder-val="{{ false }}">
                  <span onClick="{{ clearRep }}" style="font-size:11px;color:var(--gold,#C9A227);cursor:pointer;border-bottom:1px solid var(--goldLine,#43391A);">clear</span>
                </sc-if>
              </span>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:8px;flex:0 0 auto;">
            <div style="display:flex;border:1px solid var(--border,#24384F);">
              <button onClick="{{ setDark }}" style="{{ darkBtn }}">Dark</button>
              <button onClick="{{ setLight }}" style="{{ lightBtn }}">Light</button>
            </div>
            <button style="font-family:inherit;font-size:12px;padding:6px 11px;background:transparent;color:var(--muted,#8AA0BC);border:1px solid var(--border,#24384F);cursor:pointer;" style-hover="color:var(--text,#E9EEF6);border-color:var(--borderHi,#3A5470);">Export CSV</button>
            <button onClick="{{ goDesk }}" style="font-family:inherit;font-size:12px;padding:6px 11px;background:transparent;color:var(--muted,#8AA0BC);border:1px solid var(--border,#24384F);cursor:pointer;" style-hover="color:var(--text,#E9EEF6);border-color:var(--borderHi,#3A5470);">← Back to bank universe</button>
            <button style="font-family:inherit;font-size:12px;font-weight:600;padding:6px 12px;background:#E9A93C;color:#0A1420;border:1px solid #E9A93C;cursor:pointer;">{{ batchLabel }}</button>
          </div>
        </header>

        <div style="display:grid;grid-template-columns:minmax(0,1fr) 452px;align-items:start;min-height:0;">

          <section style="min-width:0;border-right:1px solid var(--line,#1B2C42);overflow-x:auto;">
            <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;padding:10px 22px 9px;border-bottom:1px solid var(--line,#1B2C42);min-width:708px;">
              <div style="display:flex;align-items:center;gap:10px;">
                <span style="font-size:10px;letter-spacing:0.14em;color:var(--dim,#5D7391);font-weight:600;">RANKED LEDGER</span>
                <span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--muted,#7E93AE);">{{ countLabel }}</span>
              </div>
              <div style="display:flex;align-items:center;gap:10px;font-size:10px;color:var(--dim,#5D7391);">
                <span style="letter-spacing:0.08em;">PERCENTILE</span>
                <div style="display:flex;align-items:center;gap:5px;">
                  <span style="font-family:'IBM Plex Mono',monospace;">0</span>
                  <div style="width:88px;height:6px;background:linear-gradient(90deg,#2F5F80,#5A7186,#8C7E62,#C08243,#E2653F);"></div>
                  <span style="font-family:'IBM Plex Mono',monospace;">100</span>
                </div>
              </div>
            </div>

            <div style="display:grid;grid-template-columns:88px minmax(150px,1fr) 96px 84px 84px 84px 78px;padding:0 22px;height:30px;align-items:center;border-bottom:1px solid var(--line,#1B2C42);background:var(--panel2,#0C1A2A);min-width:708px;">
              <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;">RANK</div>
              <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;">BANK</div>
              <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;">REP</div>
              <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;">A <span style="color:var(--faint,#3E5673);font-weight:400;">liq</span></div>
              <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;">B <span style="color:var(--faint,#3E5673);font-weight:400;">book</span></div>
              <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;">C <span style="color:var(--faint,#3E5673);font-weight:400;">n/i</span></div>
              <div style="font-size:9.5px;letter-spacing:0.12em;color:var(--dim,#5D7391);font-weight:600;text-align:right;">COMPOSITE</div>
            </div>

            <sc-for list="{{ rows }}" as="row" hint-placeholder-count="9">
              <div onClick="{{ row.select }}" style="display:grid;grid-template-columns:88px minmax(150px,1fr) 96px 84px 84px 84px 78px;padding:0 22px;height:46px;align-items:center;border-bottom:1px solid var(--line2,#14263A);cursor:pointer;border-left:2px solid {{ row.mark }};background:{{ row.bg }};min-width:708px;" style-hover="background:var(--hover,#101F31);">
                <div style="display:flex;flex-direction:column;gap:2px;">
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:13px;font-weight:500;color:var(--text,#E9EEF6);font-variant-numeric:tabular-nums;">{{ row.rankStr }}</div>
                  <svg width="64" height="5" viewBox="0 0 64 5">
                    <rect x="0" y="1.5" width="64" height="2" fill="var(--track,#1D3149)"></rect>
                    <rect x="{{ row.rankX }}" y="0" width="2" height="5" fill="var(--muted,#8AA0BC)"></rect>
                  </svg>
                </div>
                <div style="display:flex;flex-direction:column;gap:1px;min-width:0;padding-right:12px;">
                  <div style="font-size:13px;font-weight:500;color:var(--text,#E9EEF6);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{ row.bank }}</div>
                  <div style="font-size:10.5px;color:var(--dim,#5D7391);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{ row.loc }} · {{ row.assets }}</div>
                </div>
                <div style="min-width:0;padding-right:10px;">
                  <span style="font-size:11px;color:var(--text2,#9FB2C8);border:1px solid var(--border,#2C4560);padding:2px 6px;white-space:nowrap;">{{ row.rep }}</span>
                </div>
                <div style="display:flex;align-items:center;gap:7px;">
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:12.5px;color:{{ row.a.color }};width:19px;font-variant-numeric:tabular-nums;">{{ row.a.v }}</span>
                  <svg width="46" height="14" viewBox="0 0 46 14">
                    <rect x="0" y="5" width="46" height="4" fill="var(--track,#1D3149)"></rect>
                    <rect x="0" y="5" width="{{ row.a.w }}" height="4" fill="{{ row.a.color }}"></rect>
                    <rect x="{{ row.a.w }}" y="1" width="1.5" height="12" fill="{{ row.a.color }}"></rect>
                  </svg>
                </div>
                <div style="display:flex;align-items:center;gap:7px;">
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:12.5px;color:{{ row.b.color }};width:19px;font-variant-numeric:tabular-nums;">{{ row.b.v }}</span>
                  <svg width="46" height="14" viewBox="0 0 46 14">
                    <rect x="0" y="5" width="46" height="4" fill="var(--track,#1D3149)"></rect>
                    <rect x="0" y="5" width="{{ row.b.w }}" height="4" fill="{{ row.b.color }}"></rect>
                    <rect x="{{ row.b.w }}" y="1" width="1.5" height="12" fill="{{ row.b.color }}"></rect>
                  </svg>
                </div>
                <div style="display:flex;align-items:center;gap:7px;">
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:12.5px;color:{{ row.c.color }};width:19px;font-variant-numeric:tabular-nums;">{{ row.c.v }}</span>
                  <svg width="46" height="14" viewBox="0 0 46 14">
                    <rect x="0" y="5" width="46" height="4" fill="var(--track,#1D3149)"></rect>
                    <rect x="0" y="5" width="{{ row.c.w }}" height="4" fill="{{ row.c.color }}"></rect>
                    <rect x="{{ row.c.w }}" y="1" width="1.5" height="12" fill="{{ row.c.color }}"></rect>
                  </svg>
                </div>
                <div style="display:flex;align-items:center;justify-content:flex-end;gap:8px;">
                  <svg width="34" height="16" viewBox="0 0 34 16">
                    <polyline points="{{ row.spark }}" fill="none" stroke="var(--faint,#3E5673)" stroke-width="1.25"></polyline>
                  </svg>
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:600;color:{{ row.comp.color }};font-variant-numeric:tabular-nums;">{{ row.comp.v }}</span>
                </div>
              </div>
            </sc-for>

            <div style="padding:11px 22px;font-size:11px;color:var(--faint,#4E637F);display:flex;gap:16px;">
              <span>{{ footNote }}</span>
            </div>
          </section>

          <aside style="position:sticky;top:0;display:flex;flex-direction:column;background:var(--panel,#0B1826);min-height:100vh;">
            <div style="padding:14px 20px 12px;border-bottom:1px solid var(--line,#1B2C42);display:flex;align-items:center;justify-content:space-between;">
              <span style="font-size:10px;letter-spacing:0.14em;color:var(--dim,#5D7391);font-weight:600;">CALL-PREP BRIEF</span>
              <span style="font-size:10px;color:var(--faint,#4E637F);letter-spacing:0.04em;">= PDF hand-off</span>
            </div>

            <div style="padding:16px 20px 14px;border-bottom:1px solid var(--line,#1B2C42);display:flex;flex-direction:column;gap:11px;">
              <div style="display:flex;flex-direction:column;gap:3px;">
                <div style="font-size:17px;font-weight:600;letter-spacing:-0.01em;line-height:1.2;color:var(--text,#E9EEF6);">{{ sel.bank }}</div>
                <div style="font-size:11.5px;color:var(--muted,#7E93AE);">{{ sel.loc }} · {{ sel.assets }} assets · prepared for <span style="color:var(--gold,#C9A227);">{{ sel.rep }}</span></div>
              </div>
              <div style="display:flex;align-items:flex-end;gap:16px;">
                <div style="display:flex;flex-direction:column;gap:1px;">
                  <div style="font-size:9.5px;letter-spacing:0.13em;color:var(--dim,#5D7391);font-weight:600;">COMPOSITE</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:42px;font-weight:600;line-height:1;color:{{ sel.comp.color }};font-variant-numeric:tabular-nums;">{{ sel.comp.v }}</div>
                </div>
                <div style="display:flex;flex-direction:column;gap:2px;padding-bottom:3px;">
                  <div style="font-size:11.5px;color:var(--text2,#B7C7DA);">Rank <span style="font-family:'IBM Plex Mono',monospace;font-weight:600;color:var(--text,#E9EEF6);">{{ sel.rankStr }}</span> of <span style="font-family:'IBM Plex Mono',monospace;">4,530</span></div>
                  <div style="font-size:11px;color:{{ sel.verdictColor }};">{{ sel.verdict }}</div>
                </div>
              </div>
            </div>

            <div style="padding:14px 20px 16px;border-bottom:1px solid var(--line,#1B2C42);display:flex;flex-direction:column;gap:8px;">
              <div style="display:flex;align-items:center;justify-content:space-between;">
                <span style="font-size:9.5px;letter-spacing:0.13em;color:var(--dim,#5D7391);font-weight:600;">POSITION IN THE UNIVERSE</span>
                <span style="font-size:10.5px;color:var(--faint,#4E637F);">n = 4,530</span>
              </div>
              <svg width="412" height="72" viewBox="0 0 412 72" style="display:block;width:100%;height:auto;">
                <path d="M0,58 C82,58 104,52 146,33 C180,17 194,9 206,9 C218,9 232,17 266,33 C308,52 330,58 412,58 Z" fill="var(--curve,#132639)"></path>
                <path d="M0,58 C82,58 104,52 146,33 C180,17 194,9 206,9 C218,9 232,17 266,33 C308,52 330,58 412,58 Z" fill="none" stroke="var(--border,#1E344D)" stroke-width="1"></path>
                <line x1="0" y1="58" x2="412" y2="58" stroke="var(--border,#24384F)" stroke-width="1"></line>
                <line x1="103" y1="52" x2="103" y2="58" stroke="var(--border,#24384F)" stroke-width="1"></line>
                <line x1="206" y1="52" x2="206" y2="58" stroke="var(--border,#24384F)" stroke-width="1"></line>
                <line x1="309" y1="52" x2="309" y2="58" stroke="var(--border,#24384F)" stroke-width="1"></line>
                <line x1="{{ sel.markX }}" y1="4" x2="{{ sel.markX }}" y2="58" stroke="{{ sel.comp.color }}" stroke-width="2"></line>
                <circle cx="{{ sel.markX }}" cy="4" r="3" fill="{{ sel.comp.color }}"></circle>
                <text x="10" y="70" fill="var(--faint,#4E637F)" font-family="IBM Plex Mono" font-size="9">0th</text>
                <text x="192" y="70" fill="var(--faint,#4E637F)" font-family="IBM Plex Mono" font-size="9">50th</text>
                <text x="378" y="70" fill="var(--faint,#4E637F)" font-family="IBM Plex Mono" font-size="9">100th</text>
              </svg>
              <div style="font-size:11px;color:var(--muted,#7E93AE);line-height:1.5;">{{ sel.positionNote }}</div>
            </div>

            <div style="display:flex;flex-direction:column;">
              <sc-for list="{{ sel.signals }}" as="sig" hint-placeholder-count="3">
                <div style="padding:13px 20px;border-bottom:1px solid var(--line2,#14263A);display:flex;flex-direction:column;gap:7px;">
                  <div style="display:flex;align-items:center;gap:9px;">
                    <div style="width:17px;height:17px;display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-size:10.5px;font-weight:600;color:#0A1420;background:{{ sig.color }};">{{ sig.letter }}</div>
                    <div style="font-size:12.5px;font-weight:500;color:var(--text,#E9EEF6);flex:1;">{{ sig.label }}</div>
                    <div style="font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:600;color:{{ sig.color }};font-variant-numeric:tabular-nums;">{{ sig.v }}</div>
                  </div>
                  <svg width="412" height="9" viewBox="0 0 412 9" style="display:block;width:100%;height:auto;">
                    <rect x="0" y="3" width="412" height="3" fill="var(--track,#1D3149)"></rect>
                    <rect x="0" y="3" width="{{ sig.w }}" height="3" fill="{{ sig.color }}"></rect>
                    <rect x="{{ sig.w }}" y="0" width="2" height="9" fill="{{ sig.color }}"></rect>
                  </svg>
                  <div style="display:flex;flex-wrap:wrap;column-gap:18px;row-gap:4px;">
                    <sc-for list="{{ sig.figures }}" as="f" hint-placeholder-count="3">
                      <div style="display:flex;flex-direction:column;gap:1px;">
                        <span style="font-size:9.5px;color:var(--faint,#4E637F);letter-spacing:0.06em;">{{ f.k }}</span>
                        <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--text2,#B7C7DA);font-variant-numeric:tabular-nums;">{{ f.v }}</span>
                      </div>
                    </sc-for>
                  </div>
                </div>
              </sc-for>
            </div>

            <div style="padding:14px 20px;border-bottom:1px solid var(--line,#1B2C42);display:flex;flex-direction:column;gap:8px;background:var(--panel2,#0C1A2A);">
              <div style="display:flex;align-items:center;justify-content:space-between;">
                <span style="font-size:9.5px;letter-spacing:0.13em;color:var(--dim,#5D7391);font-weight:600;">NARRATIVE</span>
                <span style="font-size:10px;color:var(--gold,#C9A227);border:1px solid var(--goldLine,#43391A);padding:1px 6px;">{{ voiceLabel }}</span>
              </div>
              <p style="margin:0;font-size:12.5px;line-height:1.6;color:var(--text2,#C6D3E2);text-wrap:pretty;">{{ sel.narrative }}</p>
            </div>

            <div style="padding:14px 20px 18px;display:flex;flex-direction:column;gap:9px;">
              <div style="display:flex;gap:8px;">
                <button style="flex:1;font-family:inherit;font-size:12.5px;font-weight:600;padding:9px 12px;background:#E9A93C;color:#0A1420;border:none;cursor:pointer;letter-spacing:0.01em;">Generate PDF hand-off</button>
                <button style="font-family:inherit;font-size:12.5px;padding:9px 12px;background:transparent;color:var(--muted,#8AA0BC);border:1px solid var(--border,#24384F);cursor:pointer;">Regenerate</button>
              </div>
              <p style="margin:0;font-size:10px;line-height:1.5;color:var(--faint,#41576F);">Internal call-prep aid, not investment advice or a solicitation. Figures sourced from SNL / Capital IQ Pro call report data as-of 2026Q1.</p>
            </div>
          </aside>
        </div>
      </div>
    </sc-if>

    <sc-if value="{{ isSettings }}" hint-placeholder-val="{{ false }}">
      <div style="display:flex;flex-direction:column;min-width:0;">
        <header style="border-bottom:1px solid var(--line,#1B2C42);padding:16px 22px 0;display:flex;flex-direction:column;gap:12px;background:var(--panel,#0B1826);">
          <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:24px;">
            <div style="display:flex;flex-direction:column;gap:4px;">
              <h1 style="margin:0;font-size:19px;font-weight:600;letter-spacing:-0.01em;color:var(--text,#E9EEF6);">Settings</h1>
              <div style="font-size:11.5px;color:var(--muted,#7E93AE);">Changes apply immediately — no restart. Scoring changes re-rank the full universe on the next run.</div>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
              <div style="display:flex;border:1px solid var(--border,#24384F);">
                <button onClick="{{ setDark }}" style="{{ darkBtn }}">Dark</button>
                <button onClick="{{ setLight }}" style="{{ lightBtn }}">Light</button>
              </div>
              <button style="font-family:inherit;font-size:12px;padding:6px 11px;background:transparent;color:var(--muted,#8AA0BC);border:1px solid var(--border,#24384F);cursor:pointer;white-space:nowrap;">Reset to defaults</button>
              <button style="font-family:inherit;font-size:12px;font-weight:600;padding:6px 12px;background:#E9A93C;color:#0A1420;border:none;cursor:pointer;">Save settings</button>
            </div>
          </div>
          <div style="display:flex;gap:2px;">
            <sc-for list="{{ tabs }}" as="t" hint-placeholder-count="4">
              <div onClick="{{ t.go }}" style="{{ t.style }}">{{ t.label }}<span style="{{ t.badgeStyle }}">{{ t.badge }}</span></div>
            </sc-for>
          </div>
        </header>

        <sc-if value="{{ tabScoring }}" hint-placeholder-val="{{ true }}">
          <div style="display:grid;grid-template-columns:minmax(0,1fr) 452px;align-items:start;">
            <div style="min-width:0;border-right:1px solid var(--line,#1B2C42);overflow-x:auto;">

              <div style="padding:18px 24px 20px;border-bottom:1px solid var(--line,#1B2C42);display:flex;flex-direction:column;gap:12px;min-width:640px;">
                <div style="display:flex;align-items:baseline;justify-content:space-between;">
                  <div style="display:flex;flex-direction:column;gap:2px;">
                    <div style="font-size:13.5px;font-weight:600;color:var(--text,#E9EEF6);">Opportunity threshold</div>
                    <div style="font-size:11.5px;color:var(--muted,#7E93AE);">At or above = material opportunity. Below = relationship call.</div>
                  </div>
                  <div style="display:flex;align-items:baseline;gap:6px;">
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:30px;font-weight:600;color:var(--text,#E9EEF6);line-height:1;font-variant-numeric:tabular-nums;">{{ threshold }}</span>
                    <span style="font-size:11px;color:var(--dim,#5D7391);">th pct</span>
                  </div>
                </div>
                <input type="range" min="0" max="100" step="5" value="{{ threshold }}" onChange="{{ onThreshold }}" style="width:100%;accent-color:#E9A93C;height:4px;cursor:pointer;">
                <div style="display:flex;justify-content:space-between;font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--faint,#4E637F);">
                  <span>0</span><span>25</span><span>50</span><span>75</span><span>100</span>
                </div>
              </div>

              <div style="padding:18px 24px 20px;border-bottom:1px solid var(--line,#1B2C42);display:flex;flex-direction:column;gap:14px;min-width:640px;">
                <div style="display:flex;align-items:baseline;justify-content:space-between;">
                  <div style="display:flex;flex-direction:column;gap:2px;">
                    <div style="font-size:13.5px;font-weight:600;color:var(--text,#E9EEF6);">Composite weighting</div>
                    <div style="font-size:11.5px;color:var(--muted,#7E93AE);">Relative weight of each signal in the composite. Normalized on save.</div>
                  </div>
                  <div style="font-size:11px;color:{{ weightNoteColor }};font-family:'IBM Plex Mono',monospace;">{{ weightNote }}</div>
                </div>
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;">
                  <sc-for list="{{ weights }}" as="w" hint-placeholder-count="3">
                    <div style="border:1px solid var(--border,#24384F);padding:11px 12px 12px;display:flex;flex-direction:column;gap:9px;background:var(--panel2,#0C1A2A);">
                      <div style="display:flex;align-items:center;gap:8px;">
                        <div style="width:16px;height:16px;display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;color:#0A1420;background:{{ w.color }};">{{ w.letter }}</div>
                        <span style="font-size:12px;color:var(--text2,#B7C7DA);">{{ w.label }}</span>
                      </div>
                      <div style="display:flex;align-items:center;gap:8px;">
                        <input type="number" min="0" max="1" step="0.01" value="{{ w.value }}" onChange="{{ w.onChange }}" style="width:74px;font-family:'IBM Plex Mono',monospace;font-size:14px;padding:5px 7px;background:var(--bg,#0A1420);color:var(--text,#E9EEF6);border:1px solid var(--border,#24384F);">
                        <span style="font-family:'IBM Plex Mono',monospace;font-size:11.5px;color:var(--dim,#5D7391);">= {{ w.pct }} of composite</span>
                      </div>
                      <svg width="180" height="4" viewBox="0 0 180 4" style="display:block;width:100%;height:4px;">
                        <rect x="0" y="0" width="180" height="4" fill="var(--track,#1D3149)"></rect>
                        <rect x="0" y="0" width="{{ w.barW }}" height="4" fill="{{ w.color }}"></rect>
                      </svg>
                    </div>
                  </sc-for>
                </div>
              </div>

              <div style="padding:16px 24px 18px;border-bottom:1px solid var(--line,#1B2C42);display:flex;flex-direction:column;gap:10px;min-width:640px;">
                <div style="display:flex;align-items:center;gap:9px;">
                  <span style="font-size:9.5px;letter-spacing:0.14em;color:var(--dim,#5D7391);font-weight:600;">ADVANCED</span>
                  <div style="flex:1;height:1px;background:var(--line,#1B2C42);"></div>
                </div>
                <div style="display:flex;flex-direction:column;gap:3px;">
                  <div style="font-size:13px;font-weight:600;color:var(--text,#E9EEF6);">Signal C — earnings direction</div>
                  <div style="font-size:11.5px;color:var(--muted,#7E93AE);">Which direction of q/q net income scores higher.</div>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                  <div onClick="{{ setDecline }}" style="{{ declineStyle }}">
                    <div style="font-size:12.5px;font-weight:600;">Reward a q/q decline</div>
                    <div style="font-size:11px;color:var(--muted,#7E93AE);margin-top:2px;">Falling net income = more receptive. (Default)</div>
                  </div>
                  <div onClick="{{ setImprove }}" style="{{ improveStyle }}">
                    <div style="font-size:12.5px;font-weight:600;">Reward improvement</div>
                    <div style="font-size:11px;color:var(--muted,#7E93AE);margin-top:2px;">Rising net income scores higher.</div>
                  </div>
                </div>
              </div>
            </div>

            <aside style="position:sticky;top:0;background:var(--panel,#0B1826);min-height:100vh;display:flex;flex-direction:column;">
              <div style="padding:14px 20px 12px;border-bottom:1px solid var(--line,#1B2C42);display:flex;align-items:center;justify-content:space-between;">
                <span style="font-size:10px;letter-spacing:0.14em;color:var(--dim,#5D7391);font-weight:600;">EFFECT PREVIEW</span>
                <span style="font-size:10px;color:var(--faint,#4E637F);">live · not saved</span>
              </div>
              <div style="padding:16px 20px 14px;border-bottom:1px solid var(--line,#1B2C42);display:flex;flex-direction:column;gap:10px;">
                <div style="font-size:11.5px;color:var(--muted,#7E93AE);">Re-scored with your weights: <span style="color:var(--text,#E9EEF6);">{{ preview.bank }}</span></div>
                <div style="display:flex;align-items:flex-end;gap:16px;">
                  <div style="display:flex;flex-direction:column;gap:1px;">
                    <div style="font-size:9.5px;letter-spacing:0.13em;color:var(--dim,#5D7391);font-weight:600;">NEW COMPOSITE</div>
                    <div style="font-family:'IBM Plex Mono',monospace;font-size:42px;font-weight:600;line-height:1;color:{{ preview.color }};font-variant-numeric:tabular-nums;">{{ preview.comp }}</div>
                  </div>
                  <div style="display:flex;flex-direction:column;gap:2px;padding-bottom:4px;">
                    <div style="font-size:11.5px;color:var(--text2,#B7C7DA);">was <span style="font-family:'IBM Plex Mono',monospace;">{{ preview.was }}</span> at equal weight</div>
                    <div style="font-size:11px;color:{{ preview.verdictColor }};">{{ preview.verdict }}</div>
                  </div>
                </div>
                <svg width="412" height="76" viewBox="0 0 412 76" style="display:block;width:100%;height:auto;">
                  <path d="M0,58 C82,58 104,52 146,33 C180,17 194,9 206,9 C218,9 232,17 266,33 C308,52 330,58 412,58 Z" fill="var(--curve,#132639)"></path>
                  <line x1="0" y1="58" x2="412" y2="58" stroke="var(--border,#24384F)" stroke-width="1"></line>
                  <rect x="{{ preview.threshX }}" y="6" width="{{ preview.threshW }}" height="52" fill="#E9A93C" opacity="0.10"></rect>
                  <line x1="{{ preview.threshX }}" y1="6" x2="{{ preview.threshX }}" y2="58" stroke="#E9A93C" stroke-width="1" stroke-dasharray="3 3"></line>
                  <text x="{{ preview.threshLabelX }}" y="72" fill="#E9A93C" font-family="IBM Plex Mono" font-size="9">threshold {{ threshold }}</text>
                  <line x1="{{ preview.markX }}" y1="4" x2="{{ preview.markX }}" y2="58" stroke="{{ preview.color }}" stroke-width="2"></line>
                  <circle cx="{{ preview.markX }}" cy="4" r="3" fill="{{ preview.color }}"></circle>
                </svg>
              </div>
              <div style="padding:14px 20px;border-bottom:1px solid var(--line,#1B2C42);display:flex;flex-direction:column;gap:9px;">
                <div style="font-size:9.5px;letter-spacing:0.13em;color:var(--dim,#5D7391);font-weight:600;">ACROSS THE LAST SCREEN</div>
                <div style="display:flex;align-items:baseline;gap:8px;">
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:28px;font-weight:600;color:var(--text,#E9EEF6);line-height:1;">{{ clearCount }}</span>
                  <span style="font-size:11.5px;color:var(--muted,#7E93AE);">of {{ clearTotal }} banks clear the threshold</span>
                </div>
                <div style="display:flex;gap:3px;">
                  <sc-for list="{{ clearBars }}" as="cb" hint-placeholder-count="9">
                    <div style="flex:1;height:26px;background:{{ cb.color }};"></div>
                  </sc-for>
                </div>
                <div style="font-size:11px;color:var(--faint,#4E637F);line-height:1.5;">Gold bars clear the threshold at the current weighting; muted bars fall below it.</div>
              </div>
              <div style="padding:14px 20px;display:flex;flex-direction:column;gap:7px;">
                <div style="font-size:9.5px;letter-spacing:0.13em;color:var(--dim,#5D7391);font-weight:600;">SCORING PIPELINE</div>
                <div style="font-size:11px;color:var(--muted,#7E93AE);line-height:1.6;">Weights affect the composite and the universe rank only. Signal A, B and C percentiles are computed against all 4,530 banks before weighting and are not changed by these controls.</div>
              </div>
            </aside>
          </div>
        </sc-if>

        <sc-if value="{{ tabNarrative }}" hint-placeholder-val="{{ false }}">
          <div style="display:grid;grid-template-columns:minmax(0,1fr) 452px;align-items:start;">
            <div style="min-width:0;border-right:1px solid var(--line,#1B2C42);overflow-x:auto;">
              <div style="padding:18px 24px;border-bottom:1px solid var(--line,#1B2C42);display:flex;flex-direction:column;gap:11px;min-width:660px;">
                <div style="display:flex;flex-direction:column;gap:2px;">
                  <div style="font-size:13.5px;font-weight:600;color:var(--text,#E9EEF6);">PDF narrative voice</div>
                  <div style="font-size:11.5px;color:var(--muted,#7E93AE);">Which system prompt writes the call-prep brief.</div>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                  <div onClick="{{ setConversational }}" style="{{ convStyle }}">
                    <div style="font-size:12.5px;font-weight:600;">Conversational</div>
                    <div style="font-size:11px;color:var(--muted,#7E93AE);margin-top:2px;">Natural, plain-spoken. (Recommended)</div>
                  </div>
                  <div onClick="{{ setAnalyst }}" style="{{ analystStyle }}">
                    <div style="font-size:12.5px;font-weight:600;">Analyst</div>
                    <div style="font-size:11px;color:var(--muted,#7E93AE);margin-top:2px;">Tighter, more technical desk voice.</div>
                  </div>
                </div>
              </div>

              <div style="padding:18px 24px;border-bottom:1px solid var(--line,#1B2C42);display:flex;flex-direction:column;gap:13px;min-width:660px;">
                <div style="font-size:13.5px;font-weight:600;color:var(--text,#E9EEF6);">PDF options</div>
                <div style="display:flex;align-items:center;gap:11px;">
                  <div onClick="{{ toggleTrend }}" style="{{ trendSwitch }}"><div style="{{ trendKnob }}"></div></div>
                  <span style="font-size:12.5px;color:var(--text2,#B7C7DA);">Include a multi-quarter trend table</span>
                </div>
                <div style="display:flex;align-items:center;gap:11px;padding-left:47px;">
                  <span style="font-size:12px;color:var(--muted,#7E93AE);">Quarters of history</span>
                  <input type="number" min="2" max="12" value="{{ trendQ }}" onChange="{{ onTrendQ }}" style="width:64px;font-family:'IBM Plex Mono',monospace;font-size:13px;padding:5px 7px;background:var(--bg,#0A1420);color:var(--text,#E9EEF6);border:1px solid var(--border,#24384F);">
                  <span style="font-size:11px;color:var(--faint,#4E637F);">max 12</span>
                </div>
                <div style="display:flex;align-items:center;gap:11px;">
                  <div onClick="{{ toggleShowRep }}" style="{{ repSwitch }}"><div style="{{ repKnob }}"></div></div>
                  <span style="font-size:12.5px;color:var(--text2,#B7C7DA);">Show assigned rep on the PDF (“Prepared for: …”)</span>
                </div>
              </div>

              <div style="padding:18px 24px;display:flex;flex-direction:column;gap:12px;min-width:660px;">
                <div style="display:flex;align-items:center;gap:9px;">
                  <span style="font-size:9.5px;letter-spacing:0.14em;color:var(--dim,#5D7391);font-weight:600;">ADVANCED</span>
                  <div style="flex:1;height:1px;background:var(--line,#1B2C42);"></div>
                </div>
                <div style="display:flex;flex-direction:column;gap:2px;">
                  <div style="font-size:13px;font-weight:600;color:var(--text,#E9EEF6);">PDF table fields</div>
                  <div style="font-size:11.5px;color:var(--muted,#7E93AE);">Which metrics appear in the two PDF tables. Trend capped at 8.</div>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                  <div style="display:flex;flex-direction:column;gap:7px;">
                    <div style="display:flex;align-items:center;justify-content:space-between;">
                      <span style="font-size:11px;letter-spacing:0.1em;color:var(--dim,#5D7391);font-weight:600;">SNAPSHOT · VERIFIED FIGURES</span>
                      <span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--gold,#C9A227);">{{ snapCount }}</span>
                    </div>
                    <div style="border:1px solid var(--border,#24384F);max-height:250px;overflow-y:auto;background:var(--panel2,#0C1A2A);">
                      <sc-for list="{{ fields }}" as="f" hint-placeholder-count="10">
                        <div onClick="{{ f.toggleSnap }}" style="display:flex;align-items:center;gap:9px;padding:6px 11px;cursor:pointer;border-bottom:1px solid var(--line2,#14263A);" style-hover="background:var(--hover,#101F31);">
                          <div style="{{ f.snapBox }}"></div>
                          <span style="font-size:12px;color:var(--text2,#B7C7DA);">{{ f.label }}</span>
                          <span style="margin-left:auto;font-size:10px;color:var(--faint,#4E637F);">{{ f.group }}</span>
                        </div>
                      </sc-for>
                    </div>
                  </div>
                  <div style="display:flex;flex-direction:column;gap:7px;">
                    <div style="display:flex;align-items:center;justify-content:space-between;">
                      <span style="font-size:11px;letter-spacing:0.1em;color:var(--dim,#5D7391);font-weight:600;">TREND · HOW IT'S TRENDING</span>
                      <span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:{{ trendCountColor }};">{{ trendCount }}</span>
                    </div>
                    <div style="border:1px solid var(--border,#24384F);max-height:250px;overflow-y:auto;background:var(--panel2,#0C1A2A);">
                      <sc-for list="{{ fields }}" as="f" hint-placeholder-count="10">
                        <div onClick="{{ f.toggleTrendF }}" style="display:flex;align-items:center;gap:9px;padding:6px 11px;cursor:pointer;border-bottom:1px solid var(--line2,#14263A);" style-hover="background:var(--hover,#101F31);">
                          <div style="{{ f.trendBox }}"></div>
                          <span style="font-size:12px;color:var(--text2,#B7C7DA);">{{ f.label }}</span>
                          <span style="margin-left:auto;font-size:10px;color:var(--faint,#4E637F);">{{ f.group }}</span>
                        </div>
                      </sc-for>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <aside style="position:sticky;top:0;background:var(--panel,#0B1826);min-height:100vh;display:flex;flex-direction:column;">
              <div style="padding:14px 20px 12px;border-bottom:1px solid var(--line,#1B2C42);display:flex;align-items:center;justify-content:space-between;">
                <span style="font-size:10px;letter-spacing:0.14em;color:var(--dim,#5D7391);font-weight:600;">PDF PREVIEW</span>
                <span style="font-size:10px;color:var(--faint,#4E637F);">page 1 of 2</span>
              </div>
              <div style="padding:18px 20px;display:flex;flex-direction:column;gap:12px;">
                <div style="background:#FFFFFF;color:#12233C;padding:20px 20px 24px;display:flex;flex-direction:column;gap:12px;box-shadow:0 1px 0 rgba(0,0,0,0.4);">
                  <div style="display:flex;align-items:flex-start;justify-content:space-between;border-bottom:2px solid #002F6C;padding-bottom:9px;">
                    <div style="display:flex;flex-direction:column;gap:2px;">
                      <div style="font-size:13px;font-weight:700;color:#002F6C;">Peoples Heritage Bank</div>
                      <div style="font-size:9.5px;color:#5B6B80;">Tupelo, MS · call prep · 2026Q1</div>
                    </div>
                    <div style="font-size:8.5px;letter-spacing:0.14em;color:#9A7412;font-weight:700;text-align:right;">SOUTHSTATE<br>SECURITIES</div>
                  </div>
                  <div style="font-size:9.5px;color:{{ pdfRepColor }};">{{ pdfRepLine }}</div>
                  <div style="display:flex;flex-direction:column;gap:4px;">
                    <div style="font-size:9px;letter-spacing:0.12em;color:#7A8CA3;font-weight:700;">VERIFIED FIGURES</div>
                    <sc-for list="{{ pdfSnapRows }}" as="r" hint-placeholder-count="6">
                      <div style="display:flex;justify-content:space-between;font-size:10px;border-bottom:1px solid #E6EBF2;padding:2.5px 0;">
                        <span style="color:#42546B;">{{ r.label }}</span>
                        <span style="font-family:'IBM Plex Mono',monospace;color:#12233C;">{{ r.value }}</span>
                      </div>
                    </sc-for>
                  </div>
                  <sc-if value="{{ includeTrend }}" hint-placeholder-val="{{ true }}">
                    <div style="display:flex;flex-direction:column;gap:4px;">
                      <div style="font-size:9px;letter-spacing:0.12em;color:#7A8CA3;font-weight:700;">HOW IT'S TRENDING · {{ trendQ }} QUARTERS</div>
                      <sc-for list="{{ pdfTrendRows }}" as="r" hint-placeholder-count="3">
                        <div style="display:flex;justify-content:space-between;font-size:10px;border-bottom:1px solid #E6EBF2;padding:2.5px 0;">
                          <span style="color:#42546B;">{{ r.label }}</span>
                          <span style="font-family:'IBM Plex Mono',monospace;color:#12233C;">{{ r.value }}</span>
                        </div>
                      </sc-for>
                      <sc-if value="{{ trendEmpty }}" hint-placeholder-val="{{ false }}">
                        <div style="font-size:9.5px;color:#9AA7B8;font-style:italic;padding:3px 0;">No trend metrics selected — table will be omitted.</div>
                      </sc-if>
                    </div>
                  </sc-if>
                  <div style="font-size:9px;color:#8C99AB;line-height:1.5;border-top:1px solid #E6EBF2;padding-top:7px;">Internal call-prep aid. Not investment advice or a solicitation. Figures from SNL / Capital IQ Pro call report data.</div>
                </div>
                <div style="font-size:11px;color:var(--faint,#4E637F);line-height:1.5;">Preview reflects the field selections and options on this page. Narrative text is generated at PDF time by the active voice.</div>
              </div>
            </aside>
          </div>
        </sc-if>

        <sc-if value="{{ tabProvider }}" hint-placeholder-val="{{ false }}">
          <div style="display:grid;grid-template-columns:minmax(0,1fr) 452px;align-items:start;">
            <div style="min-width:0;border-right:1px solid var(--line,#1B2C42);padding:18px 24px;display:flex;flex-direction:column;gap:14px;overflow-x:auto;">
              <div style="display:flex;flex-direction:column;gap:2px;">
                <div style="font-size:13.5px;font-weight:600;color:var(--text,#E9EEF6);">AI provider</div>
                <div style="font-size:11.5px;color:var(--muted,#7E93AE);">Which engine writes the PDF narrative. Set <span style="font-family:'IBM Plex Mono',monospace;color:var(--text2,#B7C7DA);">LLM_PROVIDER</span> in <span style="font-family:'IBM Plex Mono',monospace;color:var(--text2,#B7C7DA);">.env</span>. Falls back to the built-in narrative if unreachable.</div>
              </div>
              <div style="border:1px solid var(--border,#24384F);">
                <sc-for list="{{ providers }}" as="p" hint-placeholder-count="5">
                  <div style="display:grid;grid-template-columns:150px 1fr auto;align-items:center;gap:12px;padding:11px 14px;border-bottom:1px solid var(--line2,#14263A);background:{{ p.bg }};">
                    <span style="font-size:12.5px;font-weight:{{ p.weight }};color:var(--text,#E9EEF6);">{{ p.name }}</span>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--faint,#4E637F);">{{ p.detail }}</span>
                    <span style="{{ p.pill }}">{{ p.status }}</span>
                  </div>
                </sc-for>
              </div>
              <div style="font-size:11.5px;color:var(--muted,#7E93AE);">Test the live chain at <span style="font-family:'IBM Plex Mono',monospace;color:var(--gold,#C9A227);">/ai-test</span>. Rep file loaded — 4,276 banks mapped across 38 reps.</div>
            </div>
            <aside style="position:sticky;top:0;background:var(--panel,#0B1826);min-height:100vh;display:flex;flex-direction:column;">
              <div style="padding:14px 20px 12px;border-bottom:1px solid var(--line,#1B2C42);">
                <span style="font-size:10px;letter-spacing:0.14em;color:var(--dim,#5D7391);font-weight:600;">FALLBACK CHAIN</span>
              </div>
              <div style="padding:16px 20px;display:flex;flex-direction:column;gap:10px;">
                <sc-for list="{{ chain }}" as="c" hint-placeholder-count="3">
                  <div style="display:flex;align-items:center;gap:11px;">
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--faint,#4E637F);width:14px;">{{ c.n }}</span>
                    <div style="width:7px;height:7px;border-radius:50%;background:{{ c.dot }};"></div>
                    <span style="font-size:12px;color:var(--text2,#B7C7DA);flex:1;">{{ c.label }}</span>
                    <span style="font-size:10.5px;color:var(--faint,#4E637F);">{{ c.note }}</span>
                  </div>
                </sc-for>
                <div style="font-size:11px;color:var(--faint,#4E637F);line-height:1.5;margin-top:4px;">If every configured provider fails, the PDF still generates using the deterministic built-in narrative. No hand-off is ever blocked by the model.</div>
              </div>
            </aside>
          </div>
        </sc-if>

        <sc-if value="{{ tabPrompts }}" hint-placeholder-val="{{ false }}">
          <div style="padding:18px 24px;display:flex;flex-direction:column;gap:14px;max-width:1100px;">
            <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
              <div style="display:flex;border:1px solid var(--border,#24384F);">
                <button onClick="{{ setPromptConv }}" style="{{ pConvBtn }}">Conversational</button>
                <button onClick="{{ setPromptAnalyst }}" style="{{ pAnalystBtn }}">Analyst</button>
              </div>
              <span style="font-size:11.5px;color:var(--muted,#7E93AE);">Active preset:</span>
              <select style="{{ selectStyle }}"><option>Default (built-in)</option><option>Desk voice v2</option></select>
              <button style="font-family:inherit;font-size:11.5px;padding:5px 10px;background:transparent;color:var(--muted,#8AA0BC);border:1px solid var(--border,#24384F);cursor:pointer;">Use this</button>
              <button style="font-family:inherit;font-size:11.5px;padding:5px 10px;background:transparent;color:var(--muted,#8AA0BC);border:1px solid var(--border,#24384F);cursor:pointer;">Revert to default</button>
              <span style="margin-left:auto;font-size:11px;color:var(--faint,#4E637F);font-family:'IBM Plex Mono',monospace;">JSON output format is locked</span>
            </div>
            <textarea value="{{ promptBody }}" onChange="{{ onPromptBody }}" spellcheck="false" style="width:100%;height:340px;font-family:'IBM Plex Mono',monospace;font-size:12px;line-height:1.65;padding:14px 16px;background:var(--panel2,#0C1A2A);color:var(--text2,#B7C7DA);border:1px solid var(--border,#24384F);resize:vertical;"></textarea>
            <div style="display:flex;align-items:center;gap:9px;flex-wrap:wrap;">
              <button style="font-family:inherit;font-size:12px;padding:6px 11px;background:transparent;color:var(--muted,#8AA0BC);border:1px solid var(--border,#24384F);cursor:pointer;">Update selected</button>
              <button style="font-family:inherit;font-size:12px;padding:6px 11px;background:transparent;color:#C4644E;border:1px solid #4A2A24;cursor:pointer;">Delete selected</button>
              <input placeholder="New prompt name" style="font-family:inherit;font-size:12px;padding:6px 9px;width:190px;background:var(--bg,#0A1420);color:var(--text,#E9EEF6);border:1px solid var(--border,#24384F);">
              <button style="font-family:inherit;font-size:12px;font-weight:600;padding:6px 12px;background:#E9A93C;color:#0A1420;border:none;cursor:pointer;">Save as new</button>
            </div>
          </div>
        </sc-if>
      </div>
    </sc-if>

  </div>
</div>
</div>

</x-dc>
<script type="text/x-dc" data-dc-script data-props="{&quot;$preview&quot;:{&quot;width&quot;:1480,&quot;height&quot;:980}}">
const BANKS = [
  {bank:"Peoples Heritage Bank", loc:"Tupelo, MS", rep:"Dana Whitfield", assets:"$742M", rank:118,
   a:91, b:88, c:74, trend:[61,68,72,79,86],
   af:[["IDLE LIQUIDITY","$96.4M"],["% OF ASSETS","13.0%"],["LOANS/DEP","64.2%"],["EA YIELD","4.61%"]],
   bf:[["FV / COST","88.4%"],["UNREALIZED","-$11.2M"],["SEC YIELD","2.11%"],["DURATION","4.6y"]],
   cf:[["NET INCOME","$1.42M"],["PRIOR Q","$1.96M"],["Q/Q","-27.6%"]],
   narr:"Top-decile composite. The bond book is the lead: $11.2M unrealized loss on a 2.11% portfolio against a 4.61% earning-asset yield — a loss trade pencils inside three years of earn-back. $96.4M of idle liquidity funds the swap without touching loan capacity. Earnings fell 27.6% q/q, which historically raises receptiveness to a restructure conversation. Open on the reinvestment gap, not the loss."},
  {bank:"Cattleman's State Bank", loc:"Amarillo, TX", rep:"Parker Grubbs", assets:"$1.3B", rank:340,
   a:78, b:93, c:66, trend:[70,72,69,76,81],
   af:[["IDLE LIQUIDITY","$141.0M"],["% OF ASSETS","10.8%"],["LOANS/DEP","71.4%"],["EA YIELD","4.88%"]],
   bf:[["FV / COST","86.1%"],["UNREALIZED","-$24.8M"],["SEC YIELD","1.94%"],["DURATION","5.3y"]],
   cf:[["NET INCOME","$3.10M"],["PRIOR Q","$3.62M"],["Q/Q","-14.4%"]],
   narr:"Deepest underwater book in this screen: FV/cost of 86.1% on $24.8M unrealized. Portfolio yields 1.94% while new money clears near 4.9% — roughly 300bp of foregone carry on the repositioned portion. Liquidity is adequate at 10.8% of assets. Lead with the carry math; the loss size will be the objection."},
  {bank:"Granite Ridge Credit Union", loc:"Boise, ID", rep:"Dana Whitfield", assets:"$588M", rank:612,
   a:84, b:61, c:71, trend:[55,59,66,70,74],
   af:[["IDLE LIQUIDITY","$88.1M"],["% OF ASSETS","15.0%"],["LOANS/DEP","58.9%"],["EA YIELD","4.24%"]],
   bf:[["FV / COST","93.7%"],["UNREALIZED","-$4.1M"],["SEC YIELD","2.68%"],["DURATION","3.1y"]],
   cf:[["NET INCOME","$0.81M"],["PRIOR Q","$1.04M"],["Q/Q","-22.1%"]],
   narr:"Liquidity story, not a loss trade. 15.0% of assets sit idle at a 58.9% loan/deposit ratio — this is a member-owned balance sheet with nowhere to put money. The book is only 6.3% underwater, so a swap is not the opener. Extension into the 3-5y part of the curve is the conversation."},
  {bank:"Merchants Trust Bank", loc:"Savannah, GA", rep:"Parker Grubbs", assets:"$2.1B", rank:894,
   a:66, b:79, c:58, trend:[74,71,69,66,68],
   af:[["IDLE LIQUIDITY","$168.0M"],["% OF ASSETS","8.0%"],["LOANS/DEP","79.1%"],["EA YIELD","5.02%"]],
   bf:[["FV / COST","90.2%"],["UNREALIZED","-$18.6M"],["SEC YIELD","2.34%"],["DURATION","4.9y"]],
   cf:[["NET INCOME","$5.44M"],["PRIOR Q","$5.71M"],["Q/Q","-4.7%"]],
   narr:"Balanced profile, moderate urgency. The book is 9.8% underwater on $18.6M, and at 79.1% loans/deposits there is less idle cash to redeploy than the rest of this list. Earnings are near flat. Treat as a relationship call with a swap idea attached, not a lead."},
  {bank:"Cornbelt Savings Bank", loc:"Cedar Falls, IA", rep:"Unassigned", assets:"$309M", rank:1204,
   a:72, b:52, c:63, trend:[48,54,58,61,63],
   af:[["IDLE LIQUIDITY","$41.2M"],["% OF ASSETS","13.3%"],["LOANS/DEP","67.8%"],["EA YIELD","4.40%"]],
   bf:[["FV / COST","94.9%"],["UNREALIZED","-$2.2M"],["SEC YIELD","2.91%"],["DURATION","2.8y"]],
   cf:[["NET INCOME","$0.44M"],["PRIOR Q","$0.52M"],["Q/Q","-15.4%"]],
   narr:"Unassigned in the rep file — worth claiming. Idle liquidity at 13.3% of assets is the only signal materially above the threshold. Short duration and a shallow 5.1% underwater position mean there is no loss trade here; this is a cash deployment call."},
  {bank:"Harbor Point Bank & Trust", loc:"New Bedford, MA", rep:"Alicia Roan", assets:"$1.7B", rank:1663,
   a:58, b:64, c:49, trend:[62,60,59,58,57],
   af:[["IDLE LIQUIDITY","$122.4M"],["% OF ASSETS","7.2%"],["LOANS/DEP","83.0%"],["EA YIELD","5.14%"]],
   bf:[["FV / COST","92.0%"],["UNREALIZED","-$13.9M"],["SEC YIELD","2.52%"],["DURATION","4.2y"]],
   cf:[["NET INCOME","$4.02M"],["PRIOR Q","$3.88M"],["Q/Q","+3.6%"]],
   narr:"Middle of the universe on every signal. Earnings improved 3.6% q/q, which under the current Signal C setting suppresses the score. Loans/deposits at 83.0% leaves little room to redeploy. Relationship maintenance."},
  {bank:"1st Federal Savings Bank of SC", loc:"Walterboro, SC", rep:"Parker Grubbs", assets:"$153M", rank:2061,
   a:50, b:56, c:49, trend:[57,55,54,53,52],
   af:[["IDLE LIQUIDITY","$22.2M"],["% OF ASSETS","14.5%"],["LOANS/DEP","86.5%"],["EA YIELD","5.08%"]],
   bf:[["FV / COST","93.0%"],["UNREALIZED","-$0.98M"],["SEC YIELD","2.84%"],["DURATION","3.4y"]],
   cf:[["NET INCOME","$0.23M"],["PRIOR Q","$0.20M"],["Q/Q","+15.0%"]],
   narr:"Median across all three signals — rank 2,061 of 4,530 puts this bank almost exactly at the center of the universe. Securities are 7.0% below cost on a small $981k unrealized loss; not enough size to justify a restructure. Earnings improved q/q. No material opportunity; call to maintain the relationship."},
  {bank:"Sierra Vista Community Bank", loc:"Reno, NV", rep:"Alicia Roan", assets:"$466M", rank:2890,
   a:41, b:38, c:52, trend:[51,49,47,45,44],
   af:[["IDLE LIQUIDITY","$27.9M"],["% OF ASSETS","6.0%"],["LOANS/DEP","91.2%"],["EA YIELD","5.36%"]],
   bf:[["FV / COST","96.4%"],["UNREALIZED","-$0.61M"],["SEC YIELD","3.42%"],["DURATION","2.1y"]],
   cf:[["NET INCOME","$1.11M"],["PRIOR Q","$1.06M"],["Q/Q","+4.7%"]],
   narr:"Loaned up at 91.2% and carrying a short, high-yielding book at 3.42%. Little idle cash, little unrealized loss. This balance sheet does not need us right now — funding and liquidity lines are the more useful conversation."},
  {bank:"Anchor Point Credit Union", loc:"Mobile, AL", rep:"Unassigned", assets:"$204M", rank:3745,
   a:29, b:22, c:38, trend:[38,36,33,31,29],
   af:[["IDLE LIQUIDITY","$8.4M"],["% OF ASSETS","4.1%"],["LOANS/DEP","94.6%"],["EA YIELD","5.51%"]],
   bf:[["FV / COST","98.1%"],["UNREALIZED","-$0.19M"],["SEC YIELD","4.02%"],["DURATION","1.4y"]],
   cf:[["NET INCOME","$0.52M"],["PRIOR Q","$0.47M"],["Q/Q","+10.6%"]],
   narr:"Bottom quartile on all three signals. Short book at 4.02%, almost no unrealized loss, and 94.6% loans/deposits. Nothing in the call report suggests a portfolio need. Deprioritize."},
  {bank:"Willamette Valley Bank", loc:"Salem, OR", rep:"Alicia Roan", assets:"$431M", rank:96,
   a:94, b:81, c:80, trend:[52,55,63,74,85],
   af:[["IDLE LIQUIDITY","$71.8M"],["% OF ASSETS","16.7%"],["LOANS/DEP","55.3%"],["EA YIELD","4.36%"]],
   bf:[["FV / COST","89.6%"],["UNREALIZED","-$6.9M"],["SEC YIELD","2.28%"],["DURATION","4.1y"]],
   cf:[["NET INCOME","$0.68M"],["PRIOR Q","$1.09M"],["Q/Q","-37.6%"]],
   narr:"Largest q/q move in the universe. Deposit inflows pushed idle liquidity to 16.7% of assets while loan demand stalled at a 55.3% loan/deposit ratio — the cash has nowhere to go. Earnings fell 37.6% on the drag. The book is only 10.4% underwater, so this is a deployment conversation first and a swap conversation second."},
  {bank:"Red Cedar State Bank", loc:"Lansing, MI", rep:"Dana Whitfield", assets:"$967M", rank:205,
   a:86, b:90, c:62, trend:[58,60,64,71,79],
   af:[["IDLE LIQUIDITY","$118.9M"],["% OF ASSETS","12.3%"],["LOANS/DEP","62.8%"],["EA YIELD","4.54%"]],
   bf:[["FV / COST","87.2%"],["UNREALIZED","-$16.4M"],["SEC YIELD","2.02%"],["DURATION","5.0y"]],
   cf:[["NET INCOME","$2.04M"],["PRIOR Q","$2.31M"],["Q/Q","-11.7%"]],
   narr:"Both balance-sheet signals cleared 85 this quarter. $16.4M unrealized on a 2.02% book against a 4.54% earning-asset yield, funded by $118.9M of idle cash. The earn-back math is the whole conversation; earnings softness gives it timing."},
  {bank:"Blue Mound National Bank", loc:"Decatur, IL", rep:"Unassigned", assets:"$274M", rank:448,
   a:82, b:77, c:69, trend:[54,58,62,67,76],
   af:[["IDLE LIQUIDITY","$38.9M"],["% OF ASSETS","14.2%"],["LOANS/DEP","61.0%"],["EA YIELD","4.31%"]],
   bf:[["FV / COST","90.8%"],["UNREALIZED","-$4.6M"],["SEC YIELD","2.21%"],["DURATION","3.9y"]],
   cf:[["NET INCOME","$0.39M"],["PRIOR Q","$0.48M"],["Q/Q","-18.8%"]],
   narr:"Unassigned in the rep file and newly inside the top decile — worth claiming before the next screen. Every signal moved up q/q. Modest size means a restructure is small in dollars, but the profile is textbook."},
  {bank:"Cape Fear Community Bank", loc:"Wilmington, NC", rep:"Parker Grubbs", assets:"$1.1B", rank:731,
   a:69, b:85, c:64, trend:[56,55,58,64,73],
   af:[["IDLE LIQUIDITY","$96.7M"],["% OF ASSETS","8.8%"],["LOANS/DEP","74.6%"],["EA YIELD","4.79%"]],
   bf:[["FV / COST","88.0%"],["UNREALIZED","-$14.1M"],["SEC YIELD","2.06%"],["DURATION","4.8y"]],
   cf:[["NET INCOME","$2.66M"],["PRIOR Q","$2.94M"],["Q/Q","-9.5%"]],
   narr:"Signal B carries this one: 12.0% below cost on $14.1M with the portfolio yielding 2.06%. Liquidity is thinner at 8.8% of assets, so a swap has to be self-funding out of the existing book rather than out of cash."},
  {bank:"Teton Basin Bank", loc:"Idaho Falls, ID", rep:"Alicia Roan", assets:"$358M", rank:1490,
   a:63, b:58, c:72, trend:[71,70,68,66,64],
   af:[["IDLE LIQUIDITY","$34.1M"],["% OF ASSETS","9.5%"],["LOANS/DEP","76.9%"],["EA YIELD","4.92%"]],
   bf:[["FV / COST","92.8%"],["UNREALIZED","-$3.3M"],["SEC YIELD","2.74%"],["DURATION","3.3y"]],
   cf:[["NET INCOME","$0.71M"],["PRIOR Q","$0.97M"],["Q/Q","-26.8%"]],
   narr:"Drifting down the ranks for five straight quarters as loans absorbed the cash. Earnings fell 26.8% q/q, but neither balance-sheet signal is compelling on its own. Relationship call with a duration idea attached."}
];

const LABELS = {a:"Idle liquidity", b:"Underwater book", c:"Net income q/q"};

const META = {
  "Peoples Heritage Bank":      {prev:71, prevRank:240,  raw:742000},
  "Cattleman's State Bank":     {prev:75, prevRank:388,  raw:1300000},
  "Granite Ridge Credit Union": {prev:66, prevRank:842,  raw:588000},
  "Merchants Trust Bank":       {prev:70, prevRank:775,  raw:2100000},
  "Cornbelt Savings Bank":      {prev:58, prevRank:1361, raw:309000},
  "Harbor Point Bank & Trust":  {prev:60, prevRank:1502, raw:1700000},
  "1st Federal Savings Bank of SC": {prev:54, prevRank:1908, raw:153000},
  "Sierra Vista Community Bank":{prev:48, prevRank:2544, raw:466000},
  "Anchor Point Credit Union":  {prev:34, prevRank:3411, raw:204000},
  "Willamette Valley Bank":     {prev:62, prevRank:690,  raw:431000},
  "Red Cedar State Bank":       {prev:64, prevRank:512,  raw:967000},
  "Blue Mound National Bank":   {prev:67, prevRank:903,  raw:274000},
  "Cape Fear Community Bank":   {prev:58, prevRank:1216, raw:1100000},
  "Teton Basin Bank":           {prev:71, prevRank:1104, raw:358000}
};

const DRIVERS = {
  "Willamette Valley Bank": "Idle liquidity 11.2% → 16.7% of assets",
  "Red Cedar State Bank": "FV/cost fell to 87.2% on rate backup",
  "Cape Fear Community Bank": "Unrealized loss widened $3.8M",
  "Peoples Heritage Bank": "Net income -27.6% q/q",
  "Blue Mound National Bank": "All three signals up q/q",
  "Teton Basin Bank": "Loan growth absorbed idle cash",
  "Granite Ridge Credit Union": "Deposit inflow, loans flat",
  "Cattleman's State Bank": "Duration extended to 5.3y"
};

const BANDS = [
  {v:"0-250000", label:"Under $250M", lo:0, hi:250000},
  {v:"250000-500000", label:"$250M – $500M", lo:250000, hi:500000},
  {v:"500000-1000000", label:"$500M – $1B", lo:500000, hi:1000000},
  {v:"1000000-3000000", label:"$1B – $3B", lo:1000000, hi:3000000},
  {v:"3000000-10000000", label:"$3B – $10B", lo:3000000, hi:10000000},
  {v:"10000000-", label:"Over $10B", lo:10000000, hi:null}
];

const QUARTERS = ["2026Q1","2025Q4","2025Q3","2025Q2","2025Q1","2024Q4","2024Q3","2024Q2","2024Q1","2023Q4","2023Q3","2023Q2","2023Q1"];

const FIELDS = [
  {id:"assets", label:"Total assets", group:"Balance sheet", v:"$742.0M"},
  {id:"loans", label:"Total loans", group:"Balance sheet", v:"$401.3M"},
  {id:"deposits", label:"Total deposits", group:"Balance sheet", v:"$625.1M"},
  {id:"secamort", label:"Securities (amort cost)", group:"Balance sheet", v:"$96.4M"},
  {id:"ld", label:"Loans / deposits", group:"Balance sheet", v:"64.2%"},
  {id:"ea", label:"Equity / assets", group:"Balance sheet", v:"9.8%"},
  {id:"lev", label:"Leverage ratio", group:"Capital", v:"10.4%"},
  {id:"ni", label:"Net income", group:"Earnings", v:"$1.42M"},
  {id:"roa", label:"Return on assets", group:"Earnings", v:"0.77%"},
  {id:"roe", label:"Return on equity", group:"Earnings", v:"7.9%"},
  {id:"nim", label:"Net interest margin", group:"Earnings", v:"3.12%"},
  {id:"eff", label:"Efficiency ratio", group:"Earnings", v:"64.8%"},
  {id:"secfv", label:"Securities fair value", group:"Securities", v:"$85.2M"},
  {id:"unreal", label:"Unrealized gain / loss", group:"Securities", v:"-$11.2M"},
  {id:"secy", label:"Securities yield", group:"Securities", v:"2.11%"},
  {id:"dur", label:"Portfolio duration", group:"Securities", v:"4.6y"}
];

const PROMPTS = {
  conversational: "You are a senior fixed-income strategist at SouthState Securities specializing in regulated depositories and optimizing their bond portfolios, versed in FINRA/SEC rules for broker-dealer recommendations to institutional customers (Reg BI/suitability, FINRA 2111; anti-churning, FINRA 2020). You are writing an INTERNAL call-prep brief for a SouthState Securities salesperson's relationship-building conversation with a bank.\n\nVOICE: Write the way one smart colleague would explain this to another over coffee — warm, natural, easy to read. Short plain sentences. No jargon or acronym soup; if a technical idea is unavoidable (a bond 'underwater'), explain it plainly the first time. Keep every number but wrap it in plain language.\n\nRules: 1) Use ONLY the figures provided; every claim ties to a figure. 2) Lean into a trade ONLY on a genuine material opportunity (see has_material_opportunity and the 0-100 percentile scores); otherwise give data-grounded relationship-building, don't manufacture one. 3) No specific trade size or product pitch. 4) Keep ALL numbers. 5) Internal aid, not advice/a solicitation.",
  analyst: "You are a senior fixed-income strategist at SouthState Securities specializing in regulated depositories and optimizing bond portfolios, versed in FINRA/SEC rules (Reg BI/suitability, FINRA 2111; anti-churning, FINRA 2020). You are writing an INTERNAL call-prep brief for a salesperson's relationship-building conversation with a bank.\n\nVOICE: Tight, precise fixed-income desk voice. Technical terms fine. Lead with the numbers. Concise and direct.\n\nRules: 1) Use ONLY the figures provided. 2) Recommend a trade ONLY on a genuine material opportunity; otherwise data-grounded relationship-building. 3) No trade size or product pitch. 4) Keep ALL numbers. 5) Internal aid, not advice/a solicitation."
};

const THEMES = {
  dark: {
    "--bg":"#0A1420", "--panel":"#0B1826", "--panel2":"#0C1A2A",
    "--line":"#1B2C42", "--line2":"#14263A", "--border":"#24384F", "--borderHi":"#3A5470",
    "--text":"#E9EEF6", "--text2":"#B7C7DA", "--muted":"#7E93AE", "--dim":"#5D7391", "--faint":"#4E637F",
    "--hover":"#101F31", "--track":"#1D3149", "--curve":"#132639",
    "--gold":"#C9A227", "--goldLine":"#43391A",
    "--rail":"#0B1826", "--railLine":"#1B2C42", "--railText":"#E9EEF6", "--railMuted":"#8AA0BC",
    "--railDim":"#5D7391", "--railFaint":"#4E637F", "--railSel":"#14283E", "--railHover":"#0F2135"
  },
  light: {
    "--bg":"#EFF2F7", "--panel":"#FFFFFF", "--panel2":"#F6F8FC",
    "--line":"#D9E0EA", "--line2":"#E9EEF4", "--border":"#CBD5E2", "--borderHi":"#9AAABF",
    "--text":"#0B2545", "--text2":"#3B5375", "--muted":"#5C7189", "--dim":"#6B7F99", "--faint":"#8DA0B6",
    "--hover":"#F3F6FB", "--track":"#DCE4EE", "--curve":"#E8EEF6",
    "--gold":"#9A7412", "--goldLine":"#E0CFA0",
    "--rail":"#002F6C", "--railLine":"#14458A", "--railText":"#FFFFFF", "--railMuted":"#AFC4E2",
    "--railDim":"#8FA9CE", "--railFaint":"#7794BE", "--railSel":"#0B4192", "--railHover":"#083A82"
  }
};

class Component extends DCLogic {
  state = {
    sel: 0, theme: "dark", screen: "desk", rep: "__all__", tab: "scoring",
    band: "__all__", q: "", customOpen: false, picked: [], quarters: ["2026Q1"],
    threshold: 70, wA: 0.33, wB: 0.33, wC: 0.33, cDecline: true,
    voice: "analyst", includeTrend: true, trendQ: 5, showRep: true,
    snap: ["assets","loans","deposits","secamort","ld","ea","lev"],
    trendF: ["ni","secy","unreal"],
    promptVoice: "conversational", promptBody: PROMPTS.conversational
  };

  componentDidMount() { this.paintBody(); }
  componentDidUpdate() { this.paintBody(); }
  paintBody() { document.body.style.background = this.state.theme === "dark" ? "#0A1420" : "#EFF2F7"; }

  dark() { return this.state.theme === "dark"; }

  color(s) {
    if (s >= 80) return "#E2653F";
    if (s >= 60) return "#C08243";
    if (s >= 40) return this.dark() ? "#7E8B9C" : "#68788C";
    if (s >= 20) return "#5A7186";
    return "#3F6584";
  }

  weightsNorm() {
    const { wA, wB, wC } = this.state;
    const t = (+wA || 0) + (+wB || 0) + (+wC || 0);
    return t > 0 ? [(+wA||0)/t, (+wB||0)/t, (+wC||0)/t] : [1/3, 1/3, 1/3];
  }

  composite(b) {
    const [x, y, z] = this.weightsNorm();
    return Math.round(b.a * x + b.b * y + b.c * z);
  }

  sig(letter, key, b) {
    const v = b[key];
    return { letter, label: LABELS[key], v, w: (v / 100 * 412).toFixed(1), color: this.color(v),
      figures: b[key + "f"].map(p => ({ k: p[0], v: p[1] })) };
  }

  spark(t) {
    const mn = Math.min(...t), mx = Math.max(...t), sp = mx - mn || 1;
    return t.map((v, i) => `${(i / (t.length - 1) * 34).toFixed(1)},${(14 - (v - mn) / sp * 12).toFixed(1)}`).join(" ");
  }

  btn(on) {
    return { fontFamily: "'IBM Plex Sans',sans-serif", fontSize: "11.5px", padding: "5px 10px", cursor: "pointer",
      border: "none", fontWeight: on ? 600 : 400,
      background: on ? (this.dark() ? "#203952" : "#0B2545") : "transparent",
      color: on ? "#FFFFFF" : (this.dark() ? "#7E93AE" : "#5C7189") };
  }

  navItem(active) {
    return { display: "flex", alignItems: "center", gap: "9px", padding: "7px 9px", fontSize: "13px",
      cursor: "pointer", fontWeight: active ? 500 : 400,
      color: active ? "var(--railText,#E9EEF6)" : "var(--railMuted,#8AA0BC)",
      background: active ? "var(--railSel,#14283E)" : "transparent",
      borderLeft: active ? "2px solid #E9A93C" : "2px solid transparent" };
  }

  navNum(active) {
    return { fontFamily: "'IBM Plex Mono',monospace", fontSize: "11px",
      color: active ? "#E9A93C" : "var(--railFaint,#4E637F)" };
  }

  card(on) {
    return { border: on ? "1px solid #E9A93C" : "1px solid var(--border,#24384F)",
      background: on ? (this.dark() ? "#17222B" : "#FFF8E9") : "var(--panel2,#0C1A2A)",
      padding: "11px 13px", cursor: "pointer", color: "var(--text,#E9EEF6)" };
  }

  switchStyle(on) {
    return { width: "36px", height: "18px", background: on ? "#E9A93C" : "var(--track,#1D3149)",
      cursor: "pointer", display: "flex", alignItems: "center",
      justifyContent: on ? "flex-end" : "flex-start", padding: "2px", flex: "0 0 auto" };
  }
  knobStyle(on) { return { width: "14px", height: "14px", background: on ? "#0A1420" : "#6E829A" }; }

  box(on) {
    return { width: "13px", height: "13px", flex: "0 0 auto",
      border: on ? "1px solid #E9A93C" : "1px solid var(--borderHi,#3A5470)",
      background: on ? "#E9A93C" : "transparent",
      boxShadow: on ? "inset 0 0 0 2px var(--panel2,#0C1A2A)" : "none" };
  }

  tabStyle(id) {
    const on = this.state.tab === id;
    return { display: "flex", alignItems: "center", gap: "7px", padding: "9px 14px", fontSize: "12.5px",
      cursor: "pointer", fontWeight: on ? 600 : 400,
      color: on ? "var(--text,#E9EEF6)" : "var(--muted,#7E93AE)",
      borderBottom: on ? "2px solid #E9A93C" : "2px solid transparent" };
  }

  badgeStyle(on) {
    return { fontFamily: "'IBM Plex Mono',monospace", fontSize: "10px", padding: "1px 5px",
      color: on ? "#E9A93C" : "var(--faint,#4E637F)",
      border: on ? "1px solid #5A4A1E" : "1px solid var(--border,#24384F)" };
  }

  pill(kind) {
    const map = { ok: ["#4E9A6A", "#20402E"], active: ["#E9A93C", "#4A3A16"], off: ["var(--faint,#4E637F)", "var(--border,#24384F)"] };
    const [c, b] = map[kind];
    return { fontSize: "10.5px", padding: "2px 8px", color: c, border: "1px solid " + b, whiteSpace: "nowrap" };
  }

  renderVals() {
    const st = this.state, dark = this.dark();
    const selectStyle = { fontFamily: "'IBM Plex Sans',sans-serif", fontSize: "11.5px", padding: "4px 22px 4px 8px",
      background: "var(--panel2,#0C1A2A)", color: "var(--text,#E9EEF6)",
      border: "1px solid var(--border,#24384F)", cursor: "pointer" };

    const repNames = ["Dana Whitfield", "Parker Grubbs", "Alicia Roan", "Unassigned"];
    const repOptions = [{ v: "__all__", label: "All reps" }].concat(
      repNames.map(n => ({ v: n, label: `${n} (${BANKS.filter(b => b.rep === n).length})` })));

    const filtered = BANKS.map((b, i) => ({ b, i }))
      .filter(o => st.rep === "__all__" || o.b.rep === st.rep);

    const selIdx = filtered.some(o => o.i === st.sel) ? st.sel : (filtered[0] ? filtered[0].i : 0);

    const rows = filtered.map(({ b, i }) => {
      const comp = this.composite(b);
      return {
        bank: b.bank, loc: b.loc, assets: b.assets, rep: b.rep,
        rankStr: b.rank.toLocaleString(),
        rankX: ((1 - b.rank / 4530) * 62).toFixed(1),
        a: { v: b.a, w: (b.a / 100 * 46).toFixed(1), color: this.color(b.a) },
        b: { v: b.b, w: (b.b / 100 * 46).toFixed(1), color: this.color(b.b) },
        c: { v: b.c, w: (b.c / 100 * 46).toFixed(1), color: this.color(b.c) },
        comp: { v: comp, color: this.color(comp) },
        spark: this.spark(b.trend),
        bg: i === selIdx ? (dark ? "#14283E" : "#E8EFF9") : "transparent",
        mark: i === selIdx ? "#E9A93C" : "transparent",
        select: () => this.setState({ sel: i })
      };
    });

    const b = BANKS[selIdx];
    const comp = this.composite(b);
    const material = comp >= st.threshold;
    const sel = {
      bank: b.bank, loc: b.loc, assets: b.assets, rep: b.rep,
      rankStr: b.rank.toLocaleString(),
      comp: { v: comp, color: this.color(comp) },
      markX: (comp / 100 * 412).toFixed(1),
      verdict: material ? `Material opportunity · above ${st.threshold}th percentile` : "Below threshold · relationship call",
      verdictColor: material ? "#E2653F" : (dark ? "#7E93AE" : "#5C7189"),
      positionNote: `Composite of ${comp} places this bank ahead of ${(4530 - b.rank).toLocaleString()} of 4,530 depositories screened for 2026Q1.`,
      signals: [this.sig("A", "a", b), this.sig("B", "b", b), this.sig("C", "c", b)],
      narrative: b.narr
    };

    const [nA, nB, nC] = this.weightsNorm();
    const wTotal = (+st.wA || 0) + (+st.wB || 0) + (+st.wC || 0);
    const weights = [
      { letter: "A", label: "Idle liquidity", value: st.wA, pct: Math.round(nA * 100) + "%", barW: (nA * 180).toFixed(1), color: "#3F6584", onChange: e => this.setState({ wA: e.target.value }) },
      { letter: "B", label: "Underwater book", value: st.wB, pct: Math.round(nB * 100) + "%", barW: (nB * 180).toFixed(1), color: "#C08243", onChange: e => this.setState({ wB: e.target.value }) },
      { letter: "C", label: "Net income q/q", value: st.wC, pct: Math.round(nC * 100) + "%", barW: (nC * 180).toFixed(1), color: "#7E8B9C", onChange: e => this.setState({ wC: e.target.value }) }
    ];

    const pB = BANKS[0], pComp = this.composite(pB), pMat = pComp >= st.threshold;
    const preview = {
      bank: pB.bank, comp: pComp, was: Math.round((pB.a + pB.b + pB.c) / 3),
      color: this.color(pComp),
      markX: (pComp / 100 * 412).toFixed(1),
      threshX: (st.threshold / 100 * 412).toFixed(1),
      threshW: ((100 - st.threshold) / 100 * 412).toFixed(1),
      threshLabelX: Math.min(st.threshold / 100 * 412 + 4, 320).toFixed(1),
      verdict: pMat ? "Clears the threshold" : "Falls below the threshold",
      verdictColor: pMat ? "#E2653F" : (dark ? "#7E93AE" : "#5C7189")
    };

    const comps = BANKS.map(x => this.composite(x));
    const clearBars = comps.map(c => ({ color: c >= st.threshold ? "#E9A93C" : (dark ? "#1D3149" : "#DCE4EE") }));

    const tabs = [
      { id: "scoring", label: "Scoring", badge: st.threshold + "th" },
      { id: "narrative", label: "Narrative & PDF", badge: st.voice === "analyst" ? "Analyst" : "Conv." },
      { id: "provider", label: "AI provider", badge: "Anthropic" },
      { id: "prompts", label: "Prompts", badge: "2" }
    ].map(t => ({ ...t, style: this.tabStyle(t.id), badgeStyle: this.badgeStyle(st.tab === t.id), go: () => this.setState({ tab: t.id }) }));

    const fields = FIELDS.map(f => ({
      label: f.label, group: f.group,
      snapBox: this.box(st.snap.includes(f.id)),
      trendBox: this.box(st.trendF.includes(f.id)),
      toggleSnap: () => this.setState(s => ({ snap: s.snap.includes(f.id) ? s.snap.filter(x => x !== f.id) : s.snap.concat(f.id) })),
      toggleTrendF: () => this.setState(s => ({ trendF: s.trendF.includes(f.id) ? s.trendF.filter(x => x !== f.id) : (s.trendF.length >= 8 ? s.trendF : s.trendF.concat(f.id)) }))
    }));

    const providers = [
      { name: "Active setting", detail: "LLM_PROVIDER=anthropic", status: "Anthropic", kind: "active", strong: true },
      { name: "Anthropic", detail: "claude · key present", status: "configured", kind: "ok" },
      { name: "Azure OpenAI", detail: "endpoint unset", status: "not configured", kind: "off" },
      { name: "OpenAI", detail: "key unset", status: "not configured", kind: "off" },
      { name: "Ollama", detail: "localhost:11434 · reachable", status: "configured", kind: "ok" }
    ].map(p => ({ name: p.name, detail: p.detail, status: p.status, pill: this.pill(p.kind),
      weight: p.strong ? 600 : 400, bg: p.strong ? "var(--panel2,#0C1A2A)" : "transparent" }));

    const chain = [
      { n: "1", label: "Anthropic", note: "primary", dot: "#4E9A6A" },
      { n: "2", label: "Ollama", note: "local fallback", dot: "#4E9A6A" },
      { n: "3", label: "Built-in narrative", note: "always available", dot: "#E9A93C" }
    ];

    const bandOf = raw => { const x = BANDS.find(bd => raw >= bd.lo && (bd.hi === null || raw < bd.hi)); return x ? x.v : null; };
    const univ = BANKS.map((bk, i) => {
      const m = META[bk.bank] || { prev: 0, prevRank: 0, raw: 0 };
      return { bk, i, comp: this.composite(bk), prev: m.prev, prevRank: m.prevRank, raw: m.raw, band: bandOf(m.raw) };
    });

    const qStr = st.q.trim().toLowerCase();
    const mQ = o => !qStr || (o.bk.bank + " " + o.bk.loc).toLowerCase().indexOf(qStr) > -1;
    const mRep = o => st.rep === "__all__" || o.bk.rep === st.rep;
    const mBand = o => st.band === "__all__" || o.band === st.band;

    const deskRepOptions = [{ v: "__all__", label: "All reps" }].concat(
      repNames.map(n => ({ n, c: univ.filter(o => o.bk.rep === n && mBand(o) && mQ(o)).length }))
        .filter(x => x.c > 0 || x.n === st.rep)
        .map(x => ({ v: x.n, label: `${x.n} (${x.c})` })));

    const bandOptions = [{ v: "__all__", label: "All sizes" }].concat(
      BANDS.map(bd => ({ bd, c: univ.filter(o => o.band === bd.v && mRep(o) && mQ(o)).length }))
        .filter(x => x.c > 0 || x.bd.v === st.band)
        .map(x => ({ v: x.bd.v, label: `${x.bd.label} (${x.c})` })));

    const openBank = i => () => this.setState({ sel: i, screen: "results" });
    const dColor = d => d > 0 ? "#E2653F" : d < 0 ? (dark ? "#5A7186" : "#68788C") : "var(--faint,#4E637F)";
    const dStr = d => d > 0 ? "+" + d : d < 0 ? String(d) : "—";

    const deskFiltered = univ.filter(o => mRep(o) && mBand(o) && mQ(o)).sort((x, y) => y.comp - x.comp);
    const deskRows = deskFiltered.map(o => {
      const d = o.comp - o.prev;
      return {
        bank: o.bk.bank, loc: o.bk.loc, assets: o.bk.assets, rep: o.bk.rep,
        rankStr: o.bk.rank.toLocaleString(),
        rankX: ((1 - o.bk.rank / 4530) * 62).toFixed(1),
        a: { v: o.bk.a, w: (o.bk.a / 100 * 46).toFixed(1), color: this.color(o.bk.a) },
        b: { v: o.bk.b, w: (o.bk.b / 100 * 46).toFixed(1), color: this.color(o.bk.b) },
        c: { v: o.bk.c, w: (o.bk.c / 100 * 46).toFixed(1), color: this.color(o.bk.c) },
        comp: { v: o.comp, color: this.color(o.comp) },
        delta: dStr(d), dColor: dColor(d),
        spark: this.spark(o.bk.trend),
        mark: o.comp >= st.threshold ? "#E9A93C" : "transparent",
        open: openBank(o.i)
      };
    });

    const movers = univ.slice().sort((x, y) => Math.abs(y.comp - y.prev) - Math.abs(x.comp - x.prev)).slice(0, 5)
      .map(o => {
        const d = o.comp - o.prev;
        return { bank: o.bk.bank, delta: dStr(d), color: dColor(d), from: o.prev, to: o.comp,
          driver: DRIVERS[o.bk.bank] || "Composite re-ranked q/q", open: openBank(o.i) };
      });

    const entrants = univ.filter(o => o.bk.rank <= 453 && o.prevRank > 453).sort((x, y) => x.bk.rank - y.bk.rank)
      .map(o => ({ bank: o.bk.bank, rep: o.bk.rep === "Unassigned" ? "Unassigned — claim in rep file" : o.bk.rep,
        rank: o.bk.rank.toLocaleString(), prevRank: o.prevRank.toLocaleString(), open: openBank(o.i) }));

    const aboveN = univ.filter(o => o.comp >= st.threshold).length;
    const pickRows = univ.map(o => ({
      bank: o.bk.bank, assets: o.bk.assets, box: this.box(st.picked.includes(o.i)),
      toggle: () => this.setState(s => ({ picked: s.picked.includes(o.i) ? s.picked.filter(x => x !== o.i) : s.picked.concat(o.i) }))
    }));
    const quarterRows = QUARTERS.map(qq => {
      const on = st.quarters.includes(qq);
      return { label: qq, style: { fontFamily: "'IBM Plex Mono',monospace", fontSize: "11px", padding: "5px 0",
          textAlign: "center", cursor: "pointer", fontVariantNumeric: "tabular-nums",
          border: on ? "1px solid #E9A93C" : "1px solid var(--border,#24384F)",
          background: on ? (dark ? "#17222B" : "#FFF8E9") : "var(--panel2,#0C1A2A)",
          color: on ? "#E9A93C" : "var(--muted,#7E93AE)" },
        toggle: () => this.setState(s => ({ quarters: s.quarters.includes(qq) ? s.quarters.filter(x => x !== qq) : s.quarters.concat(qq) })) };
    });

    const byId = Object.fromEntries(FIELDS.map(f => [f.id, f]));
    const pdfSnapRows = st.snap.map(id => ({ label: byId[id].label, value: byId[id].v }));
    const pdfTrendRows = st.trendF.map(id => ({ label: byId[id].label, value: byId[id].v + " · 5q" }));

    return {
      themeStyle: THEMES[st.theme],
      isDesk: st.screen === "desk", isResults: st.screen === "results", isSettings: st.screen === "settings",
      goDesk: () => this.setState({ screen: "desk" }),
      goSettings: () => this.setState({ screen: "settings" }),
      navAnalyze: this.navItem(st.screen !== "settings"), navAnalyzeNum: this.navNum(st.screen !== "settings"),

      deskRows, movers, entrants, deskRepOptions, bandOptions, pickRows, quarterRows,
      band: st.band, q: st.q, noop: () => {},
      onBand: e => this.setState({ band: e.target.value }),
      onQ: e => this.setState({ q: e.target.value }),
      anyFilter: st.rep !== "__all__" || st.band !== "__all__" || st.q !== "",
      clearFilters: () => this.setState({ rep: "__all__", band: "__all__", q: "" }),
      deskCount: `${deskRows.length} of ${BANKS.length} shown`,
      aboveLabel: `${aboveN} of ${BANKS.length}`,
      customOpen: st.customOpen,
      toggleCustom: () => this.setState(s => ({ customOpen: !s.customOpen })),
      customBtn: { fontFamily: "inherit", fontSize: "12px", fontWeight: 600, padding: "6px 12px", cursor: "pointer",
        border: "1px solid #E9A93C", background: st.customOpen ? "transparent" : "#E9A93C",
        color: st.customOpen ? "#E9A93C" : "#0A1420" },
      customLabel: st.customOpen ? "Custom screen ✕" : "Custom screen",
      pickedLabel: st.picked.length === 0 ? "none selected — full universe" : `${st.picked.length} selected`,
      clearPicks: () => this.setState({ picked: [], quarters: ["2026Q1"] }),
      runCustom: () => this.setState({ customOpen: false, screen: "results" }),
      deskFoot: `Ranked by composite against the full 2026Q1 universe of 4,530 depositories. The ${BANKS.length} banks shown cleared the desk's pre-screen; gold rules mark banks at or above the ${st.threshold}th percentile threshold. Click any row to open the call-prep brief.`,
      clearTotal: BANKS.length,
      navSettings: this.navItem(st.screen === "settings"), navSettingsNum: this.navNum(st.screen === "settings"),
      setDark: () => this.setState({ theme: "dark" }), setLight: () => this.setState({ theme: "light" }),
      darkBtn: this.btn(dark), lightBtn: this.btn(!dark),

      rows, sel, selectStyle, repOptions, rep: st.rep,
      repActive: st.rep !== "__all__",
      onRep: e => this.setState({ rep: e.target.value }),
      clearRep: () => this.setState({ rep: "__all__" }),
      countLabel: `${rows.length} of ${BANKS.length} banks`,
      batchLabel: `Batch PDF · ${rows.length}`,
      footNote: st.rep === "__all__"
        ? "Scores are universe percentiles for 2026Q1. Click a row to load the call-prep brief."
        : `Showing ${rows.length} bank${rows.length === 1 ? "" : "s"} assigned to ${st.rep}. Scores remain relative to the full universe of 4,530.`,
      voiceLabel: st.voice === "analyst" ? "Analyst voice" : "Conversational voice",

      tabs, tabScoring: st.tab === "scoring", tabNarrative: st.tab === "narrative",
      tabProvider: st.tab === "provider", tabPrompts: st.tab === "prompts",

      threshold: st.threshold,
      onThreshold: e => this.setState({ threshold: +e.target.value }),
      weights,
      weightNote: wTotal.toFixed(2) + " total → normalized",
      weightNoteColor: Math.abs(wTotal - 1) < 0.02 ? "var(--faint,#4E637F)" : "#C08243",
      setDecline: () => this.setState({ cDecline: true }),
      setImprove: () => this.setState({ cDecline: false }),
      declineStyle: this.card(st.cDecline), improveStyle: this.card(!st.cDecline),
      preview, clearCount: comps.filter(c => c >= st.threshold).length, clearBars,

      setConversational: () => this.setState({ voice: "conversational" }),
      setAnalyst: () => this.setState({ voice: "analyst" }),
      convStyle: this.card(st.voice === "conversational"), analystStyle: this.card(st.voice === "analyst"),
      toggleTrend: () => this.setState(s => ({ includeTrend: !s.includeTrend })),
      trendSwitch: this.switchStyle(st.includeTrend), trendKnob: this.knobStyle(st.includeTrend),
      toggleShowRep: () => this.setState(s => ({ showRep: !s.showRep })),
      repSwitch: this.switchStyle(st.showRep), repKnob: this.knobStyle(st.showRep),
      trendQ: st.trendQ, onTrendQ: e => this.setState({ trendQ: +e.target.value }),
      includeTrend: st.includeTrend, trendEmpty: st.trendF.length === 0,
      fields, snapCount: st.snap.length + " selected",
      trendCount: st.trendF.length + " of 8",
      trendCountColor: st.trendF.length >= 8 ? "#C08243" : "var(--gold,#C9A227)",
      pdfSnapRows, pdfTrendRows,
      pdfRepLine: st.showRep ? "Prepared for: Dana Whitfield · SouthState Securities" : "Prepared by SouthState Securities",
      pdfRepColor: st.showRep ? "#9A7412" : "#8C99AB",

      providers, chain,
      promptBody: st.promptBody,
      onPromptBody: e => this.setState({ promptBody: e.target.value }),
      setPromptConv: () => this.setState({ promptVoice: "conversational", promptBody: PROMPTS.conversational }),
      setPromptAnalyst: () => this.setState({ promptVoice: "analyst", promptBody: PROMPTS.analyst }),
      pConvBtn: this.btn(st.promptVoice === "conversational"),
      pAnalystBtn: this.btn(st.promptVoice === "analyst")
    };
  }
}

</script>
</body>
</html>
