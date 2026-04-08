"""
08_metrics.py - Calculate Metrics for All Pipelines

HOW TO RUN:
-----------
Make sure you have these folders with the right files:
  data/
    - reviews_clean.jsonl
    - review_groups_manual.json
    - review_groups_auto.json
    - review_groups_hybrid.json
  
  personas/
    - personas_manual.json
    - personas_auto.json
    - personas_hybrid.json
  
  spec/
    - spec_manual.md
    - spec_auto.md
    - spec_hybrid.md
  
  tests/
    - tests_manual.json
    - tests_auto.json
    - tests_hybrid.json

Then just run:
  python 08_metrics.py

OUTPUT:
-------
Creates metrics/ folder with:
  - metrics_manual.json
  - metrics_auto.json
  - metrics_hybrid.json
  - metrics_summary.json (comparison of all 3)


"""

import json
import os
import re


def count_reviews():
    """count total reviews in dataset - same for all pipelines"""
    count = 0
    with open('data/reviews_clean.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                count += 1
    return count


def get_metrics(pipeline):
    """calculate all metrics for one pipeline"""
    print(f"\nCalculating {pipeline} pipeline...")
    
    total_reviews = count_reviews()
    
    # load all the files
    with open(f'data/review_groups_{pipeline}.json', 'r', encoding='utf-8') as f:
        groups_data = json.load(f)
    
    with open(f'personas/personas_{pipeline}.json', 'r', encoding='utf-8') as f:
        personas_data = json.load(f)
    
    with open(f'spec/spec_{pipeline}.md', 'r', encoding='utf-8') as f:
        spec = f.read()
    
    with open(f'tests/tests_{pipeline}.json', 'r', encoding='utf-8') as f:
        tests_data = json.load(f)
    
    # 1. persona count
    persona_count = len(personas_data['personas'])
    
    # 2. requirements count
    # Each pipeline has different requirement ID format
    if pipeline == 'auto':
        # auto uses "## R1", "## R2", etc
        req_ids = set(re.findall(r'## (R\d+)', spec))
    elif pipeline == 'hybrid':
    
        req_ids = set(re.findall(r'Requirement ID: (FR_\d+)', spec))
    else:  # manual
        # use MULTILINE to only match actual requirement headers 
        all_reqs = re.findall(r'^Requirement ID: (FR\d+)', spec, re.MULTILINE)
        req_ids = set(all_reqs)
    
    requirements_count = len(req_ids)
    
    # 3. tests count
    tests_count = len(tests_data['tests'])
    
    # 4. traceability links
    # each persona links to a group 
    persona_to_group = persona_count
    
    # count requirements with persona links
    if pipeline == 'hybrid':
        # hybrid uses plain "Source Persona:" without markdown
        req_to_persona = len(re.findall(r'^Source Persona:', spec, re.MULTILINE))
    elif pipeline == 'auto':
        # auto uses "**Persona:**" with markdown
        req_to_persona = len(re.findall(r'\*\*Persona:\*\*', spec))
    else:  # manual
        # manual uses "Source Persona
        all_persona_links = re.findall(r'^Source Persona:', spec, re.MULTILINE)
        req_to_persona = min(len(all_persona_links), requirements_count)
    
    # count requirements with group links
    if pipeline == 'hybrid':
        # hybrid uses plain "Traceability:
        req_to_group = len(re.findall(r'^Traceability:', spec, re.MULTILINE))
    elif pipeline == 'auto':
    
        req_to_group = len(re.findall(r'\*\*Review Group:\*\*', spec))
    else:  # manual
        # manual uses "Traceability:
        all_group_links = re.findall(r'^Traceability:', spec, re.MULTILINE)
        req_to_group = min(len(all_group_links), requirements_count)
    
    traceability_links = persona_to_group + req_to_persona + req_to_group
    
    # 5. review coverage
    if isinstance(groups_data, list):
        groups = groups_data
    else:
        groups = groups_data.get('groups', [])
    
    covered_reviews = set()
    
    for group in groups:
        if 'review_ids' in group:
            # manual/hybrid format
            covered_reviews.update(group['review_ids'])
        elif 'reviews' in group:
            # auto format:
            for review_entry in group['reviews']:
                match = re.match(r'(r\d+)', review_entry)
                if match:
                    covered_reviews.add(match.group(1))
    
    review_coverage = len(covered_reviews) / total_reviews if total_reviews > 0 else 0
    
    # 6. traceability ratio
    traceability_ratio = req_to_persona / requirements_count if requirements_count > 0 else 0
    
    # 7. testability rate
    # what % of requirements have tests
    tested_reqs = set()
    for test in tests_data['tests']:
        tested_reqs.add(test['requirement_id'])
    
    # only count reqs that actually exist
    tested_reqs = tested_reqs.intersection(req_ids)
    testability_rate = len(tested_reqs) / requirements_count if requirements_count > 0 else 0
    
    # 8. ambiguity ratio
    if pipeline == 'auto':
        sections = re.split(r'## R\d+', spec)
    elif pipeline == 'hybrid':
        sections = re.split(r'Requirement ID: FR_\d+', spec)
    else:  # manual
        sections = re.split(r'Requirement ID: FR\d+', spec)
    
    # words that make requirements vague
    vague_words = [
        'fast', 'quick', 'slow', 'easy', 'simple', 'hard',
        'good', 'better', 'best', 'user-friendly', 'intuitive',
        'acceptable', 'appropriate', 'reasonable', 'efficient'
    ]
    
    ambiguous_count = 0
    for section in sections[1:]:  # skip the header section
        section_lower = section.lower()
        if any(word in section_lower for word in vague_words):
            ambiguous_count += 1
    
    ambiguity_ratio = ambiguous_count / requirements_count if requirements_count > 0 else 0
    
    # create metrics dict
    metrics = {
        "pipeline": pipeline,
        "dataset_size": total_reviews,
        "persona_count": persona_count,
        "requirements_count": requirements_count,
        "tests_count": tests_count,
        "traceability_links": traceability_links,
        "review_coverage": round(review_coverage, 4),
        "traceability_ratio": round(traceability_ratio, 4),
        "testability_rate": round(testability_rate, 4),
        "ambiguity_ratio": round(ambiguity_ratio, 4)
    }
    
    # print results
    print(f"  Dataset size: {metrics['dataset_size']}")
    print(f"  Personas: {metrics['persona_count']}")
    print(f"  Requirements: {metrics['requirements_count']}")
    print(f"  Tests: {metrics['tests_count']}")
    print(f"  Traceability links: {metrics['traceability_links']}")
    print(f"  Review coverage: {metrics['review_coverage']:.2%}")
    print(f"  Traceability ratio: {metrics['traceability_ratio']:.2%}")
    print(f"  Testability rate: {metrics['testability_rate']:.2%}")
    print(f"  Ambiguity ratio: {metrics['ambiguity_ratio']:.2%}")
    
    return metrics


def main():
    """run metrics for all three pipelines"""
    print("="*60)
    print("COMPUTING METRICS FOR ALL PIPELINES")
    print("="*60)
    
    # create metrics folder if it doesn't exist
    os.makedirs('metrics', exist_ok=True)
    
    all_metrics = {}
    
    # calculate for each pipeline
    for pipeline in ['manual', 'auto', 'hybrid']:
        metrics = get_metrics(pipeline)
        all_metrics[pipeline] = metrics
        
        # save individual metrics file
        filepath = f'metrics/metrics_{pipeline}.json'
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2)
        print(f"  Saved: {filepath}")
    
    # create summary with all three
    summary = {
        "pipelines": ["manual", "auto", "hybrid"],
        "comparison": all_metrics
    }
    
    summary_path = 'metrics/metrics_summary.json'
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print()
    print("="*60)
    print("DONE!")
    print("="*60)
    print(f"Created 4 files in metrics/:")
    print(f"  - metrics_manual.json")
    print(f"  - metrics_auto.json")
    print(f"  - metrics_hybrid.json")
    print(f"  - metrics_summary.json")
    print()
    print("Check metrics_summary.json to compare all three pipelines")


if __name__ == "__main__":
    main()
