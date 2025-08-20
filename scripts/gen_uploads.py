import os, datetime

uploads_dir = os.path.expanduser("~/godai/uploads/files")
output_file = "uploads.html"

files = []
if os.path.exists(uploads_dir):
    for fname in sorted(os.listdir(uploads_dir)):
        fpath = os.path.join(uploads_dir, fname)
        if os.path.isfile(fpath):
            files.append(f"<li><a href='{fname}' target='_blank'>{fname}</a></li>")

html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Genesis Hub | Uploads</title></head>
<body>
  <h1>📂 Genesis Uploads</h1>
  <nav>
    <a href="index.html">🏠 Home</a>
    <a href="posts.html">📖 Posts</a>
    <a href="about.html">🌍 About</a>
  </nav>
  <ul>{''.join(files) if files else '<li>No files yet.</li>'}</ul>
  <footer><p>Auto-updated: {datetime.datetime.now()}</p></footer>
</body>
</html>
"""
open(output_file,"w").write(html)
