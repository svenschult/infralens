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


def create_security_pdf_report(
    output_path,
    target_info,
    asset_inventory,
    action_plan
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

    story = []

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    # Deckblatt
    logo_path = os.path.join(
        "assets",
        "logo",
        "infralens_logo.png"
    )

    if os.path.exists(logo_path):
        logo = Image(
            logo_path,
            width=280,
            height=173
        )

        logo.hAlign = "CENTER"

        story.append(logo)

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "InfraLens Security Assessment",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Infrastructure & Security Analysis Report",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Erstellt am: {now}",
            normal
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "Vertrauliches Dokument",
            normal
        )
    )

    story.append(Spacer(1, 200))

    story.append(
        Paragraph(
            "Erstellt mit InfraLens",
            normal
        )
    )

    story.append(PageBreak())

    # Executive Summary
    story.append(Paragraph("1. Executive Summary", styles["Heading2"]))

    summary_text = (
        "Dieser Bericht fasst die wichtigsten Ergebnisse der Infrastruktur- "
        "und Security-Analyse zusammen. Der Fokus liegt auf erkannten Geräten, "
        "Risiken und priorisierten Maßnahmen."
    )

    story.append(Paragraph(summary_text, normal))
    story.append(Spacer(1, 12))

    # Zielsystem
    story.append(Paragraph("2. Zielsystem / Scan-Kontext", styles["Heading2"]))

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
    story.append(Paragraph("3. Risikoübersicht", styles["Heading2"]))

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
    story.append(Paragraph("4. Priorisierter Maßnahmenplan", styles["Heading2"]))

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

        action_table = Table(
            action_data,
            colWidths=[60, 120, 260, 50],
            repeatRows=1
        )
        action_table.setStyle(header_table_style())

        story.append(action_table)

    else:
        story.append(Paragraph("Keine priorisierten Maßnahmen erkannt.", normal))

    story.append(PageBreak())

    # Geräte-Inventarliste
    story.append(Paragraph("5. Geräte-Inventarliste", styles["Heading2"]))
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