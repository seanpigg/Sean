"""insight.py - pluggable LLM providers + deterministic voice-aware fallback."""

import json, urllib.request, urllib.error, config

DEFAULT_BODY = {
    "conversational": """You are a senior fixed-income strategist at SouthState \
Securities specializing in regulated depositories and optimizing their bond \
portfolios, versed in FINRA/SEC rules for broker-dealer recommendations to \
institutional customers (Reg BI/suitability, FINRA 2111; anti-churning, FINRA \
2020). You are writing an INTERNAL call-prep brief for a SouthState Securities \
salesperson's relationship-building conversation with a bank.

VOICE: Write the way one smart colleague would explain this to another over \
coffee - warm, natural, easy to read. Short plain sentences. No jargon or \
acronym soup; if a technical idea is unavoidable (a bond 'underwater'), explain \
it plainly the first time. Keep every number but wrap it in plain language.

Rules: 1) Use ONLY the figures provided; every claim ties to a figure. 2) Lean \
into a trade ONLY on a genuine material opportunity (see \
has_material_opportunity and the 0-100 percentile scores); otherwise give \
data-grounded relationship-building, don't manufacture one. 3) No specific trade \
size or product pitch. 4) Keep ALL numbers. 5) Internal aid, not advice/a \
solicitation.""",
    "analyst": """You are a senior fixed-income strategist at SouthState \
Securities specializing in regulated depositories and optimizing bond \
portfolios, versed in FINRA/SEC rules (Reg BI/suitability, FINRA 2111; \
anti-churning, FINRA 2020). You are writing an INTERNAL call-prep brief for a \
salesperson's relationship-building conversation with a bank.

VOICE: Tight, precise fixed-income desk voice. Technical terms fine. Lead with \
the numbers. Concise and direct.

Rules: 1) Use ONLY the figures provided. 2) Recommend a trade ONLY on a genuine \
material opportunity; otherwise data-grounded relationship-building. 3) No trade \
size or product pitch. 4) Keep ALL numbers. 5) Internal aid, not advice/a \
solicitation.""",
}
LOCKED_JSON_CONTRACT = """
Return STRICT JSON (no prose outside it) with exactly these keys:
{
 "headline": "one sentence capturing the bank",
 "opportunity_assessment": "2-4 sentences on whether there's a real chance to help their bond portfolio, using the figures; if not material, say so and note not pushing a trade is right",
 "the_read": ["3-6 short insights, each a real number AND what it means"],
 "conversation_starters": ["2-4 relationship-first opening lines"],
 "discovery_questions": ["3-5 open questions"],
 "objections": [{"objection":"pushback","response":"warm reply"}],
 "watch_for": ["2-4 cautions"],
 "what_not_to_say": ["2-3 things to avoid"],
 "compliance_note": "one short line: internal use only, not investment advice or a solicitation, and any idea should fit the institution's objectives and pass suitability review. Do NOT use defensive phrasing like 'we do not churn'."
}
"""


def get_default_body(v):
    return DEFAULT_BODY.get(v, DEFAULT_BODY["conversational"])


def get_active_body(v):
    try:
        s = config.load_settings()
        a = (s.get("ACTIVE_PROMPT") or {}).get(v, "Default")
        if a != "Default":
            t = ((s.get("PROMPT_LIBRARY") or {}).get(v) or {}).get(a)
            if t and t.strip():
                return t
    except Exception:
        pass
    return get_default_body(v)


def _system_prompt(v):
    return get_active_body(v) + "\n\n" + LOCKED_JSON_CONTRACT


def _user_prompt(f):
    return (
        f"Fact pack (dollars in $000; scores are 0-100 percentiles vs. {f.get('universe_total')} banks for {f.get('as_of')}). "
        f"Signal A=idle/low-yield liquidity. B=underwater & low-yield bond book. C=q/q net income change. Write the brief.\n\n"
        + json.dumps(f, indent=2, default=str)
    )


