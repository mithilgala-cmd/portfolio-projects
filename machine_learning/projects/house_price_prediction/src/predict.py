import os
import joblib
import numpy as np
import pandas as pd


def main():

    model_path = "../models/best_model.pkl"
    test_path = "../data/test.csv"

    if not os.path.exists(test_path):
        raise FileNotFoundError("Test dataset not found")

    model = joblib.load(model_path)

    test_df = pd.read_csv(test_path)

    ids = test_df["Id"] if "Id" in test_df.columns else None

    predictions = model.predict(test_df)

    predictions = np.expm1(predictions)

    output = pd.DataFrame({
        "Id": ids if ids is not None else range(len(predictions)),
        "SalePrice": predictions
    })

    output.to_csv("../models/submission.csv", index=False)

    print("Predictions saved")


if __name__ == "__main__":
    main()
