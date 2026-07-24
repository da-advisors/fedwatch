# Files to Copy Into GitHub

## 1. **index.html** → Repo root

Copy the contents of `index.html` from this folder.

**IMPORTANT:** Before pasting, find this line in the code:
```javascript
const GITHUB_RAW_URL = 'https://raw.githubusercontent.com/da-advisors/fedwatch/main/data/fedwatch.json';
```

Replace `da-advisors` with your org name. **For da-advisors:**
```javascript
const GITHUB_RAW_URL = 'https://raw.githubusercontent.com/da-advisors/fedwatch/main/data/fedwatch.json';
```

Then paste into GitHub → Add file → Create new file → **Filename: index.html**

---

## 2. **data/fedwatch.json** → data/ folder

Create a new file with:
- **Filename:** `data/fedwatch.json`
- **Content:** 
```json
{
  "last_updated": "2026-07-08T00:00:00",
  "record_count": 0,
  "records": []
}
```

---

## 3. **hex_fedwatch_to_github.py** → Hex notebook

Copy the Python script and paste into a Hex cell.

Update these two variables with YOUR info:
```python
OWNER = "YOUR_ORG_OR_USERNAME"  # Your org or username
REPO = "fedwatch"
```

**For da-advisors:**
```python
OWNER = "da-advisors"
REPO = "fedwatch"
```

Then in Hex Settings → Secrets, add:
- **Name:** `GITHUB_TOKEN`
- **Value:** (paste your token from Step 2 of setup guide)

Run the cell. You should see: ✅ Data pushed to GitHub successfully

---

That's it. Then test at: https://da-advisors.github.io/fedwatch/
