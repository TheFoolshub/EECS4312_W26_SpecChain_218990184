## 02_clean.py - cleaning the raw reviews
"""
02_clean.py - Clean and Preprocess Reviews

This script cleans raw user reviews for use in all pipelines.

What it does:
- Reads raw reviews from: data/reviews_raw.jsonl
- Removes duplicates and empty reviews
- Normalizes text (lowercase, remove emojis, punctuation, special characters)
- Converts numbers to words
- Removes stopwords and applies lemmatization (NLTK)
- Drops reviews with fewer than 15 words
- Assigns unique review IDs
- Saves cleaned data to: data/reviews_clean.jsonl
- Generates metadata in: data/dataset_metadata.json

How to run:
- Part of full pipeline: python src/run_all.py
- Or standalone:        python src/02_clean.py

Requirements:
- data/reviews_raw.jsonl must exist (from 01_collect_or_import.py)
- NLTK (stopwords, wordnet)
- num2words library
"""


import json, os, re, unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from num2words import num2words

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

RAW_FILE = "data/reviews_raw.jsonl"
CLEAN_FILE = "data/reviews_clean.jsonl"
META_FILE = "data/dataset_metadata.json"

MIN_WORDS = 15  # only keep reviews with at least this many words after cleaning


def convert_nums(text):
    """turns numbers into words, e.g. 5 -> five"""
    result = []
    for word in text.split():
        if word.isdigit():
            try:
                word = num2words(int(word))
            except:
                pass  # just leave it if it fails
        result.append(word)
    return " ".join(result)


def clean(text):
    if not text or not text.strip():
        return ""

    text = text.lower()

    # normalize unicode and strip non-ascii (gets rid of emojis etc)
    text = unicodedata.normalize("NFKD", text)
    ascii_only = ""
    for c in text:
        if c.isascii():
            ascii_only += c
        else:
            ascii_only += " "
    text = ascii_only

    text = convert_nums(text)
    text = re.sub(r"[^a-z\s]", " ", text)  # only keep letters
    text = re.sub(r"\s+", " ", text).strip()

    # tokenize, remove stopwords, lemmatize
    tokens = text.split()
    final = []
    for t in tokens:
        if t not in stop_words:
            final.append(lemmatizer.lemmatize(t))

    if len(final) < MIN_WORDS:
        return ""
    return " ".join(final)


## load raw
print("loading raw reviews...")
raw = []
with open(RAW_FILE, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            raw.append(json.loads(line))
print(f"got {len(raw)} raw reviews")

## deduplicate
print("removing dupes...")
seen = set()
unique = []
for r in raw:
    c = r.get("content", "")
    if not c:
        continue
    norm = re.sub(r"\s+", " ", c.strip().lower())
    if norm not in seen:
        seen.add(norm)
        unique.append(r)
print(f"removed {len(raw) - len(unique)} duplicates")

## clean each review
print("cleaning reviews...")
cleaned = []
dropped = 0
for r in unique:
    original = r.get("content", "") or ""
    c = clean(original)
    if not c:
        dropped += 1
        continue
    cleaned.append({
        "review_id": "",
        "clean_content": c,
        "score": r.get("score"),
        "userName": r.get("userName", ""),
        "at": r.get("at", "")
    })

# give them proper ids
for i in range(len(cleaned)):
    cleaned[i]["review_id"] = f"r{str(i).zfill(4)}"

print(f"dropped {dropped} reviews (too short or empty)")
print(f"kept {len(cleaned)} clean reviews")

## save
os.makedirs("data", exist_ok=True)
with open(CLEAN_FILE, "w", encoding="utf-8") as f:
    for r in cleaned:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"saved to {CLEAN_FILE}")

## metadata
meta = {
    "app_name": "Headspace",
    "package_id": "com.getsomeheadspace.android",
    "platform": "Google Play Store",
    "total_raw_reviews": len(raw),
    "total_clean_reviews": len(cleaned),
    "collection_method": "google-play-scraper Python library",
    "collection_date": "2026-04-07",
    "cleaning_steps": [
        "Removed duplicate reviews",
        "Removed emojis and non-ASCII characters",
        "Removed punctuation and special characters",
        "Converted numbers to English words",
        "Converted text to lowercase",
        "Removed extra whitespace",
        "Removed stop words (NLTK)",
        "Lemmatized with WordNet",
        "Dropped reviews under 15 words"
    ]
}
with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)

print(f"metadata saved to {META_FILE}")
print(f"done! {len(raw)} -> {len(cleaned)}")
