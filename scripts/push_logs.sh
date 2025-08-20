#!/bin/bash
cd ~/godai-genesis || exit

# Copy logs into a versioned folder
mkdir -p logs/archive
cp logs/*.log logs/archive/ 2>/dev/null

# Stage and commit logs
git add logs/*
git commit -m "Auto-log update $(date)" || echo "No new logs"

# Push safely
git push || echo "Push failed"
