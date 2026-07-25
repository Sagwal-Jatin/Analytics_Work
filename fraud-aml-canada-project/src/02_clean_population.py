import pandas as pd
import os
from config import STATCAN_POPULATION_CSV, CAFC_PROVINCE_AGG, PROCESSED_DIR

PROVINCE_NAME_MAP = {
    "newfoundland and labrador": "Newfoundland and Labrador",
    "prince edward island": "Prince Edward Island",
    "nova scotia": "Nova Scotia",
    "new brunswick": "New Brunswick",
    "quebec": "Quebec",
    "ontario": "Ontario",
    "manitoba": "Manitoba",
    "saskatchewan": "Saskatchewan",
    "alberta": "Alberta",
    "british columbia": "British Columbia",
    "yukon": "Yukon",
    "northwest territories": "Northwest Territories",
    "nunavut": "Nunavut",
}


def load_population():
    df = pd.read_csv(STATCAN_POPULATION_CSV, low_memory=False)
    keep_cols = [c for c in ["REF_DATE", "GEO", "VALUE"] if c in df.columns]
    df = df[keep_cols]
    df["REF_DATE"] = df["REF_DATE"].astype(str)
    return df


def latest_population_by_province(df):
    latest_period = df["REF_DATE"].max()
    latest = df[df["REF_DATE"] == latest_period].copy()
    latest["province"] = latest["GEO"].astype(str).str.strip().str.lower().map(PROVINCE_NAME_MAP)
    latest = latest.dropna(subset=["province"])
    latest = latest.rename(columns={"VALUE": "population"})
    return latest[["province", "population"]], latest_period


if __name__ == "__main__":
    pop_df = load_population()
    pop_latest, period = latest_population_by_province(pop_df)
    print(f"Using population estimates for period: {period}")
    print(pop_latest.sort_values("population", ascending=False).to_string(index=False))

    province_agg = pd.read_parquet(CAFC_PROVINCE_AGG)
    merged = province_agg.merge(pop_latest, on="province", how="left")
    merged["reports_per_100k"] = (merged["report_count"] / merged["population"]) * 100_000
    merged["dollar_loss_per_capita"] = merged["total_dollar_loss"] / merged["population"]

    out_path = os.path.join(PROCESSED_DIR, "chart4_province_agg.parquet")
    merged.to_parquet(out_path, index=False)
    print(f"\nSaved -> {out_path}")
    print(merged.sort_values("reports_per_100k", ascending=False).to_string(index=False))