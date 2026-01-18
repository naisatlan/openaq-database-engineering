import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import ast


BASE = Path("../orm_mongo_engine/results")

# Moyenne PM10 sur les dernières 24h disponibles
df_rolling = pd.read_csv(BASE / "rolling_24h_avg.csv", on_bad_lines='skip')

plt.figure(figsize=(10,6))
plt.barh(df_rolling["_id"], df_rolling["avg_pm10"])
plt.title("PM10 moyen - dernières 24h disponibles")
plt.xlabel("PM10")
plt.ylabel("Ville")
plt.tight_layout()
plt.savefig("rolling_24h_avg_pm10.png")
plt.close()

# Clusters de stations similaires
df_profiles = pd.read_csv(BASE / "station_profiles.csv", on_bad_lines='skip')

plt.figure(figsize=(10,6))
plt.scatter(df_profiles["avg"], df_profiles["std"], alpha=0.6)

plt.title("Profil comportemental des stations PM10")
plt.xlabel("PM10 moyen")
plt.ylabel("Variabilité (écart-type)")
plt.tight_layout()
plt.savefig("station_profiles.png")
plt.close()


# Pics de pollution extrêmes
df_spikes = pd.read_csv(BASE / "pollution_spikes.csv", on_bad_lines='skip')

df_spikes["_id"] = df_spikes["_id"].apply(ast.literal_eval)
df_spikes["hour"] = pd.to_datetime(df_spikes["_id"].apply(lambda x: x["hour"]))
df_spikes["city"] = df_spikes["_id"].apply(lambda x: x["city"])
df_spikes = df_spikes[df_spikes["hour"].dt.month != 11]

df_spikes = df_spikes.sort_values("hour").iloc[::15]  # sous-échantillonnage

plt.figure(figsize=(12,6))
plt.scatter(df_spikes["hour"], df_spikes["max_value"], alpha=0.6, label="Pic horaire")

plt.title("Pics de pollution extrêmes (PM10)")
plt.xlabel("Date / heure")
plt.ylabel("PM10 max")
plt.legend()
plt.tight_layout()
plt.savefig("pollution_spikes.png")
plt.close()

print("Graphiques NoSQL générés.")
