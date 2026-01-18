import sys
from pathlib import Path

# Add the sql_optimized directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.settings import *
from queries.analytics import avg_by_city, top10_locations_pm10, compare_rotterdam_santiago, daily_avg_city, monthly_avg_pm10
from benchmark.timer import timer

bench = {}

with timer("top10_locations_pm10", bench):
    df_top10 = top10_locations_pm10()

with timer("avg_by_city", bench):
    df_avg = avg_by_city()

with timer("compare_rotterdam_santiago", bench):
    df_comparison = compare_rotterdam_santiago()

with timer("daily_avg_city", bench):
    df_daily_avg = daily_avg_city()

with timer("monthly_avg_pm10", bench):
    df_monthly_avg = monthly_avg_pm10()

df_top10.to_csv("results/top10_locations.csv", index=False)
df_avg.to_csv("results/avg_by_city.csv", index=False)
df_comparison.to_csv("results/compare_rotterdam_santiago.csv", index=False)
df_daily_avg.to_csv("results/daily_avg_city.csv", index=False)
df_monthly_avg.to_csv("results/monthly_avg_pm10.csv", index=False)
print("CSV exporté.")
print("\nQuery execution times (seconds):")
for query_name, elapsed_time in bench.items():
    print(f"  {query_name}: {elapsed_time:.4f}s")
