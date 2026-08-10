"""SSS Bank Analysis - Flask front-end."""

import io
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
    abort,
)
import config, analysis, reps, desk

app = Flask(__name__)
app.secret_key = "change-me-to-a-random-string"


@app.context_processor
def _template_helpers():
    """Lets templates check whether a route exists before linking to it."""
    return {"has_endpoint": lambda name: name in app.view_functions}


def _provider_summary():
    prov = config.LLM_PROVIDER
    ready = {
        p: config.provider_available(p)
        for p in ("anthropic", "azure", "openai", "ollama")
    }
    active_ok = (
        (prov == "auto" and any(ready.values()))
        or config.provider_available(prov)
        or prov == "ollama"
    )
    label = "Built-in only" if prov == "off" else (prov if prov != "auto" else "auto")
    return {"provider": prov, "label": label, "ready": ready, "active_ok": active_ok}


@app.route("/", methods=["GET"])
def home():
    """Bank Universe — the screen already run. All of it lives in desk.py."""
    return desk.render_home()


@app.route("/bank", methods=["GET"])
def bank():
    """Call-prep detail for one bank. Narrative is NOT generated here."""
    return desk.render_bank()


@app.route("/bank/narrative", methods=["POST"])
def bank_narrative():
    """The one call that costs money — fired from the detail page on request."""
    return desk.narrative_json()


@app.route("/analyze", methods=["POST"])
def analyze():
    selected_banks = request.form.getlist("banks")
    selected_quarters = request.form.getlist("quarters")
    rep_filter = request.form.get("rep_filter", "__all__")
    if not selected_banks or not selected_quarters:
        flash("Please select at least one bank and one quarter.")
        return redirect(url_for("home"))
    results = analysis.run_analysis(
        banks=selected_banks, quarters=selected_quarters, rep_filter=rep_filter
    )
    as_of = sorted(selected_quarters, key=lambda q: int(q[:4]) * 10 + int(q[-1]))[-1]
    rep_label = next(
        (o["label"] for o in reps.rep_options() if o["value"] == rep_filter), "All reps"
    )
    return render_template(
        "results.html",
        results=results,
        banks=selected_banks,
        quarters=selected_quarters,
        as_of=as_of,
        rep_filter=rep_filter,
        rep_label=rep_label,
    )


@app.route("/pdf")
def pdf():
    bank = request.args.get("bank", "").strip()
    as_of = request.args.get("as_of", "").strip()
    if not bank or not as_of:
        abort(400, "bank and as_of are required")
    facts = analysis.get_bank_facts(bank, as_of)
    if facts is None:
        abort(404, f"No data for {bank} in {as_of}")
    import insight, pdf_report

    # If the detail page already wrote a narrative and the user is exporting
    # what they just read, carry THAT text through. Regenerating here would
    # spend a second model call and could return different words than the ones
    # on screen — the brief has to match what was approved.
    narrative = None
    voice = (request.args.get("voice") or "").strip()
    if request.args.get("narrative") == "1" and voice:
        narrative = desk.take_narrative(bank, as_of, voice)
    if narrative is None:
        try:
            narrative = insight.generate_insight(facts, voice) if voice \
                else insight.generate_insight(facts)
        except TypeError:
            narrative = insight.generate_insight(facts)
        if isinstance(narrative, tuple):
            narrative = narrative[0]
    trend = None
    if getattr(config, "PDF_INCLUDE_TREND", False):
        trend = analysis.get_bank_trend(
            bank, as_of, n=getattr(config, "PDF_TREND_QUARTERS", 5)
        )
    pdf_bytes = pdf_report.build_pdf(
        facts, narrative, trend=trend, show_rep=getattr(config, "PDF_SHOW_REP", True)
    )
    safe = "".join(c if c.isalnum() else "_" for c in facts["bank"])[:40]
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"CallPrep_{safe}_{as_of}.pdf",
    )


