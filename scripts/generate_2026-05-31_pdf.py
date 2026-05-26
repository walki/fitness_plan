"""Generate printable weekly plan PDF for Week of May 26-31 (FBG Build Week 2 — Peak)."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
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

    title_style = ParagraphStyle(
        "Title2", parent=styles["Title"], fontSize=15, spaceAfter=2,
        textColor=HexColor("#1a1a1a"),
    )
    subtitle_style = ParagraphStyle(
        "Subtitle2", parent=styles["Normal"], fontSize=10,
        textColor=HexColor("#555555"), spaceAfter=6, alignment=TA_CENTER,
    )
    section_style = ParagraphStyle(
        "Section", parent=styles["Heading2"], fontSize=10.5,
        spaceBefore=7, spaceAfter=3, textColor=HexColor("#2c3e50"),
    )
    small_style = ParagraphStyle(
        "Small", parent=styles["Normal"], fontSize=8.5, leading=10.5,
        spaceAfter=1,
    )
    bold_small = ParagraphStyle("BoldSmall", parent=small_style, fontName="Helvetica-Bold")
    tiny_style = ParagraphStyle(
        "Tiny", parent=styles["Normal"], fontSize=7.5, leading=9.5,
        textColor=HexColor("#555555"),
    )

    story = []

    # ==================== HEADER ====================
    story.append(Paragraph("Week of May 26-31 -- FBG Build Week 2 (Peak)", title_style))
    story.append(Paragraph(
        "Mon May 25 anchor done (62 mi Z2, IF 0.726). Highest load this week. FBG Jun 13 -- 66.7 mi / 6,186 ft.",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#2c3e50")))
    story.append(Spacer(1, 4))

    # ==================== DAILY SCHEDULE ====================
    story.append(Paragraph("DAILY SCHEDULE", section_style))

    schedule_rows = [
        ("Tue May 26", "Recovery skew. UPPER PULL + ARMS (~20 min, overdue from last week). Core micro. Optional 30 min easy spin.", False),
        ("Wed May 27", "4x6-over-under.zwo -- PEAK over-under, ~60 min. Step-up from last week's 3x6.", True),
        ("Thu May 28", "Tempo run 40-50 min outdoor, HR 145-155.", True),
        ("Fri May 29", "Easy day. Z2 ride 60 min OR rest. Core micro.", False),
        ("Sat May 30", "Strength -- FULL BODY, LOWER-FOCUSED (~40 min) with new 30/40 lb DBs + bands + rehab work.", False),
        ("Sun May 31", "LONG TEMPO RIDE -- 3 hrs Grail, 4x20 min tempo blocks. FUELING TEST at 90 g/hr -- religious.", True),
    ]

    schedule_data = [[Paragraph("<b>Day</b>", small_style), Paragraph("<b>Session</b>", small_style)]]
    for day, sess, highlight in schedule_rows:
        s = bold_small if highlight else small_style
        schedule_data.append([Paragraph(day, s), Paragraph(sess, s)])

    schedule_table = Table(schedule_data, colWidths=[1.0 * inch, 6.1 * inch])
    schedule_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f5f5f5")]),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(schedule_table)

    # ==================== WED OVER-UNDER ====================
    story.append(Paragraph("WED PEAK OVER-UNDER -- 4x6 (FTP 230W) -- ~60 min", section_style))
    story.append(Paragraph(
        "Step-up from 3x6 last week. Same intensities, added 4th block = accumulated fatigue. "
        "Each 6-min block alternates <b>1 min @ 105% (241W) / 1 min @ 95% (218W)</b>, three pairs per block. "
        "5 min easy between. <b>Goal: complete all 4 blocks.</b> If block 4 forces a dropped over (232W instead of 241W), that's still a win.",
        small_style,
    ))
    ou_data = [
        [Paragraph(f"<b>{c}</b>", small_style) for c in ["Block", "Duration", "Detail"]],
        [Paragraph("Warmup + prime", small_style), Paragraph("15 min", small_style), Paragraph("Ramp 50% -> 75%, then 60s @ 90%, then easy", small_style)],
        [Paragraph("Block 1", bold_small), Paragraph("6 min", bold_small), Paragraph("3x [1 min @ 241W -> 1 min @ 218W]", bold_small)],
        [Paragraph("Recovery", small_style), Paragraph("5 min", small_style), Paragraph("Easy spin @ 55%", small_style)],
        [Paragraph("Block 2", bold_small), Paragraph("6 min", bold_small), Paragraph("3x [1 min @ 241W -> 1 min @ 218W]", bold_small)],
        [Paragraph("Recovery", small_style), Paragraph("5 min", small_style), Paragraph("Easy spin @ 55%", small_style)],
        [Paragraph("Block 3", bold_small), Paragraph("6 min", bold_small), Paragraph("3x [1 min @ 241W -> 1 min @ 218W] (past last week's volume)", bold_small)],
        [Paragraph("Recovery", small_style), Paragraph("5 min", small_style), Paragraph("Easy spin @ 55%", small_style)],
        [Paragraph("Block 4", bold_small), Paragraph("6 min", bold_small), Paragraph("3x [1 min @ 241W -> 1 min @ 218W] (final -- empty the tank)", bold_small)],
        [Paragraph("Cooldown", small_style), Paragraph("8 min", small_style), Paragraph("Ramp 65% -> 45%", small_style)],
    ]
    ou_table = Table(ou_data, colWidths=[0.95 * inch, 0.75 * inch, 5.4 * inch])
    ou_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f5f5f5")]),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(ou_table)

    # ==================== SUN LONG TEMPO RIDE ====================
    story.append(Paragraph("SUN LONG TEMPO RIDE -- 3 hrs, FBG dress rehearsal", section_style))
    story.append(Paragraph(
        "Grail outdoors. <b>4 x 20 min tempo blocks separated by 20 min Z2 recovery.</b> "
        "Tempo target HR 135-145. Z2 recovery HR 120-130. Last tempo block, push if legs feel it.",
        small_style,
    ))

    sun_data = [
        [Paragraph(f"<b>{c}</b>", small_style) for c in ["Time", "Block", "HR Target"]],
        [Paragraph("0:00-0:20", small_style), Paragraph("Warmup Z2", small_style), Paragraph("&lt;125", small_style)],
        [Paragraph("0:20-0:40", bold_small), Paragraph("TEMPO 1", bold_small), Paragraph("135-145", bold_small)],
        [Paragraph("0:40-1:00", small_style), Paragraph("Z2 recovery", small_style), Paragraph("120-130", small_style)],
        [Paragraph("1:00-1:20", bold_small), Paragraph("TEMPO 2", bold_small), Paragraph("135-145", bold_small)],
        [Paragraph("1:20-1:40", small_style), Paragraph("Z2 recovery", small_style), Paragraph("120-130", small_style)],
        [Paragraph("1:40-2:00", bold_small), Paragraph("TEMPO 3", bold_small), Paragraph("135-145", bold_small)],
        [Paragraph("2:00-2:20", small_style), Paragraph("Z2 recovery", small_style), Paragraph("120-130", small_style)],
        [Paragraph("2:20-2:40", bold_small), Paragraph("TEMPO 4 (push)", bold_small), Paragraph("135-145+", bold_small)],
        [Paragraph("2:40-3:00", small_style), Paragraph("Cooldown easy", small_style), Paragraph("&lt;125", small_style)],
    ]
    sun_table = Table(sun_data, colWidths=[1.2 * inch, 3.5 * inch, 2.4 * inch])
    sun_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f5f5f5")]),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(sun_table)
    story.append(Paragraph(
        "<b>FUELING TEST -- 90 g/hr (270g total). Watch alarm every 30 min.</b> "
        "Carry: 6 SiS gels + 5.5 scoops Tailwind (in bottles or stickpacks if arrived). 2 gels/hr + ~2 scoops Tailwind/hr.",
        small_style,
    ))

    # Page 2 for strength + nutrition
    story.append(PageBreak())
    story.append(Paragraph("Week of May 26-31 (page 2)", title_style))
    story.append(Paragraph("Strength sessions + nutrition + rehab integration", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#2c3e50")))
    story.append(Spacer(1, 4))

    # ==================== STRENGTH ====================
    story.append(Paragraph("STRENGTH -- Tue Pull + Sat Full Body (with rehab integration)", section_style))
    strength_data = [
        [
            Paragraph(
                "<b>TUE -- Upper Pull + Arms (~20 min)</b><br/>"
                "<b>NEW:</b> Chest-supported DB row 3x10 (face down on bench)<br/>"
                "Reverse flye 3x12 @ 10-20 lb<br/>"
                "<b>Slow eccentric hammer curl</b> (3s lower / 1s up):<br/>"
                "&nbsp;&nbsp;&nbsp;LEFT 4x8 @ 10-15 lb (extra set)<br/>"
                "&nbsp;&nbsp;&nbsp;RIGHT 3x8 @ same weight<br/>"
                "Tricep dips (chair) 3x10<br/>"
                "Plank-to-shoulder-tap 2x20 taps",
                small_style,
            ),
            Paragraph(
                "<b>SAT -- Full Body, Lower (~40 min)</b><br/>"
                "<b>FIRST: Spanish squat 3x30s</b> (band/circle around shins, knees push OUT, sit back 70 deg)<br/>"
                "Goblet squat 3x8 @ <b>30 lb</b> (up from 25)<br/>"
                "DB RDL 3x8 @ <b>40 lb each</b> (clean form)<br/>"
                "<b>Box step-ups 3x8 each @ 20 lb each, matched</b> (replaces split squats, LEAD WITH LEFT)<br/>"
                "DB bench press 3x8 @ <b>30 lb each</b> wk 1 (then 40s wk 2)<br/>"
                "Chest-supported row 3x8 @ 30 lb<br/>"
                "Plank 2x60s + side plank 2x30s each",
                small_style,
            ),
        ],
    ]
    strength_table = Table(strength_data, colWidths=[3.55 * inch, 3.55 * inch])
    strength_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f9f9f9")),
    ]))
    story.append(strength_table)

    # Rehab daily
    story.append(Paragraph("REHAB DAILY OPTIONS (2 min, anywhere)", section_style))
    rehab_data = [
        [
            Paragraph(
                "<b>TKEs (Terminal Knee Extensions)</b><br/>"
                "3x15 each leg with band behind knee. Push to full lockout, 1s hold, slow return. "
                "Do daily if you want -- low risk, high yield for VMO.",
                small_style,
            ),
            Paragraph(
                "<b>Isometric wrist hold (left elbow)</b><br/>"
                "5-10 lb DB, arm extended in front, elbow straight. 3x30s. "
                "Palm UP if pain is inside elbow (medial); palm DOWN if outside (lateral).",
                small_style,
            ),
        ],
    ]
    rehab_table = Table(rehab_data, colWidths=[3.55 * inch, 3.55 * inch])
    rehab_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#fff8e1")),
    ]))
    story.append(rehab_table)

    # ==================== NUTRITION ====================
    story.append(Paragraph("NUTRITION + WATCH LIST", section_style))
    nutri_data = [
        [
            Paragraph(
                "<b>Daily targets:</b><br/>"
                "Calories: 2,100 rest / 2,400 training / 2,700+ long ride day<br/>"
                "Protein: 150g/day -- whey scoop daily<br/>"
                "<b>DIETARY sodium target: under 2,500 mg/day</b><br/>"
                "&nbsp;&nbsp;(Italian dressing, full Chipotle bowls, marinara = recurring high-sodium)<br/>"
                "Exercise sodium is reported SEPARATELY -- gets used in sweat, not BP-relevant.",
                small_style,
            ),
            Paragraph(
                "<b>Sun fueling test -- 90 g/hr non-negotiable:</b><br/>"
                "Target 270g carbs over 3 hrs<br/>"
                "6 SiS gels + 5.5 scoops Tailwind<br/>"
                "Set watch alarm every 30 min for gel<br/>"
                "Sip Tailwind continuously between gels<br/>"
                "<b>This is the FBG dress rehearsal.</b> If gut handles this at tempo for 3 hrs, FBG is ready.",
                small_style,
            ),
        ],
    ]
    nutri_table = Table(nutri_data, colWidths=[3.55 * inch, 3.55 * inch])
    nutri_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f9f9f9")),
    ]))
    story.append(nutri_table)

    # Footer
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#cccccc")))
    story.append(Paragraph(
        "Working FTP: 230W | Z2 power 129-172W / HR 120-134 | Threshold HR ~150 | BP check 2x/week | Coach: Claude",
        ParagraphStyle("Footer", parent=tiny_style, alignment=TA_CENTER, textColor=HexColor("#888888")),
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plans/2026-05-31-fbg-build-week-2-peak.pdf"
    build_pdf(output)
