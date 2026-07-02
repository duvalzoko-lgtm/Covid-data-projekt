import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px

st.title("COVID-19 Dashboard – Analyse und Ländervergleich")

st.markdown("""
Diese Anwendung analysiert und visualisiert COVID-19-Daten auf Basis einer SQLite-Datenbank.  
Die Daten wurden aus dem WHO-Datensatz importiert und in einer relationalen Datenbank gespeichert.
""")

# Daten aus SQLite laden
@st.cache_data
def load_data():
    conn = sqlite3.connect("covid.db")
    df = pd.read_sql_query("SELECT * FROM covid_data", conn)
    conn.close()
    df["date_reported"] = pd.to_datetime(df["date_reported"])
    return df

df = load_data()

st.write(
    f"Zeitraum: {df['date_reported'].min().date()} bis {df['date_reported'].max().date()}"
)

# Einzellandanalyse
st.header("Einzellandanalyse")
countries = sorted(df["country"].dropna().unique())
default_index = countries.index("Germany") if "Germany" in countries else 0
selected_country = st.selectbox("Land auswählen", countries, index=default_index)


min_date = df["date_reported"].min()
max_date = df["date_reported"].max()

start_date, end_date = st.date_input(
    "Wähle einen Zeitraum",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

filtered_df = df[
    (df["country"] == selected_country) &
    (df["date_reported"] >= pd.to_datetime(start_date)) &
    (df["date_reported"] <= pd.to_datetime(end_date))
].sort_values("date_reported")

if filtered_df.empty:
    st.error(f"Für {selected_country} wurden keine Daten gefunden.")
    st.stop()

total_cases = int(filtered_df["cumulative_cases"].iloc[-1])
total_deaths = int(filtered_df["cumulative_deaths"].iloc[-1])
total_recovered = int(filtered_df["recovered_estimated"].iloc[-1])

col1, col2, col3 = st.columns(3)
col1.metric("Gesamtfälle", f"{total_cases:,}".replace(",", "."))
col2.metric("Todesfälle", f"{total_deaths:,}".replace(",", "."))
col3.metric("Geschätzte Genesene", f"{total_recovered:,}".replace(",", "."))

fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(filtered_df["date_reported"], filtered_df["cumulative_cases"], label="Kumulative Fälle")
ax1.plot(filtered_df["date_reported"], filtered_df["cumulative_deaths"], label="Kumulative Todesfälle")
ax1.plot(filtered_df["date_reported"], filtered_df["recovered_estimated"], label="Geschätzte Genesene")
ax1.set_title(f"COVID-19-Verlauf in {selected_country}")
ax1.set_xlabel("Datum")
ax1.set_ylabel("Anzahl")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

st.divider()

st.header("Weltkarte")

st.write("Die Karte zeigt die aktuelle Verteilung der ausgewählten Kennzahl pro Land.")

# Pro Land den neuesten Datensatz bestimmen
latest_map_df = (
    df.sort_values("date_reported")
      .groupby("country", as_index=False)
      .last()
)

# Kennzahl für die Karte auswählen
map_parameter_options = {
    "Kumulative Fälle": "cumulative_cases",
    "Kumulative Todesfälle": "cumulative_deaths",
    "Neue Fälle": "new_cases",
    "Neue Todesfälle": "new_deaths",
    "Geschätzte Genesene": "recovered_estimated"
}

selected_map_label = st.selectbox(
    "Kennzahl für die Karte auswählen",
    list(map_parameter_options.keys()),
    key="map_select"
)

map_parameter = map_parameter_options[selected_map_label]

# Fehlende Werte entfernen
latest_map_df = latest_map_df.dropna(subset=[map_parameter])

# Weltkarte erzeugen
fig_map = px.choropleth(
    latest_map_df,
    locations="country",
    locationmode="country names",
    color=map_parameter,
    hover_name="country",
    hover_data={
        "cumulative_cases": True,
        "cumulative_deaths": True,
        "recovered_estimated": True,
        "new_cases": True,
        "new_deaths": True
    },
    color_continuous_scale="Reds",
    title=f"Weltkarte: {selected_map_label}"
)

fig_map.update_layout(
    geo=dict(showframe=False, showcoastlines=True),
    margin=dict(l=0, r=0, t=50, b=0)
)

st.plotly_chart(fig_map, use_container_width=True)
# Ländervergleich
st.header("Ländervergleich")
st.write("Vergleichen Sie mehrere Länder anhand einer ausgewählten Kennzahl.")

selected_countries = st.multiselect(
    "Länder zum Vergleichen auswählen",
    countries,
    default=["Germany", "Canada"] if "Germany" in countries and "Canada" in countries else countries[:2]
)

parameter_options = {
    "Kumulative Fälle": "cumulative_cases",
    "Kumulative Todesfälle": "cumulative_deaths",
    "Neue Fälle": "new_cases",
    "Neue Todesfälle": "new_deaths",
    "Geschätzte Genesene": "recovered_estimated"
}

selected_label = st.selectbox("Kennzahl auswählen", list(parameter_options.keys()))
parameter = parameter_options[selected_label]

if selected_countries:
    compare_df = df[df["country"].isin(selected_countries)].sort_values("date_reported")

    fig2, ax2 = plt.subplots(figsize=(12, 6))

    for country in selected_countries:
        country_df = compare_df[compare_df["country"] == country]
        ax2.plot(country_df["date_reported"], country_df[parameter], label=country)

    ax2.set_title(f"Vergleich von {selected_label} zwischen ausgewählten Ländern")
    ax2.set_xlabel("Datum")
    ax2.set_ylabel("Anzahl")
    ax2.legend()
    ax2.grid(True)

    st.pyplot(fig2)
    st.info("Das Diagramm zeigt die Entwicklung der ausgewählten Kennzahl im Zeitverlauf für die gewählten Länder.")
else:
    st.warning("Bitte wählen Sie mindestens ein Land aus.")

st.divider()

# Vergleichstabelle
st.header("Vergleichstabelle")

summary_data = []
for country in selected_countries:
    country_df = df[df["country"] == country].sort_values("date_reported")
    summary_data.append({
        "Land": country,
        "Kumulative Fälle": int(country_df["cumulative_cases"].iloc[-1]),
        "Kumulative Todesfälle": int(country_df["cumulative_deaths"].iloc[-1]),
        "Geschätzte Genesene": int(country_df["recovered_estimated"].iloc[-1]),
        "Ø neue Fälle": round(country_df["new_cases"].mean(), 2),
        "Ø neue Todesfälle": round(country_df["new_deaths"].mean(), 2)
    })

summary_df = pd.DataFrame(summary_data)
st.dataframe(summary_df, use_container_width=True)

st.divider()
st.markdown("""
**Datenquelle:** WHO COVID-19 Global Data  
**Speicherung:** SQLite-Datenbank  
**Hinweis:** Genesene Fälle wurden näherungsweise als `kumulative Fälle - kumulative Todesfälle` berechnet.
""")