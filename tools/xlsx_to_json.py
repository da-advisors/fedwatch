#!/usr/bin/env python3
"""
Convert the FedWatch tracking spreadsheet into the JSON files the site reads.

    python3 tools/xlsx_to_json.py "FW Spreadsheet.xlsx"

Writes:
    data/fedwatch.json     from the FedWatch sheet   (comment deadlines)
    data/potuswatch.json   from the POTUSWatch sheet (executive actions)

This is the no-Hex path — useful for the first publication, or any time you'd
rather just re-run the converter and commit than go through the notebook.
Requires openpyxl:  pip install openpyxl
"""

import datetime
import json
import re
import sys
from pathlib import Path

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl is not installed. Run: pip install openpyxl")


# sheet name (matched loosely) -> output file
SHEETS = {
    "fedwatch": "data/fedwatch.json",
    "potuswatch": "data/potuswatch.json",
}

# The Title header carries a date suffix that changes each update
# ("Title (through 6/11/26)"). Normalize it back to a stable key.
HEADER_ALIASES = {
    "main isssues": "Main Issues",   # sic — typo in the source sheet
}

# Columns held back from the published JSON. "Notes from Leading Orgs" is
# internal working commentary (analyst initials, outreach notes), so it stays
# in the spreadsheet and off the public site. Delete the entry to publish it.
DROP_COLUMNS = {
    "Notes from Leading Orgs",
}

BLANK = {"", "na", "n/a", "none", "nan", "-", "tbd"}


def clean_header(raw):
    if raw is None:
        return None
    h = str(raw).strip()
    h = re.sub(r"\s*\(through[^)]*\)\s*$", "", h, flags=re.I)  # "Title (through 6/11/26)" -> "Title"
    return HEADER_ALIASES.get(h.lower(), h)


def clean_value(v):
    if v is None:
        return None
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.date().isoformat() if isinstance(v, datetime.datetime) else v.isoformat()
    s = str(v).strip()
    if s.lower() in BLANK:
        return None
    return re.sub(r"\s+", " ", s)


def clean_url(s):
    """Repair the one common typo class: a stray character typed before http."""
    if not s:
        return s
    fixed = re.sub(r"^[^h\s]+(?=https?://)", "", s)
    if fixed != s:
        print(f"   fixed malformed URL: {s}  ->  {fixed}")
    return fixed


def convert_sheet(ws):
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []
    headers = [clean_header(h) for h in rows[0]]

    records = []
    for raw in rows[1:]:
        rec = {}
        for h, v in zip(headers, raw):
            if not h or h in DROP_COLUMNS:
                continue
            rec[h] = clean_url(clean_value(v)) if h.lower().endswith("url") else clean_value(v)
        if any(v is not None for v in rec.values()):   # skip trailing blank rows
            records.append(rec)
    return records


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)

    path = Path(sys.argv[1])
    if not path.exists():
        sys.exit(f"No such file: {path}")

    root = Path(__file__).resolve().parent.parent
    wb = openpyxl.load_workbook(path, data_only=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    for key, out_rel in SHEETS.items():
        match = next((n for n in wb.sheetnames if n.lower().startswith(key)), None)
        if not match:
            print(f"!  no sheet starting with '{key}' — skipping {out_rel}")
            continue

        records = convert_sheet(wb[match])
        out = root / out_rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(
            {"last_updated": stamp, "record_count": len(records), "records": records},
            indent=2, ensure_ascii=False,
        ))
        dated = sum(1 for r in records if r.get("Due Date"))
        print(f"OK {out_rel:<26} {len(records):>4} records from '{match}'"
              + (f"  ({dated} with a due date)" if dated else ""))

    print("\nCommit the changed files in data/ and push.")


if __name__ == "__main__":
    main()
