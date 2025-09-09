from __future__ import annotations
import pandas as pd
import numpy as np

# Analysis helpers

def multi_level_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["HospitalSite", "DiagnosisName"]).agg({
            "Age": ["mean", "median", "count"],
            "LengthOfStay": ["mean", "std"],
            "PatientID": pd.Series.nunique,
        }).round(2)
    )

def add_timeline_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["RankByAdmission"] = out.groupby("HospitalSite")["AdmissionDate"].rank(method="first")
    out = out.sort_values(["PatientID", "AdmissionDate"])  # ensure order prior to shift
    out["PrevAdmission"] = out.groupby("PatientID")["AdmissionDate"].shift(1)
    return out

def high_risk_subset(df: pd.DataFrame) -> pd.DataFrame:
    q75 = df.groupby("DiagnosisName")["LengthOfStay"].transform(lambda s: s.quantile(0.75))
    return df[(df["Age"] < 2) & (df["LengthOfStay"] > q75)]


def create_comprehensive_patient_view(patients_df: pd.DataFrame,
                                      labs_df: pd.DataFrame,
                                      admissions_df: pd.DataFrame) -> pd.DataFrame:
    result = patients_df.copy()
    lab_summary = (
        labs_df.groupby("PatientID").agg(
            LabTestName_count=("LabTestName", "count"),
            TestResultValue_mean=("TestResultValue", "mean"),
            TestResultValue_std=("TestResultValue", "std"),
        )
    )
    admission_summary = (
        admissions_df.groupby("PatientID").agg(
            Admission_count=("AdmissionDate", "count"),
            FirstAdmission=("AdmissionDate", "min"),
            LastAdmission=("AdmissionDate", "max"),
            LengthOfStay_mean=("LengthOfStay", "mean"),
            LengthOfStay_sum=("LengthOfStay", "sum"),
        )
    )
    result = result.merge(lab_summary, on="PatientID", how="left")
    result = result.merge(admission_summary, on="PatientID", how="left")
    return result


def pediatric_analysis_by_age_group(df: pd.DataFrame) -> pd.DataFrame:
    # Define pediatric bins in years; Neonate as <28 days ~ 0.0767 years
    age_bins = [0, 28/365, 1, 5, 12, 18]
    age_labels = ["Neonate", "Infant", "Preschool", "School-age", "Adolescent"]
    out = df.copy()
    out["PediatricAgeGroup"] = pd.cut(out["Age"], bins=age_bins, labels=age_labels, include_lowest=True)
    return out.groupby(["PediatricAgeGroup", "HospitalSite"], observed=True).agg({
        "LengthOfStay": ["mean", "median"],
        "PatientID": "count",
    }).round(2)


def calculate_clinical_flags(df: pd.DataFrame) -> pd.DataFrame:
    flags = pd.DataFrame({
        "PatientID": df["PatientID"],
        "LongStay": df["LengthOfStay"] > 7,
    })
    # FrequentReadmit: compute per patient then map back
    readmit_counts = df.groupby("PatientID")["AdmissionDate"].transform("count")
    flags["FrequentReadmit"] = readmit_counts > 2
    # ComplexCase: needs LabTestCount; if missing, infer from columns
    if "LabTestName_count" in df.columns:
        lab_count = df["LabTestName_count"].fillna(0)
    elif "LabTestCount" in df.columns:
        lab_count = df["LabTestCount"].fillna(0)
    else:
        lab_count = pd.Series(0, index=df.index)
    flags["ComplexCase"] = lab_count > lab_count.quantile(0.9)
    return flags

__all__ = [
    "multi_level_summary",
    "add_timeline_features",
    "high_risk_subset",
    "create_comprehensive_patient_view",
    "pediatric_analysis_by_age_group",
    "calculate_clinical_flags",
]
