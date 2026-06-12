import os
from datetime import datetime

from core.config import load_config
from core.parser import (
    parse_nmap_file,
    parse_target_info,
    parse_nmap_hosts
)
from core.report import create_markdown_report
from core.security_pdf_report import create_security_pdf_report

from security.analyzer import analyze_findings
from security.attack_paths import generate_attack_paths
from security.action_plan import create_action_plan

from infrastructure.network_analysis import analyze_network
from infrastructure.host_inventory import create_host_inventory
from infrastructure.topology import generate_topology_notes
from infrastructure.asset_discovery import discover_assets
from infrastructure.asset_inventory import create_asset_inventory

from compliance.nis2_mapper import (
    map_findings_to_nis2,
    calculate_nis2_statistics
)
from compliance.nis2_pdf_report import create_nis2_pdf_report

from automation.setup_ai import setup_ai
from automation.dependency_checker import run_dependency_check
from automation.nmap_runner import run_nmap_scan

from core.customer_manager import customer_menu


def main():
    # Konfiguration laden
    config = load_config()

    scan_dir = config["scan_directory"]
    input_file = config["scan_file"]
    report_dir = config["report_directory"]
    history_folder = config["history_directory"]

    enable_ai = config.get("enable_ai", True)
    enable_nis2 = config.get("enable_nis2", True)

    os.makedirs(report_dir, exist_ok=True)

    # Systemvoraussetzungen prüfen
    run_dependency_check()

    # KI vorbereiten
    if enable_ai:
        print("\n[+] Initialisiere KI...")
        setup_ai()
    else:
        print("\n[i] KI ist in der Konfiguration deaktiviert.")

    print("\n[+] InfraLens startet...")

    # Auftraggeber auswählen
    customer = customer_menu()

    if customer:
        print(
            f"\n[+] Aktiver Auftraggeber: "
            f"{customer['company']}"
        )

    # Scan-Auswahl
    print("\n[+] Scan-Auswahl")
    print("1 - Vorhandene scan.txt verwenden")
    print("2 - Eigenes Netzwerk scannen")
    print("3 - Beenden")

    scan_choice = input("\n[?] Auswahl: ")

    if scan_choice == "1":
        print(f"[+] Verwende vorhandene Datei: {input_file}")

    elif scan_choice == "2":
        scan_output_path = os.path.join(scan_dir, input_file)

        success = run_nmap_scan(scan_output_path)

        if not success:
            print("[!] Scan konnte nicht durchgeführt werden.")
            return

    elif scan_choice == "3":
        print("[+] Programm beendet.")
        return

    else:
        print("[!] Ungültige Eingabe.")
        return

    # Report-Auswahl
    print("\n[+] Report-Auswahl")
    print("1 - Normalen Security Report erstellen")
    print("2 - NIS2 Report erstellen")
    print("3 - Beide Reports erstellen")
    print("4 - Beenden")

    choice = input("\n[?] Auswahl: ")

    create_normal_report = False
    create_nis2_report = False

    if choice == "1":
        create_normal_report = True

    elif choice == "2" and enable_nis2:
        create_nis2_report = True

    elif choice == "3" and enable_nis2:
        create_normal_report = True
        create_nis2_report = True

    elif choice == "4":
        print("[+] Programm beendet.")
        return

    else:
        print("[!] Ungültige Eingabe oder Funktion deaktiviert.")
        return

    # Pfade vorbereiten
    input_path = os.path.join(scan_dir, input_file)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    history_dir = os.path.join(report_dir, history_folder)
    os.makedirs(history_dir, exist_ok=True)

    markdown_output_file = f"report_{timestamp}.md"
    markdown_output_path = os.path.join(history_dir, markdown_output_file)

    security_pdf_file = f"security_report_{timestamp}.pdf"
    security_pdf_path = os.path.join(history_dir, security_pdf_file)

    print(f"\n[+] Analysiere: {input_file}")

    # Scan einlesen
    findings = parse_nmap_file(input_path)
    hosts = parse_nmap_hosts(input_path)

    if not findings:
        print("[!] Keine verwertbaren Daten gefunden.")
        return

    # Zielinformationen auswerten
    target_info = parse_target_info(input_path)

    # Security-Auswertung
    analyzed_findings = analyze_findings(findings)

    # Angriffspfade erzeugen
    attack_paths = generate_attack_paths(analyzed_findings)

    # Infrastruktur-Kontext analysieren
    network_analysis = analyze_network(target_info)

    # Host-Inventar für Zielsystem
    host_inventory = create_host_inventory(
        target_info,
        analyzed_findings
    )

    # Asset Discovery für bisherige Report-Struktur
    assets = discover_assets(
        analyzed_findings,
        target_info
    )

    # Multi-Geräte-Inventarliste
    asset_inventory = create_asset_inventory(hosts)

    # Maßnahmenplan erstellen
    action_plan = create_action_plan(asset_inventory)

    # Topologie-Hinweise erzeugen
    topology_notes = generate_topology_notes(
        target_info,
        host_inventory
    )

    # NIS2-Mapping vorbereiten
    if enable_nis2:
        nis2_mapping = map_findings_to_nis2(
            analyzed_findings,
            attack_paths,
            network_analysis,
            host_inventory
        )

        nis2_statistics = calculate_nis2_statistics(
            nis2_mapping
        )
    else:
        nis2_mapping = None
        nis2_statistics = None

    # Normalen Security Report erstellen
    if create_normal_report:
        create_markdown_report(
            analyzed_findings,
            markdown_output_path,
            target_info,
            attack_paths,
            network_analysis,
            host_inventory,
            topology_notes,
            assets,
            asset_inventory,
            action_plan
        )

        create_security_pdf_report(
            security_pdf_path,
            target_info,
            asset_inventory,
            action_plan
        )

        print(f"[+] Markdown Security Report erstellt: {markdown_output_path}")
        print(f"[+] PDF Security Report erstellt: {security_pdf_path}")

    # NIS2-PDF-Report erstellen
    if create_nis2_report:
        nis2_output_file = f"nis2_report_{timestamp}.pdf"

        nis2_output_path = os.path.join(
            history_dir,
            nis2_output_file
        )

        create_nis2_pdf_report(
            nis2_mapping,
            nis2_statistics,
            target_info,
            nis2_output_path
        )

        print(f"[+] NIS2 PDF Report erstellt: {nis2_output_path}")


if __name__ == "__main__":
    main()