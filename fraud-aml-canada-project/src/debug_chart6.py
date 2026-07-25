import pandas as pd
from config import AML_GRAPH_EDGES, CHART6_NETWORK_NODES

edges = pd.read_parquet(AML_GRAPH_EDGES)
nodes = pd.read_parquet(CHART6_NETWORK_NODES)
print("edges:", edges.shape)
print("nodes:", nodes.shape)
print(edges.head())