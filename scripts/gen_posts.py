import os, datetime

posts_dir = os.path.expanduser("~/godai/uploads/posts")
output_file = "posts.html"

posts = []
if os.path.exists(posts_dir):
    for fname in sorted(os.listdir(posts_dir), reverse=True):
        fpath = os.path.join(posts_dir, fname)
        if os.path.isfile(fpath):
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(500).replace("<", "&lt;").replace(">", "&gt;")
            posts.append(f"<h2>{fname}</h2><p>{content}...</p><hr>")

html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Genesis Hub | Posts</title></head>
<body>
  <h1>📖 Genesis Posts</h1>
  <nav>
    <a href="index.html">🏠 Home</a>
    <a href="uploads.html">📂 Uploads</a>
    <a href="about.html">🌍 About</a>
  </nav>
  {''.join(posts) if posts else '<p>No posts yet.</p>'}
  <footer><p>Auto-updated: {datetime.datetime.now()}</p></footer>
</body>
</html>
"""
open(output_file,"w").write(html)
