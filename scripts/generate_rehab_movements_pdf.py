"""Generate the Left-Side Rehab Movement Reference PDF.

Standalone reference, not tied to a weekly plan. Roger keeps this on hand
during strength sessions for the left knee (post-ACL 2007) and left elbow
(Jan 2026 overuse) rehab movements.
"""

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
        topMargin=0.4 * inch,
        bottomMargin=0.35 * inch,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title2", parent=styles["Title"], fontSize=16, spaceAfter=2,
        textColor=HexColor("#1a1a1a"),
    )
    subtitle_style = ParagraphStyle(
        "Subtitle2", parent=styles["Normal"], fontSize=9.5,
        textColor=HexColor("#555555"), spaceAfter=6, alignment=TA_CENTER,
    )
    section_style = ParagraphStyle(
        "Section", parent=styles["Heading2"], fontSize=12,
        spaceBefore=8, spaceAfter=4, textColor=HexColor("#2c3e50"),
    )
    move_name = ParagraphStyle(
        "MoveName", parent=styles["Normal"], fontSize=11,
        textColor=white, fontName="Helvetica-Bold", spaceAfter=0,
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"], fontSize=9, leading=11.5,
        spaceAfter=2,
    )
    small_style = ParagraphStyle(
        "Small", parent=styles["Normal"], fontSize=8.5, leading=10.5,
        spaceAfter=1,
    )
    tiny_style = ParagraphStyle(
        "Tiny", parent=styles["Normal"], fontSize=8, leading=10,
        textColor=HexColor("#555555"),
    )

    story = []

    # ==================== HEADER ====================
    story.append(Paragraph("Left-Side Rehab Movement Reference", title_style))
    story.append(Paragraph(
        "Left knee (post-ACL 2007, persistent VMO weakness) | Left elbow (Jan 2026, chronic tendinopathy) | "
        "6-8 week build. Pain &lt;4/10 OK; spikes or lingers &gt;24h = back off.",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#2c3e50")))
    story.append(Spacer(1, 6))

    # ==================== KNEE SECTION ====================
    story.append(Paragraph("LEFT KNEE -- VMO / quad reactivation", section_style))

    # Movement card builder
    def movement_card(name, when, targets, setup, execution, sets_reps, cues):
        header = Table(
            [[Paragraph(name, move_name), Paragraph(f"<font color='white'>{when}</font>", small_style)]],
            colWidths=[3.5 * inch, 4.0 * inch],
        )
        header.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#2c3e50")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))

        body = Table([
            [Paragraph(f"<b>Targets:</b> {targets}", small_style)],
            [Paragraph(f"<b>Setup:</b> {setup}", small_style)],
            [Paragraph(f"<b>Execution:</b> {execution}", small_style)],
            [Paragraph(f"<b>Sets x Reps:</b> {sets_reps}", small_style)],
            [Paragraph(f"<b>Cues / Watch:</b> {cues}", small_style)],
        ], colWidths=[7.5 * inch])
        body.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f9f9f9")),
            ("GRID", (0, 0), (-1, -1), 0.3, HexColor("#dddddd")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        return [header, body, Spacer(1, 6)]

    # TKE
    for el in movement_card(
        "1. Terminal Knee Extension (TKE)",
        "Mon (Push) warm-up + daily option",
        "VMO (vastus medialis) -- the teardrop muscle just above inner knee. Directly trains the quad fibers that ACL surgery weakens.",
        "Loop a band around something stable at knee height (door anchor, squat rack, sturdy table leg). Step into the loop so the band is behind the back of your knee. Step back until there's tension. Stand on the leg being worked.",
        "Start with knee SLIGHTLY bent (not locked). Push knee to full lockout, squeeze quad hard, hold 1 second. Slow return. Don't let knee buckle in or out.",
        "3 x 15 each leg. Light tension band (purple or yellow). Can do daily if you want -- it's that low-risk.",
        "You should feel it in the quad just above the kneecap. If you feel it in the hamstring or calf, foot position is wrong. <b>No pain at lockout.</b>",
    ):
        story.append(el)

    # Spanish squat
    for el in movement_card(
        "2. Isometric Spanish Squat",
        "Sat (Full body) -- first movement, before goblet squats",
        "VMO + quad activation. Pre-fires the muscle group so heavier work later in the session actually recruits the weak side.",
        "Stand with feet shoulder-width. Place a mini-band/hip circle around your shins, just below the knees. Drive knees OUT against the band (band tension stays the whole time).",
        "Squat back like sitting in a chair, knees bending to ~70 degrees. Keep driving knees out against band. Chest up. Hold the position.",
        "3 x 30 seconds. Rest 30 sec between. Add 5-10 sec when 30s feels easy.",
        "If you can't feel the quad burning by 20 seconds, knees aren't pushing out hard enough into the band. <b>Burning quad = good. Knee joint pain = bad.</b>",
    ):
        story.append(el)

    # Box step-up
    for el in movement_card(
        "3. Box Step-up (replaces split squats for now)",
        "Sat (Full body)",
        "Quad strength under load with symmetric loading. Lets the left side catch up without the asymmetry penalty of split squats.",
        "Box, sturdy bench, or stair step at 10-12 inches high. Stand facing it with a DB in each hand. Same weight both sides (start at 20 lb each).",
        "Step up onto the box with one foot. <b>Drive through the working heel.</b> Don't push off the back foot -- it's just there for balance. Stand fully upright on top. Slow controlled step down.",
        "3 x 8 each leg. Lead with LEFT leg. When form is clean on both sides, bump both weights together (25 lb each, then 30 lb).",
        "If the back leg is doing the work, the box is too high OR you're pushing off it. <b>Knee tracks over the middle toes, not collapsing in.</b> Box height: knee should be at 90 degrees or less at the bottom.",
    ):
        story.append(el)

    story.append(PageBreak())

    # ==================== ELBOW SECTION ====================
    story.append(Paragraph("Left-Side Rehab Movement Reference (page 2)", title_style))
    story.append(Paragraph(
        "Left elbow movements + pain rules + progression timeline",
        subtitle_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#2c3e50")))
    story.append(Spacer(1, 6))

    story.append(Paragraph("LEFT ELBOW -- chronic tendinopathy", section_style))

    # Isometric wrist hold
    for el in movement_card(
        "4. Isometric Wrist Hold",
        "Daily option (2 min at desk)",
        "Forearm tendon (flexor or extensor depending on palm direction). Isometric loading is gold standard for chronic tendinopathy -- it stimulates remodeling without aggravating the tendon.",
        "Sit or stand. DB in left hand (start at 5 lb, work to 10 lb). Arm fully extended out in front of you, elbow locked straight.",
        "Hold the position for 30 seconds. Wrist stays neutral (not flexed up or down). <b>Palm direction depends on where your elbow hurts:</b> palm UP if pain is on the inside of elbow (medial / 'golfer's elbow'); palm DOWN if pain is on the outside (lateral / 'tennis elbow').",
        "3 x 30 seconds. Rest 30 sec between. Do 3-5 days/week. Builds tendon capacity -- safe to do often.",
        "Mild discomfort during the hold (1-3/10) is normal and OK. Sharp pain or pain that lingers next day = lighter weight.",
    ):
        story.append(el)

    # Chest-supported row
    for el in movement_card(
        "5. Chest-Supported DB Row (replaces bent-over row)",
        "Fri (Pull)",
        "Lats/rhomboids/rear delts. Removes spinal load and prevents using body english to favor the right side. Forces bilateral effort.",
        "Lay face down on a bench (or angled bench if you have one -- even an ironing board braced against couch works). DB in each hand, arms hanging straight down.",
        "Pull both DBs up to ribs simultaneously. Squeeze shoulder blades together at the top. Slow lower. <b>Both arms move at the same speed</b> -- if right gets ahead, drop weight.",
        "3 x 10. Start with whatever weight lets LEFT arm match right arm's tempo. That's the real working weight.",
        "If left arm moves slower or lags, you're working too heavy. Lighter weight that moves symmetrically &gt;&gt; heavier weight that doesn't.",
    ):
        story.append(el)

    # Slow eccentric hammer curl
    for el in movement_card(
        "6. Slow Eccentric Hammer Curl",
        "Fri (Pull) -- bias left",
        "Brachioradialis + biceps + elbow tendon remodeling. Eccentric (lowering) phase is the gold-standard tendon stimulus.",
        "DB in each hand, palms facing each other (hammer grip). Stand tall, elbows at sides.",
        "Curl up at normal speed (1 second). <b>Lower for 3 full seconds -- count Mississippi 1, Mississippi 2, Mississippi 3.</b> The slow lower is the whole point.",
        "<b>Left: 4 x 8</b> (extra set). Right: 3 x 8. Same weight both sides (10-15 lb to start). Slow eccentric makes light weight legitimately hard.",
        "If you can't control the 3-second lower, weight is too heavy. Faster lower = no tendon stimulus. Patience > weight here.",
    ):
        story.append(el)

    # Pain rules + Progression box
    story.append(Spacer(1, 4))
    rules_data = [
        [Paragraph("<b>PAIN RULES (chronic tendinopathy)</b>", small_style)],
        [Paragraph(
            "&bull; During the movement: pain &lt;4/10 is OK. Continue.<br/>"
            "&bull; After the movement: should feel normal within 24 hours.<br/>"
            "&bull; If pain spikes &gt;4/10 OR lingers next day: drop the weight by 50% next session.<br/>"
            "&bull; If still hurting at lighter weight: skip that movement that week, isometric only.",
            small_style,
        )],
    ]
    rules_table = Table(rules_data, colWidths=[7.5 * inch])
    rules_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), HexColor("#c0392b")),
        ("TEXTCOLOR", (0, 0), (0, 0), white),
        ("BACKGROUND", (0, 1), (0, 1), HexColor("#fcebea")),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#c0392b")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(rules_table)
    story.append(Spacer(1, 6))

    # Progression timeline
    story.append(Paragraph("PROGRESSION TIMELINE", section_style))
    timeline_data = [
        [Paragraph("<b>Weeks 1-2</b>", small_style),
         Paragraph("Movements feel weird; weak side feels like nothing's happening. Normal -- don't add weight.", small_style)],
        [Paragraph("<b>Weeks 3-4</b>", small_style),
         Paragraph("Left side starts feeling 'present' -- you feel the muscle working, not just executing. Neural adaptation showing up.", small_style)],
        [Paragraph("<b>Weeks 5-6</b>", small_style),
         Paragraph("Loading becomes possible on the left. Start bumping weight on step-ups in matched fashion. Knee can handle tempo split squats again.", small_style)],
        [Paragraph("<b>Week 8+</b>", small_style),
         Paragraph("Split squats back in. Asymmetry should be narrowing (not gone -- narrowing).", small_style)],
        [Paragraph("<b>Week 6 gate</b>", small_style),
         Paragraph("<b>If no measurable change in left knee step-ups or elbow loading by week 6 (~July 4): see a sports PT.</b> May need hands-on work to unlock specific deficits.", small_style)],
    ]
    timeline_table = Table(timeline_data, colWidths=[0.9 * inch, 6.6 * inch])
    timeline_table.setStyle(TableStyle([
        ("BACKGROUND", (0, -1), (-1, -1), HexColor("#fff3cd")),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(timeline_table)

    # Footer
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#cccccc")))
    story.append(Paragraph(
        "Equipment needed: 1 long loop band (light/yellow or purple) for TKEs | 1 mini-band/hip circle for Spanish squats | "
        "10-12 inch box/step/bench | DBs 10-30 lb | Coach: Claude",
        ParagraphStyle("Footer", parent=tiny_style, alignment=TA_CENTER, textColor=HexColor("#888888")),
    ))

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "weekly-plans/left-side-rehab-movements.pdf"
    build_pdf(output)
