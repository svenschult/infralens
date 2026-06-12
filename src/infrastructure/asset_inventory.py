def detect_device_role(host):
    services = [
        service.get("service", "").lower()
        for service in host.get("services", [])
    ]

    versions = " ".join([
        service.get("version", "").lower()
        for service in host.get("services", [])
    ])

    os_info = host.get("os", "").lower()
    hostname = host.get("hostname", "").lower()

    roles = []

    # Router / Gateway Hinweise
    if "router" in hostname or "gateway" in hostname:
        roles.append("Router / Gateway")

    if "domain" in versions or "kerberos" in versions or "ldap" in services:
        roles.append("Möglicher Domain Controller")

    if "http" in services or "https" in services:
        roles.append("Webserver / Webinterface")

    if "mysql" in services or "postgresql" in services or "ms-sql-s" in services:
        roles.append("Datenbankserver")

    if "microsoft-ds" in services or "netbios-ssn" in services:
        roles.append("SMB/File-Server")

    if "ssh" in services:
        roles.append("Remote-Management-System")

    if "windows" in os_info or "microsoft" in versions:
        roles.append("Windows-System")

    if "linux" in os_info or "ubuntu" in versions or "debian" in versions:
        roles.append("Linux-System")

    if not roles:
        roles.append("Unbekanntes Gerät")

    return roles


def assess_asset_risk(host):
    os_info = host.get("os", "").lower()
    services = host.get("services", [])

    risk = "Low"
    reasons = []
    recommendations = []

    service_names = [
        service.get("service", "").lower()
        for service in services
    ]

    versions = " ".join([
        service.get("version", "").lower()
        for service in services
    ])

    # Alte Betriebssysteme
    if "windows xp" in os_info or "windows xp" in versions:
        risk = "Critical"
        reasons.append("Windows XP erkannt oder vermutet")
        recommendations.append("System außer Betrieb nehmen oder ersetzen.")

    elif "windows 7" in os_info or "windows 7" in versions:
        risk = "High"
        reasons.append("Windows 7 erkannt oder vermutet")
        recommendations.append("Upgrade auf ein unterstütztes Betriebssystem durchführen.")

    elif "windows server 2003" in os_info or "windows server 2003" in versions:
        risk = "Critical"
        reasons.append("Windows Server 2003 erkannt oder vermutet")
        recommendations.append("Server dringend ersetzen oder isolieren.")

    elif "windows server 2008" in os_info or "windows server 2008" in versions:
        risk = "High"
        reasons.append("Windows Server 2008 erkannt oder vermutet")
        recommendations.append("Migration auf unterstützte Server-Version planen.")

    # Unsichere Dienste
    if "ftp" in service_names:
        risk = max_risk(risk, "High")
        reasons.append("FTP-Dienst erkannt")
        recommendations.append("FTP deaktivieren oder durch SFTP/FTPS ersetzen.")

    if "telnet" in service_names:
        risk = max_risk(risk, "Critical")
        reasons.append("Telnet-Dienst erkannt")
        recommendations.append("Telnet deaktivieren und SSH verwenden.")

    if "microsoft-ds" in service_names or "netbios-ssn" in service_names:
        risk = max_risk(risk, "High")
        reasons.append("SMB/File-Sharing-Dienst erkannt")
        recommendations.append("SMB-Freigaben, Gastzugriff und Segmentierung prüfen.")

    if "mysql" in service_names or "postgresql" in service_names or "ms-sql-s" in service_names:
        risk = max_risk(risk, "High")
        reasons.append("Datenbankdienst im Netzwerk erreichbar")
        recommendations.append("Datenbankzugriff auf notwendige Systeme beschränken.")

    # Webinterfaces / Firmware Hinweise
    if "http" in service_names or "https" in service_names:
        risk = max_risk(risk, "Medium")
        reasons.append("Webinterface oder Webdienst erkannt")
        recommendations.append("Webinterface, Firmware-Version und Authentifizierung prüfen.")

    if "fritz" in versions or "openwrt" in versions or "router" in versions:
        risk = max_risk(risk, "Medium")
        reasons.append("Router-/Firmware-Hinweis erkannt")
        recommendations.append("Firmware-Version prüfen und Updates einspielen.")

    if not reasons:
        reasons.append("Keine auffälligen Risikomerkmale erkannt.")
        recommendations.append("Gerät dokumentieren und regelmäßig erneut prüfen.")

    return {
        "risk": risk,
        "reasons": reasons,
        "recommendations": recommendations
    }


def max_risk(current, new):
    order = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4
    }

    if order[new] > order[current]:
        return new

    return current


def create_asset_inventory(hosts):
    inventory = []

    for host in hosts:
        risk_assessment = assess_asset_risk(host)

        asset = {
            "hostname": host.get("hostname", "Unbekannt"),
            "ip": host.get("ip", "Unbekannt"),
            "os": host.get("os", "Unbekannt"),
            "mac": host.get("mac", "Unbekannt"),
            "roles": detect_device_role(host),
            "services": host.get("services", []),
            "risk": risk_assessment["risk"],
            "risk_reasons": risk_assessment["reasons"],
            "recommendations": risk_assessment["recommendations"]
        }

        inventory.append(asset)

    inventory.sort(
        key=lambda item: risk_sort_value(item["risk"]),
        reverse=True
    )

    return inventory


def risk_sort_value(risk):
    values = {
        "Critical": 4,
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    return values.get(risk, 0)