# ==========================================
# Executive Action Center
# ==========================================


def create_executive_actions(action_plan):
    executive_actions = []

    for action in action_plan:

        priority = action.get("priority", "Low")

        action_entry = {
            "priority": priority,
            "title": action.get("title", "Keine Maßnahme"),
            "device": action.get("hostname", "Unbekannt"),
            "ip": action.get("ip", "Unbekannt"),
            "reason": action.get("reason", ""),
            "effort": estimate_effort(action),
            "security_gain": estimate_security_gain(action),
            "business_risk": estimate_business_risk(priority),
            "status": action.get("status", "Offen")
        }

        executive_actions.append(action_entry)

    executive_actions.sort(
        key=priority_sort_key
    )

    return executive_actions[:5]


# ==========================================
# Prioritäten sortieren
# ==========================================

def priority_sort_key(action):

    priority = action["priority"]

    order = {
        "Critical": 0,
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    return order.get(priority, 99)


# ==========================================
# Sicherheitsgewinn
# ==========================================

def estimate_security_gain(action):

    priority = action.get("priority", "Low")

    if priority == "Critical":
        return 15

    if priority == "High":
        return 10

    if priority == "Medium":
        return 5

    return 2


# ==========================================
# Aufwand
# ==========================================

def estimate_effort(action):

    title = action.get("title", "").lower()

    if "firmware" in title:
        return "★★☆☆☆"

    if "windows xp" in title:
        return "★★★★★"

    if "ftp" in title:
        return "★☆☆☆☆"

    if "smb" in title:
        return "★★★☆☆"

    return "★★☆☆☆"


# ==========================================
# Geschäftsrisiko
# ==========================================

def estimate_business_risk(priority):

    if priority == "Critical":
        return "Sehr hoch"

    if priority == "High":
        return "Hoch"

    if priority == "Medium":
        return "Mittel"

    return "Niedrig"