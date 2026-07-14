"""Generate printable weekly plan PDF for Week of Jul 13-19 (BR100 Taper Week 1).

Single page, B&W laser printer friendly (light gray headers, bold black text).
Taper: recover from the Sunday double (form -11), re-center on running, cut
volume, let form rise toward race day (Sat Jul 25).
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
    story.append(Paragraph("Week of Jul 13-19 -- BR100 Taper Week 1", title_style))
    story.append(Paragraph(
        "Dress rehearsal done (10.1 mi trail). Sunday double dropped form to -11 -- now recover, "
        "re-center on running, cut volume, let form rise. BR100 Leg 8 (12.3 mi) Sat Jul 25.",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#000000")))
    story.append(Spacer(1, 3))

    # ==================== DAILY SCHEDULE ====================
    story.append(Paragraph("DAILY SCHEDULE", section_style))

    schedule_rows = [
        ("Mon Jul 13", "Recovery -- rest or easy walk + core + TKEs + wrist hold. Shed the Sunday-double fatigue.", False),
        ("Tue Jul 14", "Easy run 3-4 mi, HR <140 + rehab. Gentle shakeout.", True),
        ("Wed Jul 15", "Easy run 4-5 mi + 4-6 x 20s strides + light Upper Push + rehab.", True),
        ("Thu Jul 16", "Easy Z2 ride 45-60 min OR rest + rehab. Aerobic touch, off the feet.", False),
        ("Fri Jul 17", "Easy run 3 mi + light Upper Pull + rehab.", True),
        ("Sat Jul 18", "LAST moderate run -- 6-8 mi trail, HR <145, full race-day fueling rehearsal.", True),
        ("Sun Jul 19", "Rest or very easy short spin/walk. Into race week fresh.", False),
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

    # ==================== TAPER LOGIC ====================
    story.append(Paragraph("WHY A TAPER NOW", section_style))
    story.append(Paragraph(
        "Fitness (CTL) is high at 72 -- the engine is built. But Sunday's 10 mi run + 43 mi ride "
        "(~310 TSS) spiked fatigue and dropped <b>form to -11 (fatigued)</b>. With the race 12 days out, "
        "the work is done -- now we <b>shed fatigue so form climbs back to +5 to +15 by race day.</b> "
        "That means <b>less volume, not more.</b> Runs stay short with a little sharpness; rides are easy and "
        "optional; heavy lifting pauses. Resting HR falling back toward 45-46 is the sign it's working.",
        small_style,
    ))

    # ==================== SAT RUN ====================
    story.append(Paragraph("SAT FINAL TUNE-UP -- 6-8 mi (not a big one)", section_style))
    story.append(Paragraph(
        "Distance is already proven twice (11.13, 10.1 mi). Saturday is a <b>fueling/pacing rehearsal + "
        "leg-sharpener</b>, HR-capped &lt;145 on trail. Run the exact race-morning fuel (Tailwind + SiS timing) "
        "so it's automatic on the 25th. <b>Finish feeling like you could've kept going.</b>",
        small_style,
    ))

    # ==================== STRENGTH + REHAB ====================
    story.append(Paragraph("STRENGTH (DELOADED) + REHAB", section_style))
    strength_data = [
        [
            Paragraph(
                "<b>Light upper only</b> (keep legs fresh):<br/>"
                "WED Upper Push ~15 min (push-ups, DB press, curls, lat raise -- 2 easy sets)<br/>"
                "FRI Upper Pull ~15 min (CS row, reverse flye, hammer curls, dips)<br/>"
                "<b>HOLD the heavy lower</b> (goblet/RDL) this week -- fresh legs beat strength gains now.",
                small_style,
            ),
            Paragraph(
                "<b>Daily rehab (continues):</b><br/>"
                "TKEs 3x15 each leg with band<br/>"
                "Iso wrist hold left 7-10 lb x 30-45s<br/>"
                "<i>Elbow week 8 -- end of the 6-8 wk arc; note how it feels.</i>",
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

    # ==================== NUTRITION ====================
    story.append(Paragraph("NUTRITION -- TAPER", section_style))
    nutri_data = [
        [
            Paragraph(
                "<b>Daily targets:</b><br/>"
                "Cal: 2,000-2,300 most days; fuel the Sat run<br/>"
                "<b>Protein 150g/day</b> -- whey scoop daily<br/>"
                "Modest deficit OK this week",
                small_style,
            ),
            Paragraph(
                "<b>Race prep note:</b><br/>"
                "Sat run = final race-morning fuel rehearsal (Tailwind + SiS)<br/>"
                "<b>NEXT week (race week): shift to fueling, not deficit</b><br/>"
                "Hydration up in the heat",
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
        "FTP ~210W | Z2 ~118-158W / HR 120-134 | run HR cap 145 | form -11 -> target +10 by Jul 25 | Coach: Claude",
        ParagraphStyle("Footer", parent=tiny_style, alignment=TA_CENTER, textColor=HexColor("#666666")),
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plans/2026-07-19-br100-taper-week-1.pdf"
    build_pdf(output)
