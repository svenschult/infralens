def parse_nmap_file(file_path):
    findings = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("PORT"):
                continue

            parts = line.split()

            if len(parts) >= 3 and "/tcp" in parts[0]:
                port = parts[0]
                state = parts[1]
                service = parts[2]
                version = " ".join(parts[3:]) if len(parts) > 3 else "unknown"

                findings.append({
                    "port": port,
                    "state": state,
                    "service": service,
                    "version": version
                })

    return findings


def parse_target_info(file_path):
    target_info = {
        "ip": "Unbekannt",
        "hostname": "Unbekannt",
        "os": "Unbekannt",
        "mac": "Unbekannt"
    }

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line.startswith("Nmap scan report for"):
                value = line.replace("Nmap scan report for", "").strip()

                if "(" in value and ")" in value:
                    hostname = value.split("(")[0].strip()
                    ip = value.split("(")[1].replace(")", "").strip()

                    target_info["hostname"] = hostname
                    target_info["ip"] = ip
                else:
                    target_info["ip"] = value

            elif line.startswith("MAC Address:"):
                target_info["mac"] = line.replace("MAC Address:", "").strip()

            elif line.startswith("OS details:"):
                target_info["os"] = line.replace("OS details:", "").strip()

            elif line.startswith("Running:"):
                if target_info["os"] == "Unbekannt":
                    target_info["os"] = line.replace("Running:", "").strip()

    return target_info


def parse_nmap_hosts(file_path):
    hosts = []
    current_host = None
    port_section_started = False

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # Neuer Host im Nmap-Report
            if line.startswith("Nmap scan report for"):
                if current_host:
                    hosts.append(current_host)

                value = line.replace("Nmap scan report for", "").strip()

                hostname = "Unbekannt"
                ip = "Unbekannt"

                if "(" in value and ")" in value:
                    hostname = value.split("(")[0].strip()
                    ip = value.split("(")[1].replace(")", "").strip()
                else:
                    ip = value

                current_host = {
                    "hostname": hostname,
                    "ip": ip,
                    "os": "Unbekannt",
                    "mac": "Unbekannt",
                    "services": []
                }

                port_section_started = False

            # MAC-Adresse erfassen
            elif current_host and line.startswith("MAC Address:"):
                current_host["mac"] = line.replace("MAC Address:", "").strip()

            # Betriebssystem erfassen
            elif current_host and line.startswith("OS details:"):
                current_host["os"] = line.replace("OS details:", "").strip()

            elif current_host and line.startswith("Running:"):
                if current_host["os"] == "Unbekannt":
                    current_host["os"] = line.replace("Running:", "").strip()

            # Port-Tabelle beginnt
            elif current_host and line.startswith("PORT"):
                port_section_started = True

            # Dienste erfassen
            elif current_host and port_section_started:
                if not line:
                    continue

                parts = line.split()

                if len(parts) >= 3 and "/tcp" in parts[0]:
                    port = parts[0]
                    state = parts[1]
                    service = parts[2]
                    version = " ".join(parts[3:]) if len(parts) > 3 else "unknown"

                    current_host["services"].append({
                        "port": port,
                        "state": state,
                        "service": service,
                        "version": version
                    })

        # letzten Host hinzufügen
        if current_host:
            hosts.append(current_host)

    return hosts