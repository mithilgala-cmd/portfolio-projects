import os
import joblib
import numpy as np
import pandas as pd


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    model_path = os.path.join(base_dir, "../models/best_model.pkl")
    test_path = os.path.join(base_dir, "../data/test.csv")

    model = joblib.load(model_path)
    test_df = pd.read_csv(test_path)

    if "Id" in test_df.columns:
        ids = test_df["Id"]
    else:
        ids = None

    predictions = model.predict(test_df)
    predictions = np.expm1(predictions)

    output = pd.DataFrame({
        "Id": ids if ids is not None else range(len(predictions)),
        "SalePrice": predictions
    })

    output.to_csv(os.path.join(base_dir, "../models/submission.csv"), index=False)
    print("Predictions saved successfully.")


if __name__ == "__main__":
    main()