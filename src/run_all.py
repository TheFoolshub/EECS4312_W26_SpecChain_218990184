"""
run_all.py - Execute Complete Automated Pipeline

============================================================
INSTRUCTIONS FOR USE
============================================================
This script runs the FULL automated pipeline for the EECS 4312
SpecChain project.

It performs the following steps automatically:

1. Data Collection (if needed)
   - Runs: 01_collect_or_import.py
   - Only runs if data/reviews_raw.jsonl is missing

2. Data Cleaning
   - Runs: 02_clean.py
   - Produces: data/reviews_clean.jsonl

3. Automated Pipeline
   - Runs: 05_personas_auto.py   → review groups + personas
   - Runs: 06_spec_generate.py   → requirements specification
   - Runs: 07_tests_generate.py  → validation tests
   - Runs: 08_metrics.py         → metrics for all pipelines

============================================================
HOW TO RUN
============================================================
From the root of the repository:

    python src/run_all.py

============================================================
NOTES
============================================================
- No user interaction is required (fully automated)
- If raw data already exists, collection step is skipped
- If any critical step fails, execution will stop
- Designed for reproducibility and TA evaluation

============================================================
OUTPUT FILES
============================================================
data/
  - reviews_raw.jsonl
  - reviews_clean.jsonl
  - review_groups_auto.json

personas/
  - personas_auto.json

spec/
  - spec_auto.md

tests/
  - tests_auto.json

metrics/
  - metrics_auto.json
  - metrics_manual.json (if exists)
  - metrics_hybrid.json (if exists)
  - metrics_summary.json

============================================================
"""

import sys
import os
import subprocess

# Base directory of this script (src/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_path(filename):
    """Return absolute path to a script inside src/"""
    return os.path.join(BASE_DIR, filename)


def run_script(script_path, description):
    """Run a script and stream output directly"""
    print("\n" + "=" * 70)
    print(f"RUNNING: {description}")
    print(f"Script: {script_path}")
    print("=" * 70)

    if not os.path.exists(script_path):
        print(f"✗ ERROR: Script not found: {script_path}")
        return False

    try:
        result = subprocess.run([sys.executable, script_path])

        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True
        else:
            print(f"✗ {description} failed (exit code {result.returncode})")
            return False

    except Exception as e:
        print(f"✗ ERROR running {description}: {e}")
        return False


def main():
    print("=" * 70)
    print("COMPLETE AUTOMATED PIPELINE EXECUTION")
    print("=" * 70)

    results = {}

   
    # STEP 1: DATA COLLECTION (only if needed)
   

    raw_data_path = os.path.join(BASE_DIR, "../data/reviews_raw.jsonl")
    collect_script = get_path("01_collect_or_import.py")

    if not os.path.exists(raw_data_path):
        print("\nRaw dataset not found → running data collection...")
        results['collect'] = run_script(
            collect_script,
            "Task 1: Collect/Import Reviews"
        )

        if not results['collect']:
            print("\n✗ FATAL: Data collection failed")
            sys.exit(1)
    else:
        print("\n✓ Raw dataset already exists → skipping data collection")
        results['collect'] = None

    # STEP 2: CLEAN DATA
   

    clean_script = get_path("02_clean.py")

    results['clean'] = run_script(
        clean_script,
        "Task 2: Clean Reviews"
    )

    if not results['clean']:
        print("\n✗ FATAL: Cleaning failed")
        sys.exit(1)

    clean_data_path = os.path.join(BASE_DIR, "../data/reviews_clean.jsonl")

    if not os.path.exists(clean_data_path):
        print("\n✗ FATAL: Cleaned dataset not found")
        sys.exit(1)

  
    # STEP 3: AUTOMATED PIPELINE
   

    steps = [
        ("05_personas_auto.py", "Task 4.1-4.2: Groups + Personas", "personas"),
        ("06_spec_generate.py", "Task 4.3: Specifications", "spec"),
        ("07_tests_generate.py", "Task 4.4: Tests", "tests"),
        ("08_metrics.py", "Task 4.5: Metrics", "metrics"),
    ]

    for script_name, description, key in steps:
        script_path = get_path(script_name)

        success = run_script(script_path, description)
        results[key] = success

        # Stop if critical step fails
        if not success and key in ["personas", "spec", "tests"]:
            print(f"\n✗ FATAL: {description} failed → stopping pipeline")
            sys.exit(1)

   
    # SUMMARY
   

    print("\n" + "=" * 70)
    print("PIPELINE EXECUTION SUMMARY")
    print("=" * 70)

    for key, value in results.items():
        if value is True:
            status = "✓ Success"
        elif value is False:
            status = "✗ Failed"
        else:
            status = "⊗ Skipped"

        print(f"{key.capitalize():<10}: {status}")

    print("\n✓ Pipeline completed successfully!")

    print("\nGenerated files include:")
    print("  data/review_groups_auto.json")
    print("  personas/personas_auto.json")
    print("  spec/spec_auto.md")
    print("  tests/tests_auto.json")
    print("  metrics/metrics_auto.json")


if __name__ == "__main__":
    main()
