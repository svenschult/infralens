import os
from datetime import datetime

from reporting.markdown_report import create_markdown_report
from reporting.security_pdf_report import create_security_pdf_report

from compliance.nis2_pdf_report import create_nis2_pdf_report


def select_report_types(enable_nis2=True):
    # Report-Auswahl
    print("\n[+] Report-Auswahl")
    print("1 - Normalen Security Report erstellen")

    if enable_nis2:
        print("2 - NIS2 Report erstellen")
        print("3 - Beide Reports erstellen")
    else:
        print("2 - NIS2 Report ist deaktiviert")
        print("3 - Nicht verfügbar")

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
        return None

    else:
        print("[!] Ungültige Eingabe oder Funktion deaktiviert.")
        return None

    return {
        "create_normal_report": create_normal_report,
        "create_nis2_report": create_nis2_report
    }


def prepare_report_paths(report_dir, history_folder):
    # Zeitgestempelte Report-Pfade vorbereiten
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    history_dir = os.path.join(
        report_dir,
        history_folder
    )

    os.makedirs(history_dir, exist_ok=True)

    return {
        "timestamp": timestamp,
        "history_dir": history_dir,
        "markdown_output_path": os.path.join(
            history_dir,
            f"report_{timestamp}.md"
        ),
        "security_pdf_path": os.path.join(
            history_dir,
            f"security_report_{timestamp}.pdf"
        ),
        "nis2_pdf_path": os.path.join(
            history_dir,
            f"nis2_report_{timestamp}.pdf"
        )
    }


def generate_reports(report_selection, report_paths, analysis, scan_context):
    # Reports erzeugen
    if report_selection["create_normal_report"]:
        create_markdown_report(
            analysis["analyzed_findings"],
            report_paths["markdown_output_path"],
            analysis["target_info"],
            analysis["attack_paths"],
            analysis["network_analysis"],
            analysis["host_inventory"],
            analysis["topology_notes"],
            analysis["assets"],
            analysis["asset_inventory"],
            analysis["action_plan"],
            scan_context,
            analysis["management_intelligence"]
        )

        create_security_pdf_report(
            report_paths["security_pdf_path"],
            analysis["target_info"],
            analysis["asset_inventory"],
            analysis["action_plan"],
            scan_context,
            analysis["management_intelligence"],
            analysis["executive_actions"]
        )

        print(
            f"[+] Markdown Security Report erstellt: "
            f"{report_paths['markdown_output_path']}"
        )

        print(
            f"[+] PDF Security Report erstellt: "
            f"{report_paths['security_pdf_path']}"
        )

    if report_selection["create_nis2_report"]:
        create_nis2_pdf_report(
            analysis["nis2_mapping"],
            analysis["nis2_statistics"],
            analysis["target_info"],
            report_paths["nis2_pdf_path"]
        )

        print(
            f"[+] NIS2 PDF Report erstellt: "
            f"{report_paths['nis2_pdf_path']}"
        )
