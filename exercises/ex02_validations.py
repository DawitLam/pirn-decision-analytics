# Day 1 - Exercise 2: Healthcare Validations
# Goal: flag invalid ages, dates, labs; check ID consistency.

import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import pandas as pd

from healthcare_tutorial.loaders import load_healthcare_data
from healthcare_tutorial.dq import (
    validate_pediatric_ages,
    validate_lab_ranges,
    validate_dates,
    validate_length_of_stay_consistency,
    validate_gender_codes,
    validate_icd10_format,
    cross_table_consistency,
)

patients, admissions, labs = load_healthcare_data(data_dir=os.path.join(ROOT, "data"))

# TODO: run each validator and print counts of flags
# age_flags = ...
# date_flags = ...
# lab_flags = ...
# los_flags = ...
# gender_flags = ...
# icd_flags = ...  # will be empty unless DiagnosisCode exists
# xt = ...

# TODO: print concise summaries (counts)
# print({"age": age_flags.sum().to_dict()})
# print({"dates": date_flags.sum().to_dict()})
# print({"labs": lab_flags.sum().to_dict()})
# print({"los_mismatch": int(los_flags.get("los_mismatch", pd.Series(dtype=bool)).sum() if not los_flags.empty else 0)})
# print({"gender": {
#   "missing": int(gender_flags.get("gender_missing", pd.Series(dtype=bool)).sum() if not gender_flags.empty else 0),
#   "invalid": int(gender_flags.get("gender_invalid", pd.Series(dtype=bool)).sum() if not gender_flags.empty else 0),
# }})
# if not icd_flags.empty:
#     print({"icd10_malformed": int(icd_flags.get("icd10_malformed", pd.Series(dtype=bool)).sum())})
# print({"cross_table": xt})

# Challenge: find admissions with discharge before admit and list 5 rows
# bad = ...
# print(bad.head())

print("Exercise 2 complete — implement the TODOs.")
