# Machine Learning Projects

Each project in this folder is a complete, production-style ML pipeline — covering data ingestion, preprocessing, model training, evaluation, and inference.

---

## Projects

| # | Project | Domain | Algorithm(s) | Dataset | Status |
|---|---------|--------|--------------|---------|--------|
| 1 | [House Price Prediction](house_price_prediction/) | Regression | Linear Regression, Random Forest | Kaggle House Prices | ✅ Complete |

---

## Project Standards

Every project in this folder follows this structure:

```
project_name/
├── data/           # Raw datasets (not tracked by git)
├── logs/           # Training logs (not tracked by git)
├── models/         # Saved model files (not tracked by git)
├── notebooks/      # EDA and experimentation notebooks
├── src/            # Modular production-ready scripts
│   ├── data_preprocessing.py
│   ├── train.py
│   └── predict.py
├── config.yml      # Hyperparameters and paths
├── requirements.txt
└── README.md
```

---

## How to Run Any Project

```bash
# Install dependencies
pip install -r requirements.txt

# Train the model
python src/train.py

# Generate predictions
python src/predict.py
```
