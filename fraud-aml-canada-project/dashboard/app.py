"""
Fraud & AML Detection Dashboard
Run from the project root with:
    streamlit run dashboard/app.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx

from config import (
    CAFC_TIME_AGG, CAFC_PROVINCE_AGG, CHART2_SCORE_DIST, CHART3_RISK_TIER,
    CHART5_STRUCTURING, CHART7_RING_SIZES, CHART8_MODEL_MONITORING, CHART9_FUNNEL,
    CHART6_NETWORK_NODES, AML_GRAPH_EDGES, CANADA_GEOJSON,
)

st.set_page_config(page_title="Fraud & AML Detection Dashboard", layout="wide")
st.title("Fraud & AML Detection Dashboard")
st.caption(
    "Real Canadian fraud-report data (CAFC) combined with a synthetic "
    "transaction-scoring and network-detection engine (PaySim / IBM AML)."
)

role = st.sidebar.selectbox(
    "View as:", ["Fraud Operations", "AML / Compliance", "Data Science", "Executive Summary"]
)


def safe_load(path, name):
    if not os.path.exists(path):
        st.warning(f"{name} not built yet — run the matching pipeline script first.")
        return None
    return pd.read_parquet(path)


if role == "Fraud Operations":
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Chart 1 — Flagged Report Volume Over Time")
        df1 = safe_load(CAFC_TIME_AGG, "Chart 1 data")
        if df1 is not None:
            fig = px.line(df1, x="date_received", y="report_count", color="dollar_loss_tier",
                          title="Weekly CAFC report volume by dollar-loss tier")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Chart 2 — Anomaly Score Distribution")
        df2 = safe_load(CHART2_SCORE_DIST, "Chart 2 data")
        if df2 is not None:
            fig = px.bar(df2, x="score_bucket", y="transaction_count",
                        title="PaySim anomaly score distribution")
            st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Chart 3 — Transactions by Risk Tier")
        df3 = safe_load(CHART3_RISK_TIER, "Chart 3 data")
        if df3 is not None:
            fig = px.bar(df3, x="transaction_count", y="risk_tier", orientation="h",
                        title="Transaction count by risk tier", text="pct_of_total")
            st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Chart 5 — Structuring Detection (near CAD $10,000)")
        df5 = safe_load(CHART5_STRUCTURING, "Chart 5 data")
        if df5 is not None:
            fig = px.scatter(df5, x="hour_of_day", y="amount_cad", color="possible_structuring",
                            title="Transactions near the FINTRAC $10,000 threshold")
            st.plotly_chart(fig, use_container_width=True)

elif role == "AML / Compliance":
    st.subheader("Chart 4 — Flagged Activity by Province")
    df4 = safe_load(CAFC_PROVINCE_AGG, "Chart 4 data")
    if df4 is not None:
        metric = st.radio("Metric:", ["reports_per_100k", "report_count", "dollar_loss_per_capita"], horizontal=True)
        if os.path.exists(CANADA_GEOJSON):
            import json
            with open(CANADA_GEOJSON, "r", encoding="utf-8") as f:
                geojson = json.load(f)
            fig = px.choropleth(
                df4, geojson=geojson, locations="province", featureidkey="properties.PRENAME",
                color=metric, scope="north america", title=f"CAFC reports by province — {metric}",
            )
            fig.update_geos(fitbounds="locations", visible=False)
        else:
            fig = px.bar(df4.sort_values(metric, ascending=False), x="province", y=metric,
                        title=f"{metric} by province (GeoJSON not found — showing bar chart)")
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Chart 6 — Account Network Graph")
        nodes_df = safe_load(CHART6_NETWORK_NODES, "Chart 6 node data")
        edges_df = safe_load(AML_GRAPH_EDGES, "Chart 6 edge data")

        if nodes_df is not None and edges_df is not None:
            if len(edges_df) == 0:
                st.info("No flagged accounts found in the current sample — try re-running "
                        "06_build_aml_network.py with a larger sample_frac.")
            else:
                MAX_NODES = 300
                degree_count = pd.concat([edges_df["source"], edges_df["target"]]).value_counts()
                top_accounts = set(degree_count.head(MAX_NODES).index)
                edges_plot = edges_df[
                    edges_df["source"].isin(top_accounts) & edges_df["target"].isin(top_accounts)
                ]

                G = nx.from_pandas_edgelist(edges_plot, "source", "target", edge_attr=True, create_using=nx.DiGraph())
                st.caption(f"Showing top {G.number_of_nodes()} accounts by connections "
                           f"(of {nodes_df.shape[0]} total flagged accounts) — {G.number_of_edges()} edges")

                pos = nx.spring_layout(G, seed=42, k=0.3)

                edge_x, edge_y = [], []
                for u, v in G.edges():
                    if u in pos and v in pos:
                        edge_x += [pos[u][0], pos[v][0], None]
                        edge_y += [pos[u][1], pos[v][1], None]
                edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color="#888"), mode="lines")

                node_x = [pos[n][0] for n in G.nodes()]
                node_y = [pos[n][1] for n in G.nodes()]
                degrees = [G.degree(n) for n in G.nodes()]
                node_trace = go.Scatter(
                    x=node_x, y=node_y, mode="markers",
                    marker=dict(size=[6 + d for d in degrees], color=degrees, colorscale="Reds", showscale=True),
                    text=list(G.nodes()),
                )
                fig = go.Figure(data=[edge_trace, node_trace],
                                layout=go.Layout(title="Flagged account network (size/color = connections)",
                                                showlegend=False, height=500))
                st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Chart 7 — Detected Ring Size Distribution")
        df7 = safe_load(CHART7_RING_SIZES, "Chart 7 data")
        if df7 is not None:
            fig = px.bar(df7, x="size_bucket", y="num_rings", title="Detected rings by size",
                        hover_data=["total_cad_moved"])
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Chart 9 — Alert-to-STR Investigation Funnel")
    df9 = safe_load(CHART9_FUNNEL, "Chart 9 data")
    if df9 is not None:
        fig = go.Figure(go.Funnel(y=df9["stage"], x=df9["count"]))
        fig.update_layout(title="Investigation funnel")
        st.plotly_chart(fig, use_container_width=True)

elif role == "Data Science":
    st.subheader("Chart 8 — Model Precision & Recall Over Time")
    df8 = safe_load(CHART8_MODEL_MONITORING, "Chart 8 data")
    if df8 is not None:
        fig = px.line(df8, x="batch", y=["precision", "recall", "f1_score"],
                      title="Model performance across evaluation batches", markers=True)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df8)

elif role == "Executive Summary":
    st.subheader("Monthly Executive Summary")
    c1, c2, c3, c4 = st.columns(4)
    df1 = safe_load(CAFC_TIME_AGG, "Chart 1")
    df7 = safe_load(CHART7_RING_SIZES, "Chart 7")
    df9 = safe_load(CHART9_FUNNEL, "Chart 9")

    # High-level Metrics Cards
    if df1 is not None:
        c1.metric("Total Reports (CAFC)", f"{df1['report_count'].sum():,.0f}")
        c2.metric("Total $ Loss Reported", f"${df1['total_dollar_loss'].sum():,.0f}")
    if df7 is not None:
        c3.metric("Rings Detected", f"{df7['num_rings'].sum():,.0f}")
    if df9 is not None:
        str_row = df9[df9["stage"] == "STR Filed"]
        if len(str_row) > 0:
            c4.metric("STRs Filed", f"{int(str_row['count'].iloc[0]):,}")

    st.markdown("---")
    
    # Trend Analysis Chart (Full Width)
    if df1 is not None:
        st.plotly_chart(px.line(df1, x="date_received", y="report_count", title="Report volume trend"),
                        use_container_width=True)
        
    # Side-by-Side High Level Comparison Charts
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Chart 7 — Detected Ring Size Distribution")
        if df7 is not None:
            fig7 = px.bar(df7, x="size_bucket", y="num_rings", title="Detected rings by size",
                          hover_data=["total_cad_moved"])
            st.plotly_chart(fig7, use_container_width=True)
            
    with col_right:
        st.subheader("Chart 9 — Alert-to-STR Investigation Funnel")
        if df9 is not None:
            fig9 = go.Figure(go.Funnel(y=df9["stage"], x=df9["count"]))
            fig9.update_layout(title="Investigation funnel stages")
            st.plotly_chart(fig9, use_container_width=True)
