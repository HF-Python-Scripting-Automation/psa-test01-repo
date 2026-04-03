# SmartLearn Service Base Framework

Dieses Repository stellt die fundamentale Projektstruktur für Python-Dienste innerhalb der SmartLearn Lernumgebung bereit. Es dient als standardisierte Ausgangslage für die Entwicklung von Netzwerk-Applikationen im Subnetz 192.168.110.0/24.

## Projektstruktur

Das Layout nutzt ein professionelles Flat-Layout. Die Trennung zwischen Applikationslogik und Infrastruktur-Automatisierung ist strikt eingehalten.

```text
.
├── ansible.cfg          # SSH-Agent Forwarding und Ansible Defaults
├── inventory.ini        # Zielserver-Definitionen (Ubuntu Server .10 - .12)
├── pyproject.toml       # Projekt-Metadaten und Setuptools Discovery-Konfiguration
├── README.md            # Projektdokumentation
├── requirements.txt     # Python Abhängigkeiten
├── logs/                # Lokale Log-Dateien (z. B. servicename.log)
├── servicename/         # Quellcode-Paket
│   ├── __init__.py      # Package-Initialisierung
│   ├── main.py          # Zentraler Einstiegspunkt und CLI-Wrapper
│   └── utils/           # Hilfsmodule und Framework-Komponenten
│       ├── __init__.py
│       └── logger_config.py # Zentralisierte Logging-Konfiguration
└── templates/           # Jinja2-Vorlagen für Systemd-Units oder Konfigurationen