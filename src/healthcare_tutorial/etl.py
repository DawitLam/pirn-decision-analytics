from __future__ import annotations
import os
import pandas as pd


def ensure_output_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def simple_cleaning(df: pd.DataFrame, dropna_cols: list[str] | None = None,
                    numeric_coerce: list[str] | None = None) -> pd.DataFrame:
    out = df.copy()
    if numeric_coerce:
        for c in numeric_coerce:
            if c in out.columns:
                out[c] = pd.to_numeric(out[c], errors="coerce")
    if dropna_cols:
        out = out.dropna(subset=[c for c in dropna_cols if c in out.columns])
    return out


def iqr_outlier_flags(series: pd.Series, k: float = 1.5) -> pd.Series:
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lo = q1 - k * iqr
    hi = q3 + k * iqr
    return (series < lo) | (series > hi)


def build_star_schema(patients: pd.DataFrame,
                      admissions: pd.DataFrame,
                      labs: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Create a simple star schema with dims and facts.

    Returns dict with: dim_patient, dim_diagnosis, dim_labtest, fact_admission, fact_lab
    """
    dim_patient = patients[["PatientID", "Gender", "Age", "HospitalSite"]].drop_duplicates("PatientID")
    # Diagnosis dimension
    dim_diag = (patients[["DiagnosisName"]].drop_duplicates().reset_index(drop=True))
    dim_diag["DiagnosisKey"] = range(1, len(dim_diag) + 1)
    patients_diag = patients.merge(dim_diag, on="DiagnosisName", how="left")

    fact_adm = admissions.merge(patients_diag[["PatientID", "DiagnosisKey"]].drop_duplicates("PatientID"),
                                on="PatientID", how="left")

    # Lab test dimension
    if "LabTestName" in labs.columns:
        dim_lab = labs[["LabTestName"]].drop_duplicates().reset_index(drop=True)
        dim_lab["LabKey"] = range(1, len(dim_lab) + 1)
        fact_lab = labs.merge(dim_lab, on="LabTestName", how="left")
    else:
        dim_lab = pd.DataFrame({"LabTestName": [], "LabKey": []})
        fact_lab = labs.copy()

    return {
        "dim_patient": dim_patient,
        "dim_diagnosis": dim_diag,
        "dim_labtest": dim_lab,
        "fact_admission": fact_adm,
        "fact_lab": fact_lab,
    }


__all__ = [
    "ensure_output_dir",
    "simple_cleaning",
    "iqr_outlier_flags",
    "build_star_schema",
]
