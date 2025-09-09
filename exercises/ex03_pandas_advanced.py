# Day 1 - Exercise 3: Advanced Pandas
# Goal: summaries, windows, and high-risk cohort filtering.

import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import pandas as pd

from healthcare_tutorial.loaders import load_healthcare_data
from healthcare_tutorial.analytics import (
    multi_level_summary,
    add_timeline_features,
    high_risk_subset,
)

patients, admissions, labs = load_healthcare_data(data_dir=os.path.join(ROOT, "data"))

# Merge minimal columns for summaries
adm = admissions.merge(patients[["PatientID", "Age", "DiagnosisName"]], on="PatientID", how="left")

# TODO: compute a multi-level summary by site and diagnosis
# summary = ...
# print(summary.head())

# TODO: add timeline features (admission rank, previous admission date)
# adm_timeline = ...
# print(adm_timeline[["PatientID", "AdmissionDate", "RankByAdmission", "PrevAdmission"]].head())

# TODO: filter a high-risk subset (age <2 and LoS above 75th percentile within diagnosis)
# hi = ...
# print({"high_risk_size": len(hi)})

print("Exercise 3 complete — fill in the TODOs above.")
