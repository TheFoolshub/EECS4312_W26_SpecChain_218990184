# SpecChain: Requirements Engineering from App Reviews

EECS 4312 - Software Requirements  
York University, Winter 2026

---

## Project Overview

This project transforms Google Play Store reviews into software requirements using three different approaches: manual analysis, automated generation with AI, and a hybrid combination of both.

---

## Application Studied

**App:** Headspace: Sleep & Meditation  
## Dataset

**Final Dataset Size:** 2,326 cleaned reviews  
**File Location:** `data/reviews_clean.jsonl`  

## Repository Structure

```
project/
├── data/
│   ├── reviews_clean.jsonl              # 2,326 cleaned reviews
│   ├── review_groups_manual.json        # Manual: 5 groups, 50 reviews
│   ├── review_groups_auto.json          # Auto: 5 groups, 21 reviews
│   └── review_groups_hybrid.json        # Hybrid: 5 groups, 50 reviews
│
├── personas/
│   ├── personas_manual.json             # Manual: 5 personas
│   ├── personas_auto.json               # Auto: 5 personas
│   └── personas_hybrid.json             # Hybrid: 5 personas
│
├── spec/
│   ├── spec_manual.md                   # Manual: 12 requirements
│   ├── spec_auto.md                     # Auto: 10 requirements
│   └── spec_hybrid.md                   # Hybrid: 12 requirements
│
├── tests/
│   ├── tests_manual.json                # Manual: 24 test cases
│   ├── tests_auto.json                  # Auto: 20 test cases
│   └── tests_hybrid.json                # Hybrid: 24 test cases
│
├── metrics/
│   ├── metrics_manual.json              # Manual pipeline metrics
│   ├── metrics_auto.json                # Auto pipeline metrics
│   ├── metrics_hybrid.json              # Hybrid pipeline metrics
│   └── metrics_summary.json             # Comparison of all 3
│
├── src/
│   ├── 00_validate_repo.py              # Check all files exist
│   ├── 01_scrape.py                     # Scrape reviews from Google Play
│   ├── 02_clean.py                      # Clean review data
│   ├── 05_personas_auto.py              # Generate groups & personas (AI)
│   ├── 06_spec_generate.py              # Generate requirements (AI)
│   ├── 07_tests_generate.py             # Generate tests (AI)
│   ├── 08_metrics.py                    # Calculate metrics
│   └── run_all.py                       # Run entire automated pipeline
│
├── reflection/
│   └── reflection.md                    # Project analysis and insights
│
└── README.md                            # This file
```

---

## Required Software and Packages

### Python
- **Version:** Python 3.8 or higher
- Check your version: `python --version`

### Required Packages
Install these before running:

```bash
pip install groq
pip install google-play-scraper
```

---

## API Configuration (IMPORTANT!)

The automated pipeline uses Groq AI to generate requirements. You need to add your own API key.

### Step 1: Get a Free API Key

1. Go to https://console.groq.com
2. Sign up for free
3. Click "API Keys"
4. Click "Create API Key"
5. Copy your key (starts with `gsk_`)

### Step 2: Add Your API Key to Source Files

You need to edit **3 files** and replace the API key:

**File 1: src/05_personas_auto.py**

Open the file and find around **line 15**:

```python
# Configuration
 client = Groq(api_key="gsk_k...") 
```

Replace `"gsk_YOUR_KEY_HERE"` with your actual API key:

```python
# Configuration
API_KEY = "gsk_abc123xyz..."  # ← YOUR ACTUAL KEY
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"
MIN_TESTS_PER_REQ = 2
```

**File 2: src/06_spec_generate.py**

Same change at **line 31** - replace the API_KEY value

**File 3: src/07_tests_generate.py**

Same change at **line 32** - replace the API_KEY value

**SAVE all three files after editing!**

---

## How to Run the Project

### Step 1: Update API Keys

Before running anything, make sure you edited these 3 files:
- src/05_personas_auto.py (line 15)
- src/06_spec_generate.py (line 15)
- src/07_tests_generate.py (line 15)

### Step 2: Run the Automated Pipeline

```bash
python src/run_all.py
```

This will execute all automated steps in order:
1. Scrape reviews from Google Play
2. Clean the review data
3. Generate review groups using AI
4. Create personas using AI
5. Generate requirements using AI
6. Create test cases using AI
7. Calculate metrics

**Time:** Takes about 2-3 minutes to complete

**Output:** Creates all files in the `*_auto.json` and `*_auto.md` format

### Step 3: Validate Repository

After running, check that all files were created:

```bash
python src/00_validate_repo.py
```

You should see:
```
All required files and folders are present!
```

---

## What Gets Generated

When you run `src/run_all.py`, these files are created:

**Data:**
- data/reviews_raw.jsonl (scraped reviews)
- data/reviews_clean.jsonl (cleaned reviews)

**Automated Pipeline:**
- data/review_groups_auto.json (5 review groups)
- personas/personas_auto.json (5 personas)
- spec/spec_auto.md (10 requirements)
- tests/tests_auto.json (20 test cases)
- metrics/metrics_auto.json (pipeline metrics)
- metrics/metrics_summary.json (comparison of all pipelines)

**Note:** Manual and hybrid files are already included and won't be overwritten.


## Troubleshooting

**Problem:** "Groq API key not found"  
**Solution:** Make sure you edited the API_KEY in src/05, src/06, and src/07

**Problem:** "Module 'groq' not found"  
**Solution:** Run `pip install groq`

**Problem:** "File not found" errors  
**Solution:** Make sure you're in the project root folder (where README.md is)

**Problem:** Scripts won't run  
**Solution:** Check Python version with `python --version` (need 3.8+)

---

## Additional Commands

### Run Just Metrics
```bash
python src/08_metrics.py
```

### Run Individual Steps
```bash
python src/05_personas_auto.py  # Just generate personas
python src/06_spec_generate.py  # Just generate requirements
python src/07_tests_generate.py # Just generate tests
```

---

## Files Already Included

The repository already contains completed manual and hybrid pipelines:

**Manual Pipeline Files:**
- data/review_groups_manual.json
- personas/personas_manual.json
- spec/spec_manual.md
- tests/tests_manual.json
- metrics/metrics_manual.json

**Hybrid Pipeline Files:**
- data/review_groups_hybrid.json
- personas/personas_hybrid.json
- spec/spec_hybrid.md
- tests/tests_hybrid.json
- metrics/metrics_hybrid.json

You don't need to create these  they're ready to use!

---

## Project Information

**Course:** EECS 4312 - Software Requirements  
**Instructor:** Maleknaz Nayebi  
**Institution:** York University  
**Term:** Winter 2026  

**Tasks Completed:**
- Task 1: Data Collection
- Task 2: Data Cleaning
- Task 3: Manual Pipeline
- Task 4: Automated Pipeline
- Task 5: Hybrid Pipeline
- Task 6: Metrics Comparison
- Task 7: Repository Scripts
- Task 8: Documentation

---


4. Open metrics/metrics_summary.json for comparison results

