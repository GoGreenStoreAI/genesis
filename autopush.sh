#!/bin/bash
cd ~/godai-genesis || exit
git add .
git commit -m "Auto-update: $(date)"
git push origin main
