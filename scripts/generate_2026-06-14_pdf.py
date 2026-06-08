"""Generate printable race-week PDF for Week of Jun 8-14 (FBG RACE WEEK).

Single page, B&W laser printer friendly.
Race-week exception: includes race day pacing plan and pre-load protocol.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
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
        topMargin=0.3 * inch,
        bottomMargin=0.25 * inch,
        leftMargin=0.4 * inch,
        rightMargin=0.4 * inch,
    )

    styles = getSampleStyleSheet()

    HEADER_BG = HexColor("#2c3e50")
    ROW_ALT = HexColor("#f0f0f0")
    BOX_BG = HexColor("#f5f5f5")
    BORDER = HexColor("#888888")

    title_style = ParagraphStyle(
        "Title2", parent=styles["Title"], fontSize=14, spaceAfter=1,
        textColor=HexColor("#000000"),
    )
    subtitle_style = ParagraphStyle(
        "Subtitle2", parent=styles["Normal"], fontSize=9,
        textColor=HexColor("#333333"), spaceAfter=3, alignment=TA_CENTER,
    )
    section_style = ParagraphStyle(
        "Section", parent=styles["Heading2"], fontSize=10,
        spaceBefore=5, spaceAfter=2, textColor=HexColor("#000000"),
    )
    small_style = ParagraphStyle(
        "Small", parent=styles["Normal"], fontSize=8.5, leading=10.5,
        spaceAfter=1,
    )
    bold_small = ParagraphStyle("BoldSmall", parent=small_style, fontName="Helvetica-Bold")
    tiny_style = ParagraphStyle(
        "Tiny", parent=styles["Normal"], fontSize=7.5, leading=9,
        textColor=HexColor("#555555"),
    )

    story = []

    # ==================== HEADER ====================
    story.append(Paragraph("RACE WEEK -- FBG Sat Jun 13 -- A RACE", title_style))
    story.append(Paragraph(
        "66.7 mi / 6,186 ft / 15 climbs / 76% unpaved (Mohican). Volume -55% from sharpen. Sleep is input #1. NO alcohol Tue-Fri.",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#000000")))
    story.append(Spacer(1, 3))

    # ==================== DAILY SCHEDULE ====================
    story.append(Paragraph("DAILY SCHEDULE", section_style))

    schedule_rows = [
        ("Mon Jun 8", "Walk + Core + Upper Push ULTRA-LIGHT (1 set/movement, ~10 min). TKEs + wrist hold.", False),
        ("Tue Jun 9", "OPENERS -- 35-40 min Z2 + 3x3 min @ 195W (85% FTP). Leave feeling BETTER not tired.", True),
        ("Wed Jun 10", "Easy run 30 min HR <135 OR easy spin 30 min Z2. Core. Bed by 10:30 PM.", False),
        ("Thu Jun 11", "REST. Walk only if anything. Hydrate. Early bed.", False),
        ("Fri Jun 12", "30 min spin + RACE PRIMER (4x1 min @ 207W / 2x30s @ 230W). PRE-LOAD DAY.", True),
        ("Sat Jun 13", "RACE DAY -- FBG 100k. See plan below.", True),
        ("Sun Jun 14", "Active recovery. Easy walk. Eat well. No structure.", False),
    ]

    schedule_data = [[Paragraph("<b>Day</b>", small_style), Paragraph("<b>Session</b>", small_style)]]
    for day, sess, highlight in schedule_rows:
        s = bold_small if highlight else small_style
        schedule_data.append([Paragraph(day, s), Paragraph(sess, s)])

    schedule_table = Table(schedule_data, colWidths=[1.0 * inch, 6.4 * inch])
    schedule_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, ROW_ALT]),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(schedule_table)

    # ==================== TUE OPENERS + FRI PRIMER ====================
    story.append(Paragraph("KEY WORKOUTS", section_style))
    story.append(Paragraph(
        "<b>TUE OPENERS (~35 min):</b> WU 12-15 min Z2 -> 3x3 min @ 195W (85% FTP) w/ 3 min rest -> CD. "
        "<b>RPE ceiling 7.</b> If it feels like real effort by rep 3, you went too hard. Remind, don't train.",
        small_style,
    ))
    story.append(Paragraph(
        "<b>FRI RACE PRIMER (~30 min):</b> WU 15 min Z2 -> 4x1 min @ 207W (90% FTP) w/ 1 min rest -> "
        "2x30s @ 230W (100% FTP) w/ 90s rest -> CD easy. Sharp, fast, fresh. Leave feeling like you could ride forever.",
        small_style,
    ))

    # ==================== RACE DAY PLAN ====================
    story.append(Paragraph("RACE DAY -- SAT JUN 13 -- PACING BY THIRDS", section_style))

    race_pace_data = [
        [Paragraph(f"<b>{c}</b>", small_style) for c in ["Miles", "Phase", "NP target", "HR ceiling", "Approach"]],
        [Paragraph("0-22", bold_small), Paragraph("DISCIPLINE", bold_small), Paragraph("165-175W (IF 0.72-0.76)", bold_small),
         Paragraph("<b>140</b>", bold_small), Paragraph("Resist surge. Let people pass. Race starts mile 22.", small_style)],
        [Paragraph("22-44", bold_small), Paragraph("RHYTHM", bold_small), Paragraph("175-185W (IF 0.76-0.80)", bold_small),
         Paragraph("145", bold_small), Paragraph("Settle in. Climbs by RPE. Save matches (15 total climbs).", small_style)],
        [Paragraph("44-66", bold_small), Paragraph("COMPETE", bold_small), Paragraph("180-195W (IF 0.78-0.85)", bold_small),
         Paragraph("go", bold_small), Paragraph("Disciplined early = legs here when others aren't. Last 10 mi empty.", small_style)],
    ]
    race_pace_table = Table(race_pace_data, colWidths=[0.5 * inch, 0.85 * inch, 1.6 * inch, 0.7 * inch, 3.75 * inch])
    race_pace_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, ROW_ALT]),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(race_pace_table)

    # ==================== FUELING + PRE-LOAD ====================
    story.append(Paragraph("FUELING + PRE-LOAD (Fri Jun 12)", section_style))
    fuel_data = [
        [
            Paragraph(
                "<b>RACE DAY ON-BIKE (non-negotiable):</b><br/>"
                "<b>80-90 g carbs/hr x 5 hrs = 400-450g total</b><br/>"
                "Carry: 6 SiS gels + 4-5 Tailwind stickpacks (100g+)<br/>"
                "First gel 20 min in, then every 25-30 min (WATCH ALARM)<br/>"
                "Tailwind in every bottle (50g per bottle)<br/>"
                "<b>Aid stations = water + bananas ONLY</b> -- assume nothing else<br/>"
                "Hydration: 1+ bottle/hr; Mortal Hydration mid-race OK",
                small_style,
            ),
            Paragraph(
                "<b>FRI PRE-LOAD DAY:</b><br/>"
                "2,500-2,800 cal / <b>350g+ carbs</b> / 130g protein<br/>"
                "<b>Sodium under 2,500 mg</b> -- NO Chipotle bombs<br/>"
                "<b>NO ALCOHOL</b><br/>"
                "Hydrate aggressively (100+ oz water + LMNT or Tailwind)<br/>"
                "Bed 10 PM<br/>"
                "<br/>"
                "<b>RACE MORNING:</b> 4 eggs + 2 toast + butter + honey + banana 2-3 hrs before. "
                "1 SiS gel 10-15 min before gun.",
                small_style,
            ),
        ],
    ]
    fuel_table = Table(fuel_data, colWidths=[3.7 * inch, 3.7 * inch])
    fuel_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, -1), BOX_BG),
    ]))
    story.append(fuel_table)

    # ==================== EQUIPMENT CHECKLIST + REHAB ====================
    story.append(Paragraph("FRIDAY EQUIPMENT CHECK + DAILY REHAB", section_style))
    equip_data = [
        [
            Paragraph(
                "<b>FRI EQUIPMENT CHECK:</b><br/>"
                "[ ] Grail: drivetrain clean, tires checked, tubeless sealant fresh<br/>"
                "[ ] <b>Power meter battery</b> + HR strap battery (May 25 dropout!)<br/>"
                "[ ] Garmin firmware update check<br/>"
                "[ ] 6 SiS gels + 4-5 Tailwind sticks in jersey pockets<br/>"
                "[ ] 2 bottles pre-mixed (50g Tailwind per bottle)<br/>"
                "[ ] Spare tube + CO2 + multi-tool<br/>"
                "[ ] Chamois cream, helmet, shoes, kit, sunglasses<br/>"
                "[ ] Cash for parking / post-race food, phone (ziplock)",
                small_style,
            ),
            Paragraph(
                "<b>DAILY REHAB (continue through race morning):</b><br/>"
                "TKEs 3x15 each leg with band<br/>"
                "Iso wrist hold left @ 10 lb, 3x30s<br/>"
                "<br/>"
                "<b>MON STRENGTH (ultra-light, ~10 min):</b><br/>"
                "1 set each: push-ups x10, DB press 1x10 @ 20, DB curl 1x10 each @ 20,<br/>"
                "OH tricep ext 1x10 @ 20, lateral raise 1x12 @ 10<br/>"
                "<b>NO STRENGTH AFTER MONDAY.</b> Quads 100% by Friday.",
                small_style,
            ),
        ],
    ]
    equip_table = Table(equip_data, colWidths=[3.7 * inch, 3.7 * inch])
    equip_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, -1), BOX_BG),
    ]))
    story.append(equip_table)

    # ==================== MENTAL APPROACH ====================
    story.append(Paragraph("MENTAL APPROACH", section_style))
    story.append(Paragraph(
        "<b>Mantra: \"Don't burn matches early. Spend them when it matters.\"</b><br/>"
        "Early = stay disciplined; conservation IS the strategy. "
        "Middle = stay steady, eat and drink on schedule, notice climbs without fearing them. "
        "Late = compete; anyone who burned matches early is hurting now, you're not.",
        small_style,
    ))

    # Footer
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
    story.append(Paragraph(
        "FTP 230W | Z2 power 129-172W / HR 120-134 | LTHR ~150 | Weight 187.9 avg | Coach: Claude",
        ParagraphStyle("Footer", parent=tiny_style, alignment=TA_CENTER, textColor=HexColor("#666666")),
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plans/2026-06-14-fbg-race-week.pdf"
    build_pdf(output)
