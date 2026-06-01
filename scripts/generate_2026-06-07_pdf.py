"""Generate printable weekly plan PDF for Week of Jun 1-7 (FBG Build Week 3 — Sharpen).

Single page, B&W laser printer friendly.
Workout step tables omitted — descriptions only.
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
    story.append(Paragraph("Week of Jun 1-7 -- FBG Build Week 3 (Sharpen)", title_style))
    story.append(Paragraph(
        "Peak week done (Sun 3-hr tempo IF 0.79 / 102 g/hr). Volume down ~40%, intensity preserved. FBG Sat Jun 13.",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#000000")))
    story.append(Spacer(1, 3))

    # ==================== DAILY SCHEDULE ====================
    story.append(Paragraph("DAILY SCHEDULE", section_style))

    schedule_rows = [
        ("Mon Jun 1", "Walk + Core Micro + UPPER PUSH + ARMS (~20 min, 2 sets per movement). TKEs + wrist hold.", False),
        ("Tue Jun 2", "Easy spin 45-60 min Z2 (140-160W, HR <130) OR rest. Core micro.", False),
        ("Wed Jun 3", "3x6-over-under.zwo -- proven dose, sharpen reminder. ~50 min.", True),
        ("Thu Jun 4", "Tempo run 30-40 min, HR CAP 145 -- maintain, NOT a PR attempt.", True),
        ("Fri Jun 5", "Core Micro + UPPER PULL + ARMS (~20 min, 2 sets per movement). TKEs + wrist hold.", False),
        ("Sat Jun 6", "Easy spin 45-60 min Z2 OR rest. NO Sat full-body strength.", False),
        ("Sun Jun 7", "Long ride 2 hrs structured (WU + 2x20 tempo + CD) OR Lake Hope w/ Anna 3-4 hrs gravel.", True),
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
    story.append(Paragraph("WED 3x6 OVER-UNDER (FTP 230W) -- ~50 min -- proven dose", section_style))
    story.append(Paragraph(
        "Same workout you nailed May 20 (max HR 164, all 3 blocks). "
        "Each 6-min block alternates <b>1 min @ 105% (241W) / 1 min @ 95% (218W)</b>, three pairs per block. "
        "5 min easy between. <b>Sharpen role: confirm the gear, don't dig a hole.</b> "
        "Pre-workout fuel is non-negotiable this time (not just gels) -- 400+ cal in the tank before starting. "
        "<i>Workout file: zwift-workouts/3x6-over-under.zwo</i>",
        small_style,
    ))

    # ==================== SUN OPTIONS (description only) ====================
    story.append(Paragraph("SUN LONG RIDE -- two options", section_style))
    story.append(Paragraph(
        "<b>Option A (default):</b> 2 hrs Grail outdoor. 30 min warmup Z2 (HR 110-125), "
        "20 min tempo (HR 135-145), 15 min Z2 (HR 120-130), 20 min tempo (HR 135-145), cooldown easy. "
        "Half the volume of last Sun, same intensity touch. Fueling ~60-70 g/hr (comfortable refeed, NOT race rate).",
        small_style,
    ))
    story.append(Paragraph(
        "<b>Option B:</b> Lake Hope w/ Anna -- 3-4 hrs gravel social pace. Ride by RPE, mostly Z2, climbs by feel. "
        "Perfect sharpen-week substitute -- no structure pressure, social terrain, great location.",
        small_style,
    ))

    # ==================== STRENGTH ====================
    story.append(Paragraph("STRENGTH -- Mon Push + Fri Pull (no Sat lower this week)", section_style))
    strength_data = [
        [
            Paragraph(
                "<b>MON -- Upper Push + Arms (~20 min)</b><br/>"
                "<b>2 sets per movement this week (was 3)</b><br/>"
                "Push-ups 2x10-15<br/>"
                "DB shoulder press 2x10 @ 20 lb<br/>"
                "DB curl 2x10 each @ 15-20 lb<br/>"
                "Overhead tricep extension 2x10 @ 20-25 lb<br/>"
                "Lateral raise 2x12 @ 10 lb",
                small_style,
            ),
            Paragraph(
                "<b>FRI -- Upper Pull + Arms (~20 min)</b><br/>"
                "<b>2 sets per movement this week (was 3)</b><br/>"
                "Chest-supported row 2x10 @ 20-25 lb<br/>"
                "Reverse flye 2x12 @ 10 lb<br/>"
                "Slow eccentric hammer curl (3s lower):<br/>"
                "&nbsp;&nbsp;LEFT 3x8 @ 10 lb (still extra set)<br/>"
                "&nbsp;&nbsp;RIGHT 2x8 @ 10 lb<br/>"
                "Tricep dips 2x10 + Plank-to-shoulder-tap 2x20",
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
                "Push to full lockout, 1s hold, slow return. Continue from peak week (no negative reactions noted).",
                small_style,
            ),
            Paragraph(
                "<b>Isometric wrist hold (left elbow)</b> -- 5 lb DB, arm extended, elbow straight. 3x30s. "
                "Palm UP if inside elbow pain; palm DOWN if outside. Continue daily.",
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
                "Dietary sodium: background tracking, not training input<br/>"
                "Normal eating all week -- NO fueling test, NO carb-up<br/>"
                "Race week (Jun 12) gets the real pre-load",
                small_style,
            ),
            Paragraph(
                "<b>Sun long ride fueling:</b><br/>"
                "~60-70 g/hr (comfortable refeed only)<br/>"
                "2 hrs structured: 2 gels + 2 scoops Tailwind<br/>"
                "OR Lake Hope 3-4 hrs: 3-4 gels + 3 scoops Tailwind<br/>"
                "This is NOT a stomach challenge -- save that for race day.",
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
        "FTP 230W | Z2 power 129-172W / HR 120-134 | LTHR ~150 | FBG Sat Jun 13 | Coach: Claude",
        ParagraphStyle("Footer", parent=tiny_style, alignment=TA_CENTER, textColor=HexColor("#666666")),
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plans/2026-06-07-fbg-build-week-3-sharpen.pdf"
    build_pdf(output)
