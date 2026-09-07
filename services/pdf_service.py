"""
=============================================================
PDF Export Service
=============================================================
Day 4  |  Part 4D

Generates a professional PDF of the full travel itinerary
using ReportLab.

Sub-parts:
  4D-i   Page setup, styles, and colour palette
  4D-ii  Cover page (destination, dates, traveler info)
  4D-iii Trip overview + budget summary table
  4D-iv  Day-by-day pages (morning / afternoon / evening)
  4D-v   Packing list + important tips page
  4D-vi  generate_pdf() — main public function
=============================================================
"""

import io
from datetime import datetime

from reportlab.lib               import colors
from reportlab.lib.pagesizes     import A4
from reportlab.lib.styles        import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units         import cm, mm
from reportlab.lib.enums         import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus          import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether,
)
from reportlab.pdfgen            import canvas as rl_canvas

from utils.helpers import format_currency


# =============================================================
# SUB-PART 4D-i  |  COLOUR PALETTE & STYLES
# =============================================================

# Brand colours
PRIMARY   = colors.HexColor("#667eea")
SECONDARY = colors.HexColor("#764ba2")
DARK      = colors.HexColor("#2d3748")
MID_GREY  = colors.HexColor("#718096")
LIGHT_BG  = colors.HexColor("#f8f9ff")
MORNING   = colors.HexColor("#4facfe")
AFTERNOON = colors.HexColor("#f093fb")
EVENING   = colors.HexColor("#764ba2")
SUCCESS   = colors.HexColor("#38a169")
WARNING   = colors.HexColor("#d69e2e")
ERROR     = colors.HexColor("#e53e3e")

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm


def _build_styles():
    """Build and return all custom paragraph styles."""
    base = getSampleStyleSheet()

    styles = {
        "cover_title": ParagraphStyle(
            "cover_title",
            fontSize=32,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            spaceAfter=6,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            fontSize=14,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName="Helvetica",
            spaceAfter=4,
            leading=20,
        ),
        "section_title": ParagraphStyle(
            "section_title",
            fontSize=16,
            textColor=colors.white,
            fontName="Helvetica-Bold",
            alignment=TA_LEFT,
            spaceAfter=4,
            spaceBefore=4,
        ),
        "day_title": ParagraphStyle(
            "day_title",
            fontSize=13,
            textColor=colors.white,
            fontName="Helvetica-Bold",
            alignment=TA_LEFT,
            spaceAfter=2,
        ),
        "slot_title": ParagraphStyle(
            "slot_title",
            fontSize=10,
            textColor=colors.white,
            fontName="Helvetica-Bold",
            alignment=TA_LEFT,
            spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "body",
            fontSize=9,
            textColor=DARK,
            fontName="Helvetica",
            leading=14,
            spaceAfter=3,
        ),
        "body_bold": ParagraphStyle(
            "body_bold",
            fontSize=9,
            textColor=DARK,
            fontName="Helvetica-Bold",
            leading=14,
            spaceAfter=2,
        ),
        "small": ParagraphStyle(
            "small",
            fontSize=8,
            textColor=MID_GREY,
            fontName="Helvetica",
            leading=12,
            spaceAfter=2,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontSize=9,
            textColor=DARK,
            fontName="Helvetica",
            leading=14,
            leftIndent=12,
            spaceAfter=2,
        ),
        "tip": ParagraphStyle(
            "tip",
            fontSize=9,
            textColor=colors.HexColor("#1a6e3c"),
            fontName="Helvetica",
            leading=13,
            leftIndent=12,
            spaceAfter=2,
        ),
        "cost": ParagraphStyle(
            "cost",
            fontSize=9,
            textColor=PRIMARY,
            fontName="Helvetica-Bold",
            alignment=TA_RIGHT,
            spaceAfter=0,
        ),
    }
    return styles


# =============================================================
# SUB-PART 4D-vi  |  MAIN PUBLIC FUNCTION
# =============================================================

def generate_pdf(itinerary: dict, user_inputs: dict) -> bytes:
    """
    Generate a professional A4 PDF for the travel itinerary.

    Args:
        itinerary  : The generated itinerary dict.
        user_inputs: User's original form preferences.

    Returns:
        PDF file as bytes — ready for st.download_button().
    """
    buffer = io.BytesIO()
    currency = user_inputs.get("currency", "INR")
    styles   = _build_styles()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title=f"Travel Itinerary — {user_inputs.get('destination', 'Trip')}",
        author="AI Travel Planner",
        subject="Personalized Travel Itinerary",
    )

    story = []

    # ── Build each section ────────────────────────────────────
    _add_cover(story, itinerary, user_inputs, styles, currency)
    story.append(PageBreak())

    _add_overview(story, itinerary, user_inputs, styles, currency)
    story.append(PageBreak())

    for day_data in itinerary.get("days", []):
        _add_day_page(story, day_data, styles, currency)
        story.append(PageBreak())

    _add_packing_and_tips(story, itinerary, styles)

    doc.build(
        story,
        onFirstPage=_add_page_footer,
        onLaterPages=_add_page_footer,
    )

    buffer.seek(0)
    return buffer.read()


