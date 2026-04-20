# House Price Prediction

Regression pipeline for the Kaggle House Prices dataset.

The project covers:

- Data loading and preprocessing
- Feature transformation with `ColumnTransformer`
- Training and comparison of multiple regressors
- Exporting the best model
- Generating `submission.csv` predictions

## Structure

```text
house_price_prediction/
|-- src/
|   |-- data_preprocessing.py
|   |-- train.py
|   `-- predict.py
|-- config.yml
|-- requirements.txt
|-- notebooks/
|-- data/
`-- models/
```

## Setup

```bash
cd machine_learning/projects/house_price_prediction
pip install -r requirements.txt
```

Download Kaggle data and place files in `data/`:

- `train.csv`
- `test.csv`

## Run

Train and evaluate models:

```bash
python src/train.py
```

Generate predictions from saved model:

```bash
python src/predict.py
```

## Outputs

Generated under `models/`:

- `best_model.pkl`
- `training_metrics.json`
- `submission.csv`

## Notes

- `SalePrice` is log-transformed during training and inverted during prediction output.
- Generated artifacts are ignored in git.
