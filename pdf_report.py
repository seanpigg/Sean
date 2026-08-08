"""pdf_report.py - branded SouthState 1-page PDF; sections kept together."""

import io, os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    Image,
    KeepTogether,
)

NAVY = colors.HexColor("#002D72")
NAVY2 = colors.HexColor("#06388D")
GOLD = colors.HexColor("#FDBE3F")
INK = colors.HexColor("#16223A")
MUTE = colors.HexColor("#5B6982")
LINE = colors.HexColor("#DFE4EC")
SOFT = colors.HexColor("#F3F6FB")
STATIC = os.path.join(os.path.dirname(__file__), "static")


def _styles():
    ss = getSampleStyleSheet()
    st = {}
    st["h1"] = ParagraphStyle(
        "h1",
        parent=ss["Title"],
        fontName="Helvetica-Bold",
        fontSize=17,
        textColor=NAVY,
        spaceAfter=2,
        leading=20,
    )
    st["sub"] = ParagraphStyle(
        "sub",
        fontName="Helvetica",
        fontSize=9,
        textColor=MUTE,
        spaceAfter=6,
        leading=12,
    )
    st["sec"] = ParagraphStyle(
        "sec",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=NAVY,
        spaceBefore=10,
        spaceAfter=4,
        leading=13,
    )
    st["body"] = ParagraphStyle(
        "body",
        parent=ss["Normal"],
        fontName="Helvetica",
        fontSize=9.3,
        textColor=INK,
        leading=13,
        alignment=TA_LEFT,
    )
    st["bullet"] = ParagraphStyle(
        "bullet", parent=st["body"], leftIndent=10, spaceAfter=3
    )
    st["headline"] = ParagraphStyle(
        "headline",
        parent=st["body"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        textColor=NAVY,
        leading=14,
    )
    st["small"] = ParagraphStyle(
        "small", fontName="Helvetica", fontSize=7.6, textColor=MUTE, leading=10
    )
    st["kpi_v"] = ParagraphStyle(
        "kpi_v",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=NAVY,
        alignment=1,
        leading=15,
    )
    st["kpi_l"] = ParagraphStyle(
        "kpi_l",
        fontName="Helvetica",
        fontSize=7,
        textColor=MUTE,
        alignment=1,
        leading=9,
    )
    st["obj"] = ParagraphStyle(
        "obj", parent=st["body"], fontName="Helvetica-Bold", fontSize=9.3, textColor=INK
    )
    return st


def _score_color(s):
    if s is None:
        return SOFT, MUTE
    if s >= 80:
        return colors.HexColor("#FDBE3F"), colors.HexColor("#3A2B06")
    if s >= 60:
        return colors.HexColor("#FDD98A"), colors.HexColor("#6f4d0f")
    if s >= 40:
        return colors.HexColor("#FCE9BC"), colors.HexColor("#875f13")
    if s >= 20:
        return colors.HexColor("#FBF4DE"), colors.HexColor("#8A6B1F")
    return colors.HexColor("#F1F4F9"), colors.HexColor("#7C879C")


def _header(story, st, facts, show_rep):
    logo = os.path.join(STATIC, "southstate_logo.png")
    left = (
        Image(logo, width=2.0 * inch, height=2.0 * inch * 215 / 829)
        if os.path.exists(logo)
        else Paragraph(
            "<font color='white'><b>SouthState Securities</b></font>", st["h1"]
        )
    )
    # right side: app label + optional "Prepared for: rep"
    rep = facts.get("rep") or {}
    rep_line = ""
    if show_rep and rep:
        who = rep.get("name", "")
        rep_line = f"<br/><font size=8 color='#FDBE3F'>Prepared for: {who}</font>"
    right = Paragraph(
        f"<font color='white'><b>Bank Portfolio Screen</b></font><br/><font size=8 color='#C7D0DE'>Fixed-Income Call Prep</font>{rep_line}",
        ParagraphStyle(
            "hr", fontName="Helvetica", fontSize=10, alignment=2, leading=13
        ),
    )
    band = Table([[left, right]], colWidths=[3.5 * inch, 3.5 * inch])
    band.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (0, 0), 12),
                ("RIGHTPADDING", (-1, -1), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    story.append(band)
    story.append(
        HRFlowable(width="100%", thickness=2.6, color=GOLD, spaceBefore=0, spaceAfter=8)
    )


def _identity_line(facts):
    loc = ", ".join([b for b in [facts.get("city"), facts.get("state")] if b])
    ids = []
    if facts.get("cert"):
        ids.append(f"Cert {facts['cert']}")
    if facts.get("inst_key"):
        ids.append(f"SNL {facts['inst_key']}")
    rep = facts.get("rep") or {}
    parts = [p for p in [loc, f"As-of {facts['as_of']}", " | ".join(ids)] if p]
    if rep:
        parts.append(
            ("Unassigned" if rep.get("unassigned") else f"Rep: {rep.get('name')}")
        )
    return "  \u2022  ".join(parts)


def _kpi_strip(story, st, facts):
    sc = facts["scores"]

    def cell(label, score):
        bg, fg = _score_color(score)
        val = "\u2014" if score is None else str(score)
        inner = Table(
            [
                [
                    Paragraph(
                        f"<font color='#{fg.hexval()[2:]}'><b>{val}</b></font>",
                        st["kpi_v"],
                    )
                ],
                [Paragraph(label, st["kpi_l"])],
            ],
            colWidths=[1.15 * inch],
        )
        inner.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), bg),
                    ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                    ("TOPPADDING", (0, 0), (0, 0), 6),
                    ("BOTTOMPADDING", (0, 1), (0, 1), 5),
                    ("TOPPADDING", (0, 1), (0, 1), 0),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ]
            )
        )
        return inner

    comp = Table(
        [
            [
                Paragraph(
                    f"<font color='white'><b>{'\u2014' if sc['composite'] is None else sc['composite']}</b></font>",
                    st["kpi_v"],
                )
            ],
            [Paragraph("<font color='white'>COMPOSITE</font>", st["kpi_l"])],
        ],
        colWidths=[1.15 * inch],
    )
    comp.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("TOPPADDING", (0, 0), (0, 0), 6),
                ("BOTTOMPADDING", (0, 1), (0, 1), 5),
                ("TOPPADDING", (0, 1), (0, 1), 0),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    rank = Table(
        [
            [Paragraph(f"{facts['universe_rank']:,}", st["kpi_v"])],
            [Paragraph(f"of {facts['universe_total']:,} banks", st["kpi_l"])],
        ],
        colWidths=[1.15 * inch],
    )
    rank.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("TOPPADDING", (0, 0), (0, 0), 6),
                ("BOTTOMPADDING", (0, 1), (0, 1), 5),
                ("TOPPADDING", (0, 1), (0, 1), 0),
            ]
        )
    )
    row = Table(
        [
            [
                cell("A \u00b7 LIQUIDITY", sc["A"]),
                cell("B \u00b7 BOND BOOK", sc["B"]),
                cell("C \u00b7 NI Q/Q", sc["C"]),
                comp,
                rank,
            ]
        ],
        colWidths=[1.25 * inch] * 5,
    )
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(row)
    story.append(Spacer(1, 4))
    story.append(
        Paragraph(
            "Scores are 0\u2013100 percentiles vs. the full universe (higher = larger opportunity).",
            st["small"],
        )
    )


