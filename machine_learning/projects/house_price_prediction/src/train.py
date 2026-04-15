import json
import logging
import sys
from pathlib import Path

import joblib
import numpy as np
import yaml

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).parent.parent

sys.path.insert(0, str(Path(__file__).parent))
from data_preprocessing import build_preprocessor, load_data, split_features_target

log_dir = ROOT / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "training.log"),
        logging.StreamHandler(),
    ],
)


def evaluate(model, X_test, y_test):
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    return mae, rmse, r2


def main():

    config_path = ROOT / "config.yml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    data_path = ROOT / config["data"]["train_path"]
    test_size = config["training"]["test_size"]
    cv_folds = config["training"]["cv_folds"]
    rf_params = config["model"]["random_forest"]

    df = load_data(data_path)
    X, y = split_features_target(df)
    preprocessor = build_preprocessor(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    models = {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(
            n_estimators=rf_params["n_estimators"],
            random_state=rf_params["random_state"],
            n_jobs=-1,
        ),
    }

    best_model = None
    best_score = -np.inf
    best_name = None
    all_metrics = {}

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
        logging.info(f"  CV R²:  {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        logging.info(f"  MAE:    {mae:.4f}")
        logging.info(f"  RMSE:   {rmse:.4f}")
        logging.info(f"  R²:     {r2:.4f}")

        all_metrics[name] = {
            "cv_r2_mean": round(float(cv_scores.mean()), 4),
            "cv_r2_std": round(float(cv_scores.std()), 4),
            "mae": round(float(mae), 4),
            "rmse": round(float(rmse), 4),
            "r2": round(float(r2), 4),
        }

        if r2 > best_score:
            best_score = r2
            best_model = pipeline
            best_name = name

    models_dir = ROOT / "models"
    models_dir.mkdir(exist_ok=True)

    joblib.dump(best_model, models_dir / "best_model.pkl")

    metrics_output = {
        "best_model": best_name,
        "best_r2": round(float(best_score), 4),
        "all_models": all_metrics,
    }

    with open(models_dir / "training_metrics.json", "w") as f:
        json.dump(metrics_output, f, indent=4)

    logging.info(f"Best model: {best_name} (R²={best_score:.4f})")
    print(f"\nBest model: {best_name}  |  R² = {best_score:.4f}")


if __name__ == "__main__":
    main()
