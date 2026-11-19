# CARPRICE AI — Used Car Valuation Studio (₹ INR)

An end-to-end Machine Learning system engineered for used automobile valuation in the Indian automotive market, featuring a leakage-free regression pipeline, sub-millisecond client-side telemetry, dual-mode deployment, and formal IEEE research publication documentation.

---

## 📌 Project Overview

- **Academic Institution:** Unitedworld Institute of Technology (UIT), Karnavati University
- **Project Investigators:**
  1. **Mankirat Singh Dhamoon** (`KU2507U0405`)
  2. **Baraiya Rudra R** (`KU2507U0720`)
  3. **Parv Hirenkumar Shah** (`2000016631`)
- **Domain:** Applied Machine Learning / Regression Telemetry
- **Dataset Size:** 10,000 verified automobile transaction records
- **Automobile Spectrum:** 10 major OEMs, 43 passenger models, 2006–2026 manufacturing lifespan
- **Target Currency:** Indian Rupees (₹ INR / Lakhs)
- **Top Model Performance:** Linear Regression achieves **R² = 0.9946** and **RMSE = ₹ 55,579**
- **Inference Latency:** < 0.4 ms in browser; dual deployment via Flask API and client-side JavaScript

---

## 📊 Comparative Model Evaluation

| Model Architecture | MAE (₹ INR) | RMSE (₹ INR) | R² Score | Model Footprint | Inference Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Linear Regression (Top Model)** | **₹ 38,910** | **₹ 55,579** | **0.9946 (99.46%)** | **1.8 KB** | **< 0.4 ms** |
| Gradient Boosting (GBDT) | ₹ 50,313 | ₹ 75,158 | 0.9900 (99.00%) | 702 KB | 4.2 ms |
| Random Forest (100 Trees) | ₹ 66,934 | ₹ 94,683 | 0.9842 (98.42%) | 18.8 MB | 14.8 ms |
| Decision Tree (CART) | ₹ 1,14,228 | ₹ 1,61,680 | 0.9539 (95.39%) | 96 KB | 0.8 ms |

---

## 🚀 Key Features

1. **Leakage-Free 80:20 Pipeline:** All scalers and encoders are fitted strictly on training data (`N = 8,000`) and applied to holdout test data (`N = 2,000`).
2. **Client-Side In-Browser Execution:** Model weights are serialized to a 4.1 KB JSON matrix, enabling zero-cloud-cost inference on static web servers.
3. **Bulk Fleet Valuation:** Drag-and-drop CSV parser evaluating 100+ vehicles simultaneously in browser memory with summary statistics.
4. **Regional Calibration:** Full Indian Rupee integration with ₹ Lakh and ₹ Crore formatting and a ₹ 1.25 Lakh scrap floor safeguard.

---

## 📁 Repository Structure

```
├── Dataset/                 # 10,000 verified automobile records (used_cars.csv)
├── graphs/                  # 19 EDA & model evaluation charts (.png)
├── models/                  # Serialized scikit-learn models & preprocessor (.pkl)
├── notebooks/               # Jupyter research notebook (eda_and_model_training.ipynb)
├── results/                 # Comparative model metrics (model_comparison.csv)
├── src/                     # Core Python pipeline scripts
├── static/                  # Web branding, styles, and logo assets
├── templates/               # Flask web interface template (index.html)
├── app.py                   # Production server entrypoint
├── server.py                # Flask production server (Port 7860)
├── index.html               # Standalone client-side web application
├── static_model_weights.json # Serialized weights for client-side regression
├── CARPRICE_AI_Research_Paper_Final.pdf  # 5-Page IEEE Conference Research Paper
├── CARPRICE_AI_Research_Paper.tex        # Overleaf / LaTeX IEEEtran Source Code
├── CARPRICE_AI_Research_Paper_Final.docx # Editable Microsoft Word Research Paper
├── CARPRICE_AI_Research_Presentation_Final.pptx # Academic research slide deck
├── PROJECT_REPORT.md        # Comprehensive technical & academic project report
├── requirements.txt         # Minimal production dependencies
└── .gitignore               # Clean git exclusions
```

---

## ⚡ Quick Start

### 1. Run Locally with Flask
```bash
pip install -r requirements.txt
python server.py
# or
python app.py
```
Open your browser at `http://localhost:7860`.

### 2. Standalone Static Web App
Open `index.html` directly in any web browser for instant client-side prediction without a Python server.

---

## 📑 Academic Documentation
- **Research Paper (Overleaf / IEEE Format):** `CARPRICE_AI_Research_Paper_Final.pdf`
- **Presentation Slides:** `CARPRICE_AI_Research_Presentation_Final.pptx`
- **Technical Report:** `PROJECT_REPORT.md`
- **Research Notebook:** `notebooks/eda_and_model_training.ipynb`
