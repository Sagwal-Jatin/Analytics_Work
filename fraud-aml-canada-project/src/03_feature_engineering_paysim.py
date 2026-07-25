import pandas as pd
import os
import numpy as np
from config import PAYSIM_CSV, PROCESSED_DIR

OUT_PATH = os.path.join(PROCESSED_DIR, "paysim_features.parquet")


def load_paysim(sample_frac=None):
    df = pd.read_csv(PAYSIM_CSV)
    if sample_frac:
        # Keep every fraud row (rare, essential class); sample the rest down
        # so this runs comfortably on a laptop.
        fraud = df[df["isFraud"] == 1]
        legit = df[df["isFraud"] == 0].sample(frac=sample_frac, random_state=42)
        df = pd.concat([fraud, legit]).sort_values("step").reset_index(drop=True)
    return df


def engineer_features(df):
    df = df.copy()

    df = df.rename(columns={
        "amount": "amount_cad",
        "nameOrig": "account_id",
        "nameDest": "counterparty_id",
    })

    # simulated hour -> turn into an actual timestamp
    base_date = pd.Timestamp("2026-01-01")
    df["timestamp"] = base_date + pd.to_timedelta(df["step"], unit="h")
    df["hour_of_day"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek

    # Transaction velocity: count of this account's txns in the trailing 24 steps
    df = df.sort_values(["account_id", "step"])
    df["txn_count_last_24h"] = (
        df.groupby("account_id")["step"]
        .transform(lambda s: s.rolling(window=24, min_periods=1).count())
    )

    # Amount z-score vs. this account's own history
    acct_stats = df.groupby("account_id")["amount_cad"].agg(["mean", "std"]).rename(
        columns={"mean": "acct_mean_amount", "std": "acct_std_amount"}
    )
    df = df.merge(acct_stats, on="account_id", how="left")
    df["acct_std_amount"] = df["acct_std_amount"].fillna(0).replace(0, 1)
    df["amount_zscore"] = (df["amount_cad"] - df["acct_mean_amount"]) / df["acct_std_amount"]

    # New-counterparty flag
    df["pair_seen_before"] = df.duplicated(subset=["account_id", "counterparty_id"], keep="first")
    df["is_new_counterparty"] = ~df["pair_seen_before"]

    # FINTRAC structuring threshold (CAD $10,000)
    df["near_structuring_threshold"] = df["amount_cad"].between(9000, 9999.99)

    # Round-number bias
    df["is_round_number"] = (df["amount_cad"] % 100 == 0)

    return df


if __name__ == "__main__":
    print("Loading PaySim...")
    raw = load_paysim(sample_frac=0.15)  # set to None for the full 6.3M rows
    print(f"  {len(raw):,} rows loaded (all fraud rows kept)")

    features = engineer_features(raw)
    features.to_parquet(OUT_PATH, index=False)
    print(f"Saved -> {OUT_PATH}")
    print("\nSample engineered features:")
    print(features[["amount_cad", "amount_zscore", "txn_count_last_24h",
                    "is_new_counterparty", "near_structuring_threshold", "isFraud"]].head())