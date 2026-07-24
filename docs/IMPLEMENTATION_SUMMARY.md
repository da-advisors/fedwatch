# FedWatch Implementation Summary

**Total setup time: ~45 minutes**

---

## What You're Building

A free, zero-ops tracker for federal data collection opportunities. Data flows:

1. **Hex.tech** — Your colleague uploads XLSX, runs Python cell
2. **GitHub** — Data auto-writes to `fedwatch` repo via API
3. **Browser** — Anyone visits fedwatch.us, sees live filtered/sorted table

---

## Quick Steps

### Manual (you do these on GitHub/Hex):

1. **GitHub repo:** ✅ Already created at https://github.com/da-advisors/fedwatch

2. **Generate token:** https://github.com/settings/tokens
   - Name: `fedwatch-hex-write`
   - Scope: `repo`
   - Save it securely

3. **Enable Pages:** https://github.com/da-advisors/fedwatch/settings/pages
   - Branch: `main`, Folder: `/root`
   - Wait 2 min → https://da-advisors.github.io/fedwatch/ live

4. **Set up Hex:**
   - Add secret: `GITHUB_TOKEN` = your token
   - Paste Python cell (OWNER = `da-advisors`, REPO = `fedwatch`)
   - Run cell → should see ✅ success

### Copy-paste (use COPY_TO_GITHUB.md):

- `index.html` → repo root (update `da-advisors` first!)
- `data/fedwatch.json` → `data/` folder
- `hex_fedwatch_to_github.py` → Hex notebook

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `index.html` | The tracker UI — copy to GitHub repo root |
| `hex_fedwatch_to_github.py` | Hex cell for pushing data — copy to Hex |
| `data_fedwatch.json` | Placeholder JSON — copy to `data/` folder |
| `COPY_TO_GITHUB.md` | Step-by-step copy instructions |
| `SETUP_GUIDE.md` | Detailed setup walkthrough |
| `ARCHITECTURE.md` | How the system works |
| `QUICK_CHECKLIST.md` | Checklist of what's done/pending |

---

## Next: Your Turn

1. Follow **SETUP_GUIDE.md** Steps 1-3 (GitHub setup)
2. Use **COPY_TO_GITHUB.md** to paste the 3 files into GitHub
3. Follow **SETUP_GUIDE.md** Steps 6-7 (Hex setup + test)
4. Optional: Step 8 for custom domain

That's it. You're live.

---

## Cost

- **$0/month** using `da-advisors.github.io/fedwatch`
- **~$1/month** with custom domain `fedwatch.us`

No servers, no database, no ongoing ops. Just GitHub.

---

## Questions?

- **Data not showing?** → Check browser console (F12), verify `GITHUB_RAW_URL` matches your username
- **Hex cell fails?** → Verify token has `repo` scope, OWNER = your username
- **Custom domain?** → See Step 8 in SETUP_GUIDE.md (DNS config only)
