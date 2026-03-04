# Models

This folder stores trained model artefacts produced by `src/train.py`.

> ⚠️ All files in this folder are excluded from version control via `.gitignore`.

---

## Generated Files

| File | Description |
|------|-------------|
| `best_model.pkl` | The best-performing sklearn Pipeline (preprocessor + model), serialised with `joblib` |
| `training_metrics.json` | MAE, RMSE, R² and cross-validation scores for all trained models |
| `submission.csv` | Final predictions on `test.csv`, ready for Kaggle submission |

---

## How Models Are Selected

`train.py` trains all configured models, evaluates them on a held-out test split, and saves the one with the highest **R² score** as `best_model.pkl`.

---

## Loading the Model

```python
import joblib

model = joblib.load("models/best_model.pkl")
predictions = model.predict(X_test)
```
