# Day 2 - Exercise 4: Integration & Pediatric Analytics
# Goal: build a comprehensive patient view and pediatric age group summaries.

import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import pandas as pd

from healthcare_tutorial.loaders import load_healthcare_data
from healthcare_tutorial.analytics import (
    create_comprehensive_patient_view,
    pediatric_analysis_by_age_group,
    calculate_clinical_flags,
)

patients, admissions, labs = load_healthcare_data(data_dir=os.path.join(ROOT, "data"))

# TODO: create a comprehensive patient view
# pv = ...
# print(pv.head())

# TODO: compute pediatric analysis by age groups (Neonate→Adolescent)
# adm_enriched = admissions.merge(patients[["PatientID", "Age"]], on="PatientID", how="left")
# ped = ...
# print(ped.head())

# TODO: derive clinical flags (LongStay, FrequentReadmit, ComplexCase)
# flags = ...
# print(flags.head())

print("Exercise 4 complete — implement the TODOs.")
