from automation.dependency_checker import run_dependency_check
from automation.setup_ai import setup_ai


def initialize_runtime(enable_ai=True):
    """
    Initialisiert die Laufzeitumgebung von InfraLens.
    """

    print("\n[+] Prüfe Systemvoraussetzungen...")
    run_dependency_check()

    if enable_ai:
        print("\n[+] Initialisiere KI...")
        setup_ai()
    else:
        print("\n[i] KI ist deaktiviert.")

    print("\n[+] InfraLens erfolgreich initialisiert.")