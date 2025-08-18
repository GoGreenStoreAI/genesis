import os
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

base_dir = Path("/data/data/com.termux/files/home/godai-genesis/catalogs")
input_file = base_dir / "full_storage_index.txt"

categories = {
    "Bills": [".pdf", "invoice", "bill", "receipt"],
    "Legal": [".doc", ".docx", "agreement", "contract"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Docs": [".txt", ".md", ".ppt", ".xls"],
    "GodAI": ["godai", "genesis", "secret", "client_secret.json"],
    "Others": []
}

styles = getSampleStyleSheet()

with open(input_file) as f:
    lines = f.readlines()

sorted_entries = {cat: [] for cat in categories}
for line in lines:
    entry = line.strip().lower()
    matched = False
    for cat, keywords in categories.items():
        if any(k in entry for k in keywords):
            sorted_entries[cat].append(line.strip())
            matched = True
            break
    if not matched:
        sorted_entries["Others"].append(line.strip())

for cat, entries in sorted_entries.items():
    out_file = base_dir / f"{cat}_catalog.pdf"
    doc = SimpleDocTemplate(str(out_file))
    story = []
    for e in entries:
        story.append(Paragraph(e, styles["Normal"]))
        story.append(Spacer(1, 6))
    doc.build(story)
