# FedWatch Architecture

## **Data Flow**

```
Hex.tech (your colleague uploads XLSX)
  ↓
  ├─ Hex parses the file
  ├─ Hex Python code reads your GitHub token from secrets
  ├─ Hex makes API call: PUT https://api.github.com/repos/.../contents/data/fedwatch.json
  ↓
GitHub (fedwatch repo)
  ├─ JSON file stored at data/fedwatch.json
  ├─ GitHub Pages serves index.html from root
  ↓
Browser (colleague/anyone visits fedwatch.us)
  ├─ Loads index.html
  ├─ JavaScript fetches data/fedwatch.json (relative path, same origin)
  ├─ Filters, sorts, paginates locally
  ├─ Renders table with Agency/Main Issues dropdowns
```

---

## **Why This Works**

1. **No backend required** — all filtering/sorting happens in the browser (JavaScript)
2. **No database** — JSON file is the "database"
3. **No server hosting costs** — GitHub Pages is free
4. **Simple update process** — colleagues just run a Hex cell (feels like uploading to a Flask app)
5. **Version control** — every update is a git commit, easy to roll back if needed

---

## **Key Files**

| File | Purpose | Who edits |
|------|---------|-----------|
| `index.html` | Main page, filter UI, sorting logic | You (once) |
| `data/fedwatch.json` | Data source | Hex.tech (automatically via Python) |
| `hex_fedwatch_to_github.py` | Python snippet to push data | Hex.tech notebook (your colleague runs this) |

---

## **What Your Colleague Does**

1. Opens Hex notebook
2. Uploads/updates the XLSX with new fedwatch data
3. Runs the Python cell that says "Push to GitHub"
4. Sees `✅ Data pushed to GitHub successfully`
5. Tells colleagues: "Check fedwatch.us, data is updated"

That's it. They don't need to know about GitHub, JSON, or anything else.

---

## **Limitations & Tradeoffs**

### ✅ Advantages
- **Free** (~$12/yr for domain, that's it)
- **Simple** — just a JSON file and static HTML
- **Fast** — no database queries, instant page load
- **Scalable** — JSON can hold thousands of records without issue
- **No ops burden** — no containers, no servers to maintain

### ⚠️ Tradeoffs
- **No real-time updates** — page only refreshes when you reload (not auto-updating in background)
- **No authentication** — anyone can see the data (public GitHub Pages)
- **No history tracking** — only the latest JSON is visible (but git history exists if you dig)
- **Client-side filtering** — slower if dataset grows to 10k+ records (still fine for <5k)

For fedwatch with 1-2 updates/week, these are non-issues.

---

## **Optional Enhancements**

If you want to add these later (not needed now):

### Auto-refresh the page
Add this to `index.html` to refresh every 5 minutes:
```javascript
setInterval(() => location.reload(), 5 * 60 * 1000);
```

### Add more columns to the table
Edit `DISPLAY_COLUMNS` in `index.html` to include "Notes from Leading Orgs" or hide "Summary of Oppty" — whatever matches your UX.

### Export to CSV
Add a button that exports the filtered table as CSV (JavaScript, no backend needed).

### GitHub Actions auto-publish
Schedule the Hex notebook to run daily via GitHub Actions (optional, advanced).

---

## **Hand-Off Instructions (if you need to pass this to someone else)**

1. Give them this folder + the SETUP_GUIDE.md
2. They follow Steps 1-5 in the guide (GitHub repo + Pages setup)
3. They give you the custom domain DNS records to set up
4. You add the `GITHUB_TOKEN` secret in Hex
5. Done — they run the Hex cell to publish updates

---

## **Cost Recap**

| Item | Cost | Notes |
|------|------|-------|
| GitHub repo + Pages | $0 | Free |
| GitHub token | $0 | Free |
| Domain (fedwatch.us) | ~$12/yr | Registrar of choice |
| Hex.tech | $0* | Free tier works; paid tiers available |
| **Total** | **~$1/mo** | Just the domain |

*Hex has a free tier with generous limits. Your colleague's upload workload (1-2/week) is well within free tier.

---

## **Security Notes**

- The GitHub token is stored as a secret in Hex — it's not visible in the code
- The token has `repo` scope, which allows read/write to the repo only
- The public GitHub Pages are read-only (no one can modify data except via the token)
- The JSON file is public, but that's by design (it's a public tracker)

If you want to restrict access, you'd need to add authentication (not needed here).

---

End of architecture notes. You're good to go!
