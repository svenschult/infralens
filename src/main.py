import os

from config.config import load_config

from infrastructure.scan_context import create_scan_context

from engines.runtime_engine import initialize_runtime
from engines.customer_engine import select_customer
from engines.scan_engine import select_scan_source
from engines.report_engine import (
    select_report_types,
    prepare_report_paths,
    generate_reports
)
from engines.analysis_engine import run_analysis


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

    # Laufzeitumgebung vorbereiten
    initialize_runtime(enable_ai)

    print("\n[+] InfraLens startet...")

    # Scan-Kontext erstellen
    scan_context = create_scan_context()

    print(
        f"\n[i] Prüfgerät erkannt: "
        f"{scan_context['scanner_ip']}"
    )

    # Auftraggeber auswählen
    customer = select_customer()

    # Scan-Quelle auswählen
    input_path = select_scan_source(
        scan_dir,
        input_file
    )

    if input_path is None:
        return

    # Report-Typen auswählen
    report_selection = select_report_types(enable_nis2)

    if report_selection is None:
        return

    # Report-Pfade vorbereiten
    report_paths = prepare_report_paths(
        report_dir,
        history_folder
    )

    print(f"\n[+] Analysiere: {input_file}")

    # Analyse durchführen
    analysis = run_analysis(
        input_path=input_path,
        scan_context=scan_context,
        enable_nis2=enable_nis2
    )

    if analysis is None:
        print("[!] Keine verwertbaren Daten gefunden.")
        return

    print(
        f"\n[+] InfraLens Security Index: "
        f"{analysis['management_intelligence']['score']}/100 "
        f"({analysis['management_intelligence']['level']})"
    )

    # Reports erzeugen
    generate_reports(
        report_selection,
        report_paths,
        analysis,
        scan_context
    )

    print("\n[+] InfraLens Vorgang abgeschlossen.")


if __name__ == "__main__":
    main()