# =============================================================
# SUB-PART 4D-ii  |  COVER PAGE
# =============================================================

def _add_cover(story, itinerary, user_inputs, styles, currency):
    """Add a gradient-style cover page."""

    summary     = itinerary.get("trip_summary", {})
    destination = summary.get("destination", user_inputs.get("destination", ""))
    start_date  = summary.get("start_date",   user_inputs.get("start_date", ""))
    end_date    = summary.get("end_date",      "")
    duration    = summary.get("duration_days", user_inputs.get("num_days", 0))
    travelers   = summary.get("num_travelers", user_inputs.get("num_travelers", 1))
    budget      = summary.get("total_budget",  user_inputs.get("budget", 0))
    style       = summary.get("travel_style",  user_inputs.get("travel_style", ""))

    # Full-width purple gradient header block (simulated with a coloured table)
    cover_data = [
        [Paragraph("✈  AI Travel Planner", styles["cover_sub"])],
        [Paragraph(destination, styles["cover_title"])],
        [Spacer(1, 6)],
        [Paragraph(
            f"{start_date}  →  {end_date}  |  {duration} Days  |  {travelers} Traveler{'s' if travelers > 1 else ''}",
            styles["cover_sub"],
        )],
        [Paragraph(
            f"{style} Trip  |  Budget: {format_currency(budget, currency)}",
            styles["cover_sub"],
        )],
    ]

    cover_table = Table(
        cover_data,
        colWidths=[PAGE_W - 2 * MARGIN],
    )
    cover_table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), PRIMARY),
        ("TOPPADDING",  (0, 0), (-1, -1), 20),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 0.6 * cm))

    # Overview text
    overview = summary.get("overview", "")
    if overview:
        story.append(Paragraph("About This Trip", styles["body_bold"]))
        story.append(Paragraph(overview, styles["body"]))
        story.append(Spacer(1, 0.4 * cm))

    # Quick info table
    interests    = user_inputs.get("interests", [])
    food_prefs   = user_inputs.get("food_preferences", [])
    accommodation = summary.get("accommodation_type", user_inputs.get("accommodation", ""))
    transport    = summary.get("transportation_mode", user_inputs.get("transportation", ""))

    info_rows = [
        ["📍 Destination",   destination,
         "📅 Duration",      f"{duration} days"],
        ["👥 Travelers",     str(travelers),
         "💰 Total Budget",  format_currency(budget, currency)],
        ["🎒 Travel Style",  style,
         "🏨 Accommodation", accommodation],
        ["🚗 Transport",     transport,
         "🍽️ Food Pref",   ", ".join(food_prefs) if food_prefs else "All"],
        ["🎯 Interests",
         ", ".join(interests[:4]) if interests else "General",
         "📆 Generated",
         datetime.now().strftime("%d %b %Y")],
    ]

    flat = [[Paragraph(str(c), styles["body_bold"] if i % 2 == 0 else styles["body"])
             for i, c in enumerate(row)] for row in info_rows]

    info_table = Table(flat, colWidths=[3.5 * cm, 5.5 * cm, 3.5 * cm, 5.5 * cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_BG),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT_BG]),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.5 * cm))

    # Branding footer for cover
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0")))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "Generated by AI Travel Planner  ·  Powered by Google Gemini AI  ·  Gen AI & Prompt Engineering Project",
        ParagraphStyle("foot", fontSize=7, textColor=MID_GREY, alignment=TA_CENTER),
    ))


# =============================================================
# SUB-PART 4D-iii  |  TRIP OVERVIEW + BUDGET TABLE
# =============================================================

