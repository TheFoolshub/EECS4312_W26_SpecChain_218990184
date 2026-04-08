"""
00_validate_repo.py - Repository Structure Validation

This script checks if all required folders and files exist in the repository.
Run this before submission to make sure nothing is missing.

Usage:
    python src/00_validate_repo.py
"""

import os
import sys


def check_file(filepath, description=""):
    """Check if a file exists and print result"""
    exists = os.path.exists(filepath)
    status = "✓ found" if exists else "✗ MISSING"
    print(f"  {filepath:<50} {status}")
    return exists


def check_folder(folder):
    """Check if a folder exists"""
    exists = os.path.exists(folder)
    if not exists:
        print(f"  {folder}/ folder MISSING")
    return exists


def main():
    print("="*70)
    print("CHECKING REPOSITORY STRUCTURE")
    print("="*70)
    print()
    
    all_good = True
    
    # Check folders exist
    print("Checking folders...")
    folders = ['data', 'personas', 'spec', 'tests', 'metrics', 'src']
    for folder in folders:
        if not check_folder(folder):
            all_good = False
    print()
    
    # Check required data files
    print("Checking data files...")
    data_files = [
        ('data/reviews_clean.jsonl', 'Cleaned review dataset'),
        ('data/review_groups_manual.json', 'Manual review groups'),
        ('data/review_groups_auto.json', 'Automated review groups'),
        ('data/review_groups_hybrid.json', 'Hybrid review groups'),
    ]
    
    for filepath, desc in data_files:
        if not check_file(filepath, desc):
            all_good = False
    print()
    
    # Check persona files
    print("Checking persona files...")
    persona_files = [
        ('personas/personas_manual.json', 'Manual personas'),
        ('personas/personas_auto.json', 'Automated personas'),
        ('personas/personas_hybrid.json', 'Hybrid personas'),
    ]
    
    for filepath, desc in persona_files:
        if not check_file(filepath, desc):
            all_good = False
    print()
    
    # Check spec files
    print("Checking specification files...")
    spec_files = [
        ('spec/spec_manual.md', 'Manual specification'),
        ('spec/spec_auto.md', 'Automated specification'),
        ('spec/spec_hybrid.md', 'Hybrid specification'),
    ]
    
    for filepath, desc in spec_files:
        if not check_file(filepath, desc):
            all_good = False
    print()
    
    # Check test files
    print("Checking test files...")
    test_files = [
        ('tests/tests_manual.json', 'Manual tests'),
        ('tests/tests_auto.json', 'Automated tests'),
        ('tests/tests_hybrid.json', 'Hybrid tests'),
    ]
    
    for filepath, desc in test_files:
        if not check_file(filepath, desc):
            all_good = False
    print()
    
    # Check metrics files
    print("Checking metrics files...")
    metrics_files = [
        ('metrics/metrics_manual.json', 'Manual pipeline metrics'),
        ('metrics/metrics_auto.json', 'Automated pipeline metrics'),
        ('metrics/metrics_hybrid.json', 'Hybrid pipeline metrics'),
        ('metrics/metrics_summary.json', 'Metrics summary'),
    ]
    
    for filepath, desc in metrics_files:
        if not check_file(filepath, desc):
            all_good = False
    print()
    
    # Check src scripts
    print("Checking source scripts...")
    src_files = [
        ('src/00_validate_repo.py', 'This validation script'),
        ('src/08_metrics.py', 'Metrics calculation script'),
        ('src/run_all.py', 'Run all automated pipeline script'),
    ]
    
    for filepath, desc in src_files:
        if not check_file(filepath, desc):
            all_good = False
    print()
    
    # Final result
    print("="*70)
    if all_good:
        print("✓ REPOSITORY VALIDATION COMPLETE")
        print("  All required files and folders are present!")
    else:
        print("✗ REPOSITORY VALIDATION FAILED")
        print("  Some required files or folders are missing.")
        print("  Check the output above for details.")
    print("="*70)
    
    # Exit with appropriate code
    sys.exit(0 if all_good else 1)


if __name__ == "__main__":
    main()
