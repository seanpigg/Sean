{% extends "base_desk.html" %}
{% block title %}Settings{% endblock %}
{% block content %}

{%- set voice_label = 'Conversational' if s.NARRATIVE_TONE == 'conversational' else 'Analyst' -%}

<header class="desk-head">
  <div class="desk-head-left">
    <h1>Settings</h1>
    <div class="desk-facts">
      <div class="desk-fact">
        <span class="desk-fact-k">THRESHOLD</span>
        <span class="desk-fact-v">{{ s.MATERIALITY_PERCENTILE }}<span
            style="font-size:11px;font-weight:400;color:var(--dim);">th</span></span>
      </div>
      <div class="desk-rule"></div>
      <div class="desk-fact">
        <span class="desk-fact-k">PDF VOICE</span>
        <span class="desk-fact-v soft" style="font-family:var(--font);font-size:13.5px;">{{ voice_label }}</span>
      </div>
      <div class="desk-rule"></div>
      <div class="desk-fact">
        <span class="desk-fact-k">WEIGHTS A / B / C</span>
        <span class="desk-fact-v soft">{{ '%.2f'|format(s.SIGNAL_WEIGHTS.A) }} · {{
          '%.2f'|format(s.SIGNAL_WEIGHTS.B) }} · {{ '%.2f'|format(s.SIGNAL_WEIGHTS.C) }}</span>
      </div>
      <div class="desk-rule"></div>
      <div class="desk-fact">
        <span class="desk-fact-k">NARRATIVE ENGINE</span>
        <span class="desk-fact-v soft"
          style="font-family:var(--font);font-size:13.5px;color:{{ '#4E9A6A' if provider.active_ok else '#E9A93C' }};">{{
          provider.label }}</span>
      </div>
    </div>
  </div>
  <div class="desk-actions">
    <div class="desk-toggle">
      <button type="button" data-theme-btn="dark">Dark</button>
      <button type="button" data-theme-btn="light">Light</button>
    </div>
    <a class="desk-btn" href="{{ url_for('home') }}" data-loading="ledger">← Bank Universe</a>
  </div>
</header>

<div class="desk-status">
  <span>Changes apply immediately — no restart</span>
  <span class="sep">|</span>
  {% if rep_status.ok %}
  <span>rep file loaded · {{ "{:,}".format(rep_status.bank_count) }} banks across {{ rep_status.rep_count }} reps</span>
  {% else %}
  <span style="color:var(--amber);">rep file: {{ rep_status.note }}</span>
  {% endif %}
  <span class="right">
    <a href="{{ url_for('ai_test') }}" target="_blank">Test the live model chain →</a>
  </span>
</div>

