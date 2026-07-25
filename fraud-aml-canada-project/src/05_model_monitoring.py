import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
from config import PAYSIM_SCORED, CHART8_MODEL_MONITORING

N_BATCHES = 10
DECISION_THRESHOLD = 0.5


def run():
    df = pd.read_parquet(PAYSIM_SCORED)
    df = df[df["in_test_set"]].sort_values("step").reset_index(drop=True)

    df["batch"] = pd.qcut(df.index, N_BATCHES, labels=[f"Batch {i+1}" for i in range(N_BATCHES)])

    results = []
    for batch, group in df.groupby("batch", observed=True):
        y_true = group["isFraud"]
        y_pred = (group["fraud_probability"] >= DECISION_THRESHOLD).astype(int)

        results.append({
            "batch": batch,
            "avg_step": group["step"].mean(),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1_score": f1_score(y_true, y_pred, zero_division=0),
            "n_transactions": len(group),
            "n_actual_fraud": y_true.sum(),
        })

    monitoring_df = pd.DataFrame(results)
    monitoring_df.to_parquet(CHART8_MODEL_MONITORING, index=False)
    print(monitoring_df.to_string(index=False))
    return monitoring_df


if __name__ == "__main__":
    run()