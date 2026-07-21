"""Generate printable weekly plan PDF for Week of Jul 20-25 (BR100 RACE WEEK).

Single page, B&W laser printer friendly (light gray headers, bold black text).
Race week: arriving fresh (form +21). Job = stay sharp, don't go flat.
BR100 Leg 8 (12.3 mi trail, +1,144 ft) ~2 AM Sat Jul 25 -- night run, adaptive timing.
Includes race-night protocol + conditions + gear checklist (race-week PDF).
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
    story.append(Paragraph("Week of Jul 20-25 -- BR100 RACE WEEK", title_style))
    story.append(Paragraph(
        "Arriving FRESH -- form +21. This week: stay sharp, don't go flat (no more building). "
        "BR100 Leg 8: 12.3 mi trail, +1,144 ft, ~2 AM Sat Jul 25 -- NIGHT run, adaptive timing.",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#000000")))
    story.append(Spacer(1, 3))

    # ==================== DAILY SCHEDULE ====================
    story.append(Paragraph("DAILY SCHEDULE", section_style))

    schedule_rows = [
        ("Mon Jul 20", "DONE -- core + rehab (iso wrist hold up to 10 lb).", False),
        ("Tue Jul 21", "Easy 3 mi + 4 x 20s strides. Easy HR, quick feet. Primer, not a workout.", True),
        ("Wed Jul 22", "Easy 2-3 mi OR short easy spin -- whatever feels good. + rehab.", False),
        ("Thu Jul 23", "Rest + rehab. STAGE GEAR: charge headlamp, batteries, pre-mix fuel.", False),
        ("Fri Jul 24", "2 mi shakeout + 2-3 strides, then done. BANK SLEEP tonight -- the one that matters.", True),
        ("Sat Jul 25", "RACE. Leg 8 ~2 AM (adaptive). Fuel across day, nap/sleep per timing, warm up at exchange.", True),
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

    # ============ STAY SHARP + CONDITIONS (2-col) ============
    twocol = [
        [
            Paragraph(
                "<b>WHY SO LIGHT -- STAY SHARP</b><br/>"
                "Form is already +21 -- maximally fresh. The risk now is going <b>FLAT, not tired.</b> "
                "Five days of pure rest = sluggish legs at 2 AM. So keep <b>light turnover</b> (strides, "
                "a few pickups) to stay primed. No volume, no intensity, no heavy lower. The work is banked.",
                small_style,
            ),
            Paragraph(
                "<b>RACE CONDITIONS (fcst Jul 20 -- check daily)</b><br/>"
                "Night ~<b>64&deg;F</b>, humidity 81%, wind light 5 mph. <b>COOL = your advantage</b> (heat's been "
                "the limiter all summer). 34% PM showers -> trail may be <b>damp/slick</b>. Moonset 2:14 AM = "
                "headlamp does all the work. <b>AIR: AQI 86 Moderate + Smoke Alert (PM2.5)</b> -- watch daily; "
                "if Unhealthy race night, back off. Fun relay -- lungs &gt; time.",
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

    # ==================== RACE-NIGHT PROTOCOL ====================
    story.append(Paragraph("RACE NIGHT -- ADAPTIVE PROTOCOL (Leg 8, ~2 AM)", section_style))
    protocol = [
        [
            Paragraph(
                "<b>TIMING (adaptive -- do NOT fix on a clock):</b><br/>"
                "Est. ~2:15 AM, real range 11 PM-4 AM. 7 runners / 88 mi ahead -- estimate errors compound. "
                "<b>Track the team's actual splits.</b> Steve (leg 7, ~11 PM, 14.4 mi) is your direct predictor -- "
                "once he's a few mi in, you know your window +/-30 min. Heat/smoke slowing earlier legs pushes "
                "you LATER = cooler + possibly cleaner air.<br/><br/>"
                "<b>SLEEP (home -- own bed):</b> Fri night = bank real sleep. Sat = sleep in + rest. Late start (3-5 AM): get a "
                "genuine sleep BLOCK first (down ~9-10 PM, wake off team progress). Early (~midnight): afternoon nap instead.",
                small_style,
            ),
            Paragraph(
                "<b>FUEL:</b> normal meals + hydrate all day. Carb-based dinner a few hrs pre. Light easy carbs "
                "1-1.5 hr before (NOT a big 1 AM meal). On course: <b>4.5 scoops Tailwind / 1.5L + SiS gels</b> "
                "(touch more fluid -- 81% humidity).<br/>"
                "<b>CAFFEINE:</b> SiS caffeine gel 30-45 min pre-start for the 2-4 AM low. Don't overdo.<br/>"
                "<b>DRIVE/ARRIVE:</b> race ~45 min from home. Work backward from est. start: ~45 min drive + arrive "
                "30-45 min early + warm-up = leave ~1.5 hr before your window (e.g. 2 AM start -> out the door ~12:30 AM).<br/>"
                "<b>WARM-UP:</b> dynamic warm-up + a few strides at the exchange (cold/stiff at 2 AM).<br/>"
                "<b>PACING/HR:</b> dark + damp + 59% unpaved -> <b>conservative opening third</b> til eyes/footing adapt. "
                "Then <b>&lt;145 / &lt;148 (climb mi 7-8, let it spike, settle on descent) / last third let it rip</b> (cool air = real upside).",
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

    # ==================== GEAR CHECKLIST ====================
    story.append(Paragraph("GEAR CHECKLIST", section_style))
    story.append(Paragraph(
        "[ ] Headlamp charged (test 2.5+ hr burn)  [ ] Backup light + spare batteries  [ ] SiS gels incl "
        "caffeine gel  [ ] Tailwind 4.5 scoops pre-mixed 1.5L  [ ] Trail shoes  [ ] Light layer (64&deg; + damp)  "
        "[ ] Phone charged (team tracking)  [ ] Watch charged",
        small_style,
    ))

    # Footer
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
    story.append(Paragraph(
        "Form +21 (fresh) | run HR cap taper | RACE HR: 1st third &lt;145 / mid &lt;148 / last third rip | "
        "Fuel 4.5 scoops Tailwind + 1.5L + SiS | Coach: Claude",
        ParagraphStyle("Footer", parent=tiny_style, alignment=TA_CENTER, textColor=HexColor("#666666")),
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plans/2026-07-20-br100-race-week.pdf"
    build_pdf(output)