{# ---------------- narrative engine ---------------- #}
<section class="desk-sec">
  <div class="desk-sec-head">
    <span class="k">NARRATIVE ENGINE</span>
    <span class="note">which model writes the PDF narrative — falls back to the built-in text if unreachable</span>
  </div>
  <div class="desk-set">
    <div>
      <div class="desk-set-t">Provider status</div>
      <div class="desk-set-d">Set <code>LLM_PROVIDER</code> in <code>.env</code>. Read-only here — this panel reports
        what the process can actually reach.</div>
    </div>
    <div class="desk-set-c">
      <div class="desk-prov">
        <div class="desk-prov-row">
          <span class="pn">Active setting</span>
          <span class="desk-pill {{ 'ok' if provider.active_ok else 'warn' }}">{{ provider.label }}</span>
        </div>
        {% for p, ok in provider.ready.items() %}
        <div class="desk-prov-row">
          <span class="pn">{{ p }}</span>
          <span class="desk-pill {{ 'ok' if ok }}">{{ 'configured' if ok else 'not configured' }}</span>
        </div>
        {% endfor %}
      </div>
    </div>
  </div>
</section>

<form action="{{ url_for('settings_save') }}" method="post" data-loading="settings">

  {# ---------------- scoring ---------------- #}
  <section class="desk-sec">
    <div class="desk-sec-head">
      <span class="k">SCORING</span>
      <span class="note">how the composite is built and where the desk draws the line</span>
    </div>

    <div class="desk-set">
      <div>
        <div class="desk-set-t">Opportunity threshold</div>
        <div class="desk-set-d">At or above this percentile is a material opportunity; below it is a relationship call.
          Also sets the gold rule on the Bank Universe ledger.</div>
      </div>
      <div class="desk-set-c">
        <div class="desk-range">
          <input type="range" id="materiality" name="materiality" min="0" max="100" step="5"
            value="{{ s.MATERIALITY_PERCENTILE }}" oninput="matOut.value=this.value">
          <output id="matOut" name="matOut">{{ s.MATERIALITY_PERCENTILE }}</output>
          <span class="unit">th percentile</span>
        </div>
      </div>
    </div>

    <div class="desk-set">
      <div>
        <div class="desk-set-t">Signal C — earnings direction</div>
        <div class="desk-set-d">Which way net income has to move to score well.</div>
      </div>
      <div class="desk-set-c">
        <div class="desk-choices">
          <label class="desk-choice {{ 'sel' if s.SIGNAL_C_REWARD_DECLINE }}">
            <input type="radio" name="signal_c_direction" value="decline" {{ 'checked' if s.SIGNAL_C_REWARD_DECLINE }}>
            <span class="ct">Reward a q/q decline</span>
            <span class="cd">Falling net income reads as more receptive. Default.</span>
          </label>
          <label class="desk-choice {{ 'sel' if not s.SIGNAL_C_REWARD_DECLINE }}">
            <input type="radio" name="signal_c_direction" value="improve" {{ 'checked' if not
              s.SIGNAL_C_REWARD_DECLINE }}>
            <span class="ct">Reward improvement</span>
            <span class="cd">Rising net income scores higher.</span>
          </label>
        </div>
      </div>
    </div>

    <div class="desk-set">
      <div>
        <div class="desk-set-t">Composite weighting</div>
        <div class="desk-set-d">Relative pull of each signal. Values are normalized, so 2 / 1 / 1 and 4 / 2 / 2 score
          identically. All three at zero falls back to equal weight.</div>
      </div>
      <div class="desk-set-c">
        <div class="desk-weights">
          <div class="desk-wt">
            <label>A · LIQUIDITY</label>
            <input class="desk-num" type="number" name="weight_a" min="0" step="any"
              value="{{ '%.2f'|format(s.SIGNAL_WEIGHTS.A) }}">
          </div>
          <div class="desk-wt">
            <label>B · BOND BOOK</label>
            <input class="desk-num" type="number" name="weight_b" min="0" step="any"
              value="{{ '%.2f'|format(s.SIGNAL_WEIGHTS.B) }}">
          </div>
          <div class="desk-wt">
            <label>C · NET INCOME</label>
            <input class="desk-num" type="number" name="weight_c" min="0" step="any"
              value="{{ '%.2f'|format(s.SIGNAL_WEIGHTS.C) }}">
          </div>
        </div>
      </div>
    </div>
  </section>

  {# ---------------- pdf output ---------------- #}
  <section class="desk-sec">
    <div class="desk-sec-head">
      <span class="k">PDF HAND-OFF</span>
      <span class="note">voice and contents of the per-bank call-prep document</span>
    </div>

    <div class="desk-set">
      <div>
        <div class="desk-set-t">Narrative voice</div>
        <div class="desk-set-d">Register of the written summary. Each voice has its own editable prompt below.</div>
      </div>
      <div class="desk-set-c">
        <div class="desk-choices">
          <label class="desk-choice {{ 'sel' if s.NARRATIVE_TONE=='conversational' }}">
            <input type="radio" name="tone" value="conversational" {{ 'checked' if
              s.NARRATIVE_TONE=='conversational' }}>
            <span class="ct">Conversational</span>
            <span class="cd">Natural and plain-spoken. Recommended.</span>
          </label>
          <label class="desk-choice {{ 'sel' if s.NARRATIVE_TONE=='analyst' }}">
            <input type="radio" name="tone" value="analyst" {{ 'checked' if s.NARRATIVE_TONE=='analyst' }}>
            <span class="ct">Analyst</span>
            <span class="cd">Tighter, more technical desk voice.</span>
          </label>
        </div>
      </div>
    </div>

    <div class="desk-set">
      <div>
        <div class="desk-set-t">Document options</div>
        <div class="desk-set-d">What appears beyond the narrative and the verified-figures table.</div>
      </div>
      <div class="desk-set-c">
        <label class="desk-switch">
          <input type="checkbox" name="include_trend" {{ 'checked' if s.PDF_INCLUDE_TREND }}>
          <span class="sw"></span>
          <span class="lbl">Include a multi-quarter trend table</span>
        </label>
        <div class="desk-set-row" style="padding-left:44px;">
          <span style="font-size:11px;color:var(--dim);">Quarters of history</span>
          <input class="desk-num" type="number" name="trend_quarters" min="2" max="12"
            value="{{ s.PDF_TREND_QUARTERS }}">
        </div>
        <label class="desk-switch">
          <input type="checkbox" name="show_rep" {{ 'checked' if s.PDF_SHOW_REP }}>
          <span class="sw"></span>
          <span class="lbl">Show the assigned rep — “Prepared for: …”</span>
        </label>
      </div>
    </div>

    <div class="desk-set">
      <div>
        <div class="desk-set-t">Table fields</div>
        <div class="desk-set-d">Which metrics fill the two PDF tables. The trend table is capped at {{ trend_max }}
          fields — beyond that it stops fitting the page.</div>
      </div>
      <div class="desk-set-c">
        <div class="desk-picks">
          <div class="desk-picks-col">
            <span class="h">SNAPSHOT — “VERIFIED FIGURES”</span>
            <input type="text" class="desk-text" placeholder="Filter…" onkeyup="filterList(this,'snapfields')">
            <div id="snapfields" class="desk-scroll">
              {% for gname, ids in groups %}
              <div class="desk-fgroup">{{ gname }}</div>
              {% for fid in ids %}
              <label class="desk-chk"><input type="checkbox" name="snapshot_fields" value="{{ fid }}" {{ 'checked' if
                  fid in snapshot_sel }}><span>{{ catalog[fid].label }}</span></label>
              {% endfor %}{% endfor %}
            </div>
          </div>
          <div class="desk-picks-col">
            <span class="h">TREND — “HOW IT’S TRENDING”</span>
            <input type="text" class="desk-text" placeholder="Filter…" onkeyup="filterList(this,'trendfields')">
            <div id="trendfields" class="desk-scroll">
              {% for gname, ids in groups %}
              <div class="desk-fgroup">{{ gname }}</div>
              {% for fid in ids %}
              <label class="desk-chk"><input type="checkbox" name="trend_fields" value="{{ fid }}" {{ 'checked' if fid
                  in trend_sel }}><span>{{ catalog[fid].label }}</span></label>
              {% endfor %}{% endfor %}
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="desk-savebar">
    <button type="submit" class="desk-btn primary" data-busy-label="Saving…">Save settings</button>
    {% if saved %}<span class="desk-pill ok">Saved ✓</span>{% endif %}
    <span class="spacer"></span>
    <button type="submit" class="desk-btn danger" data-busy-label="Resetting…"
      formaction="{{ url_for('settings_reset') }}"
      onclick="return confirm('Reset every setting on this page to its default?')">Reset to defaults</button>
  </div>
</form>

{# ---------------- prompts ---------------- #}
<section class="desk-sec">
  <div class="desk-sec-head">
    <span class="k">MODEL PROMPTS</span>
    <span class="note">instructions per voice — “Default” is built in and always available to revert to; the JSON output
      format is locked</span>
  </div>

  {% for voice in ['conversational','analyst'] %}
  {% set pdta = prompt_data[voice] %}
  <div class="desk-set">
    <div>
      <div class="desk-set-t">{{ 'Conversational' if voice=='conversational' else 'Analyst' }} voice</div>
      <div class="desk-set-d">Active: <strong style="color:var(--text2);">{{ pdta.active }}</strong></div>
      <div class="desk-set-d">Editing the text does nothing until you save it — “Update selected” overwrites the chosen
        prompt, “Save as new” keeps the original and switches to the copy.</div>
    </div>
    <div class="desk-set-c">
      <form action="{{ url_for('settings_prompt') }}" method="post" id="pf_{{ voice }}" data-loading="settings"
        style="display:flex;flex-direction:column;gap:9px;">
        <input type="hidden" name="voice" value="{{ voice }}">
        <input type="hidden" name="action" id="act_{{ voice }}" value="">
        <div class="desk-set-row">
          <select name="name" id="sel_{{ voice }}" class="desk-sel" onchange="loadPrompt('{{ voice }}')">
            <option value="Default" {{ 'selected' if pdta.active=='Default' }}>Default (built-in)</option>
            {% for cname in pdta.custom.keys() %}
            <option value="{{ cname }}" {{ 'selected' if pdta.active==cname }}>{{ cname }}</option>
            {% endfor %}
          </select>
          <button type="button" class="desk-btn sm" onclick="submitPrompt('{{ voice }}','activate')">Use this</button>
          <button type="button" class="desk-btn sm" onclick="submitPrompt('{{ voice }}','revert')">Revert to
            Default</button>
        </div>
        <textarea name="body" id="body_{{ voice }}" class="desk-prompt" spellcheck="false"></textarea>
        <div class="desk-set-row">
          <button type="button" class="desk-btn sm" onclick="submitPrompt('{{ voice }}','update')">Update
            selected</button>
          <button type="button" class="desk-btn sm danger" onclick="submitPrompt('{{ voice }}','delete')">Delete
            selected</button>
          <span class="spacer" style="margin-left:auto;"></span>
          <input type="text" name="new_name" class="desk-text" style="width:186px;" placeholder="New prompt name">
          <button type="button" class="desk-btn sm gold" onclick="submitPrompt('{{ voice }}','save_new')">Save as
            new</button>
        </div>
      </form>
    </div>
  </div>
  {% endfor %}
</section>

<div style="padding:14px 22px 26px;font-size:11px;color:var(--faint);">
  Scoring changes re-rank the whole universe and clear the cached screen, so the next Bank Universe load will take a
  moment while it rebuilds.
</div>

<script>
  const PROMPTS = {{ prompt_data| tojson }};

  function bodyFor(v, n) {
    if (n === 'Default') return PROMPTS[v].default;
    return (PROMPTS[v].custom || {})[n] || PROMPTS[v].default;
  }
  function loadPrompt(v) {
    document.getElementById('body_' + v).value = bodyFor(v, document.getElementById('sel_' + v).value);
  }
  function submitPrompt(v, a) {
    if (a === 'delete' && !confirm('Delete this saved prompt?')) return;
    document.getElementById('act_' + v).value = a;
    document.getElementById('pf_' + v).submit();
  }
  function filterList(input, listId) {
    var f = input.value.toLowerCase();
    var box = document.getElementById(listId);
    box.querySelectorAll('.desk-chk').forEach(function (row) {
      row.style.display = row.textContent.toLowerCase().indexOf(f) > -1 ? '' : 'none';
    });
    // hide a group heading when everything under it is filtered out
    box.querySelectorAll('.desk-fgroup').forEach(function (h) {
      var any = false, n = h.nextElementSibling;
      while (n && !n.classList.contains('desk-fgroup')) {
        if (n.style.display !== 'none') any = true;
        n = n.nextElementSibling;
      }
      h.style.display = any ? '' : 'none';
    });
  }

  ['conversational', 'analyst'].forEach(function (v) {
    var s = document.getElementById('sel_' + v);
    if (s) document.getElementById('body_' + v).value = bodyFor(v, s.value);
  });

  // radio cards track their own selected state
  document.querySelectorAll('.desk-choice input[type=radio]').forEach(function (r) {
    r.addEventListener('change', function () {
      Array.prototype.forEach.call(document.getElementsByName(r.name), function (o) {
        var card = o.closest('.desk-choice');
        if (card) card.classList.toggle('sel', o.checked);
      });
    });
  });
</script>
{% endblock %}
