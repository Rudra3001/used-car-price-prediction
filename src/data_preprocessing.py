"""
Data Preprocessing Module for Used Car Price Prediction
Author: Senior ML Engineer
Dataset: 10,000 records, 13 columns
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Paths
DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "Dataset", "used_cars.csv")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


def load_raw_data(filepath=DATASET_PATH):
    """
    Load raw CSV dataset.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found at {filepath}")
    df = pd.read_csv(filepath)
    return df


def inspect_data(df):
    """
    Perform thorough data inspection and return a diagnostic dictionary.
    """
    inspection_info = {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "numerical_summary": df.describe().to_dict()
    }
    return inspection_info


def clean_and_feature_engineer(df):
    """
    Clean dataset and create domain-specific engineered features.
    
    Derived Features:
      - car_age: 2024 - make_year (Age of vehicle)
      - accident_status: 1 if accidents_reported > 0 else 0 (Binary flag)
    
    Missing Value Handling:
      - service_history: fills missing entries with 'None'
    """
    df_clean = df.copy()

    # Fill missing service history with 'None'
    df_clean['service_history'] = df_clean['service_history'].fillna('None')

    # Feature Engineering
    # 1. Car age relative to 2026 (current reference year, 2006 to 2026)
    df_clean['car_age'] = 2026 - df_clean['make_year']

    # 2. Accident status binary indicator
    df_clean['accident_status'] = (df_clean['accidents_reported'] > 0).astype(int)

    return df_clean


def build_preprocessor(categorical_features, numerical_features):
    """
    Construct Scikit-Learn ColumnTransformer pipeline.
    Prevents data leakage by encapsulating encoders and scalers.
    """
    num_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    cat_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='None')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_pipeline, numerical_features),
            ('cat', cat_pipeline, categorical_features)
        ],
        remainder='drop'
    )
    return preprocessor


def get_train_test_data(filepath=DATASET_PATH, test_size=0.2, random_state=42):
    """
    Full preprocessing workflow:
    1. Loads dataset
    2. Cleans & engineers features
    3. Splits X, y using 80:20 ratio
    4. Fits preprocessing pipeline strictly on training data
    5. Transforms both train and test splits
    6. Saves fitted preprocessor pipeline to models/
    """
    df = load_raw_data(filepath)
    df_processed = clean_and_feature_engineer(df)

    # Features and Target
    target_col = 'price_usd'
    X = df_processed.drop(columns=[target_col])
    y = df_processed[target_col].values

    # Define categorical and numerical features
    categorical_features = [
        'brand', 'model', 'fuel_type', 'transmission', 
        'color', 'service_history', 'insurance_valid'
    ]
    numerical_features = [
        'make_year', 'mileage_kmpl', 'engine_cc', 
        'owner_count', 'accidents_reported', 
        'car_age', 'accident_status'
    ]

    # Split into train and test sets (80:20)
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Build and fit preprocessor ONLY on train data
    preprocessor = build_preprocessor(categorical_features, numerical_features)
    X_train = preprocessor.fit_transform(X_train_raw)
    X_test = preprocessor.transform(X_test_raw)

    # Extract feature names from fitted preprocessor
    cat_encoder = preprocessor.named_transformers_['cat'].named_steps['encoder']
    cat_feature_names = cat_encoder.get_feature_names_out(categorical_features).tolist()
    all_feature_names = numerical_features + cat_feature_names

    # Ensure models directory exists and save pipeline
    os.makedirs(MODELS_DIR, exist_ok=True)
    pipeline_path = os.path.join(MODELS_DIR, "preprocessing_pipeline.pkl")
    joblib.dump(preprocessor, pipeline_path)
    print(f"Preprocessing pipeline successfully saved to {pipeline_path}")

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "X_train_raw": X_train_raw,
        "X_test_raw": X_test_raw,
        "preprocessor": preprocessor,
        "feature_names": all_feature_names,
        "categorical_cols": categorical_features,
        "numerical_cols": numerical_features
    }


if __name__ == '__main__':
    print("Executing Data Preprocessing Step...")
    df = load_raw_data()
    print(f"Dataset Loaded. Shape: {df.shape}")
    
    info = inspect_data(df)
    print(f"Columns ({len(info['columns'])}): {info['columns']}")
    print(f"Missing Values: {info['missing_values']}")
    print(f"Duplicate records: {info['duplicates']}")

    data_dict = get_train_test_data()
    print(f"Train features shape: {data_dict['X_train'].shape}")
    print(f"Test features shape: {data_dict['X_test'].shape}")
    print(f"Total processed features: {len(data_dict['feature_names'])}")
    print("Preprocessing completed successfully.")

