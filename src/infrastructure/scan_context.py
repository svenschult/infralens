import socket


def get_scanner_ip():
    # Lokale IP des Prüfgeräts ermitteln
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))

        scanner_ip = sock.getsockname()[0]

        sock.close()

        return scanner_ip

    except Exception:
        return "Unbekannt"


def create_scan_context():
    # Kontext zum Prüfgerät erstellen
    scanner_ip = get_scanner_ip()

    return {
        "scanner_ip": scanner_ip,
        "scanner_role": "Prüfgerät / Scan-System",
        "exclude_from_inventory": True,
        "note": (
            "Dieses System wurde als Prüfgerät erkannt und wird nicht "
            "als Kunden-Asset bewertet."
        )
    }


def filter_scanner_from_assets(asset_inventory, scan_context):
    # Prüfgerät aus der Kundeninventarliste entfernen
    scanner_ip = scan_context.get("scanner_ip", "Unbekannt")

    filtered_assets = []

    for asset in asset_inventory:
        if asset.get("ip") != scanner_ip:
            filtered_assets.append(asset)

    return filtered_assets