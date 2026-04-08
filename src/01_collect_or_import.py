## 01_collect_or_import.py - scrapes headspace reviews from google play
## need to run: pip install google-play-scraper

"""
01_collect_or_import.py - Collect Raw Reviews

This script collects user reviews for the Headspace app from the
Google Play Store.

What it does:
- Uses google-play-scraper to fetch up to 5000 reviews
- Collects reviews in batches using continuation tokens
- Extracts relevant fields (content, score, user, dates, etc.)
- Saves output to: data/reviews_raw.jsonl (JSONL format)

How to run:
- Part of full pipeline: python src/run_all.py
- Or standalone:        python src/01_collect_or_import.py

Requirements:
- google-play-scraper library (pip install google-play-scraper)
- Internet connection
"""
import json, os
from google_play_scraper import reviews, Sort

APP_ID = "com.getsomeheadspace.android"
OUTPUT = "data/reviews_raw.jsonl"
MAX = 5000

os.makedirs("data", exist_ok=True)

all_reviews = []
token = None

print("collecting headspace reviews...")

while len(all_reviews) < MAX:
    batch, token = reviews(
        APP_ID,
        lang="en",
        country="us",
        sort=Sort.NEWEST,
        count=200,
        continuation_token=token
    )

    if not batch:
        print("no more reviews")
        break

    all_reviews += batch
    print(f"got {len(all_reviews)} so far...")

    if token is None:
        break

print(f"total collected: {len(all_reviews)}")

# save to jsonl
with open(OUTPUT, "w", encoding="utf-8") as f:
    for i, r in enumerate(all_reviews):
        # handle dates
        date = r["at"].isoformat() if r.get("at") else ""
        reply_date = r["repliedAt"].isoformat() if r.get("repliedAt") else ""

        data = {
            "review_id": f"r{str(i).zfill(4)}",
            "userName": r.get("userName", ""),
            "content": r.get("content", ""),
            "score": r.get("score"),
            "thumbsUpCount": r.get("thumbsUpCount", 0),
            "at": date,
            "replyContent": r.get("replyContent", ""),
            "repliedAt": reply_date
        }
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

print(f"saved {len(all_reviews)} reviews to {OUTPUT}")
