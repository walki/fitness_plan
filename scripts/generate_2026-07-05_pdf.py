"""Generate printable weekly plan PDF for Week of Jun 29-Jul 5 (BR100 build week 3).

Single page, B&W laser printer friendly (light gray headers, bold black text).
Holiday ride-trip week: ~120 mi flat Z2 Fri/Sat (Columbus <-> Yellow Springs),
strength front-loaded Mon-Thu, Sun run on tired legs.
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
        topMargin=0.35 * inch,
        bottomMargin=0.3 * inch,
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
        spaceBefore=6, spaceAfter=2, textColor=HexColor("#000000"),
    )
    small_style = ParagraphStyle(
        "Small", parent=styles["Normal"], fontSize=8.5, leading=10.5,
        spaceAfter=1,
    )
    bold_small = ParagraphStyle("BoldSmall", parent=small_style, fontName="Helvetica-Bold")
    header_text = ParagraphStyle("HeaderText", parent=bold_small, textColor=HexColor("#000000"))
    tiny_style = ParagraphStyle(
        "Tiny", parent=styles["Normal"], fontSize=7.5, leading=9,
        textColor=HexColor("#555555"),
    )

    story = []

    # ==================== HEADER ====================
    story.append(Paragraph("Week of Jun 29-Jul 5 -- BR100 Build Week 3 of 5", title_style))
    story.append(Paragraph(
        "Last Sun ✓✓ 11.13 mi @ HR 132 w/ 1,038 ft -- distance proven (Leg 8 = 12.3 mi). "
        "Holiday ride trip: ~120 mi flat Z2 Fri/Sat. BR100 Jul 25.",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#000000")))
    story.append(Spacer(1, 3))

    # ==================== DAILY SCHEDULE ====================
    story.append(Paragraph("DAILY SCHEDULE", section_style))

    schedule_rows = [
        ("Mon Jun 29", "Recovery from the 11-miler. Walk or rest + core micro + TKEs + wrist hold.", False),
        ("Tue Jun 30", "Easy run 3-4 mi, HR <140 + Upper Push (~20 min). Rehab.", True),
        ("Wed Jul 1", "Strength Full Body Lower (~35 min) + optional easy spin 30-45 min. Rehab.", False),
        ("Thu Jul 2", "Easy run 3 mi + Upper Pull (~20 min). Rehab. Drive to Columbus PM.", True),
        ("Fri Jul 3", "RIDE Columbus -> Yellow Springs, ~60 mi flat Z2, light gear. Fuel + hydrate.", True),
        ("Sat Jul 4", "RIDE Yellow Springs -> Columbus, ~60 mi flat Z2. Back-to-back endurance.", True),
        ("Sun Jul 5", "RUN ON tired legs -- 7-9 mi by feel, HR <145. Run-off-the-bike. NOT a distance push.", True),
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

    # ==================== WEEKEND RIDE TRIP ====================
    story.append(Paragraph("WEEKEND RIDE TRIP -- Columbus <-> Yellow Springs (~120 mi total)", section_style))
    story.append(Paragraph(
        "~60 mi each way, mostly flat, <b>light gear (&lt;10 lb -- extra kit + casual clothes, NOT loaded bikepacking)</b>. "
        "~3.5-4 hrs each at Z2 (HR 120-134, 129-172W). Two big aerobic days back-to-back -- the real training value of the week. "
        "<b>Fuel ~50-70 g carbs/hr</b> (Tailwind + SiS -- lighter than race intensity, but don't run empty day 1 and pay day 2). "
        "<b>Hydrate hard</b> (July heat, ~2L sweat/day expected). <b>Fri night:</b> protein + carbs at the Airbnb -- real meal, sets up Sat + Sun. "
        "<b>Don't hold a deficit Fri/Sat</b> -- these are 2,600-3,000+ cal days. Fuel and recover; trend resumes next week.",
        small_style,
    ))

    # ==================== SUN RUN ON TIRED LEGS ====================
    story.append(Paragraph("SUN RUN -- on tired legs (run-off-the-bike durability)", section_style))
    story.append(Paragraph(
        "After ~120 mi of riding, legs will be depleted and fatigued -- <b>that's the point.</b> BR100 Leg 8 is the anchor leg, "
        "run on a body that's already worked. <b>7-9 mi by feel, HR &lt;145.</b> If legs are genuinely cooked, 5-6 mi easy is a win -- no ego. "
        "Pace will be slow; HR cap is the constraint. Light fuel before + Tailwind/gel if it goes past ~70 min.",
        small_style,
    ))

    # ==================== STRENGTH ====================
    story.append(Paragraph("STRENGTH -- 3 sessions front-loaded (Tue Push / Wed Lower / Thu Pull)", section_style))
    strength_data = [
        [
            Paragraph(
                "<b>TUE -- Upper Push (~20 min)</b><br/>"
                "Push-ups 3x12-15<br/>"
                "DB shoulder press 3x10<br/>"
                "&nbsp;&nbsp;(push for 25x2 clean, then 25x3)<br/>"
                "DB curl 3x10<br/>"
                "Overhead tricep ext 3x10 @ 20-25 lb<br/>"
                "Lateral raise 3x12 @ 15 lb",
                small_style,
            ),
            Paragraph(
                "<b>WED -- Full Body Lower (~35 min)</b><br/>"
                "Spanish squat 3x30s+ (band)<br/>"
                "Goblet squat 3x8 @ 40 lb<br/>"
                "DB RDL 3x8-10 @ 40 lb each<br/>"
                "Box step-ups 3x10 @ 25 lb, LEAD LEFT<br/>"
                "Bench press 3x8-10 @ 30 lb (test 40 if fresh)<br/>"
                "CS row 3x10 @ 30 lb<br/>"
                "Plank 2x60s + side plank 2x30s each",
                small_style,
            ),
            Paragraph(
                "<b>THU -- Upper Pull (~20 min)</b><br/>"
                "<i>(before driving to Columbus)</i><br/>"
                "Chest-supported DB row 3x10 @ 30 lb<br/>"
                "Reverse flye 3x12 @ 15 lb<br/>"
                "Slow eccentric hammer curl 3x10 @ 15 lb<br/>"
                "Tricep dips 3x10<br/>"
                "Plank-to-shoulder-tap 2x20 taps",
                small_style,
            ),
        ],
    ]
    strength_table = Table(strength_data, colWidths=[2.37 * inch, 2.37 * inch, 2.37 * inch])
    strength_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, -1), BOX_BG),
    ]))
    story.append(strength_table)

    # ==================== REHAB DAILY ====================
    story.append(Paragraph("REHAB DAILY", section_style))
    rehab_data = [
        [
            Paragraph(
                "<b>TKEs</b> -- 3x15 each leg with band. Knee to full lockout, 1s hold, slow return. "
                "Building the left quad -- this is construction, not injury care.",
                small_style,
            ),
            Paragraph(
                "<b>Iso wrist hold (left elbow)</b> -- vary load/duration: 10 lb x 30s OR 5-7 lb x 45s+. "
                "Week 6 checkpoint -- combined stimulus trending up.",
                small_style,
            ),
        ],
    ]
    rehab_table = Table(rehab_data, colWidths=[3.55 * inch, 3.55 * inch])
    rehab_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, -1), BOX_BG),
    ]))
    story.append(rehab_table)

    # ==================== NUTRITION ====================
    story.append(Paragraph("NUTRITION -- WEIGHT LOSS MODE (except the ride weekend)", section_style))
    nutri_data = [
        [
            Paragraph(
                "<b>Daily targets:</b><br/>"
                "Cal: 2,000-2,300 Mon-Thu / <b>2,600-3,000+ Fri-Sat ride days</b><br/>"
                "<b>Protein 150g/day</b> -- whey scoop daily<br/>"
                "Net deficit ~250-400 cal/day Mon-Thu<br/>"
                "<b>Break even or surplus Fri/Sat -- fuel, don't deficit</b>",
                small_style,
            ),
            Paragraph(
                "<b>Ride weekend fueling:</b><br/>"
                "On-bike: 50-70 g carbs/hr (Tailwind + SiS)<br/>"
                "Hydrate hard -- July heat, 2 long days<br/>"
                "Fri night: protein + carbs, real meal<br/>"
                "<b>Scale will blip up after -- glycogen + water, not fat. Ignore it.</b>",
                small_style,
            ),
        ],
    ]
    nutri_table = Table(nutri_data, colWidths=[3.55 * inch, 3.55 * inch])
    nutri_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, -1), BOX_BG),
    ]))
    story.append(nutri_table)

    # Footer
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
    story.append(Paragraph(
        "FTP 230W | Z2 power 129-172W / HR 120-134 | LTHR ~150 | Weight ~187 7-day avg | Coach: Claude",
        ParagraphStyle("Footer", parent=tiny_style, alignment=TA_CENTER, textColor=HexColor("#666666")),
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plans/2026-07-05-br100-week-3.pdf"
    build_pdf(output)
