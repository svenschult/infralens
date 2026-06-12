import json
import os
from datetime import datetime


CUSTOMER_FILE = os.path.join("data", "customers.json")


def ensure_customer_file():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(CUSTOMER_FILE):
        with open(CUSTOMER_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4, ensure_ascii=False)


def load_customers():
    ensure_customer_file()

    with open(CUSTOMER_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_customers(customers):
    ensure_customer_file()

    with open(CUSTOMER_FILE, "w", encoding="utf-8") as file:
        json.dump(customers, file, indent=4, ensure_ascii=False)


def create_customer_id(company):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    clean_company = company.lower().replace(" ", "_")

    return f"{clean_company}_{timestamp}"


def add_note_to_customer(customer, note_type, text):
    note = {
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "type": note_type,
        "text": text
    }

    customer["notes"].append(note)

    return customer


def create_new_customer():
    print("\n[+] Neuen Auftraggeber anlegen\n")

    company = input("Firma / Auftraggeber: ")
    contact = input("Ansprechpartner: ")
    location = input("Standort: ")
    email = input("E-Mail: ")
    phone = input("Telefon: ")
    project = input("Projektbezeichnung: ")

    customer = {
        "id": create_customer_id(company),
        "company": company,
        "contact": contact,
        "location": location,
        "email": email,
        "phone": phone,
        "project": project,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "notes": []
    }

    add_first_note = input("\nNotiz / besondere Wünsche hinzufügen? (y/n): ").lower()

    if add_first_note == "y":
        note_text = input("Notiz: ")

        customer = add_note_to_customer(
            customer,
            "Erstnotiz",
            note_text
        )

    customers = load_customers()
    customers.append(customer)
    save_customers(customers)

    print(f"\n[+] Auftraggeber gespeichert: {company}")

    return customer


def select_existing_customer():
    customers = load_customers()

    if not customers:
        print("[!] Keine Auftraggeber vorhanden.")
        return None

    print("\n[+] Vorhandene Auftraggeber\n")

    for index, customer in enumerate(customers, start=1):
        print(
            f"{index} - {customer['company']} "
            f"({customer.get('project', 'Kein Projekt')})"
        )

    choice = input("\n[?] Auftraggeber auswählen: ")

    try:
        selected_index = int(choice) - 1

        if 0 <= selected_index < len(customers):
            return customers[selected_index]

    except ValueError:
        pass

    print("[!] Ungültige Auswahl.")
    return None


def customer_menu():
    print("\n[+] Auftraggeber\n")
    print("1 - Vorhandenen Auftraggeber auswählen")
    print("2 - Neuen Auftraggeber anlegen")
    print("3 - Ohne Auftraggeber fortfahren")
    print("4 - Beenden")

    choice = input("\n[?] Auswahl: ")

    if choice == "1":
        return select_existing_customer()

    if choice == "2":
        return create_new_customer()

    if choice == "3":
        print("[i] Es wird ohne Auftraggeber fortgefahren.")
        return None

    if choice == "4":
        print("[+] Programm beendet.")
        exit()

    print("[!] Ungültige Eingabe.")
    return None