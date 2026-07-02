import sqlite3
import pandas as pd

# CSV laden
df = pd.read_csv("WHO-COVID-19-global-data.csv")

# Datum umwandeln
df["Date_reported"] = pd.to_datetime(df["Date_reported"]).dt.strftime("%Y-%m-%d")

# Geschätzte Genesene berechnen
df["Recovered_estimated"] = df["Cumulative_cases"] - df["Cumulative_deaths"]

# Datenbankverbindung
conn = sqlite3.connect("covid.db")
cursor = conn.cursor()

# Daten einfügen
for _, row in df.iterrows():
    cursor.execute("""
    INSERT OR REPLACE INTO covid_data (
        date_reported,
        country,
        country_code,
        who_region,
        new_cases,
        cumulative_cases,
        new_deaths,
        cumulative_deaths,
        recovered_estimated
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["Date_reported"],
        row["Country"],
        row["Country_code"],
        row["WHO_region"],
        int(row["New_cases"]) if pd.notna(row["New_cases"]) else None,
        int(row["Cumulative_cases"]) if pd.notna(row["Cumulative_cases"]) else None,
        int(row["New_deaths"]) if pd.notna(row["New_deaths"]) else None,
        int(row["Cumulative_deaths"]) if pd.notna(row["Cumulative_deaths"]) else None,
        int(row["Recovered_estimated"]) if pd.notna(row["Recovered_estimated"]) else None
    ))

conn.commit()
conn.close()

print("Daten wurden in die SQLite-Datenbank importiert.")