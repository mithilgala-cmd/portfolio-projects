import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_data(path):
    if not path.exists():
        raise FileNotFoundError(
            f"Data file not found: {path}\n"
            "Make sure train.csv / test.csv are placed in the data/ folder."
        )
    return pd.read_csv(path)


def split_features_target(df):
    df = df.copy()

    if "Id" in df.columns:
        df = df.drop("Id", axis=1)

    # log-transform SalePrice to reduce skewness
    y = np.log1p(df["SalePrice"])
    X = df.drop("SalePrice", axis=1)

    return X, y


def build_preprocessor(X):
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
