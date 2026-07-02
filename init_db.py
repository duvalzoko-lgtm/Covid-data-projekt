import sqlite3

conn = sqlite3.connect("covid.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS covid_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_reported TEXT NOT NULL,
    country TEXT NOT NULL,
    country_code TEXT,
    who_region TEXT,
    new_cases INTEGER,
    cumulative_cases INTEGER,
    new_deaths INTEGER,
    cumulative_deaths INTEGER,
    recovered_estimated INTEGER,
    UNIQUE(date_reported, country)
)
""")

conn.commit()
conn.close()

print("Datenbank und Tabelle wurden erstellt.")