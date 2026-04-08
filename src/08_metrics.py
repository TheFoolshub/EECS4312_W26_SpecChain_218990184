import json
import os
import re
from typing import Dict, List


class MetricsCalculator:
    """Calculates quality metrics for requirements engineering pipelines"""
    
    def __init__(self, pipeline_name: str):
        self.pipeline = pipeline_name
        self.review_file = "data/reviews_clean.jsonl"
        self.group_file = f"data/review_groups_{pipeline_name}.json"
        self.persona_file = f"personas/personas_{pipeline_name}.json"
        self.spec_file = f"spec/spec_{pipeline_name}.md"
        self.test_file = f"tests/tests_{pipeline_name}.json"
    
    #  Counting Functions 
    
    def count_reviews(self) -> int:
        if not os.path.exists(self.review_file):
            return 0
        
        count = 0
        with open(self.review_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    count += 1
        return count
    
    def count_personas(self) -> int:
        if not os.path.exists(self.persona_file):
            return 0
        
        with open(self.persona_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return len(data.get("personas", []))
    
    def count_requirements(self) -> int:
        if not os.path.exists(self.spec_file):
            return 0
        
        with open(self.spec_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return len(set(re.findall(r'R\d+', content)))
    
    def count_tests(self) -> int:
        if not os.path.exists(self.test_file):
            return 0
        
        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return len(data.get("tests", []))
    
    #  Traceability Metrics 
    
    def calculate_traceability_links(self) -> int:
        links = 0
        
        if os.path.exists(self.spec_file):
            with open(self.spec_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            links += len(re.findall(r'Persona:', content))
            links += len(re.findall(r'Review Group:', content))
        
        if os.path.exists(self.persona_file):
            with open(self.persona_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for persona in data.get("personas", []):
                if persona.get("group_id"):
                    links += 1
        
        return links
    
    def calculate_review_coverage(self) -> float:
        total_reviews = self.count_reviews()
        if total_reviews == 0 or not os.path.exists(self.group_file):
            return 0.0
        
        with open(self.group_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # ✅ FIXED: handle both formats
        if isinstance(data, dict) and "groups" in data:
            groups = data["groups"]
        else:
            groups = data
        
        covered = 0
        
        for group in groups:
            if isinstance(group, dict):
                covered += len(group.get("reviews", []))
        
        return covered / total_reviews if total_reviews else 0.0
    
    def calculate_traceability_ratio(self) -> float:
        req_count = self.count_requirements()
        if req_count == 0:
            return 0.0
        
        if not os.path.exists(self.spec_file):
            return 0.0
        
        with open(self.spec_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        traced = len(re.findall(r'Persona:', content))
        
        return traced / req_count if req_count else 0.0
    
    #  Quality Metrics 
    
    def calculate_testability_rate(self) -> float:
        if not os.path.exists(self.spec_file) or not os.path.exists(self.test_file):
            return 0.0
        
        with open(self.spec_file, 'r', encoding='utf-8') as f:
            spec_content = f.read()
        
        req_ids = set(re.findall(r'R\d+', spec_content))
        
        with open(self.test_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        tested_ids = set()
        for test in test_data.get("tests", []):
            if test.get("requirement_id"):
                tested_ids.add(test["requirement_id"])
        
        if not req_ids:
            return 0.0
        
        return len(req_ids.intersection(tested_ids)) / len(req_ids)
    
    def calculate_ambiguity_ratio(self) -> float:
        if not os.path.exists(self.spec_file):
            return 0.0
        
        with open(self.spec_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sections = re.split(r'R\d+', content)
        
        vague_terms = [
            'fast', 'quick', 'slow', 'easy', 'simple', 'hard',
            'good', 'better', 'best', 'user-friendly', 'intuitive',
            'acceptable', 'appropriate', 'reasonable', 'efficient'
        ]
        
        ambiguous = 0
        total = len(sections) - 1
        
        for section in sections[1:]:
            text = section.lower()
            if any(term in text for term in vague_terms):
                ambiguous += 1
        
        return ambiguous / total if total > 0 else 0.0
    
    #  Main 
    
    def compute_all_metrics(self) -> Dict:
        return {
            "pipeline": self.pipeline,
            "dataset_size": self.count_reviews(),
            "persona_count": self.count_personas(),
            "requirements_count": self.count_requirements(),
            "tests_count": self.count_tests(),
            "traceability_links": self.calculate_traceability_links(),
            "review_coverage": round(self.calculate_review_coverage(), 4),
            "traceability_ratio": round(self.calculate_traceability_ratio(), 4),
            "testability_rate": round(self.calculate_testability_rate(), 4),
            "ambiguity_ratio": round(self.calculate_ambiguity_ratio(), 4)
        }


def save_json(data: Dict, filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def display_metrics(metrics: Dict) -> None:
    print(f"  Pipeline: {metrics['pipeline']}")
    print(f"  Dataset size: {metrics['dataset_size']}")
    print(f"  Personas: {metrics['persona_count']}")
    print(f"  Requirements: {metrics['requirements_count']}")
    print(f"  Tests: {metrics['tests_count']}")
    print(f"  Traceability links: {metrics['traceability_links']}")
    print(f"  Review coverage: {metrics['review_coverage']:.2%}")
    print(f"  Traceability ratio: {metrics['traceability_ratio']:.2%}")
    print(f"  Testability rate: {metrics['testability_rate']:.2%}")
    print(f"  Ambiguity ratio: {metrics['ambiguity_ratio']:.2%}")


def main():
    print("=" * 60)
    print("TASK 4.5 & 6: METRICS COMPUTATION")
    print("=" * 60)
    print()
    
    os.makedirs("metrics", exist_ok=True)
    
    pipelines = ["manual", "auto", "hybrid"]
    all_metrics = {}
    
    for pipeline in pipelines:
        print(f"Computing metrics for {pipeline} pipeline...\n")
        
        calculator = MetricsCalculator(pipeline)
        metrics = calculator.compute_all_metrics()
        all_metrics[pipeline] = metrics
        
        display_metrics(metrics)
        print()
        
        save_json(metrics, f"metrics/metrics_{pipeline}.json")
        print(f"  ✓ Saved: metrics/metrics_{pipeline}.json\n")
    
    summary = {
        "pipelines": pipelines,
        "comparison": all_metrics
    }
    
    save_json(summary, "metrics/metrics_summary.json")
    
    print("=" * 60)
    print("TASK 4.5 COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
