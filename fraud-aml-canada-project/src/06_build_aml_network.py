import pandas as pd
import networkx as nx
import pickle
import os
from config import IBM_AML_CSV, PROCESSED_DIR, AML_GRAPH_EDGES, CHART6_NETWORK_NODES


def load_aml(sample_frac=None):
    df = pd.read_csv(IBM_AML_CSV)
    df = df.rename(columns={
        "Account": "from_account",
        "Account.1": "to_account",
        "Amount Paid": "amount_cad",
        "Is Laundering": "is_laundering",
    })
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    if sample_frac:
        launder = df[df["is_laundering"] == 1]
        legit = df[df["is_laundering"] == 0].sample(frac=sample_frac, random_state=42)
        df = pd.concat([launder, legit]).sort_values("Timestamp").reset_index(drop=True)
    return df


def build_graph(df):
    G = nx.DiGraph()
    for _, row in df.iterrows():
        u, v = row["from_account"], row["to_account"]
        amt = row["amount_cad"]
        is_laundering = row["is_laundering"]

        if G.has_edge(u, v):
            G[u][v]["weight"] += amt
            G[u][v]["txn_count"] += 1
            G[u][v]["laundering_flag"] = max(G[u][v]["laundering_flag"], is_laundering)
        else:
            G.add_edge(u, v, weight=amt, txn_count=1, laundering_flag=is_laundering)
    return G


def flagged_subgraph(G):
    """Only accounts connected to a known laundering-labeled transaction —
    you investigate the accounts an alert points to, not the whole bank."""
    flagged_edges = [(u, v) for u, v, d in G.edges(data=True) if d["laundering_flag"] == 1]
    flagged_nodes = set()
    for u, v in flagged_edges:
        flagged_nodes.update([u, v])
        flagged_nodes.update(G.predecessors(u))
        flagged_nodes.update(G.successors(v))
    return G.subgraph(flagged_nodes).copy()


def node_summary(G):
    rows = []
    for node in G.nodes():
        rows.append({
            "account_id": node,
            "in_degree": G.in_degree(node),
            "out_degree": G.out_degree(node),
            "total_degree": G.in_degree(node) + G.out_degree(node),
            "total_amount_involved": sum(d["weight"] for _, _, d in G.edges(node, data=True)) +
                                      sum(d["weight"] for _, _, d in G.in_edges(node, data=True)),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = load_aml(sample_frac=0.1)  # set to None for the full file
    print(f"  {len(df):,} transactions loaded")

    G_full = build_graph(df)
    print(f"  Full graph: {G_full.number_of_nodes():,} accounts, {G_full.number_of_edges():,} edges")

    G_flagged = flagged_subgraph(G_full)
    print(f"  Flagged subgraph: {G_flagged.number_of_nodes():,} accounts, {G_flagged.number_of_edges():,} edges")

    nx.to_pandas_edgelist(G_flagged).to_parquet(AML_GRAPH_EDGES, index=False)
    node_summary(G_flagged).to_parquet(CHART6_NETWORK_NODES, index=False)

    with open(os.path.join(PROCESSED_DIR, "aml_flagged_graph.pkl"), "wb") as f:
        pickle.dump(G_flagged, f)
    print("Saved graph, edges, and node summary.")