# Healthcare Data Mastery – Interactive Tutorial

A hands-on, two-day practice guide for pediatric healthcare data using Pandas and SQL. This repo includes an interactive Python script with notebook-style cells, supporting utilities, and example SQL queries.

## What’s inside
- `tutorial/healthcare_data_mastery.py` – Interactive, notebook-style script (#%% cells) covering Day 1 and Day 2.
- `src/healthcare_tutorial/` – Reusable helpers for data generation, data quality checks, and analytics.
- `sql/healthcare_examples.sql` – Example SQL queries for practice.
- `requirements.txt` – Python dependencies.

## Setup (Windows PowerShell)

```powershell
# 1) Create and activate a virtual environment
py -3 -m venv .venv
. .venv\Scripts\Activate.ps1

# 2) Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3) Open the tutorial file and run cells
# In VS Code, open tutorial/healthcare_data_mastery.py
# Use the "Run Cell" code lens above each #%% cell (or Shift+Enter)
```

If VS Code asks to enable the Python Interactive window, accept. The #%% cells run like a notebook.

## Optional: Bring your own Kaggle dataset
Place CSV files in a new `data/` folder and adjust the "Load your dataset" cell in the tutorial. Columns commonly used:
- Patients: PatientID, Age, Gender, DiagnosisCode/Name, HospitalSite
- Labs: PatientID, LabTestName, TestResultValue, CollectedDate
- Admissions: PatientID, AdmissionDate, DischargeDate, LengthOfStay, HospitalSite

## Goals
- Rapid data quality assessment and clinical validations.
- Pediatric-focused analysis patterns and multi-dataset integration.
- Speed and readability under time constraints.

## Quick tips
- Prefer vectorized operations over loops.
- Validate dates (admission before discharge) and age ranges.
- Keep column names consistent across merges.
- Document assumptions briefly in comments.

Enjoy the practice and iterate fast.
