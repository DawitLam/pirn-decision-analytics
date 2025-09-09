# Day 2 - Exercise 5: ETL, ML-based Cleaning, and Viz
# Goal: clean labs, flag LoS outliers, impute age (if needed), build star schema, and plot.

import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import pandas as pd

from healthcare_tutorial.loaders import load_healthcare_data
from healthcare_tutorial.etl import simple_cleaning, iqr_outlier_flags, build_star_schema
from healthcare_tutorial.ml_clean import knn_impute_numeric, build_cleaning_pipeline
from healthcare_tutorial.viz import plot_los_by_site

patients, admissions, labs = load_healthcare_data(data_dir=os.path.join(ROOT, "data"))

# TODO: clean labs: coerce numeric and drop NAs in key columns
# labs_clean = ...
# print({"labs_clean": labs_clean.shape})

# TODO: add LoS outlier flag using IQR on LengthOfStay
# admissions["LoS_Outlier"] = ...
# print({"los_outliers": int(admissions["LoS_Outlier"].sum())})

# TODO: if any Age is missing, perform KNN imputation on Age
# if patients["Age"].isna().any():
#     patients = ...

# TODO: build a star schema and print shapes
# star = ...
# print({k: v.shape for k, v in star.items()})

# TODO: build a simple cleaning pipeline and fit_transform on a small set of columns
# num_cols = [c for c in ["Age", "LengthOfStay"] if c in admissions.columns or c in patients.columns]
# cat_cols = [c for c in ["Gender", "HospitalSite", "DiagnosisName"] if c in patients.columns]
# Example input frame
# X = admissions.merge(patients[["PatientID", "Age", "Gender", "HospitalSite", "DiagnosisName"]], on="PatientID", how="left")
# keep = [c for c in num_cols + cat_cols if c in X.columns]
# pipe = ...
# _ = pipe.fit_transform(X[keep])

# TODO: plot LOS by site (optional)
try:
    plot_los_by_site(admissions.merge(patients[["PatientID", "Age"]], on="PatientID", how="left"))
except Exception as e:
    print("plot skipped:", e)

print("Exercise 5 complete — implement the TODOs.")
