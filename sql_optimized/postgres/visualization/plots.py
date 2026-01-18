import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "orm_hibernate" / "app" / "results"
OUTPUT_DIR = Path(__file__).parent / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_plots(base_path: Path = BASE):
    os.chdir(OUTPUT_DIR)
    
    # 1. Average PM10 by city
    df_avg = pd.read_csv(base_path / "top10_polluted_cities.csv", on_bad_lines='skip')

    plt.figure(figsize=(10,6))
    sns.barplot(
        data=df_avg.sort_values("avg_pm10", ascending=False),
        x="avg_pm10", y="city"
    )
    plt.title("Top 10 villes - PM10 moyen")
    plt.xlabel("PM10 moyen")
    plt.ylabel("Ville")
    plt.tight_layout()
    plt.savefig("top10_pm10_by_city.png")
    plt.close()

    # 2. Monthly trend
    df_trend = pd.read_csv(base_path / "monthly_trend_pm10.csv")

    plt.figure(figsize=(10,6))
    sns.lineplot(data=df_trend, x="month", y="avg_value")
    plt.title("Évolution mensuelle du PM10")
    plt.tight_layout()
    plt.savefig("monthly_trend_pm10.png")
    plt.close()

    # 3. City comparison
    df_comp = pd.read_csv(base_path / "city_comparison.csv", on_bad_lines='skip')

    plt.figure(figsize=(8,5))
    sns.barplot(data=df_comp, x="city", y="avg_value")
    plt.title("Comparaison PM10 entre villes")
    plt.tight_layout()
    plt.savefig("comparison_pm10.png")
    plt.close()

    # 4. Daily PM10 for Rotterdam
    df_daily = pd.read_csv(base_path / "daily_avg_city.csv", on_bad_lines='skip')

    plt.figure(figsize=(10,6))
    sns.lineplot(
        data=df_daily[df_daily["city"] == "Rotterdam"],
        x="day", y="avg_value"
    )
    plt.title("Niveaux quotidiens de PM10 à Rotterdam")
    plt.tight_layout()
    plt.savefig("daily_avg_rotterdam.png")
    plt.close()

    print("Graphs generated.")


if __name__ == "__main__":
    generate_plots()
