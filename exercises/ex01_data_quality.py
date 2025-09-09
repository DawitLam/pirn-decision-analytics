# Day 1 - Exercise 1: Data Quality Toolkit
# Goal: produce a quick profile and explore missingness patterns.

import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import pandas as pd

from healthcare_tutorial.loaders import load_healthcare_data
from healthcare_tutorial.dq import comprehensive_data_profile

# 1) Load data (synthetic or from data/ if CSVs exist)
patients, admissions, labs = load_healthcare_data(data_dir=os.path.join(ROOT, "data"))
print({"shapes": {"patients": patients.shape, "admissions": admissions.shape, "labs": labs.shape}})

# 2) TODO: compute a profile for patients and print a concise summary
#    Hint: use comprehensive_data_profile
# profile = ...
# print("patients.profile.shape", profile["shape"]))
# print("patients.missing.top5", profile["missing_counts"].sort_values(ascending=False).head().to_dict())

# 3) TODO: Convert Age to numeric (coerce) and show basic describe()
# patients["Age"] = ...
# print(patients[["Age"]].describe())

# 4) Optional: missingness visualization with missingno (ignore if not installed)
try:
    import missingno as msno
    msno.matrix(patients)
    msno.bar(patients)
except Exception as e:
    print("missingno skipped:", e)

print("Exercise 1 complete — fill in the TODOs above.")