def _add_overview(story, itinerary, user_inputs, styles, currency):
    """Add the budget summary and day overview page."""

    # Section header
    _section_header(story, "💰  Budget Summary", styles)
    story.append(Spacer(1, 0.3 * cm))

    bd = itinerary.get("budget_breakdown", {})
    user_budget = user_inputs.get("budget", 0)
    estimated   = float(bd.get("total_estimated", 0))
    diff        = user_budget - estimated
    status      = "Under Budget" if diff >= 0 else "Over Budget"
    status_color = SUCCESS if diff >= 0 else ERROR

    # Budget table
    budget_rows = [
        ["Category", "Estimated Cost"],
        ["🏨  Accommodation",     format_currency(float(bd.get("accommodation",          0)), currency)],
        ["🍽️  Food & Dining",    format_currency(float(bd.get("food",                    0)), currency)],
        ["🚗  Transportation",    format_currency(float(bd.get("transportation",          0)), currency)],
        ["🎟️  Activities & Entry",format_currency(float(bd.get("activities_entry_fees",  0)), currency)],
        ["🛍️  Shopping & Misc",  format_currency(float(bd.get("shopping_misc",           0)), currency)],
        ["📊  TOTAL ESTIMATED",   format_currency(estimated, currency)],
        ["💳  YOUR BUDGET",       format_currency(user_budget, currency)],
        [status,                  format_currency(abs(diff), currency)],
    ]

    flat_budget = []
    for i, row in enumerate(budget_rows):
        if i == 0:
            flat_budget.append([
                Paragraph(c, styles["body_bold"]) for c in row
            ])
        elif i >= 6:
            flat_budget.append([
                Paragraph(row[0], styles["body_bold"]),
                Paragraph(row[1], styles["cost"]),
            ])
        else:
            flat_budget.append([
                Paragraph(row[0], styles["body"]),
                Paragraph(row[1], styles["cost"]),
            ])

    budget_table = Table(flat_budget, colWidths=[10 * cm, 8 * cm])
    budget_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  PRIMARY),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, 5), [colors.white, LIGHT_BG]),
        ("BACKGROUND",   (0, 6), (-1, 6),  colors.HexColor("#f0f4ff")),
        ("BACKGROUND",   (0, 7), (-1, 7),  colors.HexColor("#eef2ff")),
        ("BACKGROUND",   (0, 8), (-1, 8),  colors.HexColor("#e6ffed") if diff >= 0 else colors.HexColor("#ffe4e6")),
        ("TEXTCOLOR",    (0, 8), (-1, 8),  status_color),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING",   (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 7),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("FONTNAME",     (0, 6), (-1, 8),  "Helvetica-Bold"),
    ]))
    story.append(budget_table)
    story.append(Spacer(1, 0.6 * cm))

    # Day overview table
    _section_header(story, "📅  Trip Overview", styles)
    story.append(Spacer(1, 0.3 * cm))

    day_rows = [["Day", "Date", "Main Highlights", "Est. Cost"]]
    for day in itinerary.get("days", []):
        morning_attr   = day.get("morning",   {}).get("attraction", "")
        afternoon_attr = day.get("afternoon", {}).get("attraction", "")
        highlights     = "  |  ".join(filter(None, [morning_attr, afternoon_attr]))
        day_rows.append([
            f"Day {day.get('day', '')}",
            day.get("date", ""),
            highlights or "—",
            format_currency(float(day.get("day_total_cost", 0)), currency),
        ])

    flat_days = []
    for i, row in enumerate(day_rows):
        st_body = styles["body_bold"] if i == 0 else styles["body"]
        flat_days.append([Paragraph(str(c), st_body) for c in row])

    day_ov_table = Table(flat_days, colWidths=[2 * cm, 4.5 * cm, 10 * cm, 2.5 * cm])
    day_ov_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  PRIMARY),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    story.append(day_ov_table)


# =============================================================
# SUB-PART 4D-iv  |  DAY PAGE
# =============================================================

def _add_day_page(story, day_data: dict, styles, currency: str):
    """Add a full page for one day of the itinerary."""

    day_num  = day_data.get("day", 0)
    day_date = day_data.get("date", f"Day {day_num}")
    day_cost = float(day_data.get("day_total_cost", 0))
    day_tips = day_data.get("tips", [])

    # Day header row
    header_data = [[
        Paragraph(f"Day {day_num}", styles["day_title"]),
        Paragraph(day_date, styles["cover_sub"]),
        Paragraph(f"Est. {format_currency(day_cost, currency)}", styles["day_title"]),
    ]]
    hdr_table = Table(header_data, colWidths=[3 * cm, 10 * cm, 5 * cm])
    hdr_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), PRIMARY),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("ALIGN",         (2, 0), (2, 0),   "RIGHT"),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(hdr_table)
    story.append(Spacer(1, 0.4 * cm))

    # Three time slots
    slot_configs = [
        ("morning",   "🌅  Morning",   MORNING),
        ("afternoon", "🌞  Afternoon", AFTERNOON),
        ("evening",   "🌙  Evening",   EVENING),
    ]

    for slot_key, slot_label, slot_color in slot_configs:
        slot = day_data.get(slot_key, {})
        if not slot:
            continue

        slot_cost  = float(slot.get("estimated_cost", 0))
        time_range = slot.get("time", "")
        attraction = slot.get("attraction", "")
        activities = slot.get("activities", [])
        food       = slot.get("food", "")
        transport  = slot.get("transport", "")
        notes      = slot.get("notes", "")

        # Slot header
        slot_hdr = Table(
            [[
                Paragraph(slot_label, styles["slot_title"]),
                Paragraph(f"{format_currency(slot_cost, currency)}", styles["slot_title"]),
            ]],
            colWidths=[13 * cm, 5 * cm],
        )
        slot_hdr.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), slot_color),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
            ("ALIGN",         (1, 0), (1, 0),   "RIGHT"),
        ]))

        # Slot body content
        slot_content = []
        if time_range:
            slot_content.append(Paragraph(f"🕐 {time_range}", styles["small"]))
        if attraction:
            slot_content.append(Paragraph(f"📍 {attraction}", styles["body_bold"]))
        for act in activities:
            slot_content.append(Paragraph(f"• {act}", styles["bullet"]))
        if food:
            slot_content.append(Paragraph(f"🍽️ {food}", styles["body"]))
        if transport:
            slot_content.append(Paragraph(f"🚗 {transport}", styles["small"]))
        if notes:
            slot_content.append(Paragraph(f"💡 {notes}", styles["tip"]))

        body_table = Table(
            [[c] for c in slot_content],
            colWidths=[PAGE_W - 2 * MARGIN],
        )
        body_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), colors.white),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING",   (0, 0), (-1, -1), 12),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
            ("GRID",          (0, 0), (-1, -1), 0.3, colors.HexColor("#f0f0f0")),
        ]))

        story.append(KeepTogether([slot_hdr, body_table, Spacer(1, 0.25 * cm)]))

    # Day tips
    if day_tips:
        story.append(Spacer(1, 0.2 * cm))
        story.append(Paragraph("💡 Tips for Today", styles["body_bold"]))
        for tip in day_tips:
            story.append(Paragraph(f"  • {tip}", styles["tip"]))


