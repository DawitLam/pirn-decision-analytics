from __future__ import annotations
import os
import pandas as pd
import numpy as np
from .data_gen import SyntheticConfig, make_patients, make_admissions, make_labs


def _maybe_parse_dates(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c in out.columns:
            out[c] = pd.to_datetime(out[c], errors="coerce")
    return out


def load_healthcare_data(data_dir: str | None = None,
                         cfg: SyntheticConfig | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load patients, admissions, labs.

    If CSVs exist under data_dir, load them; otherwise generate synthetic data.

    Returns: (patients, admissions, labs)
    """
    data_dir = data_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data")
    data_dir = os.path.abspath(data_dir)

    p_csv = os.path.join(data_dir, "patients.csv")
    a_csv = os.path.join(data_dir, "admissions.csv")
    l_csv = os.path.join(data_dir, "labs.csv")

    if all(os.path.exists(p) for p in [p_csv, a_csv, l_csv]):
        patients = pd.read_csv(p_csv)
        admissions = pd.read_csv(a_csv)
        labs = pd.read_csv(l_csv)
        admissions = _maybe_parse_dates(admissions, ["AdmissionDate", "DischargeDate"]) 
        labs = _maybe_parse_dates(labs, ["CollectedDate"]) 
        return patients, admissions, labs

    # Try Synthea Kaggle files if present
    syn_pat = os.path.join(data_dir, "Patients.csv")
    syn_enc = os.path.join(data_dir, "Encounters.csv")
    syn_obs = os.path.join(data_dir, "Observations.csv")
    if all(os.path.exists(p) for p in [syn_pat, syn_enc, syn_obs]):
        patients, admissions, labs = _load_synthea(data_dir)
        return patients, admissions, labs

    # Fallback to synthetic
    cfg = cfg or SyntheticConfig()
    patients = make_patients(cfg)
    admissions = make_admissions(patients, cfg)
    labs = make_labs(patients, cfg)
    return patients, admissions, labs


__all__ = ["load_healthcare_data"]


def _load_synthea(data_dir: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Map Synthea CSVs (Patients, Encounters, Observations) into our schema in-memory.

    Expected files in data_dir:
      - Patients.csv (Id, BIRTHDATE, GENDER, ...)
      - Encounters.csv (PATIENT, START, STOP, ORGANIZATION, REASONDESCRIPTION/DESCRIPTION)
      - Observations.csv (PATIENT, DATE, DESCRIPTION, VALUE, UNIT)
    """
    syn_pat = os.path.join(data_dir, "Patients.csv")
    syn_enc = os.path.join(data_dir, "Encounters.csv")
    syn_obs = os.path.join(data_dir, "Observations.csv")

    patients_raw = pd.read_csv(syn_pat)
    enc_raw = pd.read_csv(syn_enc)
    obs_raw = pd.read_csv(syn_obs)

    # Parse dates
    for c in ["BIRTHDATE"]:
        if c in patients_raw.columns:
            patients_raw[c] = pd.to_datetime(patients_raw[c], errors="coerce")
    for c in ["START", "STOP"]:
        if c in enc_raw.columns:
            enc_raw[c] = pd.to_datetime(enc_raw[c], errors="coerce")
    if "DATE" in obs_raw.columns:
        obs_raw["DATE"] = pd.to_datetime(obs_raw["DATE"], errors="coerce")

    # Build a stable integer PatientID map from Synthea Id
    if "Id" in patients_raw.columns:
        id_series = patients_raw["Id"].astype(str)
    elif "ID" in patients_raw.columns:
        id_series = patients_raw["ID"].astype(str)
    else:
        # fallback to unique PATIENTs in encounters
        id_series = enc_raw["PATIENT"].astype(str).drop_duplicates()
    uniq_ids = pd.Index(id_series.unique())
    id_to_int = {k: i + 1 for i, k in enumerate(uniq_ids)}

    # Admissions mapping
    enc = enc_raw.copy()
    enc["PatientID"] = enc["PATIENT"].astype(str).map(id_to_int)
    # Dates
    adm = pd.DataFrame({
        "PatientID": enc["PatientID"],
        "AdmissionDate": enc.get("START"),
        "DischargeDate": enc.get("STOP"),
        "HospitalSite": enc.get("ORGANIZATION", pd.Series(["Unknown"] * len(enc))),
    })
    # DiagnosisName from reason/description if present
    if "REASONDESCRIPTION" in enc.columns:
        diag_src = enc["REASONDESCRIPTION"]
    elif "DESCRIPTION" in enc.columns:
        diag_src = enc["DESCRIPTION"]
    else:
        diag_src = pd.Series(["Unknown"] * len(enc))
    adm["DiagnosisName"] = diag_src.fillna("Unknown").astype(str).str.slice(0, 64)
    # Compute LOS
    los_days = (adm["DischargeDate"] - adm["AdmissionDate"]).dt.days
    adm["LengthOfStay"] = los_days.clip(lower=0).fillna(0).astype(int)

    # Patients mapping: Age at first encounter or at today
    first_enc = enc.groupby("PatientID")["START"].min() if "START" in enc.columns else pd.Series(dtype="datetime64[ns]")
    ref_dates = first_enc.reindex(range(1, len(uniq_ids) + 1))
    today = pd.Timestamp.today().normalize()
    # Build base patients frame
    pat = pd.DataFrame({
        "PatientID": [id_to_int[k] for k in id_series],
        "Gender": patients_raw.get("GENDER", pd.Series([np.nan] * len(patients_raw))),
    })
    # Age calc
    birth = patients_raw.get("BIRTHDATE")
    if birth is not None:
        # Map birthdate by PatientID order
        pat["_birth"] = birth.values
        # compute age by joining ref date per PatientID
        pat = pat.merge(ref_dates.rename("_ref").reset_index().rename(columns={"index": "PatientID"}), on="PatientID", how="left")
        pat["_ref"] = pat["_ref"].fillna(today)
        age_years = ((pat["_ref"] - pat["_birth"]).dt.days / 365.25).astype(float)
        pat["Age"] = np.floor(np.clip(age_years, a_min=0, a_max=120)).astype("Int64")
    else:
        pat["Age"] = pd.Series([np.nan] * len(pat), dtype="Int64")
    # HospitalSite: most frequent site from admissions
    top_site = adm.groupby("PatientID")["HospitalSite"].agg(lambda s: s.mode().iloc[0] if len(s) and not s.mode().empty else "Unknown")
    pat = pat.merge(top_site.rename("HospitalSite").reset_index(), on="PatientID", how="left")
    # DiagnosisName: most frequent from admissions
    top_dx = adm.groupby("PatientID")["DiagnosisName"].agg(lambda s: s.mode().iloc[0] if len(s) and not s.mode().empty else "Unknown")
    pat = pat.merge(top_dx.rename("DiagnosisName").reset_index(), on="PatientID", how="left")
    patients = pat[["PatientID", "Age", "Gender", "HospitalSite", "DiagnosisName"]].drop_duplicates("PatientID")

    # Labs mapping from Observations
    obs = obs_raw.copy()
    obs["PatientID"] = obs["PATIENT"].astype(str).map(id_to_int)
    labs = pd.DataFrame({
        "PatientID": obs["PatientID"],
        "LabTestName": obs.get("DESCRIPTION", pd.Series(["Unknown"] * len(obs))).astype(str).str.slice(0, 64),
        "TestResultValue": pd.to_numeric(obs.get("VALUE"), errors="coerce"),
        "CollectedDate": obs.get("DATE"),
    })
    # Keep rows with numeric results
    labs = labs.dropna(subset=["TestResultValue"]).reset_index(drop=True)

    # Ensure dtypes where present
    if "PatientID" in patients.columns:
        patients["PatientID"] = patients["PatientID"].astype(int)
    if "PatientID" in adm.columns:
        adm["PatientID"] = adm["PatientID"].astype(int)
    if "PatientID" in labs.columns:
        labs["PatientID"] = labs["PatientID"].astype(int)

    return patients, adm, labs
