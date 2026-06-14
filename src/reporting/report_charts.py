import os
import tempfile

import matplotlib.pyplot as plt


# ==========================================
# Hilfsfunktionen
# ==========================================

def create_temp_chart_path(filename):
    temp_dir = tempfile.gettempdir()

    return os.path.join(
        temp_dir,
        filename
    )


# ==========================================
# Risikoverteilung
# ==========================================

def create_risk_distribution_chart(asset_inventory):
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

    labels = []
    values = []

    for risk, count in risk_count.items():
        if count > 0:
            labels.append(risk)
            values.append(count)

    if not values:
        labels = ["Keine Daten"]
        values = [1]

    chart_path = create_temp_chart_path(
        "infralens_risk_distribution.png"
    )

    plt.figure(figsize=(5, 5))
    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Risikoverteilung")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return chart_path


# ==========================================
# Geräte-Rollen
# ==========================================

def create_asset_role_chart(asset_inventory):
    role_count = {}

    for asset in asset_inventory:
        roles = asset.get("roles", [])

        for role in roles:
            role_count[role] = role_count.get(role, 0) + 1

    if not role_count:
        role_count = {
            "Keine Daten": 1
        }

    labels = list(role_count.keys())
    values = list(role_count.values())

    chart_path = create_temp_chart_path(
        "infralens_asset_roles.png"
    )

    plt.figure(figsize=(7, 4))
    plt.bar(labels, values)
    plt.title("Geräte-Rollen")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return chart_path


# ==========================================
# Betriebssysteme
# ==========================================

def create_os_distribution_chart(asset_inventory):
    os_count = {}

    for asset in asset_inventory:
        os_info = asset.get("os", "Unbekannt")

        if not os_info:
            os_info = "Unbekannt"

        short_os = shorten_os_name(os_info)

        os_count[short_os] = os_count.get(short_os, 0) + 1

    if not os_count:
        os_count = {
            "Keine Daten": 1
        }

    labels = list(os_count.keys())
    values = list(os_count.values())

    chart_path = create_temp_chart_path(
        "infralens_os_distribution.png"
    )

    plt.figure(figsize=(7, 4))
    plt.bar(labels, values)
    plt.title("Betriebssystem-Verteilung")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return chart_path


def shorten_os_name(os_info):
    os_lower = os_info.lower()

    if "windows 11" in os_lower:
        return "Windows 11"

    if "windows 10" in os_lower:
        return "Windows 10"

    if "windows 7" in os_lower:
        return "Windows 7"

    if "windows xp" in os_lower:
        return "Windows XP"

    if "windows server" in os_lower:
        return "Windows Server"

    if "linux" in os_lower:
        return "Linux"

    if "openwrt" in os_lower:
        return "OpenWRT"

    if "android" in os_lower:
        return "Android"

    if "unbekannt" in os_lower:
        return "Unbekannt"

    return os_info[:30]