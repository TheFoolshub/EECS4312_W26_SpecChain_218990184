"""
06_spec_generate.py - Generate Requirements Specification

This script generates structured system requirements from personas
using the Groq LLM.

What it does:
- Reads personas from: personas/personas_auto.json
- Generates ≥10 clear, testable requirements (R1, R2, ...)
- Ensures traceability to personas and review groups
- Saves output to: spec/spec_auto.md

How to run:
- Part of full pipeline: python src/run_all.py
- Or standalone:        python src/06_spec_generate.py

Requirements:
- Groq API key (env or variable)
- personas/personas_auto.json must exist (from 05_personas_auto.py)
"""

import json
import os
import re
from groq import Groq



# CONFIGURATION

API_KEY = "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"  

client = Groq(api_key=API_KEY)



# GENERATE REQUIREMENTS

def generate_requirements(personas):
    prompt = f"""

Generate structured, testable system requirements for the Headspace app based on these personas.

IMPORTANT RULES:
- Generate AT LEAST 10 requirements 
- Each requirement must be CLEAR, SPECIFIC, and TESTABLE
- DO NOT use vague words like: "easy", "fast", "better", "user-friendly", "intuitive"
- Use measurable terms instead (e.g., "within 3 seconds", "at least 10 items", "90% accuracy")
- Each requirement must describe actual system behavior
- Each requirement must trace back to a persona and review group

Personas:
{json.dumps(personas, ensure_ascii=False)}

Return ONLY valid JSON.
No markdown or explanations.

Format:
[
  {{
    "requirement_id": "R1",
    "description": "The system shall [specific behavior]...",
    "persona_id": "P1",
    "group_id": "G1",
    "acceptance_criteria": [
      "Given [context], When [action], Then [measurable result]",
      "Another testable condition"
    ]
  }}
]
"""

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=3000
        )
        raw = response.choices[0].message.content

    except Exception as e:
        print(f" API Error: {e}")
        return []

    cleaned = raw.strip()

    # Extract JSON safely
    match = re.search(r'```json\s*(\[.*?\])\s*```', cleaned, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        match = re.search(r'(\[.*\])', cleaned, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            print(" No JSON found in response")
            print("RAW:", raw[:500])
            return []

    try:
        return json.loads(json_str)
    except Exception:
        print(" JSON parsing failed")
        print("RAW:", raw[:500])
        return []



# MAIN

def main():

    # Load personas
    with open("personas/personas_auto.json", encoding="utf-8") as f:
        personas = json.load(f).get("personas", [])

    print(f"Loaded {len(personas)} personas")

    # Generate requirements
    requirements = generate_requirements(personas)

    if not requirements:
        print(" Failed to generate requirements")
        return

    print(f"Generated {len(requirements)} requirements")

    # Save output
    os.makedirs("spec", exist_ok=True)
    with open("spec/spec_auto.md", "w", encoding="utf-8") as f:
        f.write("# Automated Specification\n\n")
        for r in requirements:
            f.write(f"## {r['requirement_id']}\n\n")
            f.write(f"**Description:** {r['description']}\n\n")
            f.write(f"**Persona:** {r['persona_id']}\n\n")
            f.write(f"**Review Group:** {r['group_id']}\n\n")
            f.write("**Acceptance Criteria:**\n")
            for ac in r["acceptance_criteria"]:
                f.write(f"- {ac}\n")
            f.write("\n---\n\n")

    print("✓ Saved spec/spec_auto.md\n")


if __name__ == "__main__":
    main()
