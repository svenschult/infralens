import json
import os


# Konfiguration laden
def load_config():
    config_path = os.path.join(
        "config",
        "settings.json"
    )

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Konfigurationsdatei nicht gefunden: {config_path}"
        )

    with open(
        config_path,
        "r",
        encoding="utf-8"
    ) as file:

        config = json.load(file)

    return config


# Einzelnen Wert abrufen
def get_config_value(key):
    config = load_config()

    return config.get(key)