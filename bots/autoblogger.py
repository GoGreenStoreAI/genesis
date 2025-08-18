import os, datetime, random, textwrap
from utils import OUTDIR, log_to, send_telegram

AFFILIATE_ID = "gogreenstore-21"  # Amazon.in
TOPICS = [
    ("Solar Home Kits", "B0B3S7HXXZ"),
    ("Energy-Efficient LED Bulbs", "B07WHSJY4C"),
    ("Water Purifier Cartridges", "B07N1YF9X9"),
    ("Smart Plugs for Appliances", "B07GP59V9M"),
    ("Ergonomic Chairs", "B08W8N6D4S"),
]

def mk_post():
    dt = datetime.datetime.now()
    title, asin = random.choice(TOPICS)
    slug = f"{dt.strftime('%Y%m%d-%H%M%S')}-{title.lower().replace(' ','-')}"
    url = f"https://www.amazon.in/dp/{asin}?tag={AFFILIATE_ID}"

    body = textwrap.dedent(f"""
    # {title}: Why it’s worth it in 2025

    If you’re upgrading your setup, **{title}** is one of the simplest ways to
    save time, energy, and money. We’ve seen great results at Genesis Lab (Akurdi),
    and this is our top pick today.

    👉 Quick link: {url}

    ## What to look for
    - Build quality & durability  
    - Real-world efficiency  
    - Ease of installation

    ## How we choose
    We prioritise products with consistent customer support, strong warranties,
    and credible specs.

    *Affiliate note:* When you buy using our link, we earn a small commission at no extra cost to you.
    It directly supports the Earth Node at Genesis Lab.
    """).strip()

    path = os.path.join(OUTDIR, f"{slug}.md")
    with open(path, "w") as f:
        f.write(body + "\n")

    log_to("autoblogger.log", f"📝 Created post: {path}")
    send_telegram(f"📝 AutoBlogger posted: {title}")
    return path

if __name__ == "__main__":
    mk_post()
