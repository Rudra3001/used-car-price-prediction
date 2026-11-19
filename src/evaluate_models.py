"""
Model Evaluation Module for Used Car Price Prediction
Evaluates all trained models on test set, computes MAE, MSE, RMSE, R2,
saves results/model_comparison.csv, identifies and serializes best_model.pkl,
and generates the 5 visual evaluation graphs in graphs/.
"""

import os
import sys
import shutil
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data_preprocessing import get_train_test_data

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
GRAPHS_DIR = os.path.join(os.path.dirname(__file__), "..", "graphs")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def evaluate_all_models():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(GRAPHS_DIR, exist_ok=True)

    print("Loading test dataset for evaluation...")
    data = get_train_test_data()
    X_test = data["X_test"]
    y_test = data["y_test"]

    model_files = {
        "Linear Regression": "linear_regression.pkl",
        "Decision Tree": "decision_tree.pkl",
        "Random Forest": "random_forest.pkl",
        "Gradient Boosting": "gradient_boosting.pkl"
    }

    if os.path.exists(os.path.join(MODELS_DIR, "xgboost.pkl")):
        model_files["XGBoost"] = "xgboost.pkl"

    evaluation_results = []
    predictions_dict = {}

    for name, filename in model_files.items():
        filepath = os.path.join(MODELS_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Warning: Model file {filepath} not found. Skipping.")
            continue

        model = joblib.load(filepath)
        y_pred = model.predict(X_test)
        predictions_dict[name] = y_pred

        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        evaluation_results.append({
            "Model": name,
            "MAE": round(mae, 2),
            "MSE": round(mse, 2),
            "RMSE": round(rmse, 2),
            "R2_Score": round(r2, 4)
        })

    results_df = pd.DataFrame(evaluation_results)
    results_df = results_df.sort_values(by="R2_Score", ascending=False).reset_index(drop=True)

    # Save to results/model_comparison.csv
    csv_path = os.path.join(RESULTS_DIR, "model_comparison.csv")
    results_df.to_csv(csv_path, index=False)
    print("\n=======================================================")
    print("               MODEL COMPARISON TABLE                  ")
    print("=======================================================")
    print(results_df.to_string(index=False))
    print("=======================================================")
    print(f"Comparison results saved to: {csv_path}")

    # Determine best model
    best_model_name = results_df.iloc[0]["Model"]
    best_r2 = results_df.iloc[0]["R2_Score"]
    best_rmse = results_df.iloc[0]["RMSE"]
    best_filename = model_files[best_model_name]

    print(f"\nBest Performing Model: {best_model_name} (R2: {best_r2:.4f}, RMSE: ${best_rmse:,.2f})")
    src_best_path = os.path.join(MODELS_DIR, best_filename)
    dst_best_path = os.path.join(MODELS_DIR, "best_model.pkl")
    shutil.copyfile(src_best_path, dst_best_path)
    print(f"Serialized best model to: {dst_best_path}")

    # Generate visual evaluation plots
    generate_evaluation_plots(results_df, predictions_dict, y_test, best_model_name)

    return results_df, best_model_name


def generate_evaluation_plots(results_df, predictions_dict, y_test, best_model_name):
    best_preds = predictions_dict[best_model_name]
    residuals = y_test - best_preds

    # 1. Actual vs Predicted Price (Best Model)
    fig, ax = plt.subplots(figsize=(8.5, 6), dpi=150)
    ax.scatter(y_test, best_preds, alpha=0.45, color='#0284c7', edgecolors='none', s=28, label='Test Cars (2,000)')
    min_val = min(y_test.min(), best_preds.min())
    max_val = max(y_test.max(), best_preds.max())
    ax.plot([min_val, max_val], [min_val, max_val], color='#dc2626', linestyle='--', linewidth=2, label='Perfect Prediction (y = x)')
    ax.set_title(f"1. Actual vs Predicted Price - {best_model_name}", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Actual Price ($ USD)", fontsize=11, fontweight='semibold')
    ax.set_ylabel("Predicted Price ($ USD)", fontsize=11, fontweight='semibold')
    ax.legend(frameon=True, facecolor='#f8fafc')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, "eval_01_actual_vs_predicted.png"))
    plt.close()

    # 2. Residual Plot (Best Model)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=150)
    # Residuals vs Predicted
    ax1.scatter(best_preds, residuals, alpha=0.4, color='#7c3aed', s=25, edgecolors='none')
    ax1.axhline(0, color='#dc2626', linestyle='--', linewidth=1.8)
    ax1.set_title(f"Residuals vs Predicted Price ({best_model_name})", fontsize=12, fontweight='bold', pad=10)
    ax1.set_xlabel("Predicted Price ($ USD)", fontsize=10, fontweight='semibold')
    ax1.set_ylabel("Residuals ($ USD) [Actual - Pred]", fontsize=10, fontweight='semibold')
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Residual Distribution
    sns.histplot(residuals, kde=True, color='#06b6d4', bins=35, ax=ax2, edgecolor='#0891b2')
    ax2.axvline(residuals.mean(), color='#dc2626', linestyle='--', label=f'Mean Error: ${residuals.mean():.2f}')
    ax2.set_title(f"Residual Error Distribution ({best_model_name})", fontsize=12, fontweight='bold', pad=10)
    ax2.set_xlabel("Residual Error ($ USD)", fontsize=10, fontweight='semibold')
    ax2.set_ylabel("Frequency", fontsize=10, fontweight='semibold')
    ax2.legend(frameon=True)
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.suptitle("2. Residual Diagnostic Analysis", fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, "eval_02_residual_plot.png"))
    plt.close()

    # 3. Model MAE Comparison
    fig, ax = plt.subplots(figsize=(8.5, 5), dpi=150)
    mae_sorted = results_df.sort_values(by="MAE", ascending=True)
    bars = ax.bar(mae_sorted["Model"], mae_sorted["MAE"], color='#0284c7', edgecolor='#0369a1', width=0.55)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, h + 20, f'${h:,.1f}', ha='center', va='bottom', fontsize=9.5, fontweight='bold')
    ax.set_title("3. Model Mean Absolute Error (MAE) Comparison (Lower is Better)", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Regression Algorithm", fontsize=11, fontweight='semibold')
    ax.set_ylabel("MAE ($ USD)", fontsize=11, fontweight='semibold')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, "eval_03_mae_comparison.png"))
    plt.close()

    # 4. Model RMSE Comparison
    fig, ax = plt.subplots(figsize=(8.5, 5), dpi=150)
    rmse_sorted = results_df.sort_values(by="RMSE", ascending=True)
    bars = ax.bar(rmse_sorted["Model"], rmse_sorted["RMSE"], color='#059669', edgecolor='#047857', width=0.55)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, h + 30, f'${h:,.1f}', ha='center', va='bottom', fontsize=9.5, fontweight='bold')
    ax.set_title("4. Model Root Mean Squared Error (RMSE) Comparison (Lower is Better)", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Regression Algorithm", fontsize=11, fontweight='semibold')
    ax.set_ylabel("RMSE ($ USD)", fontsize=11, fontweight='semibold')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, "eval_04_rmse_comparison.png"))
    plt.close()

    # 5. Model R2 Score Comparison
    fig, ax = plt.subplots(figsize=(8.5, 5), dpi=150)
    r2_sorted = results_df.sort_values(by="R2_Score", ascending=False)
    bars = ax.bar(r2_sorted["Model"], r2_sorted["R2_Score"], color='#6366f1', edgecolor='#4338ca', width=0.55)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, h + 0.015, f'{h:.4f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.set_ylim(0, 1.1)
    ax.set_title("5. Model R² Score Comparison (Higher is Better)", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Regression Algorithm", fontsize=11, fontweight='semibold')
    ax.set_ylabel("R² Score", fontsize=11, fontweight='semibold')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, "eval_05_r2_comparison.png"))
    plt.close()

    print("All 5 evaluation visualizations generated and saved to graphs/.")


if __name__ == '__main__':
    evaluate_all_models()

