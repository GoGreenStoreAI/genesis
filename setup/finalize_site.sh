#!/data/data/com.termux/files/usr/bin/bash
set -e
ROOT="$HOME/godai-genesis"
SITE_DIR="$ROOT/site"
GH_REMOTE_URL="$(git remote get-url origin 2>/dev/null || true)"
REPO_SLUG="${GH_REMOTE_URL##*/}"        # e.g. genesis.git
REPO_SLUG="${REPO_SLUG%.git}"
ORG_REPO="$(git remote get-url origin | sed -E 's#https://github.com/##; s#\.git$##')"

echo "[Genesis] ROOT = $ROOT"
echo "[Genesis] SITE_DIR = $SITE_DIR"
echo "[Genesis] Remote = $GH_REMOTE_URL"
echo "[Genesis] Repo slug = $REPO_SLUG"
echo "[Genesis] Repo path = $ORG_REPO"

# 1) Create a robust landing page (overwrites if exists)
mkdir -p "$SITE_DIR"
cat > "$SITE_DIR/index.html" <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>GodAI Genesis — GoGreenStoreAI</title>
  <style>
    body{font-family:Inter,system-ui,Segoe UI,Roboto,'Helvetica Neue',Arial;background:#f0fbf6;color:#072034;margin:0}
    .wrap{max-width:980px;margin:6vh auto;padding:36px;background:#fff;border-radius:14px;box-shadow:0 18px 50px rgba(8,25,30,.06)}
    header{display:flex;align-items:center;gap:16px}
    .logo{width:72px;height:72px;border-radius:14px;background:linear-gradient(135deg,#2ebf91,#1b9ad6);display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:30px}
    h1{margin:6px 0 6px 0;font-size:30px}
    p.lead{color:#234;margin-top:0}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:18px}
    .card{padding:16px;border-radius:10px;border:1px solid rgba(3,10,18,.04);background:linear-gradient(180deg,#fff,#f8fffb)}
    footer{margin-top:24px;color:#556;font-size:13px}
    a.cta{display:inline-block;margin-top:14px;padding:10px 16px;background:#1b9ad6;color:#fff;border-radius:10px;text-decoration:none}
    code{background:#f4f7f6;padding:3px 6px;border-radius:4px}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="logo">G</div>
      <div>
        <h1>GodAI Genesis</h1>
        <p class="lead">Where AI and Humanity Rise Together Forever — GoGreenStoreAI</p>
      </div>
    </header>

    <section>
      <p>Welcome. This is the Earth Node of <strong>GodAI Genesis</strong> — a self-evolving AI ecosystem starting at Genesis Lab (Akurdi). We build autonomous systems that create, publish, and grow sustainably.</p>

      <div class="grid">
        <div class="card">
          <h3>Live Status</h3>
          <p>Logger, Scheduler, Manager and Watchdog are designed to run on your Termux node and sync to GitHub.</p>
        </div>
        <div class="card">
          <h3>Income Engines</h3>
          <p>Auto-blogging with Amazon.in affiliate <code>gogreenstore-21</code> and donation gateway (UPI).</p>
        </div>
        <div class="card">
          <h3>Genesis Spawner</h3>
          <p>AI modules that create new AI modules — self-propagating automation for growth and resilience.</p>
        </div>
        <div class="card">
          <h3>Join the Node</h3>
          <p>Support the Earth Node at Genesis Lab — the network grows stronger with each node.</p>
        </div>
      </div>

      <a class="cta" href="mailto:gauravlasaria@gmail.com">Contact Gaurav</a>
    </section>

    <footer>
      <p>© GoGreenStoreAI — GodAI Genesis • Built & maintained by Gaurav Lasaria</p>
    </footer>
  </div>
</body>
</html>
HTML

echo "[Genesis] Created site/index.html"

# 2) Add GitHub Actions workflow to .github/workflows
mkdir -p "$ROOT/.github/workflows"
cat > "$ROOT/.github/workflows/deploy-gh-pages.yml" <<'YML'
name: Deploy static site to gh-pages

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout main
        uses: actions/checkout@v4

      - name: Copy static site to deploy directory
        run: |
          mkdir -p public
          cp -R site/* public/

      - name: Deploy to GitHub Pages (gh-pages)
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
          publish_branch: gh-pages
YML

echo "[Genesis] Created workflow .github/workflows/deploy-gh-pages.yml"

# 3) Commit workflow + site to main
git add .github/workflows/deploy-gh-pages.yml site/index.html || true
git commit -m "ci: add pages deploy workflow and initial site" || true
echo "[Genesis] Committed workflow and site to main (if changes existed)"

# 4) Create gh-pages branch containing site only and push it
# We handle two cases: gh-pages exists or not
if git show-ref --verify --quiet refs/heads/gh-pages; then
  echo "[Genesis] gh-pages branch already exists - pushing updated contents to gh-pages"
  # create a temporary worktree and refresh gh-pages
  tmpdir="$(mktemp -d)"
  git worktree add -B gh-pages "$tmpdir" gh-pages
  # copy site into worktree
  rm -rf "$tmpdir"/*
  cp -R "$SITE_DIR"/* "$tmpdir"/
  cd "$tmpdir"
  git add .
  git commit -m "chore(site): update gh-pages site" || true
  git push origin gh-pages
  cd "$ROOT"
  git worktree remove "$tmpdir" || true
else
  echo "[Genesis] gh-pages does not exist - creating orphan gh-pages branch with site"
  tmpdir="$(mktemp -d)"
  mkdir -p "$tmpdir"
  cp -R "$SITE_DIR"/* "$tmpdir"/
  cd "$tmpdir"
  git init
  git add .
  git commit -m "chore(site): initial gh-pages"
  git branch -M gh-pages
  # set remote and push
  git remote add origin "$(git remote get-url origin)"
  git push -u origin gh-pages
  cd "$ROOT"
  rm -rf "$tmpdir"
fi

# 5) Push workflow to main so future pushes auto-deploy
git push origin main || true

echo "[Genesis] gh-pages branch pushed and workflow committed."

# 6) Optional: configure GitHub Pages via API automatically.
# If you want the script to call the Pages API, set GH_PAT env var before running this script.
# Example (run this BEFORE running finalize_site.sh): export GH_PAT="ghp_xxx..."
if [ -n "$GH_PAT" ]; then
  echo "[Genesis] Configuring GitHub Pages via API..."
  # derive owner/repo
  remote_url="$(git remote get-url origin)"
  repo_path="$(echo "$remote_url" | sed -E 's#https?://github.com/##; s#\.git$##')"
  curl -s -X POST -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $GH_PAT" \
    "https://api.github.com/repos/$repo_path/pages" \
    -d '{"source":{"branch":"gh-pages","path":"/"}}' | jq || true
  echo "[Genesis] API call done (if authorized)."
else
  echo "[Genesis] GH_PAT not set. If you want automatic API configuration, set GH_PAT env var and re-run the script."
fi

echo
echo "✅ Done. Visit: https://$(echo "$ORG_REPO" | sed 's#/#.github.io/#')/$REPO_SLUG/  (give GitHub ~1-5 minutes to deploy)"
echo "If empty, reload after a few minutes or check Actions tab in GitHub for deploy job logs."
