import json
from config import CANADA_GEOJSON

PROVINCE_NAME_FIXES = {
    # left side: whatever weird value shows up in the file (French, abbreviation, etc)
    # right side: what the dashboard expects
    "colombie-britannique": "British Columbia",
    "québec": "Quebec", "quebec": "Quebec",
    "nouvelle-écosse": "Nova Scotia",
    "nouveau-brunswick": "New Brunswick",
    "île-du-prince-édouard": "Prince Edward Island",
    "terre-neuve-et-labrador": "Newfoundland and Labrador",
    "territoires du nord-ouest": "Northwest Territories",
    "yukon": "Yukon",
    "nunavut": "Nunavut",
    "ontario": "Ontario", "alberta": "Alberta", "manitoba": "Manitoba",
    "saskatchewan": "Saskatchewan", "nova scotia": "Nova Scotia",
}

with open(CANADA_GEOJSON) as f:
    gj = json.load(f)

# what property keys actually exist
sample_props = gj["features"][0]["properties"]
print("Available property keys:", list(sample_props.keys()))
print("Sample values:", sample_props)