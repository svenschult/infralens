import os
from datetime import datetime

from core.parser import parse_nmap_file, parse_target_info
from core.report import create_markdown_report

from security.analyzer import analyze_findings
from security.attack_paths import generate_attack_paths

from infrastructure.network_analysis import analyze_network
from infrastructure.host_inventory import create_host_inventory
from infrastructure.topology import generate_topology_notes
from infrastructure.asset_discovery import discover_assets

from compliance.nis2_mapper import (
    map_findings_to_nis2,
    calculate_nis2_statistics
)
from compliance.nis2_pdf_report import create_nis2_pdf_report

from automation.setup_ai import setup_ai
from automation.dependency_checker import run_dependency_check
from automation.nmap_runner import run_nmap_scan


def main():
    scan_dir = "scans"
    report_dir = "reports"

    os.makedirs(report_dir, exist_ok=True)

    # Systemvoraussetzungen prüfen
    run_dependency_check()

    # KI vorbereiten
    print("\n[+] Initialisiere KI...")
    setup_ai()

    print("\n[+] InfraLens Platform startet...")

    # Scan-Auswahl
    print("\n[+] Scan-Auswahl")
    print("1 - Vorhandene scan.txt verwenden")
    print("2 - Eigenes Netzwerk scannen")
    print("3 - Beenden")

    scan_choice = input("\n[?] Auswahl: ")

    if scan_choice == "1":
        print("[+] Verwende vorhandene scan.txt")

    elif scan_choice == "2":
        success = run_nmap_scan()

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

    elif choice == "2":
        create_nis2_report = True

    elif choice == "3":
        create_normal_report = True
        create_nis2_report = True

    elif choice == "4":
        print("[+] Programm beendet.")
        return

    else:
        print("[!] Ungültige Eingabe.")
        return

    # Pfade vorbereiten
    input_file = "scan.txt"
    input_path = os.path.join(scan_dir, input_file)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    history_dir = os.path.join(report_dir, "history")
    os.makedirs(history_dir, exist_ok=True)

    output_file = f"report_{timestamp}.md"
    output_path = os.path.join(history_dir, output_file)

    print(f"\n[+] Analysiere: {input_file}")

    # Scan einlesen
    findings = parse_nmap_file(input_path)

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

    # Host-Inventar erstellen
    host_inventory = create_host_inventory(
        target_info,
        analyzed_findings
    )

    # Asset Discovery erzeugen
    assets = discover_assets(
        analyzed_findings,
        target_info
    )

    # Topologie-Hinweise erzeugen
    topology_notes = generate_topology_notes(
        target_info,
        host_inventory
    )

    # NIS2-Mapping vorbereiten
    nis2_mapping = map_findings_to_nis2(
        analyzed_findings,
        attack_paths,
        network_analysis,
        host_inventory
    )

    nis2_statistics = calculate_nis2_statistics(
        nis2_mapping
    )

    # Normalen Markdown-Report erstellen
    if create_normal_report:
        create_markdown_report(
            analyzed_findings,
            output_path,
            target_info,
            attack_paths,
            network_analysis,
            host_inventory,
            topology_notes,
            assets
        )

        print(f"[+] Security Report erstellt: {output_path}")

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