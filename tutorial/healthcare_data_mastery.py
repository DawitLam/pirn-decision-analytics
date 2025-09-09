#%%
# Day 1 — Core Skills Reinforcement & Healthcare Data Mastery
# Getting started: imports and data setup
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
import pandas as pd
import numpy as np
from healthcare_tutorial.data_gen import SyntheticConfig, make_patients, make_admissions, make_labs
from healthcare_tutorial.loaders import load_healthcare_data
from healthcare_tutorial.dq import (
    comprehensive_data_profile,
    validate_pediatric_ages,
    validate_lab_ranges,
    validate_dates,
    validate_length_of_stay_consistency,
    validate_gender_codes,
    validate_icd10_format,
    cross_table_consistency,
)
from healthcare_tutorial.analytics import (
    multi_level_summary,
    add_timeline_features,
    high_risk_subset,
    create_comprehensive_patient_view,
    pediatric_analysis_by_age_group,
    calculate_clinical_flags,
)

pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 120)

# Prefer CSVs under ./data if present; otherwise generate synthetic
cfg = SyntheticConfig(n_patients=500, n_admissions_mean=1.6, lab_tests_per_patient_mean=4.0)
patients, admissions, labs = load_healthcare_data(data_dir=os.path.join(ROOT, "data"), cfg=cfg)

print("Shapes:", {"patients": patients.shape, "admissions": admissions.shape, "labs": labs.shape})

#%%
# Optional: Load your own Kaggle dataset (place files in ./data and adjust names)
# patients = pd.read_csv("data/patients.csv")
# admissions = pd.read_csv("data/admissions.csv", parse_dates=["AdmissionDate", "DischargeDate"]) 
# labs = pd.read_csv("data/labs.csv", parse_dates=["CollectedDate"]) 

# Ensure datetime dtypes
for c in ["AdmissionDate", "DischargeDate"]:
    if c in admissions.columns:
        admissions[c] = pd.to_datetime(admissions[c], errors="coerce")
if "CollectedDate" in labs.columns:
    labs["CollectedDate"] = pd.to_datetime(labs["CollectedDate"], errors="coerce")

#%%
# Hour 1-2: Data Quality Toolkit — profiles and missingness
profile_patients = comprehensive_data_profile(patients)
profile_admissions = comprehensive_data_profile(admissions)
profile_labs = comprehensive_data_profile(labs)

print("Patients profile:\n", {k: v if not isinstance(v, pd.Series) else v.to_dict() for k, v in profile_patients.items()})

#%%
# Missing data patterns
print(patients.isnull().sum())
print(patients.info())
print(patients.describe(include="all"))

# Advanced missing data analysis (missingno is optional)
try:
    import missingno as msno
    msno.matrix(patients)
    msno.bar(patients)
except Exception as e:
    print("missingno not available or plotting skipped:", e)

# Duplicates & types
print("Duplicate PatientIDs:", patients.duplicated(subset=["PatientID"]).sum())
patients_dedup = patients.drop_duplicates(keep="first")
if "AdmissionDate" in admissions.columns:
    admissions["AdmissionDate"] = pd.to_datetime(admissions["AdmissionDate"], errors="coerce")
patients["Age_num"] = pd.to_numeric(patients["Age"], errors="coerce")

#%%
# Hour 3-4: Healthcare-Specific Validations
age_flags = validate_pediatric_ages(patients, age_col="Age")
date_flags = validate_dates(admissions)
lab_flags = validate_lab_ranges(labs)
los_flags = validate_length_of_stay_consistency(admissions)
gender_flags = validate_gender_codes(patients)
icd_flags = validate_icd10_format(patients)  # no-op unless DiagnosisCode exists
xt = cross_table_consistency(patients, admissions, labs)

print("Age flags counts:", age_flags.sum().to_dict())
print("Date flags counts:", date_flags.sum().to_dict())
print("Lab flags counts:", lab_flags.sum().to_dict())
print("LOS mismatch count:", int(los_flags.get("los_mismatch", pd.Series(dtype=bool)).sum() if not los_flags.empty else 0))
print("Gender invalid/missing:", {
    "missing": int(gender_flags.get("gender_missing", pd.Series(dtype=bool)).sum() if not gender_flags.empty else 0),
    "invalid": int(gender_flags.get("gender_invalid", pd.Series(dtype=bool)).sum() if not gender_flags.empty else 0),
})
if not icd_flags.empty:
    print("ICD-10 malformed count:", int(icd_flags.get("icd10_malformed", pd.Series(dtype=bool)).sum()))
print("Cross-table consistency:", xt)

#%%
# Hour 5-6: Complex Pandas Operations
# Merge admissions with patients to get Age and DiagnosisName for summaries
adm_enriched = admissions.merge(patients[["PatientID", "Age", "DiagnosisName"]], on="PatientID", how="left")
print("Available columns after merge:", adm_enriched.columns.tolist())
summary = multi_level_summary(adm_enriched)
print(summary.head())

# Window features
adm_timeline = add_timeline_features(adm_enriched)
print(adm_timeline[["PatientID", "AdmissionDate", "RankByAdmission", "PrevAdmission"]].head())

# Complex filtering
hi_risk = high_risk_subset(adm_enriched)
print("High-risk subset size:", len(hi_risk))

#%%
# Hour 7-8: SQL Practice — see sql/healthcare_examples.sql for queries to try in your DB
print("Open sql/healthcare_examples.sql for practice queries.")

#%%
# Evening: Mock Test Practice — set a timer externally; focus on clean, readable code

#%%
# Day 2 — Integration, Speed & Healthcare Context
# Hour 1-2: Multi-Dataset Integration
patient_view = create_comprehensive_patient_view(patients, labs, admissions)
print(patient_view.head())

#%%
# Hour 3-4: Pediatric-Specific Analytics
# Merge only Age from patients to avoid duplicate HospitalSite columns
adm_enriched2 = admissions.merge(patients[["PatientID", "Age"]], on="PatientID", how="left")
ped_by_age = pediatric_analysis_by_age_group(adm_enriched2)
print(ped_by_age.head())

# Clinical decision flags
flags = calculate_clinical_flags(adm_enriched2)
print(flags.head())

#%%
# Hour 5-6: Speed Optimization & Best Practices (demonstration)
# Vectorization vs loops
# SLOW example (commented to avoid runtime cost)
# for i, row in adm_enriched2.iterrows():
#     adm_enriched2.at[i, 'IsLongStay'] = row['LengthOfStay'] > 7

# FAST
adm_enriched2["IsLongStay"] = adm_enriched2["LengthOfStay"] > 7

# Efficient types
adm_enriched2["PatientID"] = adm_enriched2["PatientID"].astype("int32")
adm_enriched2["HospitalSite"] = adm_enriched2["HospitalSite"].astype("category")

# Memory-efficient read example (comment only)
# df = pd.read_csv('data.csv', usecols=['PatientID', 'Age', 'DiagnosisCode'])

result = (
    adm_enriched2.dropna(subset=["Age"]).query("Age >= 0 & Age <= 18").groupby("HospitalSite", observed=True).agg({
        "Age": "mean",
        "PatientID": "count",
    }).round(2)
)
print(result.head())

#%%
# Hour 7: Mock Test Simulation — Use an external timer and a set of 15-20 problems.

#%%
# Evening: Context Review — see README for bullets and key reminders.

print("Tutorial complete. Explore cells above for each topic.")
