# Source Code

The main ML pipeline lives here — data loading, preprocessing, training, and inference are split into separate scripts to keep things clean.

---

## Scripts

| Script | What it does |
|--------|----|
| [`data_preprocessing.py`](data_preprocessing.py) | Loads the CSV, splits features and target, builds the sklearn preprocessing pipeline |
| [`train.py`](train.py) | Trains Linear Regression and Random Forest, runs cross-validation, saves the best model |
| [`predict.py`](predict.py) | Loads the saved model, runs inference on test data, writes `submission.csv` |

---

## Flow

```
data/train.csv
      │
      ▼
data_preprocessing.py   → load_data(), split_features_target(), build_preprocessor()
      │
      ▼
train.py                → Pipeline(preprocessor + model), cross_val_score(), evaluate()
      │
      ▼
models/best_model.pkl
      │
      ▼
predict.py              → model.predict() → np.expm1() → submission.csv
```

---

## Running

From the project root (where `config.yml` lives):

```bash
python src/train.py
python src/predict.py
```
