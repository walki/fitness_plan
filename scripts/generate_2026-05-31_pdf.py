"""Generate printable weekly plan PDF for Week of May 26-31 (FBG Build Week 2 — Peak).

Single page, B&W laser printer friendly (no color highlights).
Workout step tables omitted — descriptions only, since they live in Zwift (.zwo)
and Garmin Connect (manually built) for execution.
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
        topMargin=0.35 * inch,
        bottomMargin=0.3 * inch,
        leftMargin=0.45 * inch,
        rightMargin=0.45 * inch,
    )

    styles = getSampleStyleSheet()

    # Monochrome palette — all renders cleanly on B&W laser
    HEADER_BG = HexColor("#2c3e50")   # dark slate (prints as dark gray)
    ROW_ALT = HexColor("#f0f0f0")     # light gray
    BOX_BG = HexColor("#f5f5f5")      # very light gray
    BORDER = HexColor("#888888")      # medium gray

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
    tiny_style = ParagraphStyle(
        "Tiny", parent=styles["Normal"], fontSize=7.5, leading=9,
        textColor=HexColor("#555555"),
    )

    story = []

    # ==================== HEADER ====================
    story.append(Paragraph("Week of May 26-31 -- FBG Build Week 2 (Peak)", title_style))
    story.append(Paragraph(
        "Mon May 25 anchor done (62 mi Z2, IF 0.726). Highest load this week. FBG Jun 13 -- 66.7 mi / 6,186 ft.",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#000000")))
    story.append(Spacer(1, 3))

    # ==================== DAILY SCHEDULE ====================
    story.append(Paragraph("DAILY SCHEDULE", section_style))

    schedule_rows = [
        ("Tue May 26", "Recovery skew. UPPER PULL + ARMS (~20 min, overdue from last week). Core micro. Optional 30 min easy spin.", False),
        ("Wed May 27", "4x6-over-under.zwo -- PEAK over-under, ~60 min. Step-up from last week's 3x6.", True),
        ("Thu May 28", "Tempo run 40-50 min outdoor, HR 145-155.", True),
        ("Fri May 29", "Easy day. Z2 ride 60 min OR rest. Core micro.", False),
        ("Sat May 30", "Strength -- FULL BODY, LOWER-FOCUSED (~40 min). New 30/40 lb DBs + bands + rehab work.", False),
        ("Sun May 31", "LONG TEMPO RIDE (Garmin workout) -- 3 hrs Grail, 4x20 tempo. FUELING TEST at 90 g/hr.", True),
    ]

    schedule_data = [[Paragraph("<b>Day</b>", small_style), Paragraph("<b>Session</b>", small_style)]]
    for day, sess, highlight in schedule_rows:
        s = bold_small if highlight else small_style
        schedule_data.append([Paragraph(day, s), Paragraph(sess, s)])

    schedule_table = Table(schedule_data, colWidths=[1.0 * inch, 6.1 * inch])
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

    # ==================== WED OVER-UNDER (description only) ====================
    story.append(Paragraph("WED PEAK OVER-UNDER -- 4x6 (FTP 230W) -- ~60 min", section_style))
    story.append(Paragraph(
        "Step-up from 3x6 last week. Same intensities, added 4th block = accumulated fatigue. "
        "Each 6-min block alternates <b>1 min @ 105% (241W) / 1 min @ 95% (218W)</b>, three pairs per block. "
        "5 min easy between. <b>Goal: complete all 4 blocks.</b> If block 4 forces a dropped over (232W instead of 241W), "
        "that's still a win. <i>Workout file: zwift-workouts/4x6-over-under.zwo</i>",
        small_style,
    ))

    # ==================== SUN LONG TEMPO RIDE (description only) ====================
    story.append(Paragraph("SUN LONG TEMPO RIDE -- 3 hrs, FBG dress rehearsal", section_style))
    story.append(Paragraph(
        "Grail outdoors. <b>4 x 20 min tempo blocks (HR 135-145) separated by 20 min Z2 recovery (HR 115-130).</b> "
        "Warmup 20 min + cooldown 20 min. Last tempo block, push if legs feel it. "
        "<i>Garmin workout spec: garmin-workouts/2026-05-31-sun-long-tempo.md</i>",
        small_style,
    ))
    story.append(Paragraph(
        "<b>FUELING TEST -- 90 g/hr (270g total). Watch alarm every 30 min.</b> "
        "Carry: 6 SiS gels + 5.5 scoops Tailwind. This is the FBG dress rehearsal -- "
        "if gut handles this at tempo intensity for 3 hrs, FBG is ready.",
        small_style,
    ))

    # ==================== STRENGTH ====================
    story.append(Paragraph("STRENGTH -- Tue Pull + Sat Full Body (with rehab integration)", section_style))
    strength_data = [
        [
            Paragraph(
                "<b>TUE -- Upper Pull + Arms (~20 min)</b><br/>"
                "<b>NEW:</b> Chest-supported DB row 3x10 (face down on bench)<br/>"
                "Reverse flye 3x12 @ 10-20 lb<br/>"
                "<b>Slow eccentric hammer curl</b> (3s lower / 1s up):<br/>"
                "&nbsp;&nbsp;LEFT 4x8 @ 10-15 lb (extra set)<br/>"
                "&nbsp;&nbsp;RIGHT 3x8 @ same weight<br/>"
                "Tricep dips (chair) 3x10<br/>"
                "Plank-to-shoulder-tap 2x20 taps",
                small_style,
            ),
            Paragraph(
                "<b>SAT -- Full Body, Lower (~40 min)</b><br/>"
                "<b>FIRST: Spanish squat 3x30s</b> (band around shins, knees push out, sit 70 deg)<br/>"
                "Goblet squat 3x8 @ <b>30 lb</b> (up from 25)<br/>"
                "DB RDL 3x8 @ <b>40 lb each</b><br/>"
                "<b>Box step-ups 3x8 each @ 20 lb, matched</b> (LEAD WITH LEFT)<br/>"
                "DB bench press 3x8 @ <b>30 lb each</b> wk 1 (then 40s wk 2)<br/>"
                "Chest-supported row 3x8 @ 30 lb<br/>"
                "Plank 2x60s + side plank 2x30s each",
                small_style,
            ),
        ],
    ]
    strength_table = Table(strength_data, colWidths=[3.55 * inch, 3.55 * inch])
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
    story.append(Paragraph("REHAB DAILY OPTIONS (2 min each, anywhere)", section_style))
    rehab_data = [
        [
            Paragraph(
                "<b>TKEs (Terminal Knee Extensions)</b> -- 3x15 each leg with band behind knee. "
                "Push to full lockout, 1s hold, slow return. Low risk, high yield for VMO.",
                small_style,
            ),
            Paragraph(
                "<b>Isometric wrist hold (left elbow)</b> -- 5-10 lb DB, arm extended, elbow straight. "
                "3x30s. Palm UP if inside elbow pain; palm DOWN if outside.",
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
    story.append(Paragraph("NUTRITION + WATCH LIST", section_style))
    nutri_data = [
        [
            Paragraph(
                "<b>Daily targets:</b><br/>"
                "Cal: 2,100 rest / 2,400 training / 2,700+ long ride<br/>"
                "Protein: 150g/day -- whey scoop daily<br/>"
                "<b>DIETARY sodium under 2,500 mg/day</b> -- Italian dressing, full Chipotle bowls, marinara are recurring high-sodium hits<br/>"
                "Exercise sodium SEPARATE (gets used in sweat, not BP-relevant)",
                small_style,
            ),
            Paragraph(
                "<b>Sun fueling test -- 90 g/hr (270g total):</b><br/>"
                "6 SiS gels + 5.5 scoops Tailwind<br/>"
                "2 gels/hr + ~2 scoops Tailwind/hr<br/>"
                "Watch alarm every 30 min<br/>"
                "FBG dress rehearsal -- non-negotiable",
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
        "FTP 230W | Z2 power 129-172W / HR 120-134 | LTHR ~150 | BP 2x/week | Coach: Claude",
        ParagraphStyle("Footer", parent=tiny_style, alignment=TA_CENTER, textColor=HexColor("#666666")),
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plans/2026-05-31-fbg-build-week-2-peak.pdf"
    build_pdf(output)
