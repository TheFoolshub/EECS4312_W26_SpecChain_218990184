"""
07_tests_generate.py - Generate Validation Tests

This script generates validation test cases from the requirements
specification using the Groq LLM.

What it does:
- Reads requirements from: spec/spec_auto.md
- Extracts requirement IDs (R1, R2, ...)
- Generates ≥2 test cases per requirement using LLM
- Saves output to: tests/tests_auto.json
- Stores prompt metadata in: prompts/prompt_auto.json

How to run:
- Part of full pipeline: python src/run_all.py
- Or standalone:        python src/07_tests_generate.py

Requirements:
- Groq API key (env or variable)
- spec/spec_auto.md must exist (from 06_spec_generate.py)
"""


import json
import os
import re
from typing import List, Dict, Optional
from groq import Groq


# Configuration
API_KEY = "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"
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"
MIN_TESTS_PER_REQ = 2


class TestGenerator:
    """Generates validation tests from requirements specifications using LLM"""
    
    def __init__(self, api_key: str, model: str):
        self.client = Groq(api_key=api_key)
        self.model = model
    
    def load_specification(self, filepath: str) -> str:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_requirement_ids(self, spec_content: str) -> List[str]:
        
        return list(set(re.findall(r'R\d+', spec_content)))
    
    def extract_json(self, text: str) -> Optional[List[Dict]]:
        cleaned = text.strip()
        
        match = re.search(r'```json\s*(\[.*?\])\s*```', cleaned, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            match = re.search(r'(\[.*\])', cleaned, re.DOTALL)
            if match:
                json_str = match.group(1)
            else:
                return None
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    
    def generate_tests(self, spec_content: str, requirement_ids: List[str]) -> Optional[List[Dict]]:
        
        prompt = f"""You are a QA engineer creating test scenarios for the Headspace app.

Generate validation tests for the following requirements specification.

REQUIREMENTS:
{spec_content}

REQUIREMENTS TO TEST: {requirement_ids}

INSTRUCTIONS:
- Generate AT LEAST {MIN_TESTS_PER_REQ} test scenarios for EACH requirement
- Each test must validate a specific aspect of the requirement
- Tests must be executable with clear steps
- Include specific expected results
- Number tests sequentially (T1, T2, ...)

OUTPUT FORMAT (JSON only, no markdown or explanation):
[
  {{
    "test_id": "T1",
    "requirement_id": "R1",
    "scenario": "Verify that [specific behavior or condition]",
    "steps": [
      "Launch the Headspace app",
      "Navigate to [specific screen]",
      "Perform [specific action]",
      "Observe the result"
    ],
    "expected_result": "The system should [specific, measurable outcome]"
  }}
]

Ensure comprehensive coverage of all requirements."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=4000
            )
            
            return self.extract_json(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error generating tests: {e}")
            return None


def save_json(data: Dict, filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_prompts(metadata: Dict) -> None:
    filepath = "prompts/prompt_auto.json"
    
    prompts = {}

    # ✅ FIXED: handle corrupted JSON safely
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                prompts = json.load(f)
        except:
            print("⚠️ prompt_auto.json corrupted — resetting file")
            prompts = {}

    prompts["test_generation"] = metadata

    os.makedirs("prompts", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)


def main():
    
    generator = TestGenerator(API_KEY, MODEL_NAME)
    
    print("Step 1: Loading requirements specification...")
    spec_content = generator.load_specification("spec/spec_auto.md")
    print("  ✓ Specification loaded\n")
    
    print("Step 2: Extracting requirement IDs...")
    req_ids = generator.extract_requirement_ids(spec_content)
    print(f"  ✓ Found {len(req_ids)} requirements: {req_ids}\n")
    
    print(f"Step 3: Generating validation tests ({MIN_TESTS_PER_REQ}+ per requirement)...")
    tests = generator.generate_tests(spec_content, req_ids)
    
    if not tests:
        print("  Failed to generate tests")
        return
    
    print(f"  Generated {len(tests)} test scenarios\n")
    
    test_data = {"tests": tests}
    save_json(test_data, "tests/tests_auto.json")
    print("  Saved: tests/tests_auto.json\n")
    
    metadata = {
        "task": "Validation test generation from requirements",
        "model": MODEL_NAME,
        "temperature": 0.2,
        "max_tokens": 4000,
        "min_tests_per_requirement": MIN_TESTS_PER_REQ,
        "total_requirements": len(req_ids),
        "output_format": "JSON test scenarios"
    }
    
    update_prompts(metadata)
    print("  Updated: prompts/prompt_auto.json\n")
    
  


if __name__ == "__main__":
    main()
