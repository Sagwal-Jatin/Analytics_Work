import pandas as pd
import networkx as nx
import pickle
import os
import community as community_louvain  # pip install python-louvain

from config import PROCESSED_DIR, CHART7_RING_SIZES, CHART9_FUNNEL, CHART3_RISK_TIER

GRAPH_PATH = os.path.join(PROCESSED_DIR, "aml_flagged_graph.pkl")
STR_DOLLAR_THRESHOLD = 50_000


def run_community_detection(G):
    G_undirected = G.to_undirected()  # Louvain needs an undirected graph
    partition = community_louvain.best_partition(G_undirected, weight="weight", random_state=42)
    return pd.DataFrame(list(partition.items()), columns=["account_id", "community_id"])


def summarize_rings(G, community_df):
    edge_df = nx.to_pandas_edgelist(G)
    edge_df = edge_df.merge(
        community_df.rename(columns={"account_id": "source", "community_id": "source_comm"}), on="source"
    ).merge(
        community_df.rename(columns={"account_id": "target", "community_id": "target_comm"}), on="target"
    )
    # Keep only money moving within the same detected ring
    intra_ring_edges = edge_df[edge_df["source_comm"] == edge_df["target_comm"]]

    ring_summary = (
        intra_ring_edges.groupby("source_comm")
        .agg(total_cad_moved=("weight", "sum"), txn_count=("txn_count", "sum"))
        .reset_index().rename(columns={"source_comm": "community_id"})
    )
    ring_sizes = community_df.groupby("community_id").size().reset_index(name="num_accounts")
    ring_summary = ring_summary.merge(ring_sizes, on="community_id")
    ring_summary = ring_summary[ring_summary["num_accounts"] >= 2]  # drop isolated accounts

    ring_summary["size_bucket"] = pd.cut(
        ring_summary["num_accounts"], bins=[1, 3, 6, 100],
        labels=["2-3 accounts", "4-6 accounts", "7+ accounts"]
    )
    size_dist = (
        ring_summary.groupby("size_bucket", observed=True)
        .agg(num_rings=("community_id", "size"), total_cad_moved=("total_cad_moved", "sum"))
        .reset_index()
    )
    return ring_summary, size_dist


def build_funnel(tier_agg, ring_summary):
    """
    NOTE: PaySim and IBM AML are separate synthetic datasets with no shared
    account IDs, so this funnel shows workflow *shape*, not a literal join.
    State that explicitly in your write-up.
    """
    flagged = tier_agg[tier_agg["risk_tier"].isin(["High", "Critical"])]["transaction_count"].sum()
    reviewed = int(flagged * 0.85)
    escalated = int(ring_summary["num_accounts"].sum())
    str_filed_rings = ring_summary[ring_summary["total_cad_moved"] > STR_DOLLAR_THRESHOLD]
    str_filed = len(str_filed_rings)

    funnel_df = pd.DataFrame({
        "stage": ["Flagged", "Reviewed", "Escalated (in a detected ring)", "STR Filed"],
        "count": [flagged, reviewed, escalated, str_filed],
    })
    funnel_df["conversion_from_previous_pct"] = (
        funnel_df["count"] / funnel_df["count"].shift(1) * 100
    ).fillna(100)
    return funnel_df, str_filed_rings


if __name__ == "__main__":
    with open(GRAPH_PATH, "rb") as f:
        G = pickle.load(f)

    community_df = run_community_detection(G)
    print(f"{community_df['community_id'].nunique():,} communities detected")

    ring_summary, size_dist = summarize_rings(G, community_df)
    size_dist.to_parquet(CHART7_RING_SIZES, index=False)
    print(size_dist.to_string(index=False))

    tier_agg = pd.read_parquet(CHART3_RISK_TIER)
    funnel_df, str_rings = build_funnel(tier_agg, ring_summary)
    funnel_df.to_parquet(CHART9_FUNNEL, index=False)
    print(funnel_df.to_string(index=False))

    print(f"\n{len(str_rings)} ring(s) recommended for STR filing.")
    if len(str_rings) > 0:
        print(str_rings.sort_values("total_cad_moved", ascending=False).head(1).to_string(index=False))