from datetime import datetime
from core.ai_assistant import generate_ai_explanation


def count_risks(findings):
    risk_count = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for finding in findings:
        risk = finding.get("risk", "Low")

        if risk in risk_count:
            risk_count[risk] += 1

    return risk_count


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


def create_markdown_report(
    findings,
    output_path,
    target_info,
    attack_paths,
    network_analysis,
    host_inventory,
    topology_notes,
    assets,
    asset_inventory,
    action_plan,
    scan_context,
    management_intelligence
):
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    risk_count = count_risks(findings)
    asset_risk_count = count_asset_risks(asset_inventory)

    score = management_intelligence.get("score", 0)
    level = management_intelligence.get("level", "Unbekannt")
    potential_score = management_intelligence.get("potential_score", score)
    improvement = management_intelligence.get("improvement_potential", 0)
    summary = management_intelligence.get("summary", "")
    deductions = management_intelligence.get("deductions", [])

    content = "# InfraLens Security Assessment Report\n\n"
    content += f"Erstellt am: {now}\n\n"

    content += "---\n\n"

    # Management Summary
    content += "## 1. Management Summary\n\n"
    content += "### InfraLens Security Index\n\n"
    content += f"**{score} / 100**\n\n"
    content += f"**Bewertung:** {level}\n\n"
    content += f"`{create_score_bar(score)}`\n\n"
    content += f"{summary}\n\n"

    content += "### Verbesserungspotenzial\n\n"
    content += f"- Aktueller Index: {score} / 100\n"
    content += f"- Möglicher Index nach Umsetzung: {potential_score} / 100\n"
    content += f"- Potenzielle Verbesserung: +{improvement} Punkte\n\n"

    content += "### Wichtigste Gründe für Punktabzug\n\n"

    if deductions:
        for deduction in deductions[:8]:
            content += (
                f"- {deduction.get('category', 'Unbekannt')}: "
                f"-{deduction.get('points', 0)} Punkte – "
                f"{deduction.get('reason', 'Keine Begründung')}\n"
            )
    else:
        content += "- Keine relevanten Punktabzüge erkannt.\n"

    content += "\n---\n\n"

    # Executive Summary
    content += "## 2. Executive Summary\n\n"
    content += (
        "Dieser Bericht basiert auf einem Netzwerk- und Service-Scan. "
        "Er bewertet erkannte Geräte, offene Dienste, Infrastruktur-Kontext, "
        "mögliche Angriffspfade und defensive Maßnahmen.\n\n"
    )

    content += f"- Bewertete Geräte: {len(asset_inventory)}\n"
    content += f"- Gefundene offene Dienste: {len(findings)}\n\n"

    content += "### Risikoübersicht Geräte\n\n"
    content += f"- Critical Assets: {asset_risk_count['Critical']}\n"
    content += f"- High Assets: {asset_risk_count['High']}\n"
    content += f"- Medium Assets: {asset_risk_count['Medium']}\n"
    content += f"- Low Assets: {asset_risk_count['Low']}\n\n"

    content += "### Risikoübersicht Findings\n\n"
    content += f"- Critical Findings: {risk_count['Critical']}\n"
    content += f"- High Findings: {risk_count['High']}\n"
    content += f"- Medium Findings: {risk_count['Medium']}\n"
    content += f"- Low Findings: {risk_count['Low']}\n\n"

    content += "---\n\n"

    # Scan-Kontext
    content += "## 3. Scan-Kontext\n\n"
    content += f"- Prüfgerät / Scan-System: {scan_context.get('scanner_ip', 'Unbekannt')}\n"
    content += f"- Rolle: {scan_context.get('scanner_role', 'Unbekannt')}\n"
    content += f"- Hinweis: {scan_context.get('note', 'Keine Hinweise')}\n\n"

    content += "---\n\n"

    # Top Risiken
    content += "## 4. Top Risiken & To-do-Liste\n\n"

    top_items_found = False

    for asset in asset_inventory:
        if asset.get("risk") in ["Critical", "High"]:
            top_items_found = True

            content += f"### {asset['risk']} - {asset['ip']}\n\n"
            content += f"- Hostname: {asset['hostname']}\n"
            content += f"- Betriebssystem: {asset['os']}\n"

            content += "- Gründe:\n"
            for reason in asset["risk_reasons"]:
                content += f"  - {reason}\n"

            content += "- Empfohlene Maßnahmen:\n"
            for recommendation in asset["recommendations"]:
                content += f"  - {recommendation}\n"

            content += "\n"

    if not top_items_found:
        content += "Keine Critical- oder High-Risiken in der Gerätebewertung erkannt.\n\n"

    content += "---\n\n"

    # Maßnahmenplan
    content += "## 5. Maßnahmenplan\n\n"

    if action_plan:
        for index, action in enumerate(action_plan, start=1):
            content += f"### {index}. {action['priority']} - {action['title']}\n\n"
            content += f"- Gerät: {action['hostname']} ({action['ip']})\n"
            content += f"- Grund: {action['reason']}\n"
            content += f"- Status: {action['status']}\n\n"
    else:
        content += "Keine priorisierten Maßnahmen erkannt.\n\n"

    content += "---\n\n"

    # Asset Inventar
    content += "## 6. Geräte-Inventarliste\n\n"

    if asset_inventory:
        for asset in asset_inventory:
            content += f"### {asset['ip']}\n\n"
            content += f"- Hostname: {asset['hostname']}\n"
            content += f"- Betriebssystem: {asset['os']}\n"
            content += f"- MAC/Hersteller: {asset['mac']}\n"
            content += f"- Risiko: {asset['risk']}\n"

            content += "- Erkannte Rollen:\n"
            for role in asset["roles"]:
                content += f"  - {role}\n"

            content += "- Risikogründe:\n"
            for reason in asset["risk_reasons"]:
                content += f"  - {reason}\n"

            content += "- Dienste:\n"

            if asset["services"]:
                for service in asset["services"]:
                    content += (
                        f"  - {service['port']} / "
                        f"{service['service']} / "
                        f"{service['state']} / "
                        f"{service['version']}\n"
                    )
            else:
                content += "  - Keine offenen Dienste erkannt\n"

            content += "- Maßnahmen:\n"
            for recommendation in asset["recommendations"]:
                content += f"  - {recommendation}\n"

            content += "\n"
    else:
        content += "Keine Geräte erkannt.\n\n"

    content += "---\n\n"

    # Infrastructure Overview
    content += "## 7. Infrastructure Overview\n\n"
    content += f"- Primäres Ziel / erster Host: {target_info['ip']}\n"
    content += f"- Hostname: {target_info['hostname']}\n"
    content += f"- Betriebssystem: {target_info['os']}\n"
    content += f"- MAC/Hersteller: {target_info['mac']}\n\n"

    content += "### Netzwerk-Analyse\n\n"

    if network_analysis:
        for item in network_analysis:
            content += f"- {item}\n"
    else:
        content += "- Keine Netzwerk-Analyse verfügbar\n"

    content += "\n### Topologie-Hinweise\n\n"

    if topology_notes:
        for note in topology_notes:
            content += f"- {note}\n"
    else:
        content += "- Keine Topologie-Hinweise verfügbar\n"

    content += "\n---\n\n"

    # Security Findings
    content += "## 8. Security Findings\n\n"

    for finding in findings:
        content += f"### Port {finding['port']} - {finding['service']}\n\n"
        content += f"- Status: {finding['state']}\n"
        content += f"- Version: {finding['version']}\n"
        content += f"- Risiko: {finding['risk']}\n"
        content += f"- Priorität: {finding['priority']}\n"
        content += f"- Empfehlung: {finding['recommendation']}\n"
        content += f"- Security-Hinweis: {finding['pentest_hint']}\n"
        content += f"- KI-Erklärung: {generate_ai_explanation(finding)}\n"

        if finding.get("notes"):
            content += "- Hinweise:\n"

            for note in finding["notes"]:
                content += f"  - {note}\n"

        content += "\n"

    content += "---\n\n"

    # Attack Path Simulation
    content += "## 9. Attack Path Simulation\n\n"

    if attack_paths:
        for path in attack_paths:
            content += f"### {path['service']}\n\n"
            content += "Möglicher Angreiferpfad:\n\n"

            for step in path["attack_path"]:
                content += f"- {step}\n"

            content += "\n"
    else:
        content += "Keine spezifischen Angriffspfade erkannt.\n\n"

    content += "---\n\n"

    # Defensive Recommendations
    content += "## 10. Defensive Recommendations\n\n"

    if attack_paths:
        for path in attack_paths:
            content += f"### {path['service']}\n\n"

            for defense in path["defense"]:
                content += f"- {defense}\n"

            content += "\n"
    else:
        content += "Keine spezifischen defensiven Maßnahmen abgeleitet.\n\n"

    content += "---\n\n"

    # Next Steps
    content += "## 11. Next Steps\n\n"
    content += "- Critical- und High-Risiken priorisiert bearbeiten\n"
    content += "- Veraltete Betriebssysteme ersetzen oder isolieren\n"
    content += "- Router- und Firmware-Versionen prüfen\n"
    content += "- Nicht benötigte Dienste deaktivieren\n"
    content += "- Netzwerksegmentierung bewerten\n"
    content += "- Hardening-Maßnahmen dokumentieren\n"
    content += "- Nach Änderungen erneuten Scan durchführen\n\n"

    content += "---\n\n"

    # Hinweis
    content += "## Hinweis\n\n"
    content += (
        "Dieser Bericht dient ausschließlich der Analyse in einer kontrollierten "
        "Homelab- oder autorisierten Umgebung.\n"
    )

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content)


def create_score_bar(score):
    filled_blocks = int(score / 10)
    empty_blocks = 10 - filled_blocks

    return "█" * filled_blocks + "░" * empty_blocks