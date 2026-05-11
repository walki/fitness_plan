"""Generate a printable weekly plan PDF."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import sys
import os


def build_race_week_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=0.4 * inch,
        bottomMargin=0.3 * inch,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "Title2",
        parent=styles["Title"],
        fontSize=16,
        spaceAfter=2,
        textColor=HexColor("#1a1a1a"),
    )
    subtitle_style = ParagraphStyle(
        "Subtitle2",
        parent=styles["Normal"],
        fontSize=10,
        textColor=HexColor("#555555"),
        spaceAfter=8,
        alignment=TA_CENTER,
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=11,
        spaceBefore=10,
        spaceAfter=4,
        textColor=HexColor("#2c3e50"),
        borderPadding=(0, 0, 2, 0),
    )
    body_style = ParagraphStyle(
        "Body2",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        spaceAfter=2,
    )
    small_style = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        spaceAfter=1,
    )
    bold_small = ParagraphStyle(
        "BoldSmall",
        parent=small_style,
        fontName="Helvetica-Bold",
    )

    story = []

    # Header
    story.append(Paragraph("Week of May 12-17 -- Red Eagle Race Week", title_style))
    story.append(
        Paragraph(
            "Red Eagle Gravel Grinder | Sun May 17 | 42.6 mi, 1,479 ft | Target: Sub-3:00",
            subtitle_style,
        )
    )
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#2c3e50")))
    story.append(Spacer(1, 6))

    # Daily Schedule
    story.append(Paragraph("DAILY SCHEDULE", section_style))

    schedule_data = [
        ["Day", "Session"],
        ["Mon May 12", "Rest or walk + Core Micro (5 min)"],
        ["Tue May 13", "OPENERS -- see detail below"],
        ["Wed May 14", "Easy run 30 min, HR <135 + Core Micro"],
        ["Thu May 15", "Rest"],
        ["Fri May 16", "Rest. PRE-LOAD: 2,500+ cal / 300g+ carbs. Minimal beer."],
        ["Sat May 16", "Rest. Eat well. Sleep early."],
        ["Sun May 17", "RED EAGLE RACE DAY"],
    ]

    # Convert to Paragraphs for wrapping
    schedule_table_data = []
    for i, row in enumerate(schedule_data):
        if i == 0:
            schedule_table_data.append(
                [
                    Paragraph(f"<b>{row[0]}</b>", small_style),
                    Paragraph(f"<b>{row[1]}</b>", small_style),
                ]
            )
        else:
            day_style = bold_small if row[0] in ["Tue May 13", "Sun May 17"] else small_style
            sess_style = bold_small if "OPENERS" in row[1] or "RACE DAY" in row[1] or "PRE-LOAD" in row[1] else small_style
            schedule_table_data.append(
                [
                    Paragraph(row[0], day_style),
                    Paragraph(row[1], sess_style),
                ]
            )

    schedule_table = Table(
        schedule_table_data, colWidths=[1.2 * inch, 5.8 * inch]
    )
    schedule_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#2c3e50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f5f5f5")]),
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(schedule_table)
    story.append(Spacer(1, 6))

    # Openers Detail
    story.append(Paragraph("OPENERS (Tue May 13)", section_style))
    story.append(
        Paragraph(
            "Total: ~35 min. Hard effort: 3:30. <b>Should leave you feeling BETTER, not tired.</b>",
            body_style,
        )
    )

    opener_data = [
        ["Block", "Duration", "Power / Effort", "Cadence"],
        ["Warmup", "15:00", "Easy spin, 130-150W", "--"],
        ["Opener 1", "1:30", "198W (90% FTP). Controlled.", "90+"],
        ["Recovery", "3:00", "Easy spin, 120W", "--"],
        ["Opener 2", "1:00", "220W (100% FTP). Feel threshold.", "95+"],
        ["Recovery", "3:00", "Easy spin, 120W", "--"],
        ["Opener 3", "0:30", "242W (110% FTP). Sharp and fast.", "100+"],
        ["Recovery", "3:00", "Easy spin, 120W", "--"],
        ["Opener 4", "0:30", "242W (110% FTP). One more snap.", "100+"],
        ["Recovery", "2:00", "Easy spin", "--"],
        ["Cooldown", "5:00", "Easy spin, 120 to 100W", "--"],
    ]

    opener_table_data = []
    for i, row in enumerate(opener_data):
        if i == 0:
            opener_table_data.append(
                [Paragraph(f"<b>{c}</b>", small_style) for c in row]
            )
        else:
            is_effort = "Opener" in row[0]
            s = bold_small if is_effort else small_style
            opener_table_data.append([Paragraph(c, s) for c in row])

    opener_table = Table(
        opener_table_data,
        colWidths=[0.9 * inch, 0.7 * inch, 3.5 * inch, 0.7 * inch],
    )
    opener_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#2c3e50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f5f5f5")]),
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(opener_table)
    story.append(
        Paragraph(
            "<i>RPE should never go above 7. If it feels too easy -- perfect. Save it for Sunday.</i>",
            small_style,
        )
    )
    story.append(Spacer(1, 4))

    # Two column section: Core + Run side by side
    story.append(Paragraph("CORE MICRO (Mon, Wed) | EASY RUN (Wed)", section_style))
    combo_data = [
        [
            Paragraph(
                "<b>Core Micro (5-10 min):</b><br/>"
                "- Plank 3x60s<br/>"
                "- Side plank 2x30s each<br/>"
                "- Dead bugs 1x10/side (2-3s hold)<br/>"
                "- Bird dogs 1x10/side (2-3s hold)",
                small_style,
            ),
            Paragraph(
                "<b>Easy Run (30 min):</b><br/>"
                "- HR under 135<br/>"
                "- Walk if needed<br/>"
                "- Just stay loose<br/>"
                "- Outdoor if weather allows",
                small_style,
            ),
        ]
    ]
    combo_table = Table(combo_data, colWidths=[3.5 * inch, 3.5 * inch])
    combo_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f9f9f9")),
            ]
        )
    )
    story.append(combo_table)
    story.append(Spacer(1, 4))

    # Race Day Plan
    story.append(Paragraph("RACE DAY PLAN (Sun May 17)", section_style))
    race_data = [
        [
            Paragraph(
                "<b>Pre-Race:</b><br/>"
                "- Big breakfast 2-3 hrs before (eggs, oatmeal, toast -- 500+ cal)<br/>"
                "- First gel at 20 min into race",
                small_style,
            ),
            Paragraph(
                "<b>On-Bike Fuel:</b><br/>"
                "- 70g carbs/hr MINIMUM<br/>"
                "- 6 SiS gels + 2-3 scoops Tailwind<br/>"
                "- Hydration: weather dependent",
                small_style,
            ),
        ],
        [
            Paragraph(
                "<b>Pacing:</b><br/>"
                "- Find a fast group, sit in<br/>"
                "- Don't lead early -- race starts at mile 20<br/>"
                "- HR target: 130-140 avg<br/>"
                "- Don't chase above 150 in first half",
                small_style,
            ),
            Paragraph(
                "<b>Nutrition Targets This Week:</b><br/>"
                "- Daily: 2,300+ cal, 150g+ protein<br/>"
                "- Whey shake daily<br/>"
                "- Fri pre-load: 2,500+ cal, 300g+ carbs<br/>"
                "- Beer: minimal until after the race",
                small_style,
            ),
        ],
    ]
    race_table = Table(race_data, colWidths=[3.5 * inch, 3.5 * inch])
    race_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f9f9f9")),
            ]
        )
    )
    story.append(race_table)
    story.append(Spacer(1, 6))

    # Footer
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#cccccc")))
    story.append(
        Paragraph(
            "Weight: 188.5 avg (down 5.5 from 194 start) | Working FTP: 220W | Coach: Claude",
            ParagraphStyle("Footer", parent=small_style, alignment=TA_CENTER, textColor=HexColor("#888888")),
        )
    )

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plan.pdf"
    build_race_week_pdf(output)
