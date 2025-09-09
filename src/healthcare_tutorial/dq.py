from __future__ import annotations
import pandas as pd
import numpy as np

# Data quality and validation helpers

def comprehensive_data_profile(df: pd.DataFrame) -> dict:
    """Complete data quality assessment summary."""
    return {
        "shape": df.shape,
        "missing_counts": df.isnull().sum(),
        "missing_percentages": (df.isnull().sum() / len(df) * 100).round(2),
        "duplicates": int(df.duplicated().sum()),
        "data_types": df.dtypes,
        "memory_usage_bytes": int(df.memory_usage(deep=True).sum()),
    }

def validate_pediatric_ages(df: pd.DataFrame, age_col: str = "Age") -> pd.DataFrame:
    """Return boolean flags for pediatric-specific age validation."""
    flags = pd.DataFrame(index=df.index)
    flags["negative_age"] = df[age_col] < 0
    flags["adult_age"] = df[age_col] >= 18
    flags["extreme_age"] = df[age_col] > 21
    return flags

LAB_RANGES = {
    "Glucose": (2.8, 11.1),  # mmol/L
    "Sodium": (136, 145),    # mmol/L
    "Hemoglobin": (110, 160) # g/L
}

def validate_lab_ranges(labs_df: pd.DataFrame,
                         name_col: str = "LabTestName",
                         value_col: str = "TestResultValue") -> pd.DataFrame:
    """Check lab values against reference ranges; returns flags dataframe."""
    flags = pd.DataFrame(index=labs_df.index)
    lo = labs_df[name_col].map(lambda n: LAB_RANGES.get(n, (np.nan, np.nan))[0])
    hi = labs_df[name_col].map(lambda n: LAB_RANGES.get(n, (np.nan, np.nan))[1])
    flags["below_range"] = labs_df[value_col] < lo
    flags["above_range"] = labs_df[value_col] > hi
    flags["unknown_test"] = ~labs_df[name_col].isin(LAB_RANGES.keys())
    return flags

def validate_dates(adm_df: pd.DataFrame,
                   admit_col: str = "AdmissionDate",
                   discharge_col: str = "DischargeDate") -> pd.DataFrame:
    flags = pd.DataFrame(index=adm_df.index)
    flags["missing_admit"] = adm_df[admit_col].isna()
    flags["missing_discharge"] = adm_df[discharge_col].isna()
    flags["discharge_before_admit"] = adm_df[discharge_col] < adm_df[admit_col]
    flags["long_stay_>60d"] = (adm_df[discharge_col] - adm_df[admit_col]).dt.days > 60
    return flags


def validate_length_of_stay_consistency(adm_df: pd.DataFrame,
                                        admit_col: str = "AdmissionDate",
                                        discharge_col: str = "DischargeDate",
                                        los_col: str = "LengthOfStay") -> pd.DataFrame:
    """Check that LengthOfStay equals (discharge - admit).days where dates are present."""
    flags = pd.DataFrame(index=adm_df.index)
    valid_dates = adm_df[admit_col].notna() & adm_df[discharge_col].notna()
    expected = (adm_df[discharge_col] - adm_df[admit_col]).dt.days
    flags["los_mismatch"] = valid_dates & (adm_df[los_col] != expected)
    return flags


def validate_gender_codes(df: pd.DataFrame,
                          gender_col: str = "Gender",
                          allowed: tuple[str, ...] = ("M", "F")) -> pd.DataFrame:
    """Validate gender codes against allowed set (default: M/F)."""
    flags = pd.DataFrame(index=df.index)
    if gender_col not in df.columns:
        return flags  # silently return empty if column absent
    flags["gender_missing"] = df[gender_col].isna()
    flags["gender_invalid"] = ~df[gender_col].isin(allowed) & df[gender_col].notna()
    return flags


def validate_icd10_format(df: pd.DataFrame,
                          code_col: str = "DiagnosisCode") -> pd.DataFrame:
    """Basic ICD-10 code format check (not clinical validation).

    Pattern: Letter (A-TV-Z), 2 digits (or A/B in 3rd char), optional . and up to 4 more
    Example valid: J45, J45.901, S52.5
    """
    import re
    flags = pd.DataFrame(index=df.index)
    if code_col not in df.columns:
        return flags
    pattern = re.compile(r"^[A-TV-Z][0-9][0-9AB](\.[0-9A-TV-Z]{1,4})?$")
    codes = df[code_col].astype(str).str.strip()
    flags["icd10_missing"] = df[code_col].isna() | (codes == "")
    flags["icd10_malformed"] = ~codes.str.match(pattern, na=False)
    return flags


def cross_table_consistency(patients: pd.DataFrame,
                            admissions: pd.DataFrame,
                            labs: pd.DataFrame,
                            id_col: str = "PatientID") -> dict:
    """Basic cross-table integrity checks on patient IDs."""
    pid_pat = set(patients[id_col].dropna().astype(int)) if id_col in patients.columns else set()
    pid_adm = set(admissions[id_col].dropna().astype(int)) if id_col in admissions.columns else set()
    pid_lab = set(labs[id_col].dropna().astype(int)) if id_col in labs.columns else set()

    return {
        "admissions_with_unknown_patient": int((~admissions[id_col].isin(pid_pat)).sum()) if id_col in admissions.columns else 0,
        "labs_with_unknown_patient": int((~labs[id_col].isin(pid_pat)).sum()) if id_col in labs.columns else 0,
        "patients_missing_admissions": int(len(pid_pat - pid_adm)),
        "patients_missing_labs": int(len(pid_pat - pid_lab)),
    }

__all__ = [
    "comprehensive_data_profile",
    "validate_pediatric_ages",
    "validate_lab_ranges",
    "validate_dates",
    "validate_length_of_stay_consistency",
    "validate_gender_codes",
    "validate_icd10_format",
    "cross_table_consistency",
    "LAB_RANGES",
]