@app.route("/ai-test")
def ai_test():
    import insight

    tiny = {
        "bank": "Test Bank",
        "as_of": "2026Q1",
        "prior": "2025Q4",
        "universe_rank": 1,
        "universe_total": 1,
        "has_material_opportunity": True,
        "materiality_threshold": 70,
        "scores": {"A": 80, "B": 80, "C": 50, "composite": 70},
        "signal_facts": {
            "A": {
                "cash_est_$000": 1000,
                "cash_pct_assets": 10,
                "loans_deposits_pct": 60,
                "liquidity_pct": 20,
                "yield_earning_assets_pct": 3.5,
            },
            "B": {
                "fv_over_cost_pct": 92,
                "underwater_pct_of_cost": 8,
                "est_unrealized_loss_$000": 500,
                "securities_yield_pct": 2.5,
            },
            "C": {
                "net_income_now_$000": 100,
                "net_income_prior_$000": 110,
                "net_income_change_$000": -10,
            },
        },
        "balance_sheet": {
            "total_assets_$000": 10000,
            "total_loans_$000": 6000,
            "total_deposits_$000": 8000,
            "total_securities_amort_cost_$000": 2000,
            "equity_over_assets_pct": 10,
            "leverage_ratio_pct": 11,
        },
        "margin_funding": {
            "nim_pct": 3.2,
            "cost_of_funds_pct": 1.3,
            "yield_on_loans_pct": 6.0,
            "noninterest_bearing_dep_pct": 15,
            "brokered_dep_pct": 2,
        },
        "securities_detail": {"pledged_pct_of_secs": 60},
        "credit": {"npas_over_assets_pct": 0.1},
    }
    results = {}
    for name in ("anthropic", "azure", "openai", "ollama"):
        if not config.provider_available(name) and name != "ollama":
            results[name] = "not configured"
            continue
        try:
            data, model = insight._PROVIDERS[name](tiny, "conversational")
            results[name] = f"OK ({model}) - {str(data.get('headline',''))[:60]}"
        except Exception as e:
            results[name] = f"FAILED: {type(e).__name__}: {str(e)[:160]}"
    return {"LLM_PROVIDER": config.LLM_PROVIDER, "results": results}


@app.route("/refresh", methods=["POST"])
def refresh():
    flash(analysis.refresh_cache())
    desk.invalidate()
    return redirect(request.referrer or url_for("home"))


@app.route("/settings", methods=["GET"])
def settings():
    import insight, fields

    s = config.load_settings()
    prompt_data = {}
    for v in ("conversational", "analyst"):
        prompt_data[v] = {
            "default": insight.get_default_body(v),
            "custom": dict(s["PROMPT_LIBRARY"].get(v, {})),
            "active": s["ACTIVE_PROMPT"].get(v, "Default"),
        }
    return render_template(
        "settings.html",
        s=s,
        saved=request.args.get("saved"),
        groups=fields.GROUPS,
        catalog=fields.FIELDS,
        snapshot_sel=set(s["SNAPSHOT_FIELDS"]),
        trend_sel=set(s["TREND_FIELDS"]),
        trend_max=fields.TREND_MAX,
        prompt_data=prompt_data,
        provider=_provider_summary(),
        rep_status=reps.status(),
    )


