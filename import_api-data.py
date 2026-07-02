import requests
import sqlite3

API_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

response = requests.get(API_URL, timeout=60)
response.raise_for_status()
data = response.json()

conn = sqlite3.connect("covid.db")
cursor = conn.cursor()

for iso_code, country_data in data.items():
    country_name = country_data.get("location")
    daily_data = country_data.get("data", [])

    for entry in daily_data:
        date_reported = entry.get("date")
        new_cases = entry.get("new_cases")
        cumulative_cases = entry.get("total_cases")
        new_deaths = entry.get("new_deaths")
        cumulative_deaths = entry.get("total_deaths")

        recovered_estimated = None
        if cumulative_cases is not None and cumulative_deaths is not None:
            recovered_estimated = cumulative_cases - cumulative_deaths

        cursor.execute("""
        INSERT OR REPLACE INTO covid_data (
            date_reported,
            country,
            iso_code,
            new_cases,
            cumulative_cases,
            new_deaths,
            cumulative_deaths,
            recovered_estimated,
            source
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            date_reported,
            country_name,
            iso_code,
            new_cases,
            cumulative_cases,
            new_deaths,
            cumulative_deaths,
            recovered_estimated,
            "OWID JSON API"
        ))

conn.commit()
conn.close()

print("API-Daten wurden erfolgreich in SQLite gespeichert.")