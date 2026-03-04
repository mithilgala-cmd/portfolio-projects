import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from data_preprocessing import load_data, build_preprocessor, split_features_target


def evaluate(model, X_test, y_test):
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    return mae, rmse, r2


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "../data/train.csv")

    df = load_data(data_path)
    X, y = split_features_target(df)

    preprocessor = build_preprocessor(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(
            n_estimators=300,
            random_state=42,
            n_jobs=-1
        ),
    }

    best_model = None
    best_score = -np.inf
    best_name = None

    for name, model in models.items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model),
            ]
        )

        cv_scores = cross_val_score(
            pipeline, X_train, y_train, cv=5, scoring="r2"
        )

        pipeline.fit(X_train, y_train)
        mae, rmse, r2 = evaluate(pipeline, X_test, y_test)

        print("=" * 50)
        print(f"Model: {name}")
        print(f"CV R2: {cv_scores.mean():.4f}")
        print(f"MAE: {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"R2: {r2:.4f}")
        print("=" * 50)

        if r2 > best_score:
            best_score = r2
            best_model = pipeline
            best_name = name

    os.makedirs(os.path.join(base_dir, "../models"), exist_ok=True)
    joblib.dump(best_model, os.path.join(base_dir, "../models/best_model.pkl"))

    print(f"Best Model: {best_name} saved successfully.")


if __name__ == "__main__":
    main()