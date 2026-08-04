"""Generate printable weekly plan PDF for Week of Aug 3-9 (FALL BLOCK KICKOFF -- Testing Week).

Single page, B&W laser printer friendly (light gray headers, bold black text).
BR100 done. Pivot to fall = weight + half marathon. This week: run re-entry +
threshold testing (bike ramp Wed, run 5K TT Sat) + weight deficit resumes.
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
        topMargin=0.32 * inch,
        bottomMargin=0.28 * inch,
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
        spaceBefore=5, spaceAfter=2, textColor=HexColor("#000000"),
    )
    small_style = ParagraphStyle(
        "Small", parent=styles["Normal"], fontSize=8.3, leading=10,
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
    story.append(Paragraph("Week of Aug 3-9 -- FALL BLOCK KICKOFF (Testing Week)", title_style))
    story.append(Paragraph(
        "BR100 done. Now the pivot: fall = WEIGHT + HALF MARATHON. This week = run re-entry + threshold "
        "testing (bike ramp Wed, run 5K TT Sat) + the weight deficit RESUMES as the priority lever.",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#000000")))
    story.append(Spacer(1, 3))

    # ==================== DAILY SCHEDULE ====================
    story.append(Paragraph("DAILY SCHEDULE", section_style))

    schedule_rows = [
        ("Mon Aug 3", "DONE -- back + rehab (iso wrist hold 10 lb, plank, dead bug, bird dog).", False),
        ("Tue Aug 4", "Easy run 2-3 mi, HR easy. First re-entry -- feel out the toe at soft effort.", False),
        ("Wed Aug 5", "BIKE RAMP TEST (Zwift built-in). Warm up well. Sets your real FTP at last.", True),
        ("Thu Aug 6", "Easy run 3 mi + 3-4 strides (toe-at-speed check) + optional upper strength.", False),
        ("Fri Aug 7", "Rest or easy spin. Freshen the legs for Saturday.", False),
        ("Sat Aug 8", "RUN 5K TT -- flat/measured or track, all-out even effort. (Slip to early next wk if toe unhappy Thu.)", True),
        ("Sun Aug 9", "Easy 4-5 mi -- start rebuilding the long-run base.", False),
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

    # ============ WHY THIS WEEK + FALL FRAME (2-col) ============
    twocol = [
        [
            Paragraph(
                "<b>WHY THIS WEEK -- CALIBRATE</b><br/>"
                "Rested + fresh (form +20) off the recovery week, but <b>run-detrained</b> (8 days off) and "
                "<b>cycling-primed</b>. So test the <b>bike first</b> (Wed); run the 5K <b>after 2 easy re-entry runs</b> "
                "(Sat) so the number is honest. This week sets the <b>calibrated numbers the whole fall block runs "
                "on</b> -- no more inferring zones.",
                small_style,
            ),
            Paragraph(
                "<b>FALL BLOCK FRAME</b><br/>"
                "A-goal: <b>sub-2:00 half</b> (9:09/mi), a <b>mid-Oct-mid-Nov race -- LOCK ONE THIS WEEK.</b> "
                "Weight deficit LIVE again = the pace unlocker. Build: re-establish base -> <b>structured speed</b> "
                "(strides->200s/400s->fartlek) -> long-run progression -> tempo/threshold at <b>tested VDOT paces.</b> "
                "Bike = aerobic maintenance. Strength back to full next week.",
                small_style,
            ),
        ],
    ]
    twocol_table = Table(twocol, colWidths=[3.55 * inch, 3.55 * inch])
    twocol_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, -1), BOX_BG),
    ]))
    story.append(Spacer(1, 3))
    story.append(twocol_table)

    # ==================== TEST PROTOCOLS ====================
    story.append(Paragraph("THRESHOLD TESTS -- the point of the week", section_style))
    protocol = [
        [
            Paragraph(
                "<b>BIKE RAMP (Wed, Zwift built-in)</b><br/>"
                "Warm up, then ride the ramp to failure. Gives an <b>FTP baseline</b> + apples-to-apples vs the "
                "old pre-coaching 217. A <b>20-min test ~2 wks later</b> to compare: ramp &gt;&gt; 20-min = "
                "punchy/anaerobic; close = steady diesel. <b>Paste the number after</b> and we set real power zones.",
                small_style,
            ),
            Paragraph(
                "<b>RUN 5K TT (Sat, flat/measured or track)</b><br/>"
                "Warm up 10-15 min + a few strides. <b>Even all-out effort</b> -- resist a hot first km. Feeds "
                "<b>VDOT</b> = every training pace (Easy/Marathon/Threshold/Interval/Rep) + run LTHR + a <b>current "
                "half prediction</b> (day-one sub-2:00 gap). Re-test 6-8 wks.",
                small_style,
            ),
        ],
    ]
    protocol_table = Table(protocol, colWidths=[3.55 * inch, 3.55 * inch])
    protocol_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, -1), BOX_BG),
    ]))
    story.append(protocol_table)

    # ==================== NUTRITION + REHAB ====================
    story.append(Paragraph("NUTRITION (DEFICIT BACK ON) + REHAB", section_style))
    nutri = [
        [
            Paragraph(
                "<b>DEFICIT RESUMES ~300-400/day</b> -- the fall lever.<br/>"
                "<b>Protein 150g/day</b> -- whey scoop is the lever (beer/social days the recurring miss; "
                "matters more now for muscle retention in the deficit).<br/>"
                "<b>Weight watch:</b> confirm Aug 3's 189.4 (camp bloat) settles to 185-186 within days.",
                small_style,
            ),
            Paragraph(
                "<b>REHAB (daily):</b><br/>"
                "TKEs 3x15 each leg with band<br/>"
                "Iso wrist hold left 10 lb x 30s (elbow holding at top of arc -- no flare)<br/>"
                "<i>Full strength returns next week; this week stays light to protect the two tests.</i>",
                small_style,
            ),
        ],
    ]
    nutri_table = Table(nutri, colWidths=[3.55 * inch, 3.55 * inch])
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
        "Fresh (form +20) | tests set real FTP + VDOT zones | deficit back on (fall lever) | "
        "LOCK a half mid-Oct-mid-Nov | Coach: Claude",
        ParagraphStyle("Footer", parent=tiny_style, alignment=TA_CENTER, textColor=HexColor("#666666")),
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plans/2026-08-03-fall-kickoff-testing-week.pdf"
    build_pdf(output)