# =============================================================
# SUB-PART 4D-v  |  PACKING LIST + IMPORTANT TIPS PAGE
# =============================================================

def _add_packing_and_tips(story, itinerary: dict, styles):
    """Add the packing list and important tips as the final page."""

    _section_header(story, "🎒  Packing List", styles)
    story.append(Spacer(1, 0.3 * cm))

    packing = itinerary.get("packing_list", [])
    if packing:
        # Two-column packing list
        mid  = (len(packing) + 1) // 2
        col1 = packing[:mid]
        col2 = packing[mid:]

        max_rows = max(len(col1), len(col2))
        rows = []
        for i in range(max_rows):
            left_item  = f"☑  {col1[i]}" if i < len(col1) else ""
            right_item = f"☑  {col2[i]}" if i < len(col2) else ""
            rows.append([
                Paragraph(left_item,  styles["body"]),
                Paragraph(right_item, styles["body"]),
            ])

        pack_table = Table(rows, colWidths=[9 * cm, 9 * cm])
        pack_table.setStyle(TableStyle([
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT_BG]),
            ("GRID",           (0, 0), (-1, -1), 0.3, colors.HexColor("#e2e8f0")),
            ("TOPPADDING",     (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING",  (0, 0), (-1, -1), 6),
            ("LEFTPADDING",    (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",   (0, 0), (-1, -1), 10),
        ]))
        story.append(pack_table)
    else:
        story.append(Paragraph("No packing list generated.", styles["body"]))

    story.append(Spacer(1, 0.6 * cm))

    _section_header(story, "📌  Important Tips", styles)
    story.append(Spacer(1, 0.3 * cm))

    tips = itinerary.get("important_tips", [])
    if tips:
        for i, tip in enumerate(tips, 1):
            story.append(Paragraph(f"{i}.  {tip}", styles["tip"]))
            story.append(Spacer(1, 0.1 * cm))
    else:
        story.append(Paragraph("No tips generated.", styles["body"]))

    story.append(Spacer(1, 0.6 * cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0")))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "Safe travels! Generated by AI Travel Planner  ·  Powered by Google Gemini AI",
        ParagraphStyle("end", fontSize=8, textColor=MID_GREY, alignment=TA_CENTER),
    ))


# =============================================================
# HELPERS
# =============================================================

def _section_header(story, title: str, styles):
    """Add a section header bar."""
    hdr = Table(
        [[Paragraph(title, styles["section_title"])]],
        colWidths=[PAGE_W - 2 * MARGIN],
    )
    hdr.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), SECONDARY),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(hdr)


def _add_page_footer(canvas_obj, doc):
    """Draw page number and branding footer on every page."""
    canvas_obj.saveState()
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.setFillColor(MID_GREY)

    footer_text = "AI Travel Planner  ·  Powered by Google Gemini AI"
    canvas_obj.drawString(MARGIN, 0.8 * cm, footer_text)

    page_num = f"Page {doc.page}"
    canvas_obj.drawRightString(PAGE_W - MARGIN, 0.8 * cm, page_num)

    # Thin line above footer
    canvas_obj.setStrokeColor(colors.HexColor("#e2e8f0"))
    canvas_obj.line(MARGIN, 1.0 * cm, PAGE_W - MARGIN, 1.0 * cm)

    canvas_obj.restoreState()
