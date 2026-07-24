"""
Hex.tech cell: publish the fedwatch dataframe to GitHub.

Paste this into a Python cell in your Hex notebook, below whatever cell
produces the dataframe. It writes data/fedwatch.json into the repo; GitHub
Pages picks it up within a minute or so and the site shows the new rows.

Prerequisites (one-time):
  1. Hex -> Notebook settings -> Secrets -> add GITHUB_TOKEN
     (a GitHub personal access token with `repo` scope)
  2. The repo below must already contain data/fedwatch.json

After that, every update is: refresh the dataframe, run this cell.
"""

import base64
import json
import math
from datetime import datetime, timezone

import pandas as pd
import requests

# ---------------------------------------------------------------- configuration
GITHUB_TOKEN = "{{ secrets.GITHUB_TOKEN }}"  # from Hex secrets - never hardcode
OWNER = "da-advisors"
REPO = "fedwatch"
PATH = "data/fedwatch.json"
BRANCH = "main"

# The dataframe to publish. Rename if your cell calls it something else.
SOURCE_DF = df

# Columns the site expects. Anything missing is created empty; anything extra
# is carried through into the JSON but ignored by the page.
EXPECTED_COLUMNS = [
    "Issue Date",
    "Due Date",
    "Title",
    "URL",
    "Agency",
    "Listing Type",
    "Main Issues",
    "Summary of Oppty",
    "Notes from Leading Orgs",
]


# ---------------------------------------------------------------- serialization
def clean_value(val):
    """Turn one spreadsheet cell into a JSON-safe value."""
    if val is None:
        return None
    # pd.isna raises on arrays/lists, so guard it
    try:
        if pd.isna(val):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
        return None
    # Dates -> ISO strings the browser's Date parser understands
    if hasattr(val, "isoformat"):
        return val.isoformat()
    text = str(val).strip()
    return text or None


def serialize_data(frame):
    frame = frame.copy()

    missing = [c for c in EXPECTED_COLUMNS if c not in frame.columns]
    if missing:
        print(f"WARNING: columns missing from the dataframe, publishing them empty: {missing}")
        for col in missing:
            frame[col] = None

    records = []
    for _, row in frame.iterrows():
        record = {col: clean_value(row[col]) for col in frame.columns}
        # Skip rows that are entirely blank (trailing rows in the XLSX)
        if any(v is not None for v in record.values()):
            records.append(record)
    return records


records = serialize_data(SOURCE_DF)

if not records:
    raise SystemExit("FAILED: no rows to publish - check the dataframe before running this cell.")

output = {
    "last_updated": datetime.now(timezone.utc).isoformat(),
    "record_count": len(records),
    "records": records,
}

content = json.dumps(output, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------- push to GitHub
url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{PATH}"
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# GitHub needs the current file's SHA in order to replace it
sha = None
probe = requests.get(url, headers=headers, params={"ref": BRANCH}, timeout=30)
if probe.status_code == 200:
    sha = probe.json().get("sha")
    print("Existing file found - updating it")
elif probe.status_code == 404:
    print("No file yet - creating it")
elif probe.status_code == 401:
    raise SystemExit("FAILED: GitHub rejected the token (401). Check the GITHUB_TOKEN secret in Hex.")
else:
    raise SystemExit(f"FAILED: could not read the file ({probe.status_code}): {probe.text[:300]}")

payload = {
    "message": f"Update fedwatch data - {len(records)} records - {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}",
    "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
    "branch": BRANCH,
}
if sha:
    payload["sha"] = sha

response = requests.put(url, headers=headers, json=payload, timeout=60)

if response.status_code in (200, 201):
    print("SUCCESS: data pushed to GitHub")
    print(f"   Records:   {len(records)}")
    print(f"   Timestamp: {output['last_updated']}")
    print(f"   Live in ~1 min at: https://{OWNER}.github.io/{REPO}/")
else:
    raise SystemExit(f"FAILED: push rejected ({response.status_code}): {response.text[:500]}")
