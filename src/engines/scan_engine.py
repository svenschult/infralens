import os

from automation.nmap_runner import run_nmap_scan


def select_scan_source(scan_dir, input_file):
    # Scan-Quelle auswählen
    print("\n[+] Scan-Auswahl")
    print("1 - Vorhandene scan.txt verwenden")
    print("2 - Netzwerk scannen")
    print("3 - Beenden")

    scan_choice = input("\n[?] Auswahl: ")

    if scan_choice == "1":
        print(f"[+] Verwende vorhandene Datei: {input_file}")

        return os.path.join(
            scan_dir,
            input_file
        )

    if scan_choice == "2":
        scan_output_path = os.path.join(
            scan_dir,
            input_file
        )

        success = run_nmap_scan(scan_output_path)

        if not success:
            print("[!] Scan konnte nicht durchgeführt werden.")
            return None

        return scan_output_path

    if scan_choice == "3":
        print("[+] Programm beendet.")
        return None

    print("[!] Ungültige Eingabe.")
    return None