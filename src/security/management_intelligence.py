# ==========================================
# InfraLens Management Intelligence Engine
# ==========================================


def calculate_infralens_security_index(asset_inventory, action_plan):
    # Startwert
    score = 100

    deductions = []
    improvement_potential = 0

    # Gerätebasierte Bewertung
    for asset in asset_inventory:
        risk = asset.get("risk", "Low")
        ip = asset.get("ip", "Unbekannt")
        hostname = asset.get("hostname", "Unbekannt")
        os_info = asset.get("os", "Unbekannt")

        if risk == "Critical":
            score -= 20
            improvement_potential += 20

            deductions.append({
                "category": "Geräterisiko",
                "points": 20,
                "reason": f"Kritisches Gerät erkannt: {hostname} ({ip})",
                "detail": os_info
            })

        elif risk == "High":
            score -= 10
            improvement_potential += 10

            deductions.append({
                "category": "Geräterisiko",
                "points": 10,
                "reason": f"Hohes Risiko erkannt: {hostname} ({ip})",
                "detail": os_info
            })

        elif risk == "Medium":
            score -= 5
            improvement_potential += 5

            deductions.append({
                "category": "Geräterisiko",
                "points": 5,
                "reason": f"Mittleres Risiko erkannt: {hostname} ({ip})",
                "detail": os_info
            })

    # Maßnahmenplan berücksichtigen
    for action in action_plan:
        priority = action.get("priority", "Low")

        if priority == "Critical":
            improvement_potential += 10

        elif priority == "High":
            improvement_potential += 5

        elif priority == "Medium":
            improvement_potential += 2

    # Score begrenzen
    if score < 0:
        score = 0

    potential_score = score + improvement_potential

    if potential_score > 100:
        potential_score = 100

    return {
        "score": score,
        "level": get_score_level(score),
        "deductions": deductions,
        "potential_score": potential_score,
        "improvement_potential": potential_score - score,
        "summary": create_management_summary(score, asset_inventory, action_plan)
    }


def get_score_level(score):
    if score >= 90:
        return "Sehr gut"

    if score >= 80:
        return "Gut"

    if score >= 60:
        return "Verbesserungsbedarf"

    if score >= 40:
        return "Erhöhtes Risiko"

    return "Kritischer Zustand"


def create_management_summary(score, asset_inventory, action_plan):
    critical_assets = count_assets_by_risk(asset_inventory, "Critical")
    high_assets = count_assets_by_risk(asset_inventory, "High")

    open_actions = len(action_plan)

    summary = (
        f"Der aktuelle InfraLens Security Index liegt bei {score}/100 Punkten. "
    )

    if score >= 80:
        summary += (
            "Die aktuelle Sicherheitslage wirkt grundsätzlich stabil. "
            "Einzelne Verbesserungen sollten dennoch geprüft und dokumentiert werden."
        )

    elif score >= 60:
        summary += (
            "Die Sicherheitslage zeigt erkennbaren Verbesserungsbedarf. "
            "Mehrere Maßnahmen sollten priorisiert umgesetzt werden."
        )

    elif score >= 40:
        summary += (
            "Die Sicherheitslage weist ein erhöhtes Risiko auf. "
            "Kritische und hohe Risiken sollten zeitnah bearbeitet werden."
        )

    else:
        summary += (
            "Die Sicherheitslage ist kritisch. "
            "Eine kurzfristige technische und organisatorische Nachbesserung wird empfohlen."
        )

    summary += (
        f" Es wurden {len(asset_inventory)} bewertete Geräte erfasst. "
        f"Davon weisen {critical_assets} Geräte ein kritisches und "
        f"{high_assets} Geräte ein hohes Risiko auf. "
        f"Der Maßnahmenplan enthält {open_actions} priorisierte Punkte."
    )

    return summary


def count_assets_by_risk(asset_inventory, risk_level):
    count = 0

    for asset in asset_inventory:
        if asset.get("risk") == risk_level:
            count += 1

    return count