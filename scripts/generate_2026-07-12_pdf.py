"""Generate printable weekly plan PDF for Week of Jul 6-12 (BR100 build week 4).

Single page, B&W laser printer friendly (light gray headers, bold black text).
Last work week before taper. Unload the ride-block fatigue, rebuild run rhythm,
strength back on track, Sunday = dress-rehearsal long run.
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
    story.append(Paragraph("Week of Jul 6-12 -- BR100 Build Week 4 of 5 (last work week)", title_style))
    story.append(Paragraph(
        "Off a ~170 mi / 4-day heat ride block. Unload early, rebuild run rhythm, strength back on track. "
        "Sun = dress-rehearsal long run. BR100 Leg 8 (12.3 mi) Sat Jul 25.",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#000000")))
    story.append(Spacer(1, 3))

    # ==================== DAILY SCHEDULE ====================
    story.append(Paragraph("DAILY SCHEDULE", section_style))

    schedule_rows = [
        ("Mon Jul 6", "DONE -- ride w/ John 30 mi (4th ride day).", False),
        ("Tue Jul 7", "Recovery. Easy shakeout run 3 mi (HR <140) OR rest + walk. Core + rehab. Keep it truly easy.", False),
        ("Wed Jul 8", "Strength Full Body Lower (~35 min) + rehab. Optional easy spin.", True),
        ("Thu Jul 9", "Easy run 4-5 mi, HR <140 + Upper Push (~20 min). Rehab.", True),
        ("Fri Jul 10", "Easy run 3 mi + Upper Pull (~20 min). Rehab.", True),
        ("Sat Jul 11", "Optional easy Z2 ride 60 min OR rest + core. Legs fresh for Sunday.", False),
        ("Sun Jul 12", "DRESS REHEARSAL LONG RUN -- ~11-12 mi trail w/ climbing (CVNP), HR <145. Full race fueling + pacing.", True),
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

    # ==================== SUN DRESS REHEARSAL ====================
    story.append(Paragraph("SUN DRESS REHEARSAL -- ~11-12 mi trail (the peak session)", section_style))
    story.append(Paragraph(
        "Last big run before taper -- <b>treat it like race day.</b> Leg 8 is 12.3 mi, unpaved, rolling, big climb at mile 7-8. "
        "<b>~11-12 mi on trail w/ real climbing (CVNP, target 800+ ft), HR &lt;145</b> -- walk the steep pitches to hold it (that's the race plan). "
        "<b>Full fueling rehearsal:</b> ~60-70 g carbs/hr (Tailwind + SiS), practice the timing -- last gut check before race day. "
        "<b>Pacing:</b> honest-easy first half, save legs for the mile 7-8 climb, finish strong. Fuel + hydrate before (hot); protein within the hour after.",
        small_style,
    ))

    # ==================== STRENGTH ====================
    story.append(Paragraph("STRENGTH -- 3 sessions back (Wed Lower / Thu Push / Fri Pull)", section_style))
    strength_data = [
        [
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
                "<b>THU -- Upper Push (~20 min)</b><br/>"
                "Push-ups 3x12-15<br/>"
                "DB shoulder press 3x10<br/>"
                "&nbsp;&nbsp;(push for 25x2 clean sets)<br/>"
                "DB curl 3x10<br/>"
                "Overhead tricep ext 3x10 @ 20-25 lb<br/>"
                "Lateral raise 3x12 @ 15 lb",
                small_style,
            ),
            Paragraph(
                "<b>FRI -- Upper Pull (~20 min)</b><br/>"
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
                "<b>TKEs</b> -- 3x15 each leg with band. Full lockout, 1s hold, slow return. "
                "Building the left quad -- construction, not injury care.",
                small_style,
            ),
            Paragraph(
                "<b>Iso wrist hold (left elbow)</b> -- 7-10 lb x 30-45s, vary it. "
                "Week 7 of the 6-8 wk arc -- reassess whether it's improved under load.",
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
    story.append(Paragraph("NUTRITION -- WEIGHT LOSS MODE RESUMES", section_style))
    nutri_data = [
        [
            Paragraph(
                "<b>Daily targets:</b><br/>"
                "Cal: 2,000-2,300 most days / 2,400-2,600 Sun long run<br/>"
                "<b>Protein 150g/day</b> -- whey scoop daily (habit restored, keep it locked)<br/>"
                "Net deficit ~250-400 cal/day -- resume the downward trend",
                small_style,
            ),
            Paragraph(
                "<b>Sun long run fueling (rehearsal):</b><br/>"
                "~60-70 g carbs/hr -- Tailwind + SiS gels<br/>"
                "Practice race-day timing + amounts<br/>"
                "Fuel + hydrate before (hot)<br/>"
                "Protein within the hour after",
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
        "FTP 230W | Z2 power 129-172W / HR 120-134 | LTHR ~150 | Run HR cap 145 | Coach: Claude",
        ParagraphStyle("Footer", parent=tiny_style, alignment=TA_CENTER, textColor=HexColor("#666666")),
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plans/2026-07-12-br100-week-4.pdf"
    build_pdf(output)
