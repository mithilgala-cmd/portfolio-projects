import pandas as pd
import numpy as np


def load_data(path):
    df = pd.read_csv(path)
    return df


def preprocess_data(df):
    # Log transform target
    df["SalePrice"] = np.log1p(df["SalePrice"])

    # Drop high missing columns (>80%)
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    high_missing_cols = missing_percentage[missing_percentage > 80].index
    df = df.drop(columns=high_missing_cols)

    # Separate features and target
    X = df.drop("SalePrice", axis=1)
    y = df["SalePrice"]

    # Separate numerical and categorical
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns
    cat_cols = X.select_dtypes(include=["object"]).columns

    # Fill numerical missing with median
    X[num_cols] = X[num_cols].fillna(X[num_cols].median())

    # Fill categorical missing with "None"
    X[cat_cols] = X[cat_cols].fillna("None")

    # One-hot encode categorical variables
    X = pd.get_dummies(X, drop_first=True)

    return X, y