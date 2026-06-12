def create_action_plan(asset_inventory):
    action_plan = []

    for asset in asset_inventory:
        risk = asset.get("risk", "Low")

        if risk not in ["Critical", "High", "Medium"]:
            continue

        for recommendation in asset.get("recommendations", []):
            action = {
                "priority": risk,
                "ip": asset.get("ip", "Unbekannt"),
                "hostname": asset.get("hostname", "Unbekannt"),
                "title": recommendation,
                "reason": ", ".join(asset.get("risk_reasons", [])),
                "status": "Offen"
            }

            action_plan.append(action)

    action_plan.sort(
        key=lambda item: priority_value(item["priority"]),
        reverse=True
    )

    return action_plan


def priority_value(priority):
    values = {
        "Critical": 4,
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    return values.get(priority, 0)