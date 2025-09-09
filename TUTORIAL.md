# Healthcare Data Mastery: Two-Day Lesson (Pediatrics Focus)

A hands-on curriculum that moves from core data quality skills to advanced analytics, ETL, ML-based cleaning, and visualizations using pediatric healthcare data.

Use the interactive reference `tutorial/healthcare_data_mastery.py`. Practice with runnable exercises in `exercises/`.

## Day 1 — Core skills and healthcare data (4–6 hours)

Objectives
- Read and inspect datasets quickly
- Profile data quality: missingness, duplicates, dtypes, memory
- Apply healthcare validations (ages, labs, dates, IDs)
- Master pandas patterns (groupby, windows, transforms)

Modules
1) Data quality toolkit
- Quick profile: shape, missingness, dtypes, memory
- Missingness visuals (optional): `missingno`
- Duplicates, type coercion (to_numeric/to_datetime)

2) Healthcare validations
- Pediatric age rules; clinical lab ranges
- Date logic: admit < discharge, LoS consistency
- Coding: gender codes, ICD-10 format
- Cross-table integrity: PatientID across tables

3) Advanced pandas
- Multi-level groupby/agg
- Window features: admission rank, previous admission
- Complex filters: high-risk cohorts (e.g., infants with long stays)

Practice
- Run `exercises/ex01_data_quality.py`
- Run `exercises/ex02_validations.py`
- Run `exercises/ex03_pandas_advanced.py`

Checkpoint
- You can produce a concise profile and visualize missingness
- You can flag clinically invalid rows
- You can build a summary by site/diagnosis and compute timelines

## Day 2 — Integration, pediatric analytics, ETL/ML, viz (4–6 hours)

Objectives
- Integrate multi-table data; produce a comprehensive patient view
- Pediatric cohorts (Neonate→Adolescent); site-level metrics
- Build a simple star schema (dims/facts)
- Apply ML-based cleaning and a basic pipeline
- Create simple, informative visuals

Modules
1) Integration & pediatric analytics
- Comprehensive patient view (lab and admission summaries)
- Pediatric bins & clinical flags (LongStay, FrequentReadmit, ComplexCase)

2) ETL & ML-based cleaning (bonus)
- Simple cleaning (numeric coercion, NA handling)
- Outlier detection (IQR)
- KNN imputation; sklearn pipeline (numeric/categorical)
- Star schema: `dim_patient`, `dim_diagnosis`, `dim_labtest`, `fact_admission`, `fact_lab`

3) Visualizations
- LOS by site; distributions (histograms)

Practice
- Run `exercises/ex04_integration.py`
- Run `exercises/ex05_etl_ml_viz.py`

Checkpoint
- You can integrate datasets and calculate coherent summaries
- You can build a small star schema and apply an ML cleaning pipeline
- You can produce 1–2 clear visualizations and interpret them

## Data sources
- Synthetic (default) — auto-generated for fast practice
- Kaggle Synthea (recommended) — drop `Patients.csv`, `Encounters.csv`, `Observations.csv` into `data/` and the loader will map them automatically

## How to run
- Local
  - `py -3 -m venv .venv` then activate and `pip install -r requirements.txt`
  - Run the reference: `.venv/Scripts/python.exe tutorial/healthcare_data_mastery.py`
  - Run an exercise: `.venv/Scripts/python.exe exercises/ex01_data_quality.py`
- Colab
  - Clone the repo, install `pandas numpy missingno pyarrow scikit-learn matplotlib`
  - `!python tutorial/healthcare_data_mastery.py`
  - `!python exercises/ex01_data_quality.py`

Tips
- Keep changes incremental; print summaries, not entire frames
- Add assertions to check pre/post conditions (e.g., counts, dtypes)
- Timebox tasks (10–20 minutes each) and iterate
