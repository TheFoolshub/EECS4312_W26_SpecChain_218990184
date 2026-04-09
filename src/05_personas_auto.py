"""
05_personas_auto.py - Generate Review Groups & Personas

This script groups user reviews and generates personas using the Groq LLM.

What it does:
- Reads cleaned reviews from: data/reviews_clean.jsonl
- Groups reviews into 5 thematic clusters
- Generates one persona per group
- Saves outputs to:
    • data/review_groups_auto.json
    • personas/personas_auto.json

How to run:
- Part of full pipeline: python src/run_all.py
- Or standalone:        python src/05_personas_auto.py

Requirements:
- Groq API key (env or variable)
- data/reviews_clean.jsonl must exist (from 02_clean.py)
"""

import json
import re
from groq import Groq

client = Groq(api_key="add API key here ")


def load_clean_reviews(path):
    reviews = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            reviews.append(json.loads(line))
    return reviews


def group_reviews(reviews):
    prompt = f"""
You are grouping user reviews into meaningful clusters.

Group the following reviews into 5 distinct groups based on similar themes.

Each group must include:
- group_id
- theme
- description
- reviews (list of review texts)

Reviews:
{json.dumps(reviews[:50], ensure_ascii=False)}

Return ONLY JSON in this format:
[
  {{
    "group_id": "G1",
    "theme": "...",
    "description": "...",
    "reviews": ["...", "..."]
  }}
]
"""

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=2000
        )

        raw = response.choices[0].message.content

    except Exception as e:
        print(f"Grouping API Error: {e}")
        return []

    cleaned = raw.strip()

    # Extract JSON
    match = re.search(r'```json\s*(\[.*?\])\s*```', cleaned, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        match = re.search(r'(\[.*\])', cleaned, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            print("Error parsing groups")
            print("RAW OUTPUT:", raw)
            return []

    try:
        return json.loads(json_str)
    except:
        print("JSON decode failed for groups")
        print("RAW OUTPUT:", raw)
        return []


def save_groups(groups, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(groups, f, indent=2)


def generate_persona(group, index):
    prompt = f"""
You are generating user personas based on grouped app reviews.

Create ONE persona from this group.

Group:
{json.dumps(group, ensure_ascii=False)}

Return ONLY JSON in this format:
{{
  "persona_id": "P{index}",
  "name": "Realistic Name",
  "group_id": "{group['group_id']}",
  "description": "...",
  "goals": ["...", "..."],
  "pain_points": ["...", "..."],
  "usage_context": "..."
}}
"""

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1000
        )

        raw = response.choices[0].message.content

    except Exception as e:
        print(f" Persona API Error: {e}")
        return None

    cleaned = raw.strip()

    # Extract JSON
    match = re.search(r'```json\s*(\{.*?\})\s*```', cleaned, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        match = re.search(r'(\{.*\})', cleaned, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            print(" No JSON found in persona response")
            print("RAW OUTPUT:", raw)
            return None

    try:
        return json.loads(json_str)
    except:
        print(" Error parsing persona")
        print("RAW OUTPUT:", raw)
        return None


def save_personas(personas, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({"personas": personas}, f, indent=2)


def main():
    print("Step 1: Loading cleaned reviews...")
    reviews = load_clean_reviews("data/reviews_clean.jsonl")

    print("Step 2: Grouping reviews (4.1)...")
    groups = group_reviews(reviews)

    if not groups:
        print(" Grouping failed. Exiting.")
        return

    save_groups(groups, "data/review_groups_auto.json")
    print("Groups saved → data/review_groups_auto.json")

    print("Step 3: Generating personas (4.2)...")
    personas = []

    for i, group in enumerate(groups):
        persona = generate_persona(group, i + 1)
        if persona:
            personas.append(persona)

    save_personas(personas, "personas/personas_auto.json")

    print("Personas saved → personas/personas_auto.json")


if __name__ == "__main__":
    main()