def _bullets(st, items):
    return [Paragraph(f"\u2022&nbsp;&nbsp;{it}", st["bullet"]) for it in (items or [])]


def _facts_table(st, facts):
    items = facts.get("snapshot_table") or []
    if not items:
        return None
    data = []
    for i in range(0, len(items), 2):
        left = items[i]
        right = items[i + 1] if i + 1 < len(items) else {"label": "", "value": ""}
        data.append(
            [
                Paragraph(left["label"], st["small"]),
                Paragraph(f"<b>{left['value']}</b>", st["small"]),
                Paragraph(right["label"], st["small"]),
                Paragraph(
                    f"<b>{right['value']}</b>" if right["label"] else "", st["small"]
                ),
            ]
        )
    t = Table(data, colWidths=[1.7 * inch, 1.0 * inch, 1.7 * inch, 1.0 * inch])
    t.setStyle(
        TableStyle(
            [
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, SOFT]),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINE),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def _trend_table(st, trend):
    if not trend or not trend.get("quarters"):
        return None
    quarters = list(reversed(trend["quarters"]))
    data = [
        [Paragraph("<b>Metric</b>", st["small"])]
        + [Paragraph(f"<b>{q}</b>", st["small"]) for q in quarters]
    ]
    for row in trend["rows"]:
        vals = list(reversed(row["values"]))
        cells = [Paragraph(row["label"], st["small"])]
        for v in vals:
            cells.append(Paragraph(str(v) if v is not None else "n/a", st["small"]))
        data.append(cells)
    ncol = len(quarters)
    w0 = 1.9 * inch
    wq = (7.0 * inch - w0) / max(ncol, 1)
    t = Table(data, colWidths=[w0] + [wq] * ncol)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), SOFT),
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, LINE),
                ("LINEBELOW", (0, 1), (-1, -2), 0.3, LINE),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
            ]
        )
    )
    return t


