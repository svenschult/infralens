from customers.customer_manager import customer_menu


def select_customer():
    # Auftraggeber auswählen oder ohne Auftraggeber fortfahren
    customer = customer_menu()

    if customer:
        print(
            f"\n[+] Aktiver Auftraggeber: "
            f"{customer['company']}"
        )
    else:
        print("\n[i] Kein Auftraggeber ausgewählt.")

    return customer
