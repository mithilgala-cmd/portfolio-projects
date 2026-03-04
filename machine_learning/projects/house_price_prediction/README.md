
# House Price Prediction

An end-to-end machine learning project that predicts residential property prices using structured tabular housing data.
This repository demonstrates a complete regression pipeline including exploratory data analysis, preprocessing,
model training, evaluation, and prediction generation.

Repository Owner:
https://github.com/mithilgala-cmd

---

## Project Motivation

Accurate property valuation is important for buyers, sellers, investors, and real-estate platforms.
This project builds a machine learning system capable of estimating house prices using historical housing data and property attributes.

The project focuses on building a clean and reproducible ML pipeline that can be easily extended for experimentation or deployment.

---

## Key Features

- End-to-end machine learning workflow
- Automated preprocessing pipeline
- Handling missing values and categorical features
- Feature engineering and transformations
- Multiple regression model training
- Cross-validation for reliable evaluation
- Model performance comparison
- Model persistence for inference
- Prediction generation for unseen data

---

## Machine Learning Workflow

### 1. Data Collection

The dataset contains structured housing information including:

- Lot size
- Building type
- Construction year
- Neighborhood
- Number of rooms
- Garage information
- Property condition
- Additional amenities

Target variable:

SalePrice — the final sale price of the property.

---

### 2. Exploratory Data Analysis (EDA)

Initial analysis is performed in:

notebooks/eda.ipynb

This includes:

- Dataset overview
- Missing value analysis
- Feature distribution plots
- Correlation heatmap
- Relationship between features and price

---

### 3. Data Preprocessing

The preprocessing pipeline handles:

Numerical Features
- Median imputation
- Standard scaling

Categorical Features
- Missing value handling
- One-hot encoding

Target Variable
- Log transformation applied to reduce skewness

The preprocessing pipeline is implemented using:

- sklearn ColumnTransformer
- sklearn Pipeline

This guarantees consistent transformations during both training and prediction.

---

## Models Implemented

Linear Regression
Baseline regression model used to establish initial performance.

Random Forest Regressor
Ensemble learning model that improves prediction accuracy by combining multiple decision trees.

Future models that can be added:

- Gradient Boosting
- XGBoost
- LightGBM

---

## Model Evaluation Metrics

The models are evaluated using:

MAE (Mean Absolute Error)
Average difference between predicted and actual prices.

RMSE (Root Mean Squared Error)
Penalizes large prediction errors.

R² Score
Measures how well the model explains variance in house prices.

---

## Project Structure

house_price_prediction/

data/
    train.csv
    test.csv

logs/
    training.log

models/
    best_model.pkl
    training_metrics.json

notebooks/
    eda.ipynb

src/
    data_preprocessing.py
    train.py
    predict.py

config.yml
requirements.txt
README.md

---

## Installation

Clone the repository

git clone https://github.com/mithilgala-cmd/portfolio-projects.git

Navigate to the project folder

cd portfolio-projects/machine_learning/projects/house_price_prediction

Install dependencies

pip install -r requirements.txt

---

## Training the Model

Run the training script

python src/train.py

This will:

- preprocess the dataset
- train regression models
- evaluate performance
- select the best model
- save the trained model

Training logs are saved in logs/training.log

---

## Generating Predictions

Run the prediction script

python src/predict.py

This will:

- load the trained model
- generate predictions on the test dataset
- save predictions as submission.csv

---

## Configuration

Model and training parameters are stored in config.yml

Example:

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

---

## Technologies Used

Python  
NumPy  
Pandas  
Scikit-Learn  
Matplotlib  
Seaborn  
Jupyter Notebook  

---

## Future Improvements

- Hyperparameter tuning
- Feature importance visualization
- Gradient boosting models
- Automated evaluation reports
- API deployment with FastAPI
- Docker containerization

---

## Author

Mithil Gala

GitHub:
https://github.com/mithilgala-cmd

---

## License

This project is intended for educational and portfolio purposes.