def build_pdf(facts, narrative, trend=None, show_rep=True):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        topMargin=0.5 * inch,
        bottomMargin=0.55 * inch,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        title=f"Call Prep - {facts['bank']} {facts['as_of']}",
        author="SouthState Securities",
    )
    st = _styles()
    story = []
    _header(story, st, facts, show_rep)
    story.append(Paragraph(facts["bank"], st["h1"]))
    story.append(Paragraph(_identity_line(facts), st["sub"]))
    _kpi_strip(story, st, facts)
    material = facts.get("has_material_opportunity")
    tag = (
        "MATERIAL OPPORTUNITY"
        if material
        else "RELATIONSHIP CALL \u2014 NO ACTIONABLE TRADE THIS QUARTER"
    )
    tagbg = GOLD if material else SOFT
    tagfg = "#3A2B06" if material else "#5B6982"
    banner = Table(
        [
            [
                Paragraph(
                    f"<font color='{tagfg}'><b>{tag}</b></font>",
                    ParagraphStyle(
                        "b", fontName="Helvetica-Bold", fontSize=9, leading=12
                    ),
                )
            ]
        ],
        colWidths=[7.0 * inch],
    )
    banner.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), tagbg),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.append(Spacer(1, 8))
    story.append(banner)
    story.append(Spacer(1, 6))
    story.append(Paragraph(narrative.get("headline", ""), st["headline"]))
    story.append(Spacer(1, 3))
    story.append(Paragraph(narrative.get("opportunity_assessment", ""), st["body"]))

    def section(heading, flows):
        flows = [f for f in flows if f is not None]
        if not flows:
            return
        story.append(KeepTogether([Paragraph(heading, st["sec"])] + flows))

    section(
        "The read \u2014 what the numbers say, in plain English",
        _bullets(st, narrative.get("the_read") or narrative.get("sharp_read")),
    )
    section(
        "Verified figures (traceable to the call report)", [_facts_table(st, facts)]
    )
    if trend and trend.get("quarters") and len(trend["quarters"]) > 1:
        section(f"How it\u2019s trending ({len(trend['quarters'])}-quarter view)", [_trend_table(st, trend)])
    section(
        "Conversation starters (relationship-first)",
        _bullets(st, narrative.get("conversation_starters")),
    )
    section("Discovery questions", _bullets(st, narrative.get("discovery_questions")))
    objs = narrative.get("objections") or []
    if objs:
        of = []
        for o in objs:
            of.append(Paragraph(f"\u201c{o.get('objection','')}\u201d", st["obj"]))
            of.append(Paragraph(f"\u2192&nbsp;{o.get('response','')}", st["bullet"]))
            of.append(Spacer(1, 2))
        section("Likely objections &amp; responses", of)
    if narrative.get("watch_for"):
        section("What to watch for", _bullets(st, narrative.get("watch_for")))
    if narrative.get("what_not_to_say"):
        section("What NOT to say", _bullets(st, narrative.get("what_not_to_say")))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.8, color=LINE, spaceAfter=4))
    comp = narrative.get(
        "compliance_note",
        "Internal analytical aid only \u2014 not investment advice or a solicitation. Any idea here should fit the institution\u2019s objectives and pass suitability review before action.",
    )
    src_key = narrative.get("_source", "fallback")
    src = (
        f"Narrative generated by the built-in engine. [{narrative.get('_reason','AI not active')}]"
        if src_key == "fallback"
        else f"Narrative generated by {src_key} ({narrative.get('_model','')})."
    )
    story.append(
        Paragraph(
            f"<b>Compliance:</b> {comp}  Figures are from SNL/Capital IQ call-report data, traceable to the FFIEC filing via the identifiers above. {src} For internal SouthState Securities use.",
            st["small"],
        )
    )
    doc.build(story)
    return buf.getvalue()
