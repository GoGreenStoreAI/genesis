#!/bin/bash
OUTPUT_DIR="output"
INDEX_FILE="$OUTPUT_DIR/index.html"

mkdir -p "$OUTPUT_DIR"

DATE=$(date +"%A, %d %B %Y %H:%M:%S")

cat > "$INDEX_FILE" <<HTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Go Green Store 🌱</title>
  <style>
    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f4fff4; }
    h1 { color: #2e7d32; }
    p { color: #444; }
    footer { margin-top: 50px; font-size: 0.9em; color: #888; }
  </style>
</head>
<body>
  <h1>Welcome to GoGreenStoreAI 🌍</h1>
  <p>🚀 AI-powered eco-friendly marketplace.</p>
  <p>🌱 Auto-generated on <strong>$DATE</strong></p>
  <footer>Powered by GodAI Genesis · © 2025 GoGreenStoreAI</footer>
</body>
</html>
HTML
