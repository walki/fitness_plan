"""Generate printable weekly plan PDF for Week of Aug 31 - Sep 6 (BUILD 1, Wk 1 -- Re-entry).

Single page, B&W laser printer friendly (light gray headers, bold black text).
August was an offseason from structure. New shape: build 3 / recover 1 / build 3,
no race on the calendar, no 5K TT -- speed work is effort-based and the repeated
sessions are the test data.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER
import sys


def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=0.32 * inch,
        bottomMargin=0.28 * inch,
        leftMargin=0.45 * inch,
        rightMargin=0.45 * inch,
    )

    styles = getSampleStyleSheet()

    HEADER_BG = HexColor("#dddddd")
    ROW_ALT = HexColor("#f0f0f0")
    BOX_BG = HexColor("#f5f5f5")
    BORDER = HexColor("#888888")

    title_style = ParagraphStyle(
        "Title2", parent=styles["Title"], fontSize=14, spaceAfter=1,
        textColor=HexColor("#000000"),
    )
    subtitle_style = ParagraphStyle(
        "Subtitle2", parent=styles["Normal"], fontSize=9,
        textColor=HexColor("#333333"), spaceAfter=4, alignment=TA_CENTER,
    )
    section_style = ParagraphStyle(
        "Section", parent=styles["Heading2"], fontSize=10,
        spaceBefore=5, spaceAfter=2, textColor=HexColor("#000000"),
    )
    small_style = ParagraphStyle(
        "Small", parent=styles["Normal"], fontSize=8.3, leading=10, spaceAfter=1,
    )
    bold_small = ParagraphStyle("BoldSmall", parent=small_style, fontName="Helvetica-Bold")
    header_text = ParagraphStyle("HeaderText", parent=bold_small, textColor=HexColor("#000000"))
    lift_style = ParagraphStyle("Lift", parent=styles["Normal"], fontSize=7.9, leading=9.4)
    tiny_style = ParagraphStyle(
        "Tiny", parent=styles["Normal"], fontSize=7.5, leading=9,
        textColor=HexColor("#555555"),
    )

    def box(cells, widths):
        t = Table([cells], colWidths=widths)
        t.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("BACKGROUND", (0, 0), (-1, -1), BOX_BG),
        ]))
        return t

    story = []

    # ==================== HEADER ====================
    story.append(Paragraph("Week of Aug 31 - Sep 6  |  BUILD 1, Wk 1 -- RE-ENTRY", title_style))
    story.append(Paragraph(
        "August was an offseason -- that is over, not audited. New shape: <b>build 3 / recover 1 / build 3</b>, "
        "no race on the calendar, no 5K TT. One <b>effort-based speed touch per week</b>; the repeated sessions "
        "ARE the test data. This week: get run frequency back at genuinely easy effort.",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#000000")))
    story.append(Spacer(1, 3))

    # ==================== DAILY SCHEDULE ====================
    story.append(Paragraph("DAILY SCHEDULE", section_style))

    schedule_rows = [
        ("Mon Aug 31", "DONE -- Zwift Z2 35:46 (153W NP, HR 125) + Upper Pull + Arms 25:23 + rehab. Ahead of plan.", False),
        ("Tue Sep 1", "Easy run 3 mi. HR under 135, conversational. Deliberately slow -- first run in 9 days.", False),
        ("Wed Sep 2", "UPPER PUSH strength (see below) + easy Z2 spin 45-60 min if you want it.", True),
        ("Thu Sep 3", "Easy run 3.5 mi + 4-6 x 20s STRIDES.  &lt;-- the week's speed touch.", True),
        ("Fri Sep 4", "Rest or easy spin. Nothing that needs legs.", False),
        ("Sat Sep 5", "Ride -- distance and route by feel. Whatever the day wants.", False),
        ("Sun Sep 6", "Easy run 4-5 mi + FULL BODY LOWER strength (see below).", True),
    ]

    schedule_data = [[Paragraph("<b>Day</b>", header_text), Paragraph("<b>Session</b>", header_text)]]
    for day, sess, highlight in schedule_rows:
        s = bold_small if highlight else small_style
        schedule_data.append([Paragraph(day, s), Paragraph(sess, s)])

    schedule_table = Table(schedule_data, colWidths=[1.0 * inch, 6.1 * inch])
    schedule_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), black),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#ffffff"), ROW_ALT]),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(schedule_table)

    # ============ QUALITY SESSION + BLOCK FRAME ============
    story.append(Spacer(1, 3))
    story.append(box([
        Paragraph(
            "<b>THE SPEED TOUCH -- STRIDES (Thu)</b><br/>"
            "Off the back of the easy 3.5. <b>4-6 x 20 seconds</b> relaxed-fast -- not a sprint, about mile-race "
            "effort with loose shoulders and quick feet. <b>Walk or jog until fully recovered</b> between each "
            "(45-90s). Neuromuscular only; it should cost you nothing. The point after 9 days off is to remind "
            "the legs how to turn over before real speed work starts next week.",
            small_style,
        ),
        Paragraph(
            "<b>BLOCK FRAME -- 7 WEEKS, NO RACE</b><br/>"
            "Wk1 strides | Wk2 fartlek 6x1min | Wk3 strides | <b>Wk4 recovery</b> | Wk5 5x2min @10K effort | "
            "Wk6 20min cruise | <b>Wk7 repeat the Wk2 fartlek</b>. That last one is the trick -- same session six "
            "weeks apart, and the pace/HR comparison tells us what a TT would have, without running one. "
            "Long run 5 -&gt; 6 -&gt; 7 -&gt; 8 -&gt; 9 mi. <b>20-min FTP test lands in Block 2.</b>",
            small_style,
        ),
    ], [3.55 * inch, 3.55 * inch]))

    # ==================== STRENGTH ====================
    story.append(Paragraph("STRENGTH -- 2 sessions this week (loads from your last logged session)", section_style))
    story.append(box([
        Paragraph(
            "<b>WED -- UPPER PUSH + ARMS</b><br/>"
            "Push-up &mdash; 3 x 12<br/>"
            "DB shoulder press &mdash; 3 x 10 @ 20 lb<br/>"
            "DB bicep curl &mdash; 3 x 10 @ 20 lb<br/>"
            "DB triceps extension &mdash; 3 x 10 @ 20 lb<br/>"
            "Lateral raise &mdash; 3 x 12 @ 10 lb<br/>"
            "<i>Shoulder press has sat at 20 lb a while -- try 25 on set 1 and see. "
            "Load is yours to pick; drop it when form breaks.</i>",
            lift_style,
        ),
        Paragraph(
            "<b>SUN -- FULL BODY LOWER</b><br/>"
            "Goblet squat &mdash; 3 x 10 @ 40 lb<br/>"
            "DB Romanian deadlift &mdash; 3 x 10 @ 40 lb<br/>"
            "<b>Box step-up &mdash; 3 x 10 each side @ 20 lb (LEAD LEFT)</b><br/>"
            "<b>Split squat &mdash; 2 x 8 each side, load by feel</b><br/>"
            "DB bench press &mdash; 3 x 10 @ 30 lb<br/>"
            "<i>Step-ups and split squats have dropped out of the log -- they are the left-quad work. "
            "Put them back.</i>",
            lift_style,
        ),
    ], [3.55 * inch, 3.55 * inch]))

    # ==================== REHAB + NUTRITION ====================
    story.append(Paragraph("REHAB (DAILY) + NUTRITION / WATCH LIST", section_style))
    story.append(box([
        Paragraph(
            "<b>REHAB -- every day, pick what fits:</b><br/>"
            "TKEs &mdash; 3 x 15 each leg, black band<br/>"
            "Iso wrist hold (left) &mdash; 3 x 30s @ 10 lb<br/>"
            "Spanish squat &mdash; 3 x 30s<br/>"
            "Hammer curl &mdash; 3 x 12 @ 15 lb, slow eccentric, left bias<br/>"
            "<b>Elbow just went 10 -&gt; 15 lb with no flare, 8 months out. That arc is working.</b> "
            "Rule holds: pain under 4/10 while loading is fine; higher, or lingering past 24h, back off.",
            small_style,
        ),
        Paragraph(
            "<b>NUTRITION:</b> deficit ~300-400/day, protein <b>150 g</b> (whey scoop is the lever).<br/><br/>"
            "<b>WATCH LIST:</b><br/>"
            "&bull; <b>Calves and achilles.</b> 9 days off running at 56 -- easy means easy. This is the one "
            "thing that could cost weeks.<br/>"
            "&bull; <b>BP -- 2 readings.</b> Zero in four weeks; get the cadence back.<br/>"
            "&bull; <b>Bedtime.</b> Drifted past midnight most of August. Cheapest recovery lever there is.<br/>"
            "&bull; Weight re-anchors at mid-week check-in (MFP is the only source).",
            small_style,
        ),
    ], [3.55 * inch, 3.55 * inch]))

    # Footer
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
    story.append(Paragraph(
        "FTP ~215W working (ramp 229 / intervals 214, Aug 5) | Bike Z2 120-161W, HR 120-134 | Bike LTHR ~150 | "
        "Run easy HR &lt;135 (~10:50-11:10/mi recent) | Fitness CTL 45 | Coach: Claude",
        ParagraphStyle("Footer", parent=tiny_style, alignment=TA_CENTER, textColor=HexColor("#666666")),
    ))

    doc.build(story)
    print("PDF generated: " + output_path)


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plans/2026-08-31-build1-wk1-re-entry.pdf"
    build_pdf(output)
