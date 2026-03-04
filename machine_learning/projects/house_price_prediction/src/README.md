# Source Code

This folder contains all modular, production-ready Python scripts for the house price prediction pipeline.

---

## Scripts

| Script | Purpose |
|--------|---------|
| [`data_preprocessing.py`](data_preprocessing.py) | Loads data, splits features/target, builds sklearn `ColumnTransformer` pipeline |
| [`train.py`](train.py) | Trains multiple regression models, evaluates with cross-validation, saves the best model |
| [`predict.py`](predict.py) | Loads the saved model, runs inference on test data, writes `submission.csv` |

---

## Pipeline Flow

```
data/train.csv
      │
      ▼
data_preprocessing.py   ← load_data(), split_features_target(), build_preprocessor()
      │
      ▼
train.py                ← Pipeline(preprocessor + model), cross_val_score(), evaluate()
      │
      ▼
models/best_model.pkl   ← saved with joblib
      │
      ▼
predict.py              ← model.predict(test_df) → np.expm1() → submission.csv
```

---

## Running the Scripts

Always run from the **project root** (where `config.yml` lives):

```bash
# Train
python src/train.py

# Predict
python src/predict.py
```

> All file paths are resolved using `pathlib` relative to the project root — scripts work correctly regardless of the current working directory.
