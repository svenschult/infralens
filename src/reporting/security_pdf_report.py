import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    Image
)

from reporting.report_charts import (
    create_risk_distribution_chart,
    create_asset_role_chart,
    create_os_distribution_chart
)


def create_security_pdf_report(
    output_path,
    target_info,
    asset_inventory,
    action_plan,
    scan_context,
    management_intelligence,
    executive_actions
):
    # Zielordner erstellen
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # PDF vorbereiten
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    normal = styles["BodyText"]
    normal.wordWrap = "CJK"

    small = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontSize=8,
        leading=10,
        wordWrap="CJK"
    )

    score_style = ParagraphStyle(
        "ScoreStyle",
        parent=styles["Title"],
        fontSize=28,
        leading=34,
        alignment=1
    )

    story = []
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    # Deckblatt
    logo_path = os.path.join("assets", "logo", "infralens_logo.png")

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=280, height=173)
        logo.hAlign = "CENTER"
        story.append(logo)

    story.append(Spacer(1, 20))
    story.append(Paragraph("InfraLens Security Assessment", styles["Title"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Infrastructure & Security Analysis Report", styles["Heading2"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Erstellt am: {now}", normal))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Vertrauliches Dokument", normal))
    story.append(Spacer(1, 200))
    story.append(Paragraph("Erstellt mit InfraLens", normal))
    story.append(PageBreak())

    # Management Summary
    story.append(Paragraph("1. Management Summary", styles["Heading2"]))
    story.append(Spacer(1, 10))

    score = management_intelligence.get("score", 0)
    level = management_intelligence.get("level", "Unbekannt")
    potential_score = management_intelligence.get("potential_score", score)
    improvement = management_intelligence.get("improvement_potential", 0)
    summary = management_intelligence.get("summary", "")

    story.append(Paragraph("InfraLens Security Index", styles["Heading2"]))
    story.append(Paragraph(f"{score} / 100", score_style))
    story.append(Paragraph(f"Bewertung: {level}", styles["Heading3"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(create_score_bar(score), normal))
    story.append(Spacer(1, 16))
    story.append(Paragraph(summary, normal))
    story.append(Spacer(1, 20))

    # Verbesserungspotenzial
    story.append(Paragraph("Verbesserungspotenzial", styles["Heading3"]))

    potential_data = [
        [Paragraph("Aktueller Index", small), Paragraph(f"{score} / 100", small)],
        [Paragraph("Möglicher Index nach Umsetzung", small), Paragraph(f"{potential_score} / 100", small)],
        [Paragraph("Potenzielle Verbesserung", small), Paragraph(f"+{improvement} Punkte", small)]
    ]

    potential_table = Table(potential_data, colWidths=[250, 160])
    potential_table.setStyle(default_table_style())
    story.append(potential_table)
    story.append(PageBreak())

    # Executive Action Center
    story.append(Paragraph("2. Executive Action Center", styles["Heading2"]))
    story.append(Spacer(1, 10))

    action_intro = (
        "Diese Übersicht zeigt die wichtigsten Maßnahmen, die aus Management-Sicht "
        "zuerst betrachtet werden sollten. Die Maßnahmen wurden nach Priorität, "
        "Sicherheitsgewinn und geschätztem Aufwand eingeordnet."
    )

    story.append(Paragraph(action_intro, normal))
    story.append(Spacer(1, 16))

    if executive_actions:
        for index, action in enumerate(executive_actions, start=1):
            action_block = []

            title = (
                f"{index}. {action.get('priority', 'Unbekannt')} - "
                f"{action.get('title', 'Keine Maßnahme')}"
            )

            action_block.append(Paragraph(title, styles["Heading3"]))

            action_data = [
                [
                    Paragraph("Gerät", small),
                    Paragraph(
                        f"{action.get('device', 'Unbekannt')} "
                        f"({action.get('ip', 'Unbekannt')})",
                        small
                    )
                ],
                [
                    Paragraph("Geschäftsrisiko", small),
                    Paragraph(action.get("business_risk", "Unbekannt"), small)
                ],
                [
                    Paragraph("Geschätzter Aufwand", small),
                    Paragraph(action.get("effort", "Unbekannt"), small)
                ],
                [
                    Paragraph("Sicherheitsgewinn", small),
                    Paragraph(f"+{action.get('security_gain', 0)} Punkte", small)
                ],
                [
                    Paragraph("Status", small),
                    Paragraph(action.get("status", "Offen"), small)
                ],
                [
                    Paragraph("Grund", small),
                    Paragraph(action.get("reason", "Keine Begründung"), small)
                ]
            ]

            action_table = Table(action_data, colWidths=[140, 330])
            action_table.setStyle(default_table_style())

            action_block.append(action_table)
            action_block.append(Spacer(1, 14))

            story.append(KeepTogether(action_block))
    else:
        story.append(Paragraph("Keine priorisierten Executive Actions erkannt.", normal))

    story.append(PageBreak())

    # Management Dashboard
    story.append(Paragraph("3. Management Dashboard", styles["Heading2"]))
    story.append(Spacer(1, 10))

    risk_chart_path = create_risk_distribution_chart(asset_inventory)
    role_chart_path = create_asset_role_chart(asset_inventory)
    os_chart_path = create_os_distribution_chart(asset_inventory)

    story.append(Paragraph("Risikoverteilung", styles["Heading3"]))
    risk_chart = Image(risk_chart_path, width=300, height=300)
    risk_chart.hAlign = "CENTER"
    story.append(risk_chart)

    story.append(Spacer(1, 18))

    story.append(Paragraph("Geräte-Rollen", styles["Heading3"]))
    role_chart = Image(role_chart_path, width=430, height=250)
    role_chart.hAlign = "CENTER"
    story.append(role_chart)

    story.append(PageBreak())

    story.append(Paragraph("Betriebssystem-Verteilung", styles["Heading3"]))
    os_chart = Image(os_chart_path, width=430, height=250)
    os_chart.hAlign = "CENTER"
    story.append(os_chart)

    story.append(Spacer(1, 20))

    # Top Abzüge
    story.append(Paragraph("Wichtigste Gründe für Punktabzug", styles["Heading3"]))

    deductions = management_intelligence.get("deductions", [])

    if deductions:
        deduction_data = [
            [
                Paragraph("Kategorie", small),
                Paragraph("Punkte", small),
                Paragraph("Begründung", small)
            ]
        ]

        for deduction in deductions[:8]:
            deduction_data.append([
                Paragraph(deduction.get("category", "Unbekannt"), small),
                Paragraph(f"-{deduction.get('points', 0)}", small),
                Paragraph(deduction.get("reason", "Keine Begründung"), small)
            ])

        deduction_table = Table(deduction_data, colWidths=[110, 60, 300], repeatRows=1)
        deduction_table.setStyle(header_table_style())
        story.append(deduction_table)
    else:
        story.append(Paragraph("Keine relevanten Punktabzüge erkannt.", normal))

    story.append(PageBreak())

    # Executive Summary
    story.append(Paragraph("4. Executive Summary", styles["Heading2"]))

    summary_text = (
        "Dieser Bericht fasst die wichtigsten Ergebnisse der Infrastruktur- "
        "und Security-Analyse zusammen. Der Fokus liegt auf erkannten Geräten, "
        "Risiken und priorisierten Maßnahmen."
    )

    story.append(Paragraph(summary_text, normal))
    story.append(Spacer(1, 12))

    # Scan-Kontext
    story.append(Paragraph("5. Scan-Kontext", styles["Heading2"]))

    scan_context_data = [
        [
            Paragraph("Prüfgerät / Scan-System", small),
            Paragraph(scan_context.get("scanner_ip", "Unbekannt"), small)
        ],
        [
            Paragraph("Rolle", small),
            Paragraph(scan_context.get("scanner_role", "Unbekannt"), small)
        ],
        [
            Paragraph("Hinweis", small),
            Paragraph(scan_context.get("note", "Keine Hinweise"), small)
        ]
    ]

    scan_context_table = Table(scan_context_data, colWidths=[150, 320])
    scan_context_table.setStyle(default_table_style())

    story.append(scan_context_table)
    story.append(Spacer(1, 20))

    # Zielsystem
    story.append(Paragraph("6. Zielsystem / Scan-Kontext", styles["Heading2"]))

    target_data = [
        [Paragraph("Primärer Host", small), Paragraph(target_info.get("ip", "Unbekannt"), small)],
        [Paragraph("Hostname", small), Paragraph(target_info.get("hostname", "Unbekannt"), small)],
        [Paragraph("Betriebssystem", small), Paragraph(target_info.get("os", "Unbekannt"), small)],
        [Paragraph("MAC / Hersteller", small), Paragraph(target_info.get("mac", "Unbekannt"), small)]
    ]

    target_table = Table(target_data, colWidths=[130, 330])
    target_table.setStyle(default_table_style())

    story.append(target_table)
    story.append(Spacer(1, 20))

    # Risikoübersicht
    story.append(Paragraph("7. Risikoübersicht", styles["Heading2"]))

    risk_count = count_asset_risks(asset_inventory)

    risk_data = [
        [Paragraph("Risikostufe", small), Paragraph("Anzahl Geräte", small)],
        [Paragraph("Critical", small), Paragraph(str(risk_count["Critical"]), small)],
        [Paragraph("High", small), Paragraph(str(risk_count["High"]), small)],
        [Paragraph("Medium", small), Paragraph(str(risk_count["Medium"]), small)],
        [Paragraph("Low", small), Paragraph(str(risk_count["Low"]), small)]
    ]

    risk_table = Table(risk_data, colWidths=[220, 120])
    risk_table.setStyle(header_table_style())

    story.append(risk_table)
    story.append(Spacer(1, 20))

    # Maßnahmenplan
    story.append(Paragraph("8. Priorisierter Maßnahmenplan", styles["Heading2"]))

    if action_plan:
        action_data = [
            [
                Paragraph("Priorität", small),
                Paragraph("Gerät", small),
                Paragraph("Maßnahme", small),
                Paragraph("Status", small)
            ]
        ]

        for action in action_plan:
            device = (
                f"{action.get('hostname', 'Unbekannt')} "
                f"({action.get('ip', 'Unbekannt')})"
            )

            action_data.append([
                Paragraph(action.get("priority", "Unbekannt"), small),
                Paragraph(device, small),
                Paragraph(action.get("title", "Keine Maßnahme"), small),
                Paragraph(action.get("status", "Offen"), small)
            ])

        action_table = Table(action_data, colWidths=[60, 120, 260, 50], repeatRows=1)
        action_table.setStyle(header_table_style())
        story.append(action_table)
    else:
        story.append(Paragraph("Keine priorisierten Maßnahmen erkannt.", normal))

    story.append(PageBreak())

    # Geräte-Inventarliste
    story.append(Paragraph("9. Geräte-Inventarliste", styles["Heading2"]))
    story.append(Spacer(1, 8))

    if asset_inventory:
        for asset in asset_inventory:
            asset_block = []

            title = (
                f"{asset.get('ip', 'Unbekannt')} "
                f"- Risiko: {asset.get('risk', 'Unbekannt')}"
            )

            asset_block.append(Paragraph(title, styles["Heading3"]))

            roles = ", ".join(asset.get("roles", []))
            if not roles:
                roles = "Unbekannt"

            asset_data = [
                [Paragraph("Hostname", small), Paragraph(asset.get("hostname", "Unbekannt"), small)],
                [Paragraph("Betriebssystem", small), Paragraph(asset.get("os", "Unbekannt"), small)],
                [Paragraph("MAC / Hersteller", small), Paragraph(asset.get("mac", "Unbekannt"), small)],
                [Paragraph("Rollen", small), Paragraph(roles, small)]
            ]

            asset_table = Table(asset_data, colWidths=[120, 350])
            asset_table.setStyle(default_table_style())

            asset_block.append(asset_table)
            asset_block.append(Spacer(1, 8))
            asset_block.append(Paragraph("Risikogründe:", normal))

            for reason in asset.get("risk_reasons", []):
                asset_block.append(Paragraph(f"- {reason}", small))

            asset_block.append(Spacer(1, 6))
            asset_block.append(Paragraph("Empfohlene Maßnahmen:", normal))

            for recommendation in asset.get("recommendations", []):
                asset_block.append(Paragraph(f"- {recommendation}", small))

            asset_block.append(Spacer(1, 12))

            story.append(KeepTogether(asset_block))
    else:
        story.append(Paragraph("Keine Geräte erkannt.", normal))

    story.append(PageBreak())

    # Hinweis
    story.append(Paragraph("Hinweis", styles["Heading2"]))

    note = (
        "Dieser Bericht dient der technischen Orientierung und Dokumentation "
        "in einer kontrollierten oder autorisierten Umgebung. Er ersetzt keine "
        "vollständige rechtliche oder organisatorische Sicherheitsprüfung."
    )

    story.append(Paragraph(note, normal))

    # PDF schreiben
    doc.build(story)

    # Temporäre Diagramme entfernen
    cleanup_chart_files([
        risk_chart_path,
        role_chart_path,
        os_chart_path
    ])


def create_score_bar(score):
    filled_blocks = int(score / 10)
    empty_blocks = 10 - filled_blocks

    return "█" * filled_blocks + "░" * empty_blocks


def count_asset_risks(asset_inventory):
    risk_count = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for asset in asset_inventory:
        risk = asset.get("risk", "Low")

        if risk in risk_count:
            risk_count[risk] += 1

    return risk_count


def default_table_style():
    return TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP")
    ])


def header_table_style():
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP")
    ])


def cleanup_chart_files(chart_paths):
    for chart_path in chart_paths:
        try:
            if os.path.exists(chart_path):
                os.remove(chart_path)
        except Exception:
            pass
