from config.settings import *
from queries.analytics import avg_by_city, top10_locations_pm10, compare_rotterdam_santiago, daily_avg_city, monthly_avg_pm10

df_top10 = top10_locations_pm10()
df_avg = avg_by_city()
df_comparison = compare_rotterdam_santiago()
df_daily_avg = daily_avg_city()
df_monthly_avg = monthly_avg_pm10()

df_top10.to_csv("results/top10_locations.csv", index=False)
df_avg.to_csv("results/avg_by_city.csv", index=False)
df_comparison.to_csv("results/compare_rotterdam_santiago.csv", index=False)
df_daily_avg.to_csv("results/daily_avg_city.csv", index=False)
df_monthly_avg.to_csv("results/monthly_avg_pm10.csv", index=False)
print("CSV exporté.")
