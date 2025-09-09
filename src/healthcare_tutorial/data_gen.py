from __future__ import annotations
import numpy as np
import pandas as pd
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Tuple

@dataclass
class SyntheticConfig:
    n_patients: int = 1000
    n_admissions_mean: float = 1.5
    lab_tests_per_patient_mean: float = 5.0
    start_date: str = "2022-01-01"
    end_date: str = "2024-12-31"

HOSPITAL_SITES = [
    "HSC", "CHEO", "LHSC", "SickKids", "McMaster", "Hamilton", "OttawaGen"
]
DIAGNOSES = [
    "Asthma", "Bronchiolitis", "Fracture", "Gastroenteritis", "Sepsis", "Influenza"
]
LABS = ["Glucose", "Sodium", "Hemoglobin"]
GENDERS = ["M", "F"]

rng = np.random.default_rng(42)

def _random_dates(n: int, start: datetime, end: datetime) -> pd.Series:
    span_days = (end - start).days
    offs = rng.integers(0, span_days + 1, size=n)
    return pd.to_datetime(start + pd.to_timedelta(offs, unit="D"))

def make_patients(cfg: SyntheticConfig) -> pd.DataFrame:
    ages = rng.integers(0, 18, size=cfg.n_patients)  # pediatric ages 0-17
    patient_ids = np.arange(1, cfg.n_patients + 1)
    genders = rng.choice(GENDERS, size=cfg.n_patients)
    sites = rng.choice(HOSPITAL_SITES, size=cfg.n_patients)
    dx = rng.choice(DIAGNOSES, size=cfg.n_patients)
    return pd.DataFrame({
        "PatientID": patient_ids,
        "Age": ages,
        "Gender": genders,
        "HospitalSite": sites,
        "DiagnosisName": dx,
    })

def make_admissions(patients: pd.DataFrame, cfg: SyntheticConfig) -> pd.DataFrame:
    start = pd.to_datetime(cfg.start_date)
    end = pd.to_datetime(cfg.end_date)
    rows = []
    for pid in patients["PatientID"]:
        n = max(1, int(rng.poisson(cfg.n_admissions_mean)))
        ad_dates = _random_dates(n, start, end).sort_values().to_list()
        for ad in ad_dates:
            los = int(max(0, rng.normal(3, 2)))  # mean ~3 days
            disch = ad + timedelta(days=los)
            rows.append({
                "PatientID": pid,
                "AdmissionDate": ad,
                "DischargeDate": disch,
                "LengthOfStay": (disch - ad).days,
                "HospitalSite": rng.choice(HOSPITAL_SITES),
            })
    return pd.DataFrame(rows)

def make_labs(patients: pd.DataFrame, cfg: SyntheticConfig) -> pd.DataFrame:
    start = pd.to_datetime(cfg.start_date)
    end = pd.to_datetime(cfg.end_date)
    rows = []
    for pid in patients["PatientID"]:
        n = max(0, int(rng.poisson(cfg.lab_tests_per_patient_mean)))
        for _ in range(n):
            test = rng.choice(LABS)
            if test == "Glucose":
                val = rng.normal(5.5, 1.2)
            elif test == "Sodium":
                val = rng.normal(140, 3)
            else:  # Hemoglobin (g/L)
                val = rng.normal(130, 15)
            rows.append({
                "PatientID": pid,
                "LabTestName": test,
                "TestResultValue": float(np.round(val, 1)),
                "CollectedDate": _random_dates(1, start, end)[0],
            })
    return pd.DataFrame(rows)

__all__ = [
    "SyntheticConfig",
    "make_patients",
    "make_admissions",
    "make_labs",
]
