import pandas as pd
import numpy as np
from config import CAFC_CSV, CAFC_CLEAN, CAFC_TIME_AGG, CAFC_PROVINCE_AGG

PROVINCE_MAP = {
    "ontario": "Ontario", "on": "Ontario",
    "quebec": "Quebec", "qc": "Quebec", "québec": "Quebec",
    "british columbia": "British Columbia", "bc": "British Columbia",
    "alberta": "Alberta", "ab": "Alberta",
    "manitoba": "Manitoba", "mb": "Manitoba",
    "saskatchewan": "Saskatchewan", "sk": "Saskatchewan",
    "nova scotia": "Nova Scotia", "ns": "Nova Scotia",
    "new brunswick": "New Brunswick", "nb": "New Brunswick",
    "newfoundland and labrador": "Newfoundland and Labrador", "nl": "Newfoundland and Labrador",
    "prince edward island": "Prince Edward Island", "pe": "Prince Edward Island", "pei": "Prince Edward Island",
    "yukon": "Yukon", "yt": "Yukon",
    "northwest territories": "Northwest Territories", "nt": "Northwest Territories",
    "nunavut": "Nunavut", "nu": "Nunavut",
}


def load_cafc():
    df = pd.read_csv(CAFC_CSV, encoding="utf-8-sig", low_memory=False)
    return df


def clean(df):
    df = df.copy()

    rename_map = {
        "Date Received / Date reçue": "date_received",
        "Complaint Received Type": "complaint_received_type",
        "Country": "country",
        "Province/State": "province_raw",
        "Fraud and Cybercrime Thematic Categories": "fraud_category",
        "Solicitation Method": "solicitation_method",
        "Gender": "gender",
        "Language of Correspondence": "language",
        "Victim Age Range / Tranche d'âge des victimes": "age_range",
        "Number of Victims / Nombre de victimes": "num_victims",
        "Dollar Loss /pertes financières": "dollar_loss",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    df["date_received"] = pd.to_datetime(df["date_received"], errors="coerce")
    df = df.dropna(subset=["date_received"])

    df["dollar_loss"] = (
        df["dollar_loss"].astype(str).str.replace(r"[$,]", "", regex=True).str.strip()
    )
    df["dollar_loss"] = pd.to_numeric(df["dollar_loss"], errors="coerce").fillna(0)

    df["province"] = (
        df["province_raw"].astype(str).str.strip().str.lower().map(PROVINCE_MAP)
    )
    df["is_canada"] = df["country"].astype(str).str.strip().str.lower().isin(["canada", "ca"])

    df["dollar_loss_tier"] = pd.cut(
        df["dollar_loss"],
        bins=[-1, 0, 1000, 10000, 50000, np.inf],
        labels=["No loss reported", "Low (<$1K)", "Medium ($1K-$10K)", "High ($10K-$50K)", "Critical (>$50K)"],
    )

    return df


def build_time_aggregate(df):
    """Feeds Chart 1: report volume over time by loss tier."""
    agg = (
        df.groupby([pd.Grouper(key="date_received", freq="W"), "dollar_loss_tier"], observed=True)
        .agg(report_count=("dollar_loss", "size"), total_dollar_loss=("dollar_loss", "sum"))
        .reset_index()
    )
    return agg


def build_province_aggregate(df):
    """Feeds Chart 4: activity by province."""
    canada_df = df[df["is_canada"] & df["province"].notna()]
    agg = (
        canada_df.groupby("province")
        .agg(report_count=("dollar_loss", "size"), total_dollar_loss=("dollar_loss", "sum"))
        .reset_index()
    )
    return agg


if __name__ == "__main__":
    print("Loading CAFC data...")
    raw = load_cafc()
    print(f"  {len(raw):,} raw rows")

    clean_df = clean(raw)
    print(f"  {len(clean_df):,} rows after cleaning")
    clean_df.to_parquet(CAFC_CLEAN, index=False)

    time_agg = build_time_aggregate(clean_df)
    time_agg.to_parquet(CAFC_TIME_AGG, index=False)
    print(f"  Chart 1 aggregate: {len(time_agg):,} rows -> {CAFC_TIME_AGG}")

    province_agg = build_province_aggregate(clean_df)
    province_agg.to_parquet(CAFC_PROVINCE_AGG, index=False)
    print(f"  Chart 4 aggregate: {len(province_agg):,} rows -> {CAFC_PROVINCE_AGG}")
    print(province_agg.sort_values("report_count", ascending=False).to_string(index=False))

    print("Done.")