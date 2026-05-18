"""Generate printable weekly plan PDF for Week of May 18-24 (FBG Build Week 1)."""

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
        spaceBefore=8, spaceAfter=3, textColor=HexColor("#2c3e50"),
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

    # Header
    story.append(Paragraph("Week of May 18-24 -- FBG Build Week 1 of 4", title_style))
    story.append(Paragraph(
        "Post-Red Eagle (2:40:15, NP 199W). Funk Bottoms Jun 13 -- 66.7 mi / 6,186 ft. Peak week is May 25-31.",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#2c3e50")))
    story.append(Spacer(1, 4))

    # Daily Schedule
    story.append(Paragraph("DAILY SCHEDULE", section_style))

    schedule_rows = [
        ("Mon May 18", "Walk + Core Micro + UPPER PUSH/ARMS (~20 min)", False),
        ("Tue May 19", "Openers -- 40 min Z2 trainer + 2x3 min @ 75% FTP", False),
        ("Wed May 20", "YOUR CALL: Tempo run (35-45 min, HR 145-155) OR Over-Under (3x6-over-under.zwo)", True),
        ("Thu May 21", "HIGH EFFORT -- whichever you did NOT do Wednesday", True),
        ("Fri May 22", "Core Micro + UPPER PULL/ARMS (~20 min). Easy day otherwise.", False),
        ("Sat May 23", "Strength -- FULL BODY, LOWER-FOCUSED (~35 min) + optional easy spin", False),
        ("Sun May 24", "LONG RIDE 3.5-4 hrs outdoor (Grail). Fueling test: 90+ g carbs/hr.", True),
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

    # Wed Over-Under
    story.append(Paragraph("WED OVER-UNDER -- 3x6 (FTP 230W) -- ~50 min total", section_style))
    story.append(Paragraph(
        "Each 6-min block alternates <b>1 min @ 105% (241W) / 1 min @ 95% (218W)</b>, three pairs per block. "
        "5 min easy between blocks. <b>Diagnostic intent:</b> Rep 1 = hard but doable. Rep 2 = truth-teller "
        "(does the &quot;under&quot; recover you, or are you drowning?). Rep 3 = can you come back? "
        "Cadence 88-95 on overs.",
        small_style,
    ))
    ou_data = [
        [Paragraph(f"<b>{c}</b>", small_style) for c in ["Block", "Duration", "Detail"]],
        [Paragraph("Warmup", small_style), Paragraph("12 min", small_style), Paragraph("Ramp 50% -> 75% FTP", small_style)],
        [Paragraph("Block 1", bold_small), Paragraph("6 min", bold_small), Paragraph("3x [1 min @ 241W -> 1 min @ 218W]", bold_small)],
        [Paragraph("Recovery", small_style), Paragraph("5 min", small_style), Paragraph("Easy spin @ 55%", small_style)],
        [Paragraph("Block 2", bold_small), Paragraph("6 min", bold_small), Paragraph("3x [1 min @ 241W -> 1 min @ 218W]", bold_small)],
        [Paragraph("Recovery", small_style), Paragraph("5 min", small_style), Paragraph("Easy spin @ 55%", small_style)],
        [Paragraph("Block 3", bold_small), Paragraph("6 min", bold_small), Paragraph("3x [1 min @ 241W -> 1 min @ 218W]", bold_small)],
        [Paragraph("Cooldown", small_style), Paragraph("8 min", small_style), Paragraph("Ramp 65% -> 45%", small_style)],
    ]
    ou_table = Table(ou_data, colWidths=[0.9 * inch, 0.8 * inch, 5.4 * inch])
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

    # Strength
    story.append(Paragraph("STRENGTH -- 3 sessions/week (home dumbbells)", section_style))
    strength_data = [
        [
            Paragraph(
                "<b>MON -- Upper Push + Arms (~20 min)</b><br/>"
                "Push-ups -- 3x10-15<br/>"
                "DB shoulder press -- 3x10 (20-30 lb)<br/>"
                "DB curl -- 3x10 each (20-30 lb)<br/>"
                "Overhead tricep extension -- 3x10 (25-35 lb)<br/>"
                "Lateral raise -- 2x12 (10-15 lb)",
                small_style,
            ),
            Paragraph(
                "<b>FRI -- Upper Pull + Arms (~20 min)</b><br/>"
                "Single-arm row -- 3x10 each (30-40 lb)<br/>"
                "Reverse flye -- 3x12 (10-20 lb)<br/>"
                "Hammer curl -- 3x10 each (25-35 lb)<br/>"
                "Tricep dips (chair) -- 3x10<br/>"
                "Plank-to-shoulder-tap -- 2x20",
                small_style,
            ),
            Paragraph(
                "<b>SAT -- Full Body, Lower (~35 min)</b><br/>"
                "Goblet squat -- 3x8<br/>"
                "DB Romanian deadlift -- 3x8<br/>"
                "DB split squat -- 3x8 each<br/>"
                "DB floor press -- 3x10<br/>"
                "Single-arm row (heavier) -- 3x6 each<br/>"
                "Plank 2x60s + side plank 2x30s each",
                small_style,
            ),
        ],
    ]
    strength_table = Table(strength_data, colWidths=[2.37 * inch, 2.37 * inch, 2.37 * inch])
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

    # Nutrition + Watch List
    story.append(Paragraph("NUTRITION + WATCH LIST", section_style))
    nutri_data = [
        [
            Paragraph(
                "<b>Daily targets:</b><br/>"
                "Calories: 2,100 rest / 2,400 training / 2,700+ long ride day<br/>"
                "Protein: 150g/day (whey scoop is the lever)<br/>"
                "Sodium: target back under 2,500 mg -- last 2 wks ran 3,800-5,500 mg<br/>"
                "  (BP context: this matters. Chipotle + brats + beer was the pattern.)",
                small_style,
            ),
            Paragraph(
                "<b>Sun long ride fueling test:</b><br/>"
                "Target 90+ g carbs/hr (Red Eagle: 117 g/hr, no GI issues)<br/>"
                "Practice: 2 SiS gels/hr + 1 scoop Tailwind/bottle<br/>"
                "This is the dress rehearsal for FBG. Take it seriously.",
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
        "Working FTP: 230W (revised post-Red Eagle) | Weight: 190.2 7-day avg | BP check 2x/week | Coach: Claude",
        ParagraphStyle("Footer", parent=tiny_style, alignment=TA_CENTER, textColor=HexColor("#888888")),
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plans/2026-05-24-fbg-build-week-1.pdf"
    build_pdf(output)
