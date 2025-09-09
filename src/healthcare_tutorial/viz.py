from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt


def show_missing_matrix(df: pd.DataFrame):
    try:
        import missingno as msno
        msno.matrix(df)
    except Exception:
        print("missingno not available")


def plot_age_distribution(df: pd.DataFrame, age_col: str = "Age"):
    df[age_col].dropna().plot(kind="hist", bins=20, alpha=0.7, title="Age Distribution")
    plt.xlabel(age_col); plt.ylabel("Count"); plt.tight_layout(); plt.show()


def plot_los_by_site(df: pd.DataFrame):
    ax = df.groupby("HospitalSite")["LengthOfStay"].mean().sort_values().plot(kind="bar", title="Mean LOS by Site")
    ax.set_ylabel("Days"); plt.tight_layout(); plt.show()


__all__ = [
    "show_missing_matrix",
    "plot_age_distribution",
    "plot_los_by_site",
]