@app.route("/settings", methods=["POST"])
def settings_save():
    f = request.form
    try:
        mat = int(f.get("materiality", 70))
    except ValueError:
        mat = 70
    mat = max(0, min(100, mat))
    tone = f.get("tone", "conversational")
    if tone not in ("conversational", "analyst"):
        tone = "conversational"
    include_trend = f.get("include_trend") == "on"
    show_rep = f.get("show_rep") == "on"
    try:
        tq = int(f.get("trend_quarters", 5))
    except ValueError:
        tq = 5
    tq = max(2, min(12, tq))
    reward_decline = f.get("signal_c_direction", "decline") == "decline"

    def _w(n, d):
        try:
            return max(0.0, float(f.get(n, d)))
        except ValueError:
            return d

    wa, wb, wc = _w("weight_a", 1), _w("weight_b", 1), _w("weight_c", 1)
    if wa + wb + wc == 0:
        wa = wb = wc = 1
    import fields

    snapshot = fields.sanitize(f.getlist("snapshot_fields"), fields.DEFAULT_SNAPSHOT)
    trend = fields.sanitize(f.getlist("trend_fields"), fields.DEFAULT_TREND)[
        : fields.TREND_MAX
    ]
    config.save_settings(
        {
            "MATERIALITY_PERCENTILE": mat,
            "NARRATIVE_TONE": tone,
            "PDF_INCLUDE_TREND": include_trend,
            "PDF_TREND_QUARTERS": tq,
            "SIGNAL_C_REWARD_DECLINE": reward_decline,
            "SIGNAL_WEIGHTS": {"A": wa, "B": wb, "C": wc},
            "SNAPSHOT_FIELDS": snapshot,
            "TREND_FIELDS": trend,
            "PDF_SHOW_REP": show_rep,
        }
    )
    analysis.refresh_cache()
    desk.invalidate()
    flash("Settings saved. They apply immediately \u2014 no restart needed.")
    return redirect(url_for("settings", saved=1))


@app.route("/settings/reset", methods=["POST"])
def settings_reset():
    config.save_settings(dict(config.SETTINGS_DEFAULTS))
    analysis.refresh_cache()
    desk.invalidate()
    flash("Settings reset to defaults.")
    return redirect(url_for("settings"))


@app.route("/settings/prompt", methods=["POST"])
def settings_prompt():
    f = request.form
    action = f.get("action", "")
    voice = f.get("voice", "conversational")
    if voice not in ("conversational", "analyst"):
        voice = "conversational"
    s = config.load_settings()
    lib = s["PROMPT_LIBRARY"]
    active = s["ACTIVE_PROMPT"]
    name = (f.get("name") or "").strip()
    new_name = (f.get("new_name") or "").strip()
    body = (f.get("body") or "").strip()
    if action == "activate":
        active[voice] = name if (name == "Default" or name in lib[voice]) else "Default"
        flash(f"Active {voice} prompt set to \u201c{active[voice]}\u201d.")
    elif action == "save_new":
        if not new_name:
            flash("Please enter a name for the new prompt.")
        elif new_name == "Default":
            flash("\u2018Default\u2019 is reserved.")
        elif not body:
            flash("The prompt text is empty.")
        else:
            lib[voice][new_name] = body
            active[voice] = new_name
            flash(f"Saved and activated \u201c{new_name}\u201d.")
    elif action == "update":
        if name == "Default" or name not in lib[voice]:
            flash("Pick a saved custom prompt to update.")
        elif not body:
            flash("The prompt text is empty.")
        else:
            lib[voice][name] = body
            active[voice] = name
            flash(f"Updated \u201c{name}\u201d.")
    elif action == "delete":
        if name in lib[voice]:
            del lib[voice][name]
            if active[voice] == name:
                active[voice] = "Default"
            flash(f"Deleted \u201c{name}\u201d.")
        else:
            flash("Nothing to delete.")
    elif action == "revert":
        active[voice] = "Default"
        flash(f"{voice.capitalize()} prompt reverted to Default.")
    config.save_settings({"PROMPT_LIBRARY": lib, "ACTIVE_PROMPT": active})
    return redirect(url_for("settings"))


@app.route("/validate")
def validate():
    return render_template("validate.html", reports=analysis.validate_all())


@app.route("/health")
def health():
    return {
        "status": "ok",
        "ai": _provider_summary(),
        "cache": analysis.cache_status(),
        "reps": reps.status(),
        "data_dir": config.DATA_DIR,
    }


if __name__ == "__main__":
    app.run(debug=True)
