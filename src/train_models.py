"""
Model Training Module for Used Car Price Prediction
Trains 4 core regression algorithms (Linear Regression, Decision Tree, Random Forest, Gradient Boosting)
Saves each trained model to the models/ directory.
"""

import os
import sys
import time
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data_preprocessing import get_train_test_data

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


def get_model_definitions():
    """
    Returns dictionary of regression algorithms with explanations of working principles.
    """
    models = {
        "Linear Regression": {
            "model": LinearRegression(),
            "filename": "linear_regression.pkl",
            "principle": "Models the linear relationship between features and target by minimizing the sum of squared residuals (OLS)."
        },
        "Decision Tree": {
            "model": DecisionTreeRegressor(random_state=42, max_depth=12, min_samples_split=6),
            "filename": "decision_tree.pkl",
            "principle": "Partitions feature space recursively based on variance reduction (MSE) to make piecewise constant predictions."
        },
        "Random Forest": {
            "model": RandomForestRegressor(n_estimators=100, max_depth=16, min_samples_split=4, random_state=42, n_jobs=-1),
            "filename": "random_forest.pkl",
            "principle": "Ensemble bagging method constructing multiple de-correlated decision trees with bootstrap aggregation to reduce variance."
        },
        "Gradient Boosting": {
            "model": GradientBoostingRegressor(n_estimators=150, learning_rate=0.1, max_depth=5, random_state=42),
            "filename": "gradient_boosting.pkl",
            "principle": "Ensemble boosting technique sequentially fitting shallow trees to the pseudo-residuals of the previous models via gradient descent."
        }
    }

    # Optional XGBoost Regressor check
    try:
        import xgboost as xgb
        models["XGBoost"] = {
            "model": xgb.XGBRegressor(n_estimators=150, learning_rate=0.1, max_depth=5, random_state=42, n_jobs=-1),
            "filename": "xgboost.pkl",
            "principle": "Highly optimized scalable gradient boosting framework utilizing second-order Taylor approximations and regularized objective functions."
        }
    except ImportError:
        pass

    return models


def train_and_save_all_models():
    os.makedirs(MODELS_DIR, exist_ok=True)
    print("Loading preprocessed training and test data...")
    data = get_train_test_data()
    X_train = data["X_train"]
    y_train = data["y_train"]

    print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
    models_dict = get_model_definitions()

    trained_models = {}

    for name, info in models_dict.items():
        print(f"\n==========================================")
        print(f"Training: {name}")
        print(f"Working Principle: {info['principle']}")
        print(f"==========================================")

        start_time = time.time()
        clf = info["model"]
        clf.fit(X_train, y_train)
        elapsed = time.time() - start_time

        save_path = os.path.join(MODELS_DIR, info["filename"])
        joblib.dump(clf, save_path)
        print(f"Training completed in {elapsed:.2f}s. Saved to: {save_path}")
        trained_models[name] = clf

    print("\nAll models successfully trained and serialized.")
    return trained_models


if __name__ == '__main__':
    train_and_save_all_models()

