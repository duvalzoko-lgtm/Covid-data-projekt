# COVID-19 Dashboard

Ein interaktives Dashboard zur Visualisierung globaler COVID-19-Daten, gebaut mit [Streamlit](https://streamlit.io/) und Daten der WHO (World Health Organization).

## 🎯 Funktionen

- Visualisierung globaler COVID-19-Fallzahlen
- Datenbankgestützte Abfrage (SQLite)
- Import aktueller Daten über API sowie aus lokalen CSV-Dateien

## 📁 Projektstruktur

```
├── app.py                     # Haupt-Streamlit-App
├── init_db.py                  # Initialisiert die SQLite-Datenbank
├── import_data.py              # Importiert Daten aus der CSV-Datei
├── import_api-data.py          # Importiert Daten über eine API
├── covid.db                    # SQLite-Datenbank mit COVID-19-Daten
├── WHO-COVID-19-global-data.csv # Rohdaten von der WHO
└── README.md
```

## 🚀 Installation & Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Die App ist danach unter `http://localhost:8501` erreichbar.

## 📊 Datenquelle

Die Daten stammen von der [World Health Organization (WHO)](https://covid19.who.int/data).

## 🛠️ Verwendete Technologien

- Python
- Streamlit
- SQLite
- Pandas

## 📄 Lizenz

Dieses Projekt dient Lern- und Demonstrationszwecken.
