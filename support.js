{% extends "base.html" %}
{% block title %}Analyze{% endblock %}
{% block content %}
<style>
  .atag{display:inline-block;font-size:11.5px;font-weight:700;color:#0f3d2e;background:#E7F3EC;
        border:1px solid #BFE3CE;border-radius:12px;padding:1px 9px;flex:0 0 auto;font-variant-numeric:tabular-nums;}
  .filter-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:12px;}
  .filter-row .prompt-sel{min-width:200px;}
  .filter-row label{color:var(--muted);font-size:13.5px;}
</style>
<div class="page-head"><h2>Bond-Portfolio Opportunity Screen</h2>
<div class="sub">Score any depository on idle liquidity, an underwater book, and earnings momentum — ranked against the full universe, with a one-click PDF hand-off.</div></div>
<section class="card"><h2>Data source</h2>
  <p class="path" style="margin-top:4px;">{{ data_dir }}<a href="{{ url_for('validate') }}" style="float:right;font-family:var(--font);">Run data QC &rarr;</a></p>
  <div class="kpis">
    <div class="kpi"><div class="k-val">{{ quarters|length }}</div><div class="k-lbl">Quarters detected</div></div>
    <div class="kpi"><div class="k-val">{{ "{:,}".format(banks|length) }}</div><div class="k-lbl">Banks in newest file</div></div>
    <div class="kpi"><div class="k-val">{{ rep_status.rep_count if rep_status.ok else "—" }}</div><div class="k-lbl">Reps {{ "loaded" if rep_status.ok else "(file not found)" }}</div></div>
  </div>
  <div style="margin-top:10px;display:flex;align-items:center;gap:12px;">
    <form action="{{ url_for('refresh') }}" method="post" style="margin:0;"><button type="submit" class="btn btn-sm">↻ Refresh data</button></form>
    <span class="muted">{{ cache.workbooks_cached }} workbook(s) cached. {% if rep_status.ok %}Rep assignments: {{ rep_status.bank_count }} banks mapped.{% else %}Rep file: {{ rep_status.note }}.{% endif %}</span>
  </div>
</section>
<section class="card"><h2>Select banks &amp; quarters</h2>
  <form action="{{ url_for('analyze') }}" method="post">
    <div class="filter-row">
      <label>Filter by rep:</label>
      <select name="rep_filter" id="repFilter" class="prompt-sel" onchange="onFilterChange()"></select>
      <label style="margin-left:6px;">Asset size:</label>
      <select id="assetFilter" class="prompt-sel" onchange="onFilterChange()"></select>
      <button type="button" class="btn btn-sm" onclick="clearFilters()">Clear filters</button>
      <span class="muted" id="repCount"></span>
    </div>
    <div class="grid">
      <div><h3>Bank(s)</h3>
        <input type="text" id="bankSearch" class="filter" onkeyup="applyBankFilter()" placeholder="Type to filter {{ '{:,}'.format(banks|length) }} banks…">
        <div id="banklist" class="scrollbox">
          {% for b in banks %}<label class="chk" data-rep="{{ '__unassigned__' if (b.rep and b.rep.unassigned) else (b.rep.name if b.rep else '__unassigned__') }}" data-assets="{{ b.assets_raw if b.assets_raw is not none else '' }}"><input type="checkbox" name="banks" value="{{ b.key }}"> {{ b.label }}{% if b.rep %} <span class="{{ 'rtag-un' if b.rep.unassigned else 'rtag' }}">{{ 'Unassigned' if b.rep.unassigned else b.rep.name }}</span>{% endif %}{% if b.assets_fmt %} <span class="atag">{{ b.assets_fmt }}</span>{% endif %}</label>{% endfor %}
        </div></div>
      <div><h3>Quarter(s)</h3>
        <div class="scrollbox">{% for q in quarters %}<label class="chk"><input type="checkbox" name="quarters" value="{{ q }}"> {{ q }}</label>{% endfor %}</div></div>
    </div>
    <p class="muted" style="margin:4px 0 8px;">Scores are always relative to the full universe for the most recent quarter you select.</p>
    <button type="submit" class="btn primary">Run analysis</button>
  </form>
