# Changelog

Alle wichtigen Änderungen am Projekt werden hier dokumentiert.

## Unreleased - Refactor / Engine Architecture

### Hinzugefügt
- Engine-Architektur eingeführt
- `runtime_engine.py` hinzugefügt
- `customer_engine.py` hinzugefügt
- `scan_engine.py` hinzugefügt
- `analysis_engine.py` hinzugefügt
- `report_engine.py` hinzugefügt
- `README_DE.md` ergänzt
- `ARCHITECTURE.md` ergänzt
- `PRODUCT_VISION.md` ergänzt
- Sprint-Dokumentation für Clean Structure ergänzt

### Geändert
- `main.py` deutlich verschlankt
- Analyse-Logik in `analysis_engine.py` ausgelagert
- Report-Erzeugung in `report_engine.py` ausgelagert
- Scan-Auswahl in `scan_engine.py` ausgelagert
- Runtime-Initialisierung in `runtime_engine.py` ausgelagert
- Kunden-Auswahl in `customer_engine.py` ausgelagert
- Reporting-Dateien nach `src/reporting/` verschoben
- Kundendateien nach `src/customers/` verschoben
- KI-Dateien nach `src/ai/` verschoben
- Config-Dateien nach `src/config/` verschoben
- Parser nach `src/parsing/` verschoben
- README vollständig überarbeitet

### Verbessert
- Projektstruktur professionalisiert
- Architektur besser auf GUI, Auditor Assistant und weitere Reporttypen vorbereitet
- Verantwortlichkeiten klarer getrennt
- Wartbarkeit verbessert
- Codebasis stärker auf Produktentwicklung ausgerichtet

---

## Version 5.0

### Geändert
- Projektname von "Mini Mythos Platform" auf "InfraLens" geändert
- Dokumentation vereinheitlicht
- Branding aktualisiert

---

## Version 4.4

### Hinzugefügt
- automatischer Netzwerk-Scan integriert
- plattformübergreifende Nmap-Erkennung
- Dependency Checker integriert
- Asset Discovery Modul ergänzt
- NIS2 PDF Reporting hinzugefügt
- statistische Risiko-Auswertung ergänzt
- Donut-Chart für NIS2-Risikoverteilung integriert
- Verlaufshistorie für Reports ergänzt
- automatische Zeitstempel für Reports eingeführt

### Verbessert
- Infrastruktur-Analyse erweitert
- Plattform-Architektur weiter modularisiert
- Report-Generierung erweitert
- Cross-Platform-Unterstützung verbessert
- Benutzerführung im CLI verbessert

### Neue Module
- `automation/dependency_checker.py`
- `automation/nmap_runner.py`
- `infrastructure/asset_discovery.py`
- `compliance/nis2_mapper.py`
- `compliance/nis2_pdf_report.py`

---

## Version 4.3

### Hinzugefügt
- `topology.py` hinzugefügt
- erste Topologie-Hinweise integriert
- Infrastruktur-Kontext im Report erweitert
- Hinweise zu privaten Netzbereichen, Homelab-Segmenten und möglichen lateralen Bewegungen

### Verbessert
- Infrastructure Layer weiter ausgebaut
- Report um Topologie-Hinweise erweitert

---

## Version 4.2

### Hinzugefügt
- Infrastructure Layer erweitert
- `host_inventory.py` hinzugefügt
- automatische Rollen-Erkennung für Zielsysteme
- offene Dienste werden als Host-Inventar dokumentiert

### Verbessert
- `main.py` als zentraler Orchestrator stabilisiert
- Report-Engine an neue Module angepasst
- Refactor-Branch konsolidiert

---

## Version 4.1

### Hinzugefügt
- `network_analysis.py` hinzugefügt
- einfache Netzwerk-Analyse integriert
- Erkennung privater Netzbereiche
- Homelab-/internes Netzwerk wird im Report erwähnt

---

## Version 4.0

### Plattform-Restrukturierung
- Projekt von einem einfachen Pentest-Tool zu einer modularen Security- und Infrastructure-Analysis-Plattform weiterentwickelt
- modulare Architektur eingeführt
- neue Modulstruktur aufgebaut:
  - core
  - security
  - automation
  - infrastructure

### Architektur
- Parser in eigenes Core-Modul verschoben
- Report-Engine modularisiert
- KI-Modul modularisiert
- Analyzer in Security-Modul ausgelagert
- automatische KI-Initialisierung in eigenes Automation-Modul verschoben

### Security Features
- Angriffspfad-Simulation hinzugefügt
- defensive Empfehlungen integriert
- Security Findings erweitert
- Priorisierung verbessert

### Reporting
- Report komplett restrukturiert
- neue Bereiche:
  - Executive Summary
  - Infrastructure Overview
  - Host Inventory
  - Security Findings
  - Attack Path Simulation
  - Defensive Recommendations
  - Next Steps

### Infrastruktur-Analyse
- automatische Zielerkennung verbessert
- Erkennung von:
  - Hostname
  - IP-Adresse
  - Betriebssystem
  - MAC-Adresse

---

## Version 3.1

### Hinzugefügt
- automatische Zielerkennung aus Nmap-Scans
- Erkennung von IP-Adresse, Hostname, Betriebssystem und MAC-Adresse

### Verbessert
- dynamischer Zielsystem-Block im Report
- vereinfachte Scan-Datei (`scan.txt`)

---

## Version 3.0

### Hinzugefügt
- KI-Modul über Ollama
- KI-gestützte Erklärungen
- automatische KI-Initialisierung
- automatischer Modell-Check

### Technologien
- Ollama
- Requests

---

## Version 2.2

### Hinzugefügt
- Pentest-Hinweise
- Priorisierung von Diensten
- Top-Targets im Report

### Verbessert
- Risikoanalyse erweitert

---

## Version 2.1

### Hinzugefügt
- CLI-Dateiauswahl

---

## Version 2.0

### Hinzugefügt
- Analyse realer Metasploitable-Scans
- verbesserte Risikoanalyse

---

## Version 1.0

### Erstes Release
- Projektstruktur erstellt
- Parser implementiert
- Report-Generator erstellt
- erste Analyse-Logik