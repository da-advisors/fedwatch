# FedWatch Setup Guide

Free GitHub Pages + Hex.tech integration for data collection tracking.

---

## **Step 1: Create GitHub Repository**

✅ **Already done** — your repo is at https://github.com/da-advisors/fedwatch

---

## **Step 2: Create GitHub Personal Access Token**

1. Go to https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. **Token name:** `fedwatch-hex-write`
4. **Expiration:** No expiration (or pick an annual reminder)
5. **Scopes:** Check `repo` (full repo access)
6. Click **Generate token**
7. **Copy the token immediately** — you won't see it again

---

## **Step 3: Set Up GitHub Pages**

1. In your `fedwatch` repo (https://github.com/da-advisors/fedwatch), go to **Settings** → **Pages**
2. Under "Build and deployment":
   - **Source:** Deploy from a branch
   - **Branch:** `main` / `root`
3. Click **Save**
4. Wait ~2 minutes for GitHub to deploy (you'll see a green checkmark)
5. Your site is now live at: **`https://da-advisors.github.io/fedwatch/`**

---

## **Step 4: Upload index.html**

1. In your `fedwatch` repo, click **Add file** → **Create new file**
2. **Filename:** `index.html`
3. Paste the contents of the `index.html` file provided
4. **Important:** In the JavaScript, find this line:
   ```javascript
   const GITHUB_RAW_URL = 'https://raw.githubusercontent.com/da-advisors/fedwatch/main/data/fedwatch.json';
   ```
5. Click **Commit changes**

---

## **Step 5: Create Data Directory**

1. Click **Add file** → **Create new file**
2. **Filename:** `data/fedwatch.json`
3. Paste this placeholder:
   ```json
   {
     "last_updated": "2026-07-08T00:00:00",
     "record_count": 0,
     "records": []
   }
   ```
4. Click **Commit changes**

---

## **Step 6: Set Up Hex.tech Integration**

### In Hex:

1. Create a new cell in your Hex notebook
2. Paste the code from `hex_fedwatch_to_github.py`
3. Update these variables:
   ```python
   OWNER = "da-advisors"
   REPO = "fedwatch"
   ```
4. Go to **Notebook settings** (gear icon) → **Secrets**
5. Click **Add secret**
   - **Name:** `GITHUB_TOKEN`
   - **Value:** Paste the token you generated in Step 2
6. Click **Create secret**
7. Run the cell to test it (should push data to GitHub)

---

## **Step 7: Test the Setup**

1. Visit `https://da-advisors.github.io/fedwatch/` (or your custom domain, see below)
2. You should see the FedWatch page with your data
3. Test filtering, searching, sorting, pagination

---

## **Step 8: Set Custom Domain (Optional)**

If you want `fedwatch.us` instead of `da-advisors.github.io/fedwatch/`:

1. In your `fedwatch` repo, go to **Settings** → **Pages**
2. Under "Custom domain," enter `fedwatch.us`
3. Click **Save**
4. GitHub will show DNS instructions. Go to your domain registrar (wherever you bought `fedwatch.us`)
5. Add a **CNAME record:**
   - **Name:** `fedwatch` (or leave blank if it's the apex domain)
   - **Value:** `da-advisors.github.io`
6. Wait 5-30 minutes for DNS to propagate
7. Return to GitHub Pages settings and verify the domain (it'll show a green checkmark when ready)

**Alternative apex domain setup:**
If using `fedwatch.us` (not `www.fedwatch.us`), use GitHub's A records instead:
- Add 4 A records pointing to GitHub's IPs:
  - `185.199.108.153`
  - `185.199.109.153`
  - `185.199.110.153`
  - `185.199.111.153`

---

## **Ongoing Use**

### Your colleague updates data:

1. In Hex, they run the notebook cell that calls the GitHub API
2. The data is written to `data/fedwatch.json` in the repo
3. Refresh the FedWatch page — it automatically fetches the latest JSON

### To make regular updates automatic:

1. Set up a **GitHub Action** workflow in `.github/workflows/fedwatch-schedule.yml` (optional — requires some CI/CD setup)
2. Or just schedule the Hex notebook to run on a timer

---

## **Troubleshooting**

### Data not showing on the page?
- Check browser console (F12 → Console tab) for errors
- Verify the `GITHUB_RAW_URL` in `index.html` matches your repo path
- Make sure `data/fedwatch.json` exists and is valid JSON

### Hex cell fails to push?
- Verify `GITHUB_TOKEN` secret is set correctly
- Check that the token has `repo` scope
- Ensure `OWNER` and `REPO` variables match your GitHub account

### Custom domain not working?
- DNS changes take time (5-30 min). Wait and refresh.
- Verify the CNAME or A records are set correctly at your registrar
- Check GitHub Pages settings for any error messages

---

## **Cost Breakdown**

- GitHub repo: **Free**
- GitHub Pages hosting: **Free**
- Hex.tech: **Free** (if just using for data export; paid tiers available)
- Custom domain (fedwatch.us): **~$12/year** at a registrar

**Total: ~$1/month** (just the domain)

---

## **File Structure**

```
fedwatch/
├── index.html              # Main page (GitHub Pages serves this)
├── data/
│   └── fedwatch.json       # Data file (updated by Hex)
├── README.md               # Project description
└── .gitignore              # (auto-generated)
```

---

Done! Your colleague can now upload data via Hex, and it'll appear on fedwatch.us automatically.
