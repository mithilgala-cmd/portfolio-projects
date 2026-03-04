import os

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_data(path):
    """Load CSV from *path*, raising a clear error if the file is missing."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Data file not found: {path}\n"
            "Make sure train.csv / test.csv are placed in the data/ folder."
        )
    return pd.read_csv(path)


def split_features_target(df):
    """
    Drop Id, log-transform SalePrice, and return (X, y).
    Expects the raw train DataFrame (with SalePrice column).
    """
    df = df.copy()

    if "Id" in df.columns:
        df = df.drop("Id", axis=1)

    y = np.log1p(df["SalePrice"])
    X = df.drop("SalePrice", axis=1)

    return X, y


def build_preprocessor(X):
    """
    Build a ColumnTransformer for *X* (features only — no Id, no SalePrice).

    Numeric features  → median imputation → standard scaling
    Categorical features → 'None' imputation → one-hot encoding
    """
    X = X.copy()

    numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="None")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )

    return preprocessor
