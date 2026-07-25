import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

CAFC_CSV = os.path.join(RAW_DIR, "cafc-open-gouv-database-2021-01-01-to-2025-09-30-extracted-2025-10-01.csv")

RANDOM_SEED = 42

CAFC_CLEAN = os.path.join(PROCESSED_DIR, "cafc_clean.parquet")
CAFC_PROVINCE_AGG = os.path.join(PROCESSED_DIR, "chart4_province_agg.parquet")
CAFC_TIME_AGG = os.path.join(PROCESSED_DIR, "chart1_volume_over_time.parquet")

STATCAN_POPULATION_CSV = os.path.join(RAW_DIR, "17100009.csv")

PAYSIM_CSV = os.path.join(RAW_DIR, "PS_20174392719_1491204439457_log.csv")

PAYSIM_SCORED = os.path.join(PROCESSED_DIR, "paysim_scored.parquet")
CHART2_SCORE_DIST = os.path.join(PROCESSED_DIR, "chart2_score_distribution.parquet")
CHART3_RISK_TIER = os.path.join(PROCESSED_DIR, "chart3_risk_tier.parquet")
CHART5_STRUCTURING = os.path.join(PROCESSED_DIR, "chart5_structuring.parquet")

CHART8_MODEL_MONITORING = os.path.join(PROCESSED_DIR, "chart8_precision_recall.parquet")

IBM_AML_CSV = os.path.join(RAW_DIR, "HI-Small_Trans.csv")
AML_GRAPH_EDGES = os.path.join(PROCESSED_DIR, "aml_graph_edges.parquet")
CHART6_NETWORK_NODES = os.path.join(PROCESSED_DIR, "chart6_network_nodes.parquet")

CHART7_RING_SIZES = os.path.join(PROCESSED_DIR, "chart7_ring_size_distribution.parquet")
CHART9_FUNNEL = os.path.join(PROCESSED_DIR, "chart9_investigation_funnel.parquet")

CANADA_GEOJSON = os.path.join(RAW_DIR, "canada_provinces.geojson")