def _openai_chat(base_url, api_key, model, facts, voice, extra_headers=None, query=""):
    url = base_url.rstrip("/") + "/chat/completions" + (query or "")
    payload = {
        "model": model,
        "temperature": 0.4,
        "max_tokens": 2000,
        "messages": [
            {"role": "system", "content": _system_prompt(voice)},
            {"role": "user", "content": _user_prompt(facts)},
        ],
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers=headers, method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        body = json.loads(r.read().decode())
    return _parse(body["choices"][0]["message"]["content"])


def _call_anthropic(facts, voice):
    import anthropic

    c = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    m = c.messages.create(
        model=config.ANTHROPIC_MODEL,
        max_tokens=2000,
        temperature=0.4,
        system=_system_prompt(voice),
        messages=[{"role": "user", "content": _user_prompt(facts)}],
    )
    return (
        _parse("".join(b.text for b in m.content if getattr(b, "type", "") == "text")),
        config.ANTHROPIC_MODEL,
    )


def _call_azure(facts, voice):
    base = f"{config.AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/deployments/{config.AZURE_OPENAI_DEPLOYMENT}"
    q = f"?api-version={config.AZURE_OPENAI_API_VERSION}"
    return (
        _openai_chat(
            base,
            None,
            config.AZURE_OPENAI_DEPLOYMENT,
            facts,
            voice,
            extra_headers={"api-key": config.AZURE_OPENAI_API_KEY},
            query=q,
        ),
        f"azure:{config.AZURE_OPENAI_DEPLOYMENT}",
    )


def _call_openai(facts, voice):
    return (
        _openai_chat(
            config.OPENAI_BASE_URL,
            config.OPENAI_API_KEY,
            config.OPENAI_MODEL,
            facts,
            voice,
        ),
        f"openai:{config.OPENAI_MODEL}",
    )


def _call_ollama(facts, voice):
    return (
        _openai_chat(
            config.OLLAMA_BASE_URL.rstrip("/") + "/v1",
            "ollama",
            config.OLLAMA_MODEL,
            facts,
            voice,
        ),
        f"ollama:{config.OLLAMA_MODEL}",
    )


_PROVIDERS = {
    "anthropic": _call_anthropic,
    "azure": _call_azure,
    "openai": _call_openai,
    "ollama": _call_ollama,
}


def _parse(text):
    text = (text or "").strip()
    if "```" in text:
        for p in text.split("```"):
            p = p.strip()
            if p.startswith("json"):
                p = p[4:].strip()
            if p.startswith("{"):
                text = p
                break
    try:
        return json.loads(text)
    except Exception:
        s, e = text.find("{"), text.rfind("}")
        if s != -1 and e != -1:
            return json.loads(text[s : e + 1])
    raise ValueError("no JSON in response")


def _providers_to_try():
    p = (config.LLM_PROVIDER or "auto").lower()
    if p == "off":
        return []
    if p == "auto":
        return [
            n
            for n in ("anthropic", "azure", "openai", "ollama")
            if config.provider_available(n)
        ]
    return [p] if (config.provider_available(p) or p == "ollama") else []


def generate_insight(facts, voice=None):
    if voice is None:
        voice = getattr(config, "NARRATIVE_TONE", "conversational")
    tried = []
    for name in _providers_to_try():
        try:
            data, model = _PROVIDERS[name](facts, voice)
            if not isinstance(data, dict):
                raise ValueError("bad shape")
            data["_source"] = name
            data["_model"] = model
            return data
        except Exception as e:
            tried.append(f"{name}: {type(e).__name__}")
            continue
    reason = (
        ("provider(s) failed [" + "; ".join(tried) + "]")
        if tried
        else f"no provider configured (LLM_PROVIDER={config.LLM_PROVIDER})"
    )
    return _fallback(facts, voice, reason)


def _m(x, dp=1, pct=False, dollars=False):
    if x is None:
        return "n/a"
    if dollars:
        return f"${x:,.0f}k"
    if pct:
        return f"{x:.{dp}f}%"
    return f"{x:,.{dp}f}"


def _fallback(facts, voice="conversational", reason=""):
    A = facts["signal_facts"]["A"]
    B = facts["signal_facts"]["B"]
    C = facts["signal_facts"]["C"]
    sc = facts["scores"]
    mf = facts["margin_funding"]
    material = facts.get("has_material_opportunity")
    thr = facts.get("materiality_threshold", 70)
    an = voice == "analyst"
    read = []
    if A["cash_est_$000"] is not None:
        read.append(
            (
                f"Idle liquidity ~{_m(A['cash_est_$000'],dollars=True)} ({_m(A['cash_pct_assets'],pct=True)} of assets); L/D {_m(A['loans_deposits_pct'],pct=True)}; liquidity {_m(A['liquidity_pct'],pct=True)}; EA yield {_m(A['yield_earning_assets_pct'],2,pct=True)}."
            )
            if an
            else (
                f"They\u2019re sitting on roughly {_m(A['cash_est_$000'],dollars=True)} that isn\u2019t working very hard \u2014 about {_m(A['cash_pct_assets'],pct=True)} of the bank in cash or low-earning spots, with only {_m(A['loans_deposits_pct'],pct=True)} of deposits lent out. Real room to put money to work."
            )
        )
    if B["fv_over_cost_pct"] is not None:
        read.append(
            (
                f"Book marked {_m(B['fv_over_cost_pct'],pct=True)} of amortized cost (~{_m(B['est_unrealized_loss_$000'],dollars=True)} unrealized loss); securities yield {_m(B['securities_yield_pct'],2,pct=True)}."
            )
            if an
            else (
                f"Their bonds are worth a bit less than they paid \u2014 marked at {_m(B['fv_over_cost_pct'],pct=True)} of cost (~{_m(B['est_unrealized_loss_$000'],dollars=True)} paper loss) and only earning {_m(B['securities_yield_pct'],2,pct=True)}. Usually where there\u2019s something to talk through."
            )
        )
    if C["net_income_change_$000"] is not None:
        d = "down" if (C["net_income_change_$000"] or 0) < 0 else "up"
        read.append(
            (
                f"Net income {d} q/q: {_m(C['net_income_prior_$000'],dollars=True)} -> {_m(C['net_income_now_$000'],dollars=True)} ({_m(C['net_income_change_$000'],dollars=True)})."
            )
            if an
            else (
                f"Earnings went {d} last quarter \u2014 from {_m(C['net_income_prior_$000'],dollars=True)} to {_m(C['net_income_now_$000'],dollars=True)} (a change of {_m(C['net_income_change_$000'],dollars=True)})."
            )
        )
    if mf.get("nim_pct") is not None:
        read.append(
            f"NIM {_m(mf['nim_pct'],2,pct=True)}, cost of funds {_m(mf['cost_of_funds_pct'],2,pct=True)}, loan yield {_m(mf['yield_on_loans_pct'],2,pct=True)}."
        )
    if material:
        assess = (
            f"Material opportunity: top-tier on at least one signal (bar={thr}th pct). Idle liquidity and/or a low-yield, underwater book support a redeployment conversation."
            if an
            else f"There\u2019s a real, numbers-backed reason to talk portfolio here \u2014 top-tier of the universe on at least one signal (bar is the {thr}th percentile). Lead with curiosity, not a pitch."
        )
        starters = [
            "\u201cA chunk of the bond book is low-coupon and below cost \u2014 how are you thinking about redeploying as it rolls down?\u201d",
            "\u201cYou\u2019ve got meaningful cash sitting relatively idle; how are you weighing putting it to work vs. the cushion?\u201d",
        ]
    else:
        assess = (
            f"No signal clears the {thr}th-pct bar \u2014 not a quarter to push a trade. Relationship call is the right move."
            if an
            else f"Honestly, nothing here screams \u2018trade\u2019 this quarter \u2014 no signal clears our {thr}th-percentile bar, and that\u2019s fine. Smart play is a relationship call and being first when something real comes up."
        )
        starters = [
            "\u201cNo pitch \u2014 I\u2019d just like to compare notes on how you\u2019re positioning the balance sheet.\u201d",
            "\u201cYour book looks well-managed; where are you spending the most time \u2014 funding, liquidity, or securities?\u201d",
        ]
    return {
        "headline": f"{facts['bank']} \u2014 rank {facts['universe_rank']:,} of {facts['universe_total']:,} on the composite screen for {facts['as_of']}.",
        "opportunity_assessment": assess,
        "the_read": read or ["Limited data available this quarter."],
        "conversation_starters": starters,
        "discovery_questions": [
            "As low-coupon securities roll down, are you reinvesting, letting cash build, or funding loan growth?",
            "How much of the securities book is AFS vs HTM \u2014 how much of any mark flows through capital?",
            "How are you thinking about funding costs and deposit stickiness from here?",
        ],
        "objections": [
            {
                "objection": "We\u2019re happy with our current partners.",
                "response": "Totally understand \u2014 not here to displace anyone, just to be a useful resource.",
            },
            {
                "objection": "We\u2019re not looking to do anything right now.",
                "response": "Perfect \u2014 no ask today. I\u2019d just like to build the relationship so we\u2019re helpful when the timing\u2019s right.",
            },
        ],
        "watch_for": [
            "Don\u2019t over-read a single quarter \u2014 one-quarter swings can overstate a trend.",
            "Understand the AFS/HTM split before concluding how a securities mark hits capital.",
        ],
        "what_not_to_say": [
            "Don\u2019t frame a bond restructuring as a rescue \u2014 if there\u2019s an angle, it\u2019s harvesting yield as low-coupon paper rolls down.",
            "Don\u2019t assert problems the numbers don\u2019t support; ask questions instead.",
        ],
        "compliance_note": "Internal analytical aid only \u2014 not investment advice or a solicitation. Any idea should fit the institution\u2019s objectives and pass suitability review before action.",
        "_source": "fallback",
        "_reason": reason,
    }
