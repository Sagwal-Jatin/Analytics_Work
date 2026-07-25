import pandas as pd
import numpy as np
import os
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from config import (
    PROCESSED_DIR, PAYSIM_SCORED, CHART2_SCORE_DIST, CHART3_RISK_TIER,
    CHART5_STRUCTURING, RANDOM_SEED,
)

FEATURES_PATH = os.path.join(PROCESSED_DIR, "paysim_features.parquet")

FEATURE_COLS = [
    "amount_cad", "amount_zscore", "txn_count_last_24h",
    "hour_of_day", "day_of_week", "is_new_counterparty",
    "near_structuring_threshold", "is_round_number",
]


def prep_features(df):
    X = df[FEATURE_COLS].copy()
    for col in ["is_new_counterparty", "near_structuring_threshold", "is_round_number"]:
        X[col] = X[col].astype(int)
    return X.fillna(0)


def run_isolation_forest(df, X):
    iso = IsolationForest(n_estimators=200, contamination=0.02, random_state=RANDOM_SEED, n_jobs=-1)
    iso.fit(X)
    raw_score = -iso.decision_function(X)  # flip: higher = more anomalous
    df["anomaly_score"] = (raw_score - raw_score.min()) / (raw_score.max() - raw_score.min())
    return df


def run_xgboost(df, X):
    y = df["isFraud"]
    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X, y, df.index, test_size=0.25, random_state=RANDOM_SEED, stratify=y
    )
    model = XGBClassifier(
        n_estimators=300, max_depth=5, learning_rate=0.1,
        scale_pos_weight=(y_train == 0).sum() / max((y_train == 1).sum(), 1),
        eval_metric="aucpr", random_state=RANDOM_SEED,
    )
    model.fit(X_train, y_train)

    df["fraud_probability"] = np.nan
    df.loc[idx_test, "fraud_probability"] = model.predict_proba(X_test)[:, 1]
    df.loc[idx_train, "fraud_probability"] = model.predict_proba(X_train)[:, 1]
    df["in_test_set"] = df.index.isin(idx_test)
    return df, model


def build_risk_tiers(df):
    quantiles = df["anomaly_score"].quantile([0.70, 0.90, 0.98]).values
    df["risk_tier"] = pd.cut(
        df["anomaly_score"],
        bins=[-np.inf, quantiles[0], quantiles[1], quantiles[2], np.inf],
        labels=["Low", "Medium", "High", "Critical"],
    )
    tier_agg = (
        df.groupby("risk_tier", observed=True)
        .agg(transaction_count=("amount_cad", "size"), total_amount_cad=("amount_cad", "sum"))
        .reset_index()
    )
    tier_agg["pct_of_total"] = tier_agg["transaction_count"] / tier_agg["transaction_count"].sum() * 100
    return df, tier_agg


def build_score_distribution(df):
    df["score_bucket"] = (df["anomaly_score"] // 0.05) * 0.05
    return df.groupby("score_bucket").size().reset_index(name="transaction_count")


def build_structuring_view(df):
    near_threshold = df[df["near_structuring_threshold"]].copy()
    same_day_counts = (
        near_threshold.groupby(["account_id", near_threshold["timestamp"].dt.date])
        .size().reset_index(name="near_threshold_txns_same_day")
    )
    near_threshold = near_threshold.merge(
        same_day_counts,
        left_on=["account_id", near_threshold["timestamp"].dt.date],
        right_on=["account_id", "timestamp"], suffixes=("", "_daycount"),
    )
    near_threshold["possible_structuring"] = near_threshold["near_threshold_txns_same_day"] >= 2
    cols = ["account_id", "amount_cad", "hour_of_day", "timestamp",
            "near_threshold_txns_same_day", "possible_structuring", "anomaly_score"]
    return near_threshold[cols]


if __name__ == "__main__":
    df = pd.read_parquet(FEATURES_PATH)
    X = prep_features(df)

    print("Running Isolation Forest...")
    df = run_isolation_forest(df, X)

    print("Running XGBoost...")
    df, model = run_xgboost(df, X)

    print("Building risk tiers (Chart 3)...")
    df, tier_agg = build_risk_tiers(df)
    tier_agg.to_parquet(CHART3_RISK_TIER, index=False)
    print(tier_agg.to_string(index=False))

    build_score_distribution(df).to_parquet(CHART2_SCORE_DIST, index=False)
    build_structuring_view(df).to_parquet(CHART5_STRUCTURING, index=False)

    df.to_parquet(PAYSIM_SCORED, index=False)
    print(f"Saved full scored dataset -> {PAYSIM_SCORED}")