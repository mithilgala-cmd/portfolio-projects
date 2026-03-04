# Notebooks

This folder contains Jupyter notebooks for exploratory analysis and experimentation.

---

## Notebooks

| Notebook | Purpose |
|----------|---------|
| [`eda.ipynb`](eda.ipynb) | Exploratory Data Analysis — distributions, missing values, correlations, and feature–price relationships |

---

## What EDA Covers

- **Dataset overview** — shape, dtypes, summary statistics
- **Missing value analysis** — heatmaps and counts per column
- **Target distribution** — raw vs log-transformed `SalePrice`
- **Feature distributions** — histograms for numeric features
- **Correlation heatmap** — identify features most correlated with price
- **Categorical analysis** — boxplots of key categorical features vs price

---

## Note

All production-ready logic (preprocessing, training, prediction) lives in `src/`.
Notebooks are for exploration only and are **not** part of the training pipeline.
