# ==========================================
# InfraLens Security Score
# ==========================================


def calculate_security_score(asset_inventory, findings):
    score = 100
    reasons = []

    # ==========================================
    # Gerätebewertung
    # ==========================================

    for asset in asset_inventory:

        risk = asset.get("risk", "Low")

        if risk == "Critical":
            score -= 20
            reasons.append(
                f"Critical Risk: {asset['ip']}"
            )

        elif risk == "High":
            score -= 10
            reasons.append(
                f"High Risk: {asset['ip']}"
            )

        elif risk == "Medium":
            score -= 5

    # ==========================================
    # Findings
    # ==========================================

    for finding in findings:

        risk = finding.get("risk", "Low")

        if risk == "Critical":
            score -= 5

        elif risk == "High":
            score -= 3

        elif risk == "Medium":
            score -= 1

    # ==========================================
    # Untergrenze
    # ==========================================

    if score < 0:
        score = 0

    # ==========================================
    # Bewertung
    # ==========================================

    if score >= 90:
        level = "Excellent"

    elif score >= 80:
        level = "Good"

    elif score >= 60:
        level = "Needs Improvement"

    elif score >= 40:
        level = "High Risk"

    else:
        level = "Critical"

    return {
        "score": score,
        "level": level,
        "reasons": reasons
    }