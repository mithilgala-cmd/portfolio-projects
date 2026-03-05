# Machine Learning Projects

End-to-end ML projects covering the full pipeline — data ingestion, preprocessing, model training, evaluation, and inference.

---

## Projects

| # | Project | Type | Model(s) | Dataset | Status |
|---|---------|------|----------|---------|--------|
| 1 | [House Price Prediction](house_price_prediction/) | Regression | Linear Regression, Random Forest | Kaggle House Prices | ✅ Complete |

---

## Structure

Each project follows this layout:

```
project_name/
├── data/           # raw datasets (not tracked)
├── logs/           # training logs (not tracked)
├── models/         # saved models and outputs (not tracked)
├── notebooks/      # EDA and experimentation
├── src/            # training and inference scripts
│   ├── data_preprocessing.py
│   ├── train.py
│   └── predict.py
├── config.yml
├── requirements.txt
└── README.md
```

---

## Running any project

```bash
pip install -r requirements.txt
python src/train.py
python src/predict.py
```
