# House Price Prediction

A regression project built on the Kaggle House Prices dataset. The goal was to predict residential property sale prices using structured tabular data — covering the full ML workflow from EDA to model deployment.

**Author:** [Mithil Gala](https://github.com/mithilgala-cmd) &nbsp;|&nbsp; **Dataset:** [Kaggle House Prices](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)

---

## Results

| Model | CV R² | MAE | RMSE | Test R² |
|-------|------:|----:|-----:|--------:|
| **Linear Regression** | 0.8277 ± 0.032 | 0.0904 | 0.1321 | **0.9064** |
| Random Forest | 0.8607 ± 0.030 | 0.0978 | 0.1454 | 0.8867 |

> Metrics are on log-transformed `SalePrice`. Linear Regression came out as the best model on the test set despite Random Forest having a higher CV score.

---

## Project Structure

```
house_price_prediction/
├── src/
│   ├── data_preprocessing.py   # data loading, feature/target split, preprocessing pipeline
│   ├── train.py                # model training, cross-validation, and evaluation
│   └── predict.py              # inference on test data
│
├── notebooks/
│   └── eda.ipynb               # exploratory data analysis
│
├── config.yml                  # paths and hyperparameters
├── requirements.txt
└── README.md
```

> Data files (`data/`), logs (`logs/`), and generated model files (`models/`) are excluded from version control.

---

## How it Works

### Data

The dataset has 79 features covering things like lot size, neighbourhood, number of rooms, garage, and construction year. `SalePrice` is log-transformed before training to handle the right skew.

### Preprocessing

Used `sklearn`'s `ColumnTransformer` inside a `Pipeline` so the same transforms apply consistently to both train and test data:

| Feature Type | Imputation | Transform |
|---|---|---|
| Numeric | Median | StandardScaler |
| Categorical | `"None"` constant | OneHotEncoder |

### Models

Both models are wrapped in a full pipeline and evaluated with 5-fold cross-validation:

- **Linear Regression** — baseline
- **Random Forest** — 300 trees

---

## Setup

```bash
git clone https://github.com/mithilgala-cmd/portfolio-projects.git
cd portfolio-projects/machine_learning/projects/house_price_prediction
pip install -r requirements.txt
```

Download the dataset from Kaggle and put `train.csv` and `test.csv` in the `data/` folder:

```bash
kaggle competitions download -c house-prices-advanced-regression-techniques -p data/ --unzip
```

---

## Usage

```bash
python src/train.py
python src/predict.py
```

After training, the `models/` folder will contain:
- `best_model.pkl` — the saved pipeline
- `training_metrics.json` — evaluation results for both models
- `submission.csv` — predictions on the test set

---

## Config

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

## Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)

---

## What I'd improve next

- Hyperparameter tuning with `GridSearchCV` or Optuna
- Add XGBoost / LightGBM
- Feature importance plots
- Wrap the model in a simple FastAPI endpoint

---

## License

For educational and portfolio purposes. MIT License.
