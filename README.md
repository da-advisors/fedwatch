# FedWatch

A public tracker for federal regulatory activity, in two views:

- **Comment deadlines** — rules, notices, and RFIs open for public comment,
  sorted so the soonest deadline is at the top.
- **Executive actions** — executive orders, proclamations, and presidential
  memoranda, newest first.

Both are filterable, sortable, and searchable. Tabs are linkable:
`#fedwatch` and `#potuswatch`.

No backend, no database, no servers: a static page plus a JSON file, served free
from GitHub Pages.

**Live site:** https://da-advisors.github.io/fedwatch/

---

## How it works

```
Hex.tech notebook  ->  GitHub repo          ->  GitHub Pages  ->  browser
  (XLSX in)            (data/fedwatch.json)     (index.html)
```

Someone refreshes the spreadsheet in Hex and runs one cell. That cell writes
`data/fedwatch.json` into this repo via the GitHub API. The page fetches that
file and does all filtering, sorting, and pagination in the browser.

## Repo contents

| Path | Purpose |
|---|---|
| `index.html` | The whole site — markup, styles, and logic in one file |
| `data/fedwatch.json` | Comment-deadline dataset (the "Comment deadlines" tab) |
| `data/potuswatch.json` | Executive-actions dataset (the "Executive actions" tab) |
| `tools/xlsx_to_json.py` | Converts the tracking spreadsheet into both JSON files |
| `hex_fedwatch_to_github.py` | The Hex cell that publishes the data |
| `assets/` | Logo, favicons, social preview image |
| `serve.command` | Double-click to preview the site locally |
| `docs/` | Setup guide, architecture notes, checklist |

## Updating the data

Two ways. Either is fine.

**From the spreadsheet (no Hex needed):**

```bash
pip install openpyxl                      # once
python3 tools/xlsx_to_json.py "FW Spreadsheet.xlsx"
git add data/ && git commit -m "Update data" && git push
```

**From Hex, once it's set up:**

1. Open the Hex notebook and refresh the dataframe from the latest XLSX.
2. Run the publish cell. It should print `SUCCESS: data pushed to GitHub`.
3. Wait ~1 minute for Pages to rebuild, then reload the site.

Either way the site picks up the change on next load.

## Previewing locally

**Double-click `serve.command`.** It starts a small local web server and opens
the page in your browser. Close the Terminal window when you're done.

Don't double-click `index.html` directly — browsers refuse to let a page opened
as a `file://` URL read other local files, so the table comes up empty. (The
page detects this and falls back to reading the published data from GitHub, but
that only works once the repo has been pushed.)

If you'd rather do it by hand:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Design

All colors, fonts, spacing, and radii are defined as CSS custom properties in
one `:root` block at the top of `index.html`. Change a value there and it
propagates everywhere — nothing below that block uses raw hex.

Deadline urgency is shown with a colored pill, but the color is reinforcement
only: every pill also carries a glyph and a written label ("6 days left",
"Closed 12 days ago"), so it still reads correctly in greyscale, in print, and
for colorblind readers.

## Data format

`data/fedwatch.json`:

```json
{
  "last_updated": "2026-07-24T18:00:00+00:00",
  "record_count": 1,
  "records": [
    {
      "Issue Date": "2026-07-01",
      "Due Date": "2026-08-15",
      "Title": "Request for Information on Household Survey Methods",
      "URL": "https://www.federalregister.gov/example",
      "Agency": "Census Bureau",
      "Listing Type": "RFI",
      "Main Issues": "Survey methodology",
      "Summary of Oppty": "Comment on proposed changes to the sampling frame."
    }
  ]
}
```

Columns are read by name, so column order in the XLSX doesn't matter. A missing
column publishes as empty rather than breaking the page.

**"Notes from Leading Orgs" is deliberately not published.** It holds internal
working commentary — analyst initials, outreach notes — so `tools/xlsx_to_json.py`
strips it via `DROP_COLUMNS`. It stays in the spreadsheet. Delete the entry in
that set to publish it.

Rows with a blank or unparseable due date still appear — they sort to the bottom
and show "No comment period".

## First-time setup

See [`docs/SETUP_GUIDE.md`](docs/SETUP_GUIDE.md) — GitHub Pages, the access
token, the Hex secret, and the optional custom domain.

## Cost

GitHub Pages and the Hex free tier are $0. The only line item is the domain,
about $12/year.
