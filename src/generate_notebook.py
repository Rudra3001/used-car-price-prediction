"""
Generates the comprehensive eda_and_model_training.ipynb notebook.
"""

import json
import os

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Used Car Price Prediction Using Machine Learning Regression Algorithms\n",
                "**Project Number:** 4  \n",
                "**Domain:** Artificial Intelligence and Machine Learning  \n",
                "**Learning Type:** Supervised Learning  \n",
                "**Problem Type:** Regression  \n",
                "\n",
                "---\n",
                "## 1. Project Overview\n",
                "This project demonstrates the complete end-to-end machine learning lifecycle for predicting the market selling price (in USD) of used automobiles. The system leverages specifications, vehicle condition, ownership counts, and service history across 10,000 vehicle records and 13 features.\n",
                "\n",
                "Four regression algorithms are analyzed and compared:\n",
                "1. **Linear Regression** (Baseline Ordinary Least Squares)\n",
                "2. **Decision Tree Regressor** (Recursive variance reduction)\n",
                "3. **Random Forest Regressor** (Ensemble bootstrap bagging)\n",
                "4. **Gradient Boosting Regressor** (Sequential pseudo-residual boosting)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Environment Setup and Data Ingestion"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "import numpy as np\n",
                "import pandas as pd\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "from sklearn.model_selection import train_test_split\n",
                "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n",
                "from sklearn.compose import ColumnTransformer\n",
                "from sklearn.pipeline import Pipeline\n",
                "from sklearn.impute import SimpleImputer\n",
                "from sklearn.linear_model import LinearRegression\n",
                "from sklearn.tree import DecisionTreeRegressor\n",
                "from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor\n",
                "from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score\n",
                "import joblib\n",
                "\n",
                "# Styling\n",
                "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
                "plt.rcParams['font.sans-serif'] = 'DejaVu Sans'\n",
                "print('All libraries imported successfully.')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Load Dataset\n",
                "data_path = os.path.join('..', 'Dataset', 'used_cars.csv')\n",
                "df = pd.read_csv(data_path)\n",
                "print(f'Dataset Shape: {df.shape[0]} rows x {df.shape[1]} columns')\n",
                "print('\\nFirst 5 Records:')\n",
                "display(df.head(5))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Data Inspection & Diagnostics"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print('--- Dataset Info ---')\n",
                "print(df.info())\n",
                "\n",
                "print('\\n--- Missing Value Count ---')\n",
                "print(df.isnull().sum())\n",
                "\n",
                "print(f'\\nDuplicate rows: {df.duplicated().sum()}')\n",
                "\n",
                "print('\\n--- Descriptive Summary ---')\n",
                "display(df.describe())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Exploratory Data Analysis (EDA)\n",
                "Analyzing target distributions, feature frequencies, and relationships with car valuation."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
                "sns.histplot(df['price_usd'], kde=True, color='#0284c7', bins=35, ax=axes[0])\n",
                "axes[0].set_title('Used Car Selling Price Distribution ($ USD)', fontsize=12, fontweight='bold')\n",
                "axes[0].set_xlabel('Price ($ USD)')\n",
                "\n",
                "sns.boxplot(x='make_year', y='price_usd', data=df, palette='Blues', ax=axes[1])\n",
                "axes[1].set_title('Price Trend vs Manufacturing Year (Depreciation Curve)', fontsize=12, fontweight='bold')\n",
                "axes[1].set_xlabel('Manufacturing Year')\n",
                "axes[1].set_ylabel('Selling Price ($ USD)')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
                "brand_avg = df.groupby('brand')['price_usd'].mean().sort_values(ascending=False)\n",
                "sns.barplot(x=brand_avg.index, y=brand_avg.values, palette='crest', ax=axes[0])\n",
                "axes[0].set_title('Average Selling Price by Brand', fontsize=12, fontweight='bold')\n",
                "axes[0].tick_params(axis='x', rotation=35)\n",
                "axes[0].set_ylabel('Mean Price ($ USD)')\n",
                "\n",
                "fuel_avg = df.groupby('fuel_type')['price_usd'].mean().sort_values(ascending=False)\n",
                "sns.barplot(x=fuel_avg.index, y=fuel_avg.values, palette='viridis', ax=axes[1])\n",
                "axes[1].set_title('Average Selling Price by Fuel Type', fontsize=12, fontweight='bold')\n",
                "axes[1].set_ylabel('Mean Price ($ USD)')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "plt.figure(figsize=(9, 6))\n",
                "num_cols = ['make_year', 'mileage_kmpl', 'engine_cc', 'owner_count', 'accidents_reported', 'price_usd']\n",
                "sns.heatmap(df[num_cols].corr(), annot=True, fmt='.2f', cmap='Blues', linewidths=0.5)\n",
                "plt.title('Correlation Heatmap of Numerical Features', fontsize=13, fontweight='bold')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Feature Engineering & Preprocessing Pipeline\n",
                "Derived Features:\n",
                "- `car_age = 2024 - make_year` (vehicle age in years)\n",
                "- `accident_status = (accidents_reported > 0).astype(int)` (binary accident indicator)\n",
                "\n",
                "Pipeline Construction:\n",
                "- Numerical features scaled using `StandardScaler`\n",
                "- Categorical features encoded using `OneHotEncoder(handle_unknown='ignore')`\n",
                "- Strict 80:20 train-test split (`random_state=42`) with preprocessor fit strictly on training set to prevent data leakage."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Feature Engineering\n",
                "df_proc = df.copy()\n",
                "df_proc['service_history'] = df_proc['service_history'].fillna('None')\n",
                "df_proc['car_age'] = 2024 - df_proc['make_year']\n",
                "df_proc['accident_status'] = (df_proc['accidents_reported'] > 0).astype(int)\n",
                "\n",
                "X = df_proc.drop(columns=['price_usd'])\n",
                "y = df_proc['price_usd'].values\n",
                "\n",
                "categorical_cols = ['brand', 'model', 'fuel_type', 'transmission', 'color', 'service_history', 'insurance_valid']\n",
                "numerical_cols = ['make_year', 'mileage_kmpl', 'engine_cc', 'owner_count', 'accidents_reported', 'car_age', 'accident_status']\n",
                "\n",
                "X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n",
                "\n",
                "preprocessor = ColumnTransformer(\n",
                "    transformers=[\n",
                "        ('num', Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]), numerical_cols),\n",
                "        ('cat', Pipeline([('imputer', SimpleImputer(strategy='constant', fill_value='None')), ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]), categorical_cols)\n",
                "    ]\n",
                ")\n",
                "\n",
                "X_train = preprocessor.fit_transform(X_train_raw)\n",
                "X_test = preprocessor.transform(X_test_raw)\n",
                "print(f'Transformed Training Matrix Shape: {X_train.shape}')\n",
                "print(f'Transformed Testing Matrix Shape: {X_test.shape}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Model Training and Comparison\n",
                "We train four distinct regression algorithms and evaluate them across MAE, MSE, RMSE, and R2."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "models = {\n",
                "    'Linear Regression': LinearRegression(),\n",
                "    'Decision Tree': DecisionTreeRegressor(random_state=42, max_depth=12),\n",
                "    'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=16, random_state=42, n_jobs=-1),\n",
                "    'Gradient Boosting': GradientBoostingRegressor(n_estimators=150, learning_rate=0.1, max_depth=5, random_state=42)\n",
                "}\n",
                "\n",
                "evaluation_metrics = []\n",
                "predictions = {}\n",
                "\n",
                "for name, model in models.items():\n",
                "    model.fit(X_train, y_train)\n",
                "    preds = model.predict(X_test)\n",
                "    predictions[name] = preds\n",
                "    \n",
                "    mae = mean_absolute_error(y_test, preds)\n",
                "    mse = mean_squared_error(y_test, preds)\n",
                "    rmse = np.sqrt(mse)\n",
                "    r2 = r2_score(y_test, preds)\n",
                "    \n",
                "    evaluation_metrics.append({\n",
                "        'Model': name,\n",
                "        'MAE ($)': round(mae, 2),\n",
                "        'MSE': round(mse, 2),\n",
                "        'RMSE ($)': round(rmse, 2),\n",
                "        'R2 Score': round(r2, 4)\n",
                "    })\n",
                "\n",
                "comp_df = pd.DataFrame(evaluation_metrics).sort_values(by='R2 Score', ascending=False).reset_index(drop=True)\n",
                "print('=== MODEL COMPARISON TABLE ===')\n",
                "display(comp_df)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7. Visual Evaluation & Residual Diagnostics"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "best_name = comp_df.iloc[0]['Model']\n",
                "best_preds = predictions[best_name]\n",
                "residuals = y_test - best_preds\n",
                "\n",
                "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
                "axes[0].scatter(y_test, best_preds, alpha=0.45, color='#0284c7', s=25)\n",
                "axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=2, label='Ideal Line (y=x)')\n",
                "axes[0].set_title(f'Actual vs Predicted Price ({best_name})', fontsize=12, fontweight='bold')\n",
                "axes[0].set_xlabel('Actual Price ($ USD)')\n",
                "axes[0].set_ylabel('Predicted Price ($ USD)')\n",
                "axes[0].legend()\n",
                "\n",
                "sns.histplot(residuals, kde=True, color='#059669', ax=axes[1], bins=35)\n",
                "axes[1].axvline(0, color='r', linestyle='--')\n",
                "axes[1].set_title(f'Residual Distribution ({best_name})', fontsize=12, fontweight='bold')\n",
                "axes[1].set_xlabel('Residual ($ USD)')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 8. Standalone Real-Time Inference Demonstration"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "sample_query = {\n",
                "    'brand': 'Hyundai',\n",
                "    'model': 'Creta',\n",
                "    'make_year': 2022,\n",
                "    'mileage_kmpl': 17.0,\n",
                "    'engine_cc': 1497,\n",
                "    'fuel_type': 'Petrol',\n",
                "    'transmission': 'Manual',\n",
                "    'color': 'White',\n",
                "    'owner_count': 1,\n",
                "    'service_history': 'Authorized Dealer',\n",
                "    'accidents_reported': 0,\n",
                "    'insurance_valid': 'Yes',\n",
                "    'car_age': 2024 - 2022,\n",
                "    'accident_status': 0\n",
                "}\n",
                "\n",
                "sample_df = pd.DataFrame([sample_query])\n",
                "sample_X = preprocessor.transform(sample_df)\n",
                "predicted_val = models[best_name].predict(sample_X)[0]\n",
                "\n",
                "print('=== SAMPLE INFERENCE RESULT ===')\n",
                "print(f'Vehicle: 2022 Hyundai Creta Petrol Manual')\n",
                "print(f'Estimated Market Valuation: ${predicted_val:,.2f} USD')\n",
                "print(f'Prediction Model Used: {best_name}')"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.11.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

output_path = os.path.join(os.path.dirname(__file__), "..", "notebooks", "eda_and_model_training.ipynb")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

print(f"Jupyter Notebook successfully created at {output_path}")

