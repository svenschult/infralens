import os
import tempfile

import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)


def create_risk_chart(nis2_statistics):
    labels = []
    sizes = []

    for category, data in nis2_statistics.items():
        if data["count"] > 0:
            labels.append(category)
            sizes.append(data["percentage"])

    if not sizes:
        labels = ["Keine Findings"]
        sizes = [100]

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp_file.close()

    plt.figure(figsize=(6, 6))
    plt.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"width": 0.4}
    )
    plt.title("NIS2-orientierte Risikoverteilung")
    plt.tight_layout()
    plt.savefig(temp_file.name)
    plt.close()

    return temp_file.name


def create_nis2_pdf_report(
    nis2_mapping,
    nis2_statistics,
    target_info,
    output_path
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("InfraLens NIS2 Security Overview Report", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Executive Summary", styles["Heading2"]))
    story.append(Paragraph(
        "Dieser Bericht stellt eine NIS2-orientierte technische Übersicht auf Basis "
        "der erkannten Infrastruktur- und Security-Findings dar. "
        "Er dient als technische Gap-Analyse und ersetzt keine rechtsverbindliche Compliance-Prüfung.",
        styles["BodyText"]
    ))
    story.append(Spacer(1, 16))

    story.append(Paragraph("Zielsystem", styles["Heading2"]))

    target_data = [
        ["Hostname", target_info.get("hostname", "Unbekannt")],
        ["IP-Adresse", target_info.get("ip", "Unbekannt")],
        ["Betriebssystem", target_info.get("os", "Unbekannt")],
        ["MAC/Hersteller", target_info.get("mac", "Unbekannt")]
    ]

    target_table = Table(target_data, colWidths=[120, 350])
    target_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(target_table)
    story.append(Spacer(1, 16))

    story.append(Paragraph("Statistische Übersicht", styles["Heading2"]))

    chart_path = create_risk_chart(nis2_statistics)
    story.append(Image(chart_path, width=320, height=320))
    story.append(Spacer(1, 16))

    stats_data = [["NIS2-Kategorie", "Anzahl", "Anteil"]]

    for category, data in nis2_statistics.items():
        stats_data.append([
            category,
            str(data["count"]),
            f"{data['percentage']} %"
        ])

    stats_table = Table(stats_data, colWidths=[260, 80, 80])
    stats_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(stats_table)
    story.append(PageBreak())

    story.append(Paragraph("NIS2-orientiertes Mapping", styles["Heading2"]))

    for category, items in nis2_mapping.items():
        story.append(Paragraph(category, styles["Heading3"]))

        if items:
            for item in items:
                story.append(Paragraph(f"- {item}", styles["BodyText"]))
        else:
            story.append(Paragraph(
                "- Keine direkten technischen Hinweise aus dem aktuellen Scan erkannt.",
                styles["BodyText"]
            ))

        story.append(Spacer(1, 10))

    story.append(PageBreak())

    story.append(Paragraph("Priorisierte Empfehlungen", styles["Heading2"]))

    recommendations = [
        "Kritische und hohe Risiken priorisiert prüfen.",
        "Zugriffskontrollen und administrative Zugänge überprüfen.",
        "Nicht benötigte Dienste deaktivieren.",
        "Netzwerksegmentierung bewerten.",
        "Monitoring und Incident-Response-Prozesse prüfen.",
        "Backups und Wiederherstellungsprozesse dokumentieren.",
        "Regelmäßige Scans und Vorher/Nachher-Vergleiche durchführen."
    ]

    for recommendation in recommendations:
        story.append(Paragraph(f"- {recommendation}", styles["BodyText"]))

    story.append(Spacer(1, 16))

    story.append(Paragraph("Hinweis", styles["Heading2"]))
    story.append(Paragraph(
        "Dieser Bericht ist eine technische, NIS2-orientierte Einschätzung. "
        "Er stellt keine Rechtsberatung und keine vollständige Compliance-Prüfung dar.",
        styles["BodyText"]
    ))

    doc.build(story)

    try:
        os.remove(chart_path)
    except Exception:
        pass