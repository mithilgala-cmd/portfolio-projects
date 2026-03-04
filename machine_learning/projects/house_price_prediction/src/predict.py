from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import yaml

# ── Resolve project root regardless of where the script is run from ──────────
ROOT = Path(__file__).parent.parent


def main():

    config_path = ROOT / "config.yml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    model_path = ROOT / "models" / "best_model.pkl"
    test_path = ROOT / config["data"]["test_path"]

    if not test_path.exists():
        raise FileNotFoundError(
            f"Test dataset not found: {test_path}\n"
            "Place test.csv in the data/ folder."
        )

    if not model_path.exists():
        raise FileNotFoundError(
            f"Trained model not found: {model_path}\n"
            "Run train.py first to generate the model."
        )

    model = joblib.load(model_path)

    test_df = pd.read_csv(test_path)

    ids = test_df["Id"] if "Id" in test_df.columns else None

    # Drop Id column — the training pipeline was built without it
    if "Id" in test_df.columns:
        test_df = test_df.drop("Id", axis=1)

    predictions = model.predict(test_df)

    # Reverse the log1p transform applied during training
    predictions = np.expm1(predictions)

    output = pd.DataFrame(
        {
            "Id": ids if ids is not None else range(len(predictions)),
            "SalePrice": predictions,
        }
    )

    output_path = ROOT / "models" / "submission.csv"
    output.to_csv(output_path, index=False)

    print(f"✅ Predictions saved to {output_path}")


if __name__ == "__main__":
    main()
