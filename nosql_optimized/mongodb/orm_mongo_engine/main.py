import db
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from queries.queries_nosql import *
import pandas as pd
from benchmark.timer import timer

Path("results").mkdir(exist_ok=True)

print("Count ORM:", Measurement.objects.count())

bench = {}

with timer("rolling_last_24h_available", bench):
    df_rolling = rolling_last_24h_available()

with timer("station_profiles", bench):
    df_profile = station_profiles()

df_rolling.to_csv("results/rolling_24h_avg.csv", index=False)
df_profile.to_csv("results/station_profiles.csv", index=False)

with timer("last_measures", bench):
    df_last = last_measures(sensor_id=13866, limit=10)
pd.DataFrame(df_last).to_csv("results/last_measures_sensor_13866.csv", index=False)

with timer("pollution_spikes", bench):
    df_spikes = pollution_spikes(threshold=600)
df_spikes.to_csv("results/pollution_spikes.csv", index=False)

print("Exports NoSQL générés.")
print("\nQuery execution times (seconds):")
for query_name, elapsed_time in bench.items():
    print(f"  {query_name}: {elapsed_time:.4f}s")
