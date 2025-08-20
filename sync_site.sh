#!/bin/bash
set -e
REPO="$HOME/godai-genesis"
UP="$REPO/uploads"
DOCS="$REPO/docs"

mkdir -p "$DOCS/blog" "$DOCS/dashboard"

# Convert Markdown -> HTML using Python's markdown lib
render_md () {
  python - "$1" "$2" << 'PY'
import sys, pathlib, markdown
src = pathlib.Path(sys.argv[1])
dst = pathlib.Path(sys.argv[2])
title = src.stem
html = markdown.markdown(src.read_text(encoding="utf-8"))
dst.write_text(f"""<!doctype html><html><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title></head>
<body style="font-family:Arial;max-width:800px;margin:auto;padding:2rem;background:#f8fff8">
<h1>{title}</h1>
{html}
<p><a href="./index.html">⬅ Back to Blog</a></p>
</body></html>""", encoding="utf-8")
PY
}

# Blog index
echo "<!doctype html><html><head><meta charset='utf-8'><title>Genesis Blog</title></head><body style='font-family:Arial;max-width:900px;margin:auto;padding:2rem;background:#f8fff8'><h1>📰 Genesis Blog</h1><ul>" > "$DOCS/blog/index.html"
if compgen -G "$UP/blog/*.md" > /dev/null; then
  for f in "$UP"/blog/*.md; do
    base="$(basename "$f" .md)"
    out="$DOCS/blog/$base.html"
    render_md "$f" "$out"
    echo "<li><a href='./$base.html'>$base</a></li>" >> "$DOCS/blog/index.html"
  done
else
  echo "<li>No posts yet — check back soon.</li>" >> "$DOCS/blog/index.html"
fi
echo "</ul><p><a href='../index.html'>⬅ Back to Home</a></p></body></html>" >> "$DOCS/blog/index.html"

# Dashboard index (simple)
echo "<!doctype html><html><head><meta charset='utf-8'><title>Genesis Dashboard</title></head><body style='font-family:Arial;max-width:900px;margin:auto;padding:2rem;background:#f0fdf4'><h1>📊 Genesis Dashboard</h1><ul>" > "$DOCS/dashboard/index.html"
if compgen -G "$UP/dashboard/*" > /dev/null; then
  for f in "$UP"/dashboard/*; do
    name="$(basename "$f")"
    echo "<li><pre>$(sed 's/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g' "$f")</pre><small>$name</small></li>" >> "$DOCS/dashboard/index.html"
  done
else
  echo "<li>No reports yet.</li>" >> "$DOCS/dashboard/index.html"
fi
echo "</ul><p><a href='../index.html'>⬅ Back to Home</a></p></body></html>" >> "$DOCS/dashboard/index.html"

cd "$REPO"
git add docs
git commit -m "🌐 Auto-sync site $(date +'%F %T')" || true
git push origin main
