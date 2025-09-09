from __future__ import annotations
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


def knn_impute_numeric(df: pd.DataFrame, cols: list[str], n_neighbors: int = 5) -> pd.DataFrame:
    out = df.copy()
    imputer = KNNImputer(n_neighbors=n_neighbors)
    out[cols] = imputer.fit_transform(out[cols])
    return out


def build_cleaning_pipeline(numeric_features: list[str], categorical_features: list[str]) -> Pipeline:
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
    ])
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
    pre = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )
    pipe = Pipeline(steps=[("prep", pre)])
    return pipe


__all__ = [
    "knn_impute_numeric",
    "build_cleaning_pipeline",
]
