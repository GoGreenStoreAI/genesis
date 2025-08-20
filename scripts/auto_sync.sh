#!/data/data/com.termux/files/usr/bin/bash
cd ~/godai-genesis
python3 scripts/gen_posts.py
python3 scripts/gen_uploads.py
git add .
git commit -m "Auto-update Genesis Hub $(date)"
git push origin main
