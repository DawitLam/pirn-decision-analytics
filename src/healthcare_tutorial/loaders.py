from __future__ import annotations
import os
import pandas as pd
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

    # Fallback to synthetic
    cfg = cfg or SyntheticConfig()
    patients = make_patients(cfg)
    admissions = make_admissions(patients, cfg)
    labs = make_labs(patients, cfg)
    return patients, admissions, labs


__all__ = ["load_healthcare_data"]
