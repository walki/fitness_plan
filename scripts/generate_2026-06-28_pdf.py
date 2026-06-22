"""Generate printable weekly plan PDF for Week of Jun 22-28 (BR100 build week 2).

Single page, B&W laser printer friendly (lighter table headers).
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
    story.append(Paragraph("Week of Jun 22-28 -- BR100 Build Week 2 of 5", title_style))
    story.append(Paragraph(
        "Last Sun ✓ 6.14 mi @ HR 138 @ 12:53/mi w/ 329 ft. This week: 7 mi at CVNP w/ 500+ ft. BR100 Jul 25.",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#000000")))
    story.append(Spacer(1, 3))

    # ==================== DAILY SCHEDULE ====================
    story.append(Paragraph("DAILY SCHEDULE", section_style))

    schedule_rows = [
        ("Mon Jun 22", "Walk or rest. Core micro + TKEs + wrist hold.", False),
        ("Tue Jun 23", "Easy run 3-4 mi, HR <140. Rehab.", True),
        ("Wed Jun 24", "Easy Z2 ride 60-75 min (140-160W) + Upper Push (~20 min, 2-3 sets). Rehab.", False),
        ("Thu Jun 25", "Easy run 3-4 mi, HR <140. Rehab.", True),
        ("Fri Jun 26", "Easy run 3 mi + Upper Pull (~20 min, 3 sets). Rehab.", True),
        ("Sat Jun 27", "Strength Full Body Lower (~35 min) + optional easy Z2 ride 60 min. Rehab.", False),
        ("Sun Jun 28", "LONG TRAIL RUN at CVNP -- 7 mi, conversational pace, HR <145. Pick route w/ 500+ ft.", True),
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
    story.append(Paragraph("SUN LONG TRAIL RUN @ CVNP -- 7 mi w/ 500+ ft (BR100 week 2 anchor)", section_style))
    story.append(Paragraph(
        "+1 mi from last week, but the bigger change is <b>elevation</b>. CVNP has real climbs. "
        "Re-introduces sustained climbing under fatigue -- BR100 Leg 8's big climb hits at mile 7-8 fresh; "
        "here we practice climbing on tired legs. <b>HR cap is the constraint, not pace.</b> "
        "If HR hits 150 on a climb, walk a step or two. Expect 13:00-13:30/mi at HR &lt;145 (slower than last week "
        "due to climbs -- normal). Fueling: 1 Tailwind bottle + 1-2 SiS gels mid-run. ~1:30-1:40 total.",
        small_style,
    ))

    # ==================== STRENGTH ====================
    story.append(Paragraph("STRENGTH -- 3 sessions (Wed Push / Fri Pull / Sat Full Body Lower)", section_style))
    strength_data = [
        [
            Paragraph(
                "<b>WED -- Upper Push (~20 min)</b><br/>"
                "Push-ups 2-3x12-15<br/>"
                "DB shoulder press 2-3x10<br/>"
                "&nbsp;&nbsp;(stay 25/20 split until 25x2 sets clean)<br/>"
                "DB curl 2-3x10 -- same auto-regulate<br/>"
                "Overhead tricep ext 2-3x10 @ 20-25 lb<br/>"
                "Lateral raise 2-3x12 @ 15 lb",
                small_style,
            ),
            Paragraph(
                "<b>FRI -- Upper Pull (~20 min)</b><br/>"
                "Chest-supported DB row 3x10 @ 30 lb<br/>"
                "Reverse flye 3x12 @ 15 lb<br/>"
                "Slow eccentric hammer curl 3x8 each @ 15 lb<br/>"
                "Tricep dips 3x10<br/>"
                "Plank-to-shoulder-tap 2x20 taps",
                small_style,
            ),
            Paragraph(
                "<b>SAT -- Full Body Lower (~35 min)</b><br/>"
                "Spanish squat 3x30s (target 30s clean)<br/>"
                "Goblet squat 3x8 @ 40 lb<br/>"
                "DB RDL 3x8 @ 40 lb each<br/>"
                "Box step-ups 3x8 each @ 20-25 lb, LEAD LEFT<br/>"
                "<b>Bench press 3x8 -- try 40 lb each</b> (drop to 30 if form breaks)<br/>"
                "Chest-supported row 3x8 @ 30 lb<br/>"
                "Plank 2x60s (target) + side plank 2x30s each",
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
                "<b>TKEs</b> -- 3x15 each leg with band. Knee to full lockout, 1s hold, slow return.",
                small_style,
            ),
            Paragraph(
                "<b>Iso wrist hold (left elbow)</b> -- vary load/duration: 10 lb x 30s OR 5 lb x 50s+. "
                "Combined stimulus trending up.",
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
    story.append(Paragraph("NUTRITION -- WEIGHT LOSS MODE", section_style))
    nutri_data = [
        [
            Paragraph(
                "<b>Daily targets:</b><br/>"
                "Cal: 2,000-2,300 most days / 2,400-2,600 long run/ride days<br/>"
                "<b>Protein 150g/day</b> -- whey scoop daily<br/>"
                "Net deficit target: ~250-400 cal/day<br/>"
                "Trend goal: <b>0.5-0.75 lb/week -- PACE is the success metric</b>",
                small_style,
            ),
            Paragraph(
                "<b>Sun long run fueling:</b><br/>"
                "1 Tailwind bottle (~25g carbs)<br/>"
                "1-2 SiS gels mid-run<br/>"
                "Coffee + light breakfast before<br/>"
                "Not a fueling stress test -- comfortable refuel only.",
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
        "FTP 230W | Z2 power 129-172W / HR 120-134 | LTHR ~150 | Weight 187.8 7-day avg | Coach: Claude",
        ParagraphStyle("Footer", parent=tiny_style, alignment=TA_CENTER, textColor=HexColor("#666666")),
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plans/2026-06-28-br100-week-2.pdf"
    build_pdf(output)
