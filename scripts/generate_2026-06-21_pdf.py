"""Generate printable weekly plan PDF for Week of Jun 15-21 (Post-FBG, BR100 build week 1).

Single page, B&W laser printer friendly.
FIRST PDF using the new lighter table headers per CLAUDE.md update.
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

    # New B&W palette (per Roger feedback Jun 14, 2026):
    # Light gray header bg with bold black text — prints clean on B&W laser
    HEADER_BG = HexColor("#dddddd")    # light gray header
    ROW_ALT = HexColor("#f0f0f0")      # very light gray alternating
    BOX_BG = HexColor("#f5f5f5")       # very light gray boxes
    BORDER = HexColor("#888888")       # medium gray borders

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
    story.append(Paragraph("Week of Jun 15-21 -- Post-FBG | BR100 Build Week 1", title_style))
    story.append(Paragraph(
        "FBG ✓ done (6:23 / NP 174 / IF 0.76). Running primary, cycling maintenance, weight loss active. "
        "BR100 Jul 25 Leg 8 (12.3 mi / +1,144 ft trail).",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#000000")))
    story.append(Spacer(1, 3))

    # ==================== DAILY SCHEDULE ====================
    story.append(Paragraph("DAILY SCHEDULE", section_style))

    schedule_rows = [
        ("Mon Jun 15", "Walk or rest. Core micro + TKEs + wrist hold. NO strength (FBG was Sat).", False),
        ("Tue Jun 16", "Easy run 3 mi, HR <140. Outdoor if weather. Rehab.", True),
        ("Wed Jun 17", "Easy Z2 ride 60-75 min (140-160W) + Upper Push LIGHT (~15 min, 2 sets). Rehab.", False),
        ("Thu Jun 18", "Easy run 3-4 mi, HR <140. Rehab.", True),
        ("Fri Jun 19", "Easy run 3 mi + Upper Pull (~20 min, 2-3 sets). Rehab.", True),
        ("Sat Jun 20", "Strength Full Body Lower (~35 min) + optional easy Z2 ride 60 min. Rehab.", False),
        ("Sun Jun 21", "LONG TRAIL RUN -- 6 mi conversational pace, HR <145. Pick a trail w/ some elevation.", True),
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

    # ==================== SUN LONG TRAIL RUN ====================
    story.append(Paragraph("SUN LONG TRAIL RUN -- 6 mi (BR100 build week 1 anchor)", section_style))
    story.append(Paragraph(
        "6 mi at conversational pace, HR &lt;145. Modest step from last Sun's 5-mi shakeout. "
        "<b>Pick a trail with some elevation</b> -- BR100 Leg 8 has its big climb at mile 7-8, "
        "so we re-introduce climbing fatigue gradually. Trail running ≠ road running -- uneven footing, slower turnover, "
        "eccentric quad loading on descents. Don't compare pace. Fueling: 1 gel mid-run OR a Tailwind bottle is plenty.",
        small_style,
    ))

    # ==================== STRENGTH ====================
    story.append(Paragraph("STRENGTH -- 3 sessions (Wed Push / Fri Pull / Sat Full Body)", section_style))
    strength_data = [
        [
            Paragraph(
                "<b>WED -- Upper Push LIGHT (~15 min)</b><br/>"
                "<b>2 sets per movement (recovery week)</b><br/>"
                "Push-ups 2x10-12<br/>"
                "DB shoulder press 2x10 @ 20-25 lb<br/>"
                "DB curl 2x10 each @ 20 lb<br/>"
                "Overhead tricep extension 2x10 @ 20-25 lb<br/>"
                "Lateral raise 2x12 @ 10-15 lb",
                small_style,
            ),
            Paragraph(
                "<b>FRI -- Upper Pull (~20 min)</b><br/>"
                "<b>2-3 sets per movement (normal back)</b><br/>"
                "Chest-supported DB row 3x10 @ 25-30 lb<br/>"
                "Reverse flye 3x12 @ 15 lb<br/>"
                "Slow eccentric hammer curl: L 3x8 @ 10-15 lb, R 3x8<br/>"
                "Tricep dips 3x10<br/>"
                "Plank-to-shoulder-tap 2x20 taps",
                small_style,
            ),
            Paragraph(
                "<b>SAT -- Full Body Lower (~35 min)</b><br/>"
                "Spanish squat 3x30s (mini-band)<br/>"
                "Goblet squat 3x8 @ 30 lb<br/>"
                "DB RDL 3x8 @ 40 lb each<br/>"
                "Box step-ups 3x8 each @ 20-25 lb, LEAD LEFT<br/>"
                "DB bench press 3x8 @ 30-40 lb each<br/>"
                "Chest-supported row 3x8 @ 30 lb<br/>"
                "Plank 2x60s + side plank 2x30s each",
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
    story.append(Paragraph("REHAB DAILY (continuing 7+ week streak)", section_style))
    rehab_data = [
        [
            Paragraph(
                "<b>TKEs (Terminal Knee Extensions)</b> -- 3x15 each leg with band. "
                "Knee to full lockout, 1s hold, slow return. VMO targeting.",
                small_style,
            ),
            Paragraph(
                "<b>Isometric wrist hold (left elbow)</b> -- 10 lb DB, arm extended, elbow straight, 3x30s. "
                "Palm UP if inside elbow / DOWN if outside.",
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

    # ==================== NUTRITION (weight loss mode) ====================
    story.append(Paragraph("NUTRITION -- WEIGHT LOSS MODE", section_style))
    nutri_data = [
        [
            Paragraph(
                "<b>Daily targets:</b><br/>"
                "Cal: 2,000-2,300 most days / 2,400-2,600 long run/ride days<br/>"
                "<b>Protein 150g/day</b> -- whey scoop daily is the lever<br/>"
                "Net deficit target: ~300-500 cal/day<br/>"
                "Trend goal: <b>0.5-0.75 lb/week down</b><br/>"
                "Dietary sodium: tracked, not a decision input (Roger's call)",
                small_style,
            ),
            Paragraph(
                "<b>Weight loss context:</b><br/>"
                "Year-end goal: <b>165 lb</b> (currently ~188).<br/>"
                "23 lb in 28 weeks = 0.82 lb/week required -- ambitious but in reach.<br/>"
                "Lighter body = sub-2:00 half marathon comes into range.<br/>"
                "Lighter body = next FBG ~30 min faster.<br/>"
                "<b>No race-week refeeds for a while</b> -- BR100 doesn't qualify (not an A race).",
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
        "FTP 230W | Z2 power 129-172W / HR 120-134 | LTHR ~150 | Weight ~188 -> 165 goal | Coach: Claude",
        ParagraphStyle("Footer", parent=tiny_style, alignment=TA_CENTER, textColor=HexColor("#666666")),
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plans/2026-06-21-post-fbg-br100-week-1.pdf"
    build_pdf(output)
