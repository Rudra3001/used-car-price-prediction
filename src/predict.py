"""
Prediction Module for Used Car Price Prediction
Provides standalone inference utility using serialized preprocessing pipeline and best model.
Outputs in Indian Rupees (₹ INR) and USD.
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np

# Ensure UTF-8 console output on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
PREPROCESSOR_PATH = os.path.join(MODELS_DIR, "preprocessing_pipeline.pkl")
MODEL_PATH = os.path.join(MODELS_DIR, "best_model.pkl")

# Fixed conversion rate: 1 USD = 83.5 INR
USD_TO_INR = 83.5


class CarPricePredictor:
    def __init__(self, preprocessor_path=PREPROCESSOR_PATH, model_path=MODEL_PATH):
        if not os.path.exists(preprocessor_path):
            raise FileNotFoundError(f"Preprocessor not found at {preprocessor_path}. Run training first.")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}. Run training first.")

        self.preprocessor = joblib.load(preprocessor_path)
        self.model = joblib.load(model_path)

    def prepare_input(self, car_dict):
        """
        Accepts dictionary of 12 original features, derives car_age and accident_status.
        """
        df = pd.DataFrame([car_dict])

        # Fill missing service history with 'None' if missing
        if 'service_history' not in df.columns or pd.isna(df['service_history'].iloc[0]):
            df['service_history'] = 'None'

        # Feature engineering matching training logic (current reference year 2026, span 2006-2026)
        df['car_age'] = 2026 - int(df['make_year'].iloc[0])
        df['accident_status'] = 1 if int(df['accidents_reported'].iloc[0]) > 0 else 0

        # Transform using fitted preprocessor
        X_transformed = self.preprocessor.transform(df)
        return X_transformed

    def predict(self, car_dict):
        """
        Predict selling price in USD.
        """
        X_feat = self.prepare_input(car_dict)
        pred_usd = self.model.predict(X_feat)[0]
        # Ensure realistic minimum price floor ($1,500)
        pred_usd = max(1500.0, float(pred_usd))
        return round(pred_usd, 2)

    def predict_inr(self, car_dict):
        """
        Predict selling price in Indian Rupees (₹ INR).
        """
        usd_price = self.predict(car_dict)
        inr_price = usd_price * USD_TO_INR
        return round(inr_price, 2)

    def format_inr(self, inr_val):
        """
        Format value into Indian Lakhs / Crores string.
        """
        if inr_val >= 10000000:
            return f"₹ {inr_val/10000000:.2f} Cr"
        elif inr_val >= 100000:
            return f"₹ {inr_val/100000:.2f} Lakh"
        return f"₹ {inr_val:,.0f}"


def predict_price(car_dict):
    predictor = CarPricePredictor()
    return predictor.predict(car_dict)


def predict_price_inr(car_dict):
    predictor = CarPricePredictor()
    return predictor.predict_inr(car_dict)


if __name__ == '__main__':
    # Sample Test Car: 2020 Kia Seltos Petrol Automatic
    sample_car = {
        "brand": "Kia",
        "model": "Seltos",
        "make_year": 2020,
        "mileage_kmpl": 16.5,
        "engine_cc": 1497,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "color": "Silver",
        "owner_count": 1,
        "service_history": "Authorized Dealer",
        "accidents_reported": 0,
        "insurance_valid": "Yes"
    }

    predictor = CarPricePredictor()
    est_price_usd = predictor.predict(sample_car)
    est_price_inr = predictor.predict_inr(sample_car)
    formatted_inr = predictor.format_inr(est_price_inr)

    print("==========================================")
    print("   CAR PRICE INFERENCE TEST (INR)         ")
    print("==========================================")
    for k, v in sample_car.items():
        print(f"  {k:20}: {v}")
    print("------------------------------------------")
    try:
        print(f"  Predicted Price (INR): {formatted_inr} (Rs. {est_price_inr:,.0f})")
    except UnicodeEncodeError:
        print(f"  Predicted Price (INR): Rs. {est_price_inr:,.0f}")
    print(f"  Equivalent (USD)     : ${est_price_usd:,.2f}")
    print("==========================================")
