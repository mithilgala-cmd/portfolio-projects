import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer


def load_data(path):
    return pd.read_csv(path)


def split_features_target(df):
    df = df.copy()

    if "Id" in df.columns:
        df = df.drop("Id", axis=1)

    y = np.log1p(df["SalePrice"])
    X = df.drop("SalePrice", axis=1)

    return X, y


def build_preprocessor(df):
    df = df.copy()

    if "Id" in df.columns:
        df = df.drop("Id", axis=1)

    numeric_features = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = df.select_dtypes(include=["object"]).columns.tolist()

    if "SalePrice" in numeric_features:
        numeric_features.remove("SalePrice")

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="None")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )

    return preprocessor
