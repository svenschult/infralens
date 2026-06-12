# InfraLens Platform

Eine modulare Plattform für Infrastructure-, Netzwerk- und Security-Analyse mit Python, Automatisierung und KI-Unterstützung.

InfraLens dient als praxisnahes Homelab- und Portfolio-Projekt mit Fokus auf:

- Infrastruktur verstehen
- Netzwerke analysieren
- Security bewerten
- Angriffswege nachvollziehen
- defensive Maßnahmen ableiten
- Automatisierung und Reporting

---
## Lizenz

Dieses Projekt steht unter der MIT License.
---

## Screenshots

### Plattform-Architektur

![Architecture](docs/screenshots/current/architecture.png)

---

### Security Assessment Report

![Report](docs/screenshots/current/report_v4.png)

---

### Angriffspfad-Simulation

![Attack Paths](docs/screenshots/current/attack_paths.png)

---

### Automatische Zielerkennung

![Target Detection](docs/screenshots/current/target_detection.png)

---

## Projektziel

InfraLens soll langfristig zu einer modularen Security- und Infrastructure-Analysis-Plattform ausgebaut werden.

Das Projekt kombiniert:

- Python-Automatisierung
- Netzwerk-Analyse
- Security Assessment
- KI-Unterstützung
- Reporting & Dokumentation
- Homelab-Integration

---

## Kernfunktionen

### Infrastructure Discovery
- Analyse von Nmap-Scans
- automatische Zielerkennung
- Erkennung von:
  - Hostname
  - IP-Adresse
  - Betriebssystem
  - MAC-Adresse / Hersteller

### Infrastructure Analysis
- Netzwerk-Analyse
- Host Inventory
- Topologie-Hinweise
- Infrastruktur-Kontext

### Security Analysis
- Risikobewertung
- Priorisierung kritischer Dienste
- Security Findings
- Angriffspfad-Simulation

### Defensive Recommendations
- Hardening-Empfehlungen
- defensive Maßnahmen
- Security-Kontext

### Automation
- automatische KI-Initialisierung
- Ollama-Integration
- automatisierte Report-Erstellung

### Reporting
- Executive Summary
- Infrastructure Overview
- Host Inventory
- Security Findings
- Attack Path Simulation
- Defensive Recommendations
- Next Steps

---

## Architektur

infralens-platform
│
├── src/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── parser.py
│   │   ├── report.py
│   │   └── ai_assistant.py
│   │
│   ├── security/
│   │   ├── analyzer.py
│   │   ├── attack_paths.py
│   │   └── defensive_recommendations.py
│   │
│   ├── infrastructure/
│   │   ├── network_analysis.py
│   │   ├── host_inventory.py
│   │   └── topology.py
│   │
│   └── automation/
│       └── setup_ai.py
│
├── scans/
├── reports/
├── docs/
│
├── README.md
├── CHANGELOG.md
├── requirements.txt
└── .gitignore

---

## Voraussetzungen

- Python 3.x
- Nmap
- Ollama

Ollama Download:

https://ollama.com

---

## Installation

Repository klonen:

git clone https://github.com/DEINNAME/infralens-platform

Projektordner öffnen:

cd infralens-platform

Abhängigkeiten installieren:

pip install -r requirements.txt

---

## Nutzung

### 1. Nmap-Scan erstellen

Beispiel:

nmap -sV -O -oN scan.txt <ZIEL-IP>

Die Datei anschließend speichern unter:

scans/scan.txt

---

### 2. Plattform starten

Windows:

python src/main.py

Linux / Kali:

python3 src/main.py

---

## Automatische KI-Initialisierung

Beim Start passiert automatisch:

- Ollama wird gestartet
- KI-Modell wird geprüft
- Modell wird geladen (falls nötig)

Keine manuelle Einrichtung erforderlich.

---

## Security-Ansatz

InfraLens fokussiert sich nicht nur auf Angriffe, sondern auf das Verständnis kompletter Security-Szenarien.

Die Plattform analysiert:
- mögliche Angriffspfade
- Risiken
- Fehlkonfigurationen
- defensive Maßnahmen
- Infrastruktur-Kontext
- Netzwerk-Topologie

---

## Geplante Erweiterungen

### Infrastructure
- Netzwerksegmentierung
- Asset Discovery
- mehrere Hosts analysieren
- Infrastruktur-Korrelation

### Security
- laterale Bewegungsanalyse
- Hardening-Checks
- erweiterte Angriffspfade
- Schwachstellen-Korrelation

### Automation
- automatischer Nmap-Scan
- Vergleich mehrerer Scans
- geplante Scans

### Reporting
- PDF-Export
- Dashboard
- modernes Web UI

---

## Technologien

- Python
- Nmap
- Ollama
- Requests
- Git / GitHub

---

## Projektstatus

Aktive Entwicklung

Aktueller Fokus:
- modulare Architektur
- Infrastruktur-Analyse
- Security-Analyse
- Homelab-Integration
- Automatisierung
- Reporting

---

## Autor

Sven

---

## Hinweis

Dieses Projekt dient ausschließlich zu Lern-, Analyse- und Demonstrationszwecken in kontrollierten Umgebungen.

Keine Nutzung gegen fremde Systeme ohne ausdrückliche Erlaubnis.