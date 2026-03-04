# House Price Prediction

An end-to-end machine learning project that predicts residential property prices using structured tabular housing data.
Demonstrates a complete regression pipeline — EDA, preprocessing, model training, cross-validation, evaluation, and inference.

**Author:** [Mithil Gala](https://github.com/mithilgala-cmd) &nbsp;|&nbsp; **Dataset:** [Kaggle House Prices](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)

---

## Results

| Model | CV R² | MAE | RMSE | Test R² |
|-------|------:|----:|-----:|--------:|
| **Linear Regression** ✅ | 0.8277 ± 0.032 | 0.0904 | 0.1321 | **0.9064** |
| Random Forest | 0.8607 ± 0.030 | 0.0978 | 0.1454 | 0.8867 |

> Metrics are on log-transformed `SalePrice`. Linear Regression was selected as the best model.

---

## Project Structure

```text
house_price_prediction/
├── src/                        # ⭐️ Production-ready ML pipeline
│   ├── data_preprocessing.py   # Clean, modular sklearn transformers
│   ├── train.py                # Cross-validation & model selection
│   └── predict.py              # Inference & submission generation
│
├── notebooks/                  
│   └── eda.ipynb               # ⭐️ In-depth Exploratory Data Analysis
│
├── config.yml                  # Model hyperparameters and pipeline config
├── requirements.txt            # Pinned dependencies
└── README.md
```

> ℹ️ **Note for Reviewers:** Data files (`data/`), runtime logs (`logs/`), and generated model files (`models/`) are intentionally excluded from version control to maintain a clean repository.

---

## Machine Learning Workflow

### 1. Data

The Kaggle House Prices dataset contains 79 features describing residential properties:
- Lot size, building type, construction year, neighbourhood
- Number of rooms, garage, basement, and amenity information

**Target:** `SalePrice` — log-transformed during training to reduce skewness.

### 2. Preprocessing

Built using `sklearn` `Pipeline` and `ColumnTransformer` for consistent train/test transforms:

| Feature Type | Imputation | Encoding |
|---|---|---|
| Numeric | Median | StandardScaler |
| Categorical | `"None"` constant | OneHotEncoder (ignore unknown) |

### 3. Models

| Model | Notes |
|-------|-------|
| Linear Regression | Baseline |
| Random Forest Regressor | 300 trees, all cores |

Each model is wrapped in a full `Pipeline(preprocessor + model)` and evaluated with 5-fold cross-validation.

### 4. Evaluation Metrics

| Metric | Description |
|--------|-------------|
| **MAE** | Average absolute error in log-price space |
| **RMSE** | Penalises large prediction errors |
| **R²** | Proportion of variance explained (higher = better) |

---

## Installation

```bash
# Clone the repository
git clone https://github.com/mithilgala-cmd/portfolio-projects.git

# Navigate to the project folder
cd portfolio-projects/machine_learning/projects/house_price_prediction

# Install dependencies
pip install -r requirements.txt
```

---

## Dataset Setup

Download the dataset from Kaggle and place files in `data/`:

```bash
kaggle competitions download -c house-prices-advanced-regression-techniques -p data/ --unzip
```

Or download manually from [kaggle.com/c/house-prices-advanced-regression-techniques/data](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data).

---

## Usage

```bash
# Train all models and save the best one
python src/train.py

# Generate predictions on the test set
python src/predict.py
```

Output files written to `models/`:

- `best_model.pkl` — serialised sklearn pipeline
- `training_metrics.json` — per-model evaluation results
- `submission.csv` — predictions ready for Kaggle submission

---

## Configuration

All paths and hyperparameters live in `config.yml`:

```yaml
data:
  train_path: data/train.csv
  test_path: data/test.csv

training:
  test_size: 0.2
  cv_folds: 5

model:
  random_forest:
    n_estimators: 300
    random_state: 42
```

---

## Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)

---

## Future Improvements

- [ ] Hyperparameter tuning with `GridSearchCV` or `Optuna`
- [ ] Feature importance visualisation
- [ ] Gradient Boosting / XGBoost / LightGBM models
- [ ] Automated evaluation reports (HTML or PDF)
- [ ] REST API deployment with FastAPI
- [ ] Docker containerisation

---

## License

This project is intended for educational and portfolio purposes. MIT License.
