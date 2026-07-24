# FedWatch Setup Checklist

## **You Have:**
- ✅ `index.html` — the main page
- ✅ `hex_fedwatch_to_github.py` — the Hex snippet
- ✅ `SETUP_GUIDE.md` — detailed steps
- ✅ `ARCHITECTURE.md` — how it all works

## **Follow SETUP_GUIDE.md in order:**

- [ ] Step 1: Create `fedwatch` repo on GitHub
- [ ] Step 2: Generate GitHub personal access token
- [ ] Step 3: Enable GitHub Pages (branch: main, folder: root)
- [ ] Step 4: Upload `index.html` to repo root
  - [ ] **Update line with da-advisors** in the JavaScript
- [ ] Step 5: Create `data/fedwatch.json` placeholder
- [ ] Step 6: Set up Hex integration
  - [ ] Add `GITHUB_TOKEN` secret in Hex
  - [ ] Update `OWNER` variable in the Python snippet
  - [ ] Run the cell to test
- [ ] Step 7: Test the site at `https://da-advisors.github.io/fedwatch`
- [ ] Step 8 (optional): Set up custom domain `fedwatch.us`

## **First Test Run:**

1. In Hex, paste the Python snippet with your GitHub token configured
2. Run the cell
3. You should see: `✅ Data pushed to GitHub successfully`
4. Visit `https://da-advisors.github.io/fedwatch` (or your custom domain)
5. You should see the FedWatch page with your data in a table
6. Test: Click a column header to sort, filter by Agency, search for a term

## **For Your Colleague:**

Once you've completed the setup, they just need to:
1. Upload XLSX file to Hex
2. Run the notebook cell that pushes to GitHub (you'll set this up)
3. Say "Check fedwatch.us"

No other steps. No SSH, no git, no Docker. Just run the cell.

## **Cost:**
- **$0/month** if using `da-advisors.github.io/fedwatch`
- **~$1/month** if using custom domain like `fedwatch.us`

## **Need Help?**

Check `ARCHITECTURE.md` → **Troubleshooting** section

---

**You're ~45 min of work away from a fully functional, zero-cost fedwatch site.**

Go build it!