</section>
<script>
var REP_OPTS = {{ rep_options|tojson }};
var BANDS = [
  {v:"0-250000",       label:"Under $250M",  lo:0,        hi:250000},
  {v:"250000-500000",  label:"$250M – $500M",lo:250000,   hi:500000},
  {v:"500000-1000000", label:"$500M – $1B",  lo:500000,   hi:1000000},
  {v:"1000000-3000000",label:"$1B – $3B",    lo:1000000,  hi:3000000},
  {v:"3000000-10000000",label:"$3B – $10B",  lo:3000000,  hi:10000000},
  {v:"10000000-",      label:"Over $10B",    lo:10000000, hi:null}
];
function bandOf(a){
  if(a===null||a===''||isNaN(a)) return null;
  for(var i=0;i<BANDS.length;i++){var b=BANDS[i]; if(a>=b.lo && (b.hi===null||a<b.hi)) return b.v;}
  return null;
}
var ROWS=[];
(function(){
  var labels=document.getElementById('banklist').getElementsByClassName('chk');
  for(var i=0;i<labels.length;i++){
    var rep=labels[i].getAttribute('data-rep')||'__unassigned__';
    var aStr=labels[i].getAttribute('data-assets');
    var a=(aStr===''||aStr===null)?null:parseFloat(aStr);
    ROWS.push({rep:rep, band:bandOf(a)});
  }
})();
function currentRep(){return document.getElementById('repFilter').value||'__all__';}
function currentBand(){return document.getElementById('assetFilter').value||'__all__';}
function repCounts(band){
  var m={};
  for(var i=0;i<ROWS.length;i++){var r=ROWS[i]; if(band!=='__all__'&&r.band!==band)continue; m[r.rep]=(m[r.rep]||0)+1;}
  return m;
}
function bandCounts(rep){
  var m={};
  for(var i=0;i<ROWS.length;i++){var r=ROWS[i]; if(rep!=='__all__'&&r.rep!==rep)continue; if(r.band!==null)m[r.band]=(m[r.band]||0)+1;}
  return m;
}
function rebuildSelects(){
  var repSel=document.getElementById('repFilter');
  var bandSel=document.getElementById('assetFilter');
  var repVal=repSel.value||'__all__';
  var bandVal=bandSel.value||'__all__';
  var rc=repCounts(bandVal);
  var bc=bandCounts(repVal);

  // rep options reflect the chosen band (NO counts in labels)
  var repHtml='';
  for(var i=0;i<REP_OPTS.length;i++){
    var o=REP_OPTS[i];
    if(o.value==='__all__'){ repHtml+='<option value="__all__">All reps</option>'; continue; }
    var cnt=rc[o.value]||0;
    if(cnt>0 || o.value===repVal){ repHtml+='<option value="'+o.value+'">'+o.label+'</option>'; }
  }
  repSel.innerHTML=repHtml; repSel.value=repVal;

  // band options reflect the chosen rep (NO counts in labels)
  var bandHtml='<option value="__all__">All sizes</option>';
  for(var j=0;j<BANDS.length;j++){
    var b=BANDS[j]; var cnt2=bc[b.v]||0;
    if(cnt2>0 || b.v===bandVal){ bandHtml+='<option value="'+b.v+'">'+b.label+'</option>'; }
  }
  bandSel.innerHTML=bandHtml; bandSel.value=bandVal;
}
function applyBankFilter(){
  var rep=currentRep(), band=currentBand();
  var text=(document.getElementById('bankSearch').value||'').toLowerCase();
  var lo=null,hi=null;
  if(band!=='__all__'){var p=band.split('-');lo=(p[0]==='')?null:parseFloat(p[0]);hi=(p[1]===''||p[1]===undefined)?null:parseFloat(p[1]);}
  var labels=document.getElementById('banklist').getElementsByClassName('chk');
  var shown=0;
  for(var i=0;i<labels.length;i++){
    var lab=labels[i];
    var labRep=lab.getAttribute('data-rep')||'__unassigned__';
    var repOk=(rep==='__all__')||(labRep===rep);
    var textOk=(text==='')||(lab.textContent.toLowerCase().indexOf(text)>-1);
    var assetOk=true;
    if(lo!==null||hi!==null){
      var aStr=lab.getAttribute('data-assets');
      if(aStr===''||aStr===null){assetOk=false;}
      else{var a=parseFloat(aStr); if(lo!==null&&a<lo)assetOk=false; if(hi!==null&&a>=hi)assetOk=false;}
    }
    var vis=repOk&&textOk&&assetOk;
    lab.style.display=vis?'':'none';
    if(vis)shown++;
  }
  var c=document.getElementById('repCount');
  c.textContent=(rep==='__all__'&&band==='__all__'&&text==='')?'':(shown.toLocaleString()+' bank'+(shown===1?'':'s')+' shown');
}
function onFilterChange(){ rebuildSelects(); applyBankFilter(); }
function clearFilters(){
  document.getElementById('repFilter').value='__all__';
  document.getElementById('assetFilter').value='__all__';
  document.getElementById('bankSearch').value='';
  rebuildSelects();      // repopulate both dropdowns to full lists
  applyBankFilter();     // re-show all banks
}
rebuildSelects();
applyBankFilter();
</script>
{% endblock %}
