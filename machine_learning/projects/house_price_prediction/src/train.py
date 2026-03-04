import os
import yaml
import json
import logging
import joblib
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from data_preprocessing import load_data, build_preprocessor, split_features_target


logging.basicConfig(
    filename="../logs/training.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def evaluate(model, X_test, y_test):
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    return mae, rmse, r2


def main():

    with open("../config.yaml", "r") as f:
        config = yaml.safe_load(f)

    data_path = config["data"]["train_path"]
    test_size = config["training"]["test_size"]
    cv_folds = config["training"]["cv_folds"]
    rf_params = config["model"]["random_forest"]

    df = load_data(data_path)

    X, y = split_features_target(df)
    preprocessor = build_preprocessor(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    models = {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(
            n_estimators=rf_params["n_estimators"],
            random_state=rf_params["random_state"],
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
            pipeline, X_train, y_train, cv=cv_folds, scoring="r2"
        )

        pipeline.fit(X_train, y_train)

        mae, rmse, r2 = evaluate(pipeline, X_test, y_test)

        logging.info(f"Model: {name}")
        logging.info(f"CV R2: {cv_scores.mean():.4f}")
        logging.info(f"MAE: {mae:.4f}")
        logging.info(f"RMSE: {rmse:.4f}")
        logging.info(f"R2: {r2:.4f}")

        if r2 > best_score:
            best_score = r2
            best_model = pipeline
            best_name = name

    os.makedirs("../models", exist_ok=True)

    joblib.dump(best_model, "../models/best_model.pkl")

    metrics = {
        "model": best_name,
        "r2_score": float(best_score)
    }

    with open("../models/training_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    print(f"Best Model: {best_name}")


if __name__ == "__main__":
    main()
