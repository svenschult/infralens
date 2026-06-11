# Projektplan - InfraLens Platform

## Projektziel

Entwicklung einer modularen Plattform zur Analyse von Infrastruktur-, Netzwerk- und Security-Daten mit Python und KI-Unterstützung.

InfraLens soll langfristig als Security- und Infrastructure-Analysis-Plattform dienen und praxisnahe Homelab-Umgebungen analysieren.

Das Projekt kombiniert:

- Infrastruktur-Analyse
- Netzwerkverständnis
- Security Assessment
- Angriffspfad-Simulation
- defensive Empfehlungen
- Automatisierung
- Reporting & Dokumentation

---

## Projektübersicht

Projektname: InfraLens Platform  
Technologie: Python  
Einsatzbereich: Infrastructure & Security Analysis  

Verwendete Umgebung:
- Kali Linux
- Windows Server
- Metasploitable
- VirtualBox Homelab

---

## Projektarchitektur

### Core
Verantwortlich für:
- Parser
- Reporting
- KI-Unterstützung

### Security
Verantwortlich für:
- Risikoanalyse
- Angriffspfade
- defensive Empfehlungen

### Infrastructure
Verantwortlich für:
- Netzwerk-Analyse
- Host-Inventory
- Infrastruktur-Kontext
- Topologie-Hinweise
- Asset Discovery
- Infrastruktur-Korrelation
- Multi-Host-Unterstützung

### Automation
Verantwortlich für:
- KI-Initialisierung
- Setup-Routinen
- zukünftige Automatisierungen
- automatischer Netzwerk-Scan
- Dependency Management
- plattformübergreifende Tool-Erkennung

### Compliance
- NIS2-orientierte Risikoanalyse
- PDF-Compliance-Reporting
- statistische Sicherheitsbewertung
- Risiko-Visualisierung

---

## Aktuelle Architektur

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
│   ├── compliance/
│   │   ├── nis2_mapper.py
│   │   └── nis2_pdf_report.py
│   │
│   ├── security/
│   │   ├── analyzer.py
│   │   ├── attack_paths.py
│   │   └── defensive_recommendations.py
│   │
│   ├── infrastructure/
│   │   ├── network_analysis.py
│   │   ├── host_inventory.py
│   │   ├── asset_discovery.py
│   │   └── topology.py
│   │
│   └── automation/
│       ├── setup_ai.py
│       ├── dependency_checker.py
│       └── nmap_runner.py
├── scans/
├── reports/
├── docs/
│
├── README.md
├── CHANGELOG.md
├── requirements.txt
└── .gitignore

---

## Funktionsweise

1. Nmap-Scan wird erstellt
2. Scan-Datei wird eingelesen
3. Zielsystem wird erkannt
4. Netzwerk-Kontext wird analysiert
5. Dienste werden analysiert
6. Risiken werden bewertet
7. Angriffspfade werden simuliert
8. defensive Maßnahmen werden abgeleitet
9. KI erstellt zusätzliche Einschätzungen
10. Topologie-Hinweise werden generiert
11. strukturierter Report wird generiert

---

## Meilensteine

### Version 1
- [x] Projektstruktur erstellt
- [x] Parser implementiert
- [x] einfacher Report

### Version 2
- [x] Risikoanalyse erweitert
- [x] Priorisierung integriert
- [x] CLI-Version erstellt

### Version 3
- [x] KI-Modul integriert
- [x] Ollama-Anbindung
- [x] automatische KI-Initialisierung

### Version 3.1
- [x] automatische Zielerkennung
- [x] dynamische Zielsystem-Erkennung
- [x] Infrastrukturinformationen erweitert

### Version 4.0
- [x] modulare Plattform-Architektur
- [x] Security-Module getrennt
- [x] Angriffspfad-Simulation
- [x] defensive Empfehlungen
- [x] professionelles Reporting
- [x] Plattform-Rebranding

### Version 4.1
- [x] Infrastructure Layer eingeführt
- [x] Netzwerk-Analyse integriert
- [x] privates Netzwerk wird erkannt

### Version 4.2
- [x] Host Inventory integriert
- [x] Rollen-Erkennung für Hosts
- [x] offene Dienste werden dokumentiert

### Version 4.3
- [x] Topologie-Modul integriert
- [x] Topologie-Hinweise im Report ergänzt
- [x] Infrastruktur-Kontext erweitert

### Version 4.4
- [x] automatischer Netzwerk-Scan integriert
- [x] Dependency Checker integriert
- [x] Asset Discovery erweitert
- [x] NIS2 PDF Reporting integriert
- [x] statistische Risikoanalyse ergänzt
- [x] Verlaufshistorie für Reports eingeführt
- [x] plattformübergreifende Nmap-Erkennung integriert
---

## Geplante Erweiterungen

### Infrastructure
- Netzwerk-Topologie
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

## Risiken

- einfache Heuristiken können Fehlbewertungen erzeugen
- KI kann ungenaue Einschätzungen liefern
- externe Abhängigkeiten:
  - Nmap
  - Ollama
- große Scans können längere Analysezeiten verursachen

---

## Ziel des Projekts

Das Projekt dient als:

- Lernprojekt
- Homelab-Plattform
- Portfolio-Projekt

Es demonstriert:
- Python-Kenntnisse
- Infrastrukturverständnis
- Security-Analyse
- Automatisierung
- Dokumentation
- modulares Softwaredesign