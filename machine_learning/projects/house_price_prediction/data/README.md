# Data

This folder stores the raw datasets used for training and prediction.

**Files expected:**

| File | Description | Rows | Source |
|------|-------------|------|--------|
| `train.csv` | Labelled training data with `SalePrice` target | 1,460 | [Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques) |
| `test.csv` | Unlabelled test data for prediction | 1,459 | [Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques) |

> ⚠️ CSV files are excluded from version control via `.gitignore`.
> Download both files from Kaggle and place them here before running the scripts.

---

## Download via Kaggle CLI

```bash
kaggle competitions download -c house-prices-advanced-regression-techniques -p data/ --unzip
```
