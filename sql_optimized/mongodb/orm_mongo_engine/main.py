import sys
from pathlib import Path

# Add the sql_optimized directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mongodb.orm_mongo_engine.config.settings import *
from mongodb.orm_mongo_engine.queries.analytics import avg_by_city, top10_locations_pm10, compare_rotterdam_santiago, daily_avg_city, monthly_avg_pm10
from benchmark.timer import timer

bench = {}

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

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

df_top10.to_csv(RESULTS_DIR / "top10_locations.csv", index=False)
df_avg.to_csv(RESULTS_DIR / "avg_by_city.csv", index=False)
df_comparison.to_csv(RESULTS_DIR / "compare_rotterdam_santiago.csv", index=False)
df_daily_avg.to_csv(RESULTS_DIR / "daily_avg_city.csv", index=False)
df_monthly_avg.to_csv(RESULTS_DIR / "monthly_avg_pm10.csv", index=False)
print("CSV exporté.")
print("\nQuery execution times (seconds):")
for query_name, elapsed_time in bench.items():
    print(f"  {query_name}: {elapsed_time:.4f}s")
