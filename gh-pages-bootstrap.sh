#!/data/data/com.termux/files/usr/bin/bash
set -e
ROOT="$HOME/godai-genesis"
BOTSDIR="$ROOT/bots"

echo "[Genesis] Creating landing page and GitHub Pages workflow..."

# 1) create simple landing page (index.html)
mkdir -p "$ROOT/site"
cat > "$ROOT/site/index.html" <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>GodAI Genesis — GoGreenStoreAI</title>
  <style>
    body{font-family:Inter,system-ui,Segoe UI,Roboto,'Helvetica Neue',Arial;line-height:1.6;color:#0b1220;background:#f6fbf9;margin:0;padding:0}
    .wrap{max-width:980px;margin:6vh auto;padding:40px;background:white;border-radius:14px;box-shadow:0 12px 40px rgba(6,22,35,.08)}
    header{display:flex;align-items:center;gap:18px}
    .logo{width:72px;height:72px;border-radius:14px;background:linear-gradient(135deg,#2ebf91,#1b9ad6);display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:26px}
    h1{margin:6px 0 6px 0;font-size:28px}
    p.lead{color:#234; margin-top:0}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:18px}
    .card{padding:14px;border-radius:10px;border:1px solid rgba(3,10,18,.04);background:linear-gradient(180deg, rgba(255,255,255,1), rgba(250,255,251,1))}
    footer{margin-top:24px;color:#556; font-size:13px}
    a.cta{display:inline-block;margin-top:14px;padding:8px 14px;background:#1b9ad6;color:#fff;border-radius:8px;text-decoration:none}
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
          <p>Logger, Scheduler, Manager and Watchdog are running on your Termux node.</p>
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

# 2) create .github workflow to deploy site (build from main -> gh-pages)
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

      - name: Setup Node (for future builds)
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Copy static site to deploy directory
        run: |
          # If you later generate site with a build step, replace this.
          mkdir -p public
          cp -R site/* public/

      - name: Deploy to GitHub Pages (gh-pages)
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
          publish_branch: gh-pages
YML

# 3) prepare first gh-pages commit (branch)
cd "$ROOT"
git add site/.gitignore >/dev/null 2>&1 || true
git add .github/workflows/deploy-gh-pages.yml
git add site/index.html
git commit -m "chore(site): add initial landing page and GH Actions workflow" || true

# 4) ensure gh-pages branch exists, push public site branch
if git show-ref --verify --quiet refs/heads/gh-pages; then
  echo "[Genesis] gh-pages branch exists"
else
  echo "[Genesis] creating gh-pages branch"
  git checkout --orphan gh-pages
  git reset --hard
  # add index only to gh-pages temporary
  mkdir -p tmp-gh-pages
  cp -R site/* tmp-gh-pages/
  cd tmp-gh-pages
  git init
  git add .
  git commit -m "chore(site): initial gh-pages"
  git branch -M gh-pages
  git remote add origin "$(git remote get-url origin)"
  git push -u origin gh-pages
  cd "$ROOT"
  # return to main
  git checkout -f main
fi

# 5) push workflow to main (so future pushes auto-deploy)
git add .github/workflows/deploy-gh-pages.yml site/index.html
git commit -m "ci: add pages deploy workflow and initial site" || true
git push origin main

echo "[Genesis] bootstrap complete. Site files committed and workflow pushed."
echo "Visit https://gogreenstoreai.github.io/genesis/ once GitHub Pages activates (give GitHub ~1-5 minutes)."
