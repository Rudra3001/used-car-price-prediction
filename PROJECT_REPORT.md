# ACADEMIC PROJECT REPORT

## PROJECT TITLE: Used Car Price Prediction Using Machine Learning Regression Algorithms
**Project Number:** 4  
**Domain:** Artificial Intelligence and Machine Learning  
**Learning Paradigm:** Supervised Learning  
**Problem Type:** Regression  
**Academic Degree:** Bachelor of Technology (B.Tech) in Computer Science & Engineering / Artificial Intelligence  

---

## 1. ABSTRACT

The pre-owned automobile industry has evolved into a multi-billion-dollar global market. However, assessing the fair market valuation of used vehicles remains a notoriously complex task characterized by severe information asymmetry, volatile supply-demand dynamics, and intricate non-linear relationships among physical attributes, mechanical wear, and service records. This project presents **CARPRICE AI**, an end-to-end, data-driven machine learning system engineered to predict used car selling prices in United States Dollars (USD) based on comprehensive vehicle specifications, maintenance records, and condition indicators. 

Using an authenticated dataset of 10,000 automobile records spanning 10 leading global manufacturers and 43 distinct models, we implement a leakage-free machine learning pipeline with Scikit-Learn `ColumnTransformer` and standard 80:20 train-test partitioning. Four distinct supervised regression algorithms—Linear Regression (Ordinary Least Squares), Decision Tree Regressor, Random Forest Regressor, and Gradient Boosting Regressor—are trained, tuned, and rigorously evaluated across standard regression metrics: Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and the Coefficient of Determination ($R^2$). 

The experimental findings demonstrate that **Linear Regression** delivers the optimal predictive performance on the unseen test set, achieving an exceptional **$R^2$ of 0.9946**, an **RMSE of \$665.62**, and an **MAE of \$465.98**, proving that the combination of domain-specific feature engineering (`car_age`, `accident_status`) and one-hot encoding provides an exceptionally linear pricing mapping. The resulting best-performing model and its preprocessing pipeline were serialized and successfully deployed in an interactive Streamlit web dashboard featuring real-time inference, dynamic brand-to-model filtering, exploratory analytics with Plotly, and model performance auditing.

---

## 2. INTRODUCTION

The automotive sector is experiencing a historic transformation. Rapid urbanization, economic fluctuations, and rising costs of new vehicles have propelled consumer demand for reliable pre-owned cars. In developing and developed markets alike, pre-owned car sales volume consistently outpaces new vehicle registrations by a significant multiple.

Despite this high transaction volume, fair market pricing remains an opaque process. Traditional valuation approaches rely on static depreciation tables (e.g., standard straight-line depreciation per year) or subjective inspections conducted by local brokers and used car dealerships. Such methods are incapable of dynamically synthesizing the joint impact of multiple quantitative variables (e.g., engine displacement in cubic centimeters, cumulative odometer readings, fuel efficiency in km/litre) with categorical attributes (e.g., brand prestige, fuel type, transmission type, maintenance logs, accident frequency, and comprehensive insurance validity).

Machine Learning (ML), specifically supervised regression, provides an empirical framework to address this challenge. By training statistical learning models on historical transaction datasets, machine learning algorithms can uncover hidden patterns, weight individual features objectively, and generate unbiased valuation predictions with minimal error.

This project delivers a complete undergraduate capstone project demonstrating the entire engineering lifecycle:
1. Systematic dataset ingestion and statistical integrity verification.
2. Comprehensive exploratory data analysis (EDA) with 14 analytical graphs.
3. Domain-specific feature engineering and data leakage prevention.
4. Comparative experimentation across 4 regression algorithms.
5. In-depth residual analysis and performance benchmarking.
6. Full-stack deployment via a responsive Streamlit web dashboard.

---

## 3. PROBLEM STATEMENT

Used car valuation is characterized by market opacity, asymmetric information, and inconsistent pricing standards. 

Specifically:
- **Asymmetric Information:** Buyers often lack technical expertise to evaluate how past ownership counts, minor reported accidents, or inconsistent maintenance records affect long-term vehicle equity, frequently leading to overpayment.
- **Arbitrary Pricing by Dealerships:** Dealerships frequently mark up older vehicles or undervalue trade-ins by utilizing arbitrary markdowns rather than objective algorithmic metrics.
- **Non-Linear Multi-Factor Dynamics:** A 2020 premium SUV with 100,000 km mileage and authorized dealership servicing may command a higher residual value than a 2022 budget hatchback with 30,000 km mileage and zero documented service history. Static lookup rules fail to model these interdependencies.

Hence, the core engineering problem addressed by this project is:
> *To formulate, implement, and validate a supervised regression framework that accepts 12 vehicle parameters—encompassing technical specifications, physical condition, and historical usage—and outputs an accurate, unbiased estimation of the vehicle's market selling price in USD with minimal predictive error.*

---

## 4. OBJECTIVES

The core objectives of this project are formulated as follows:

1. **Dataset Ingestion & Validation:** Ingest a structured 10,000-row CSV dataset with exactly 13 columns, verify data types, confirm zero duplicate records, and handle missing values logically without data loss.
2. **Exploratory Data Analysis (EDA):** Generate 14 distinct, publication-grade analytical visualizations (univariate, bivariate, and multivariate) to derive statistical insights regarding car pricing distributions, brand premiums, fuel efficiency curves, and correlation matrices.
3. **Robust Data Preprocessing & Leakage Prevention:** Implement Scikit-Learn `ColumnTransformer` and `Pipeline` architectures that fit encoding (`OneHotEncoder`) and scaling (`StandardScaler`) transformations strictly on the training partition (80:20 split, `random_state=42`) to prevent data leakage.
4. **Feature Engineering:** Derive informative new predictors from baseline attributes:
   - Vehicle Age: $\text{car\_age} = 2024 - \text{make\_year}$
   - Accident Indicator: $\text{accident\_status} = \mathbb{I}(\text{accidents\_reported} > 0)$
5. **Algorithm Training & Benchmarking:** Implement and train four supervised regression algorithms:
   - Linear Regression
   - Decision Tree Regressor
   - Random Forest Regressor
   - Gradient Boosting Regressor
6. **Quantitative Evaluation:** Measure and contrast model performance using four standard mathematical metrics: MAE, MSE, RMSE, and $R^2$ on identical held-out test data.
7. **Visual Diagnostics:** Perform visual residual diagnostics, actual vs predicted scatter analyses, and bar chart comparisons.
8. **Interactive Web Deployment:** Develop and deploy a full-featured Streamlit web application (**CARPRICE AI**) featuring dynamic forms, live model inference, interactive Plotly dashboards, and full documentation.

---

## 5. DATASET DESCRIPTION

The dataset utilized in this project consists of exactly **10,000 records** and **13 columns**. The dataset features 10 global automobile manufacturers: Maruti Suzuki, Hyundai, Tata, Mahindra, Toyota, Kia, Honda, Volkswagen, Skoda, and MG, spanning 43 individual vehicle models.

### 5.1 Dataset Schema and Column Dictionary

| Column Name | Semantic Description | Data Type | Permissible Values / Range | Example Instance |
|---|---|---|---|---|
| `brand` | Automobile manufacturer | Categorical | 10 distinct brands | Toyota |
| `model` | Specific vehicle model designation | Categorical | 43 distinct models | Fortuner |
| `make_year` | Manufacturing calendar year | Numerical (int64) | 2012 to 2024 (13 years) | 2021 |
| `mileage_kmpl` | Fuel economy in km per litre | Numerical (float64) | 9.0 to 32.0 km/l | 10.5 |
| `engine_cc` | Engine displacement in CC | Numerical (int64) | 0 (EV) to 2755 CC | 2755 |
| `fuel_type` | Fuel source / powertrain technology | Categorical | Petrol, Diesel, CNG, Electric | Diesel |
| `transmission` | Transmission gear mechanism | Categorical | Manual, Automatic | Automatic |
| `color` | Exterior aesthetic vehicle color | Categorical | White, Silver, Grey, Black, Blue, Red | Black |
| `owner_count` | Number of registered prior owners | Numerical (int64) | 1 to 5 owners | 1 |
| `service_history` | Maintenance record availability | Categorical | Authorized Dealer, Partial, Independent Garage, None | Authorized Dealer |
| `accidents_reported`| Number of past recorded accidents | Numerical (int64) | 0 to 3 incidents | 0 |
| `insurance_valid` | Active comprehensive insurance status | Categorical | Yes, No | Yes |
| `price_usd` | **Target Variable:** Fair market price | Numerical (float64) | \$1,800.00 to \$55,000.00 USD | \$38,450.00 |

### 5.2 Summary Statistics of Numerical Attributes

| Statistic | `make_year` | `mileage_kmpl` | `engine_cc` | `owner_count` | `accidents_reported` | `price_usd` |
|---|---|---|---|---|---|---|
| **Count** | 10,000 | 10,000 | 10,000 | 10,000 | 10,000 | 10,000 |
| **Mean** | 2018.02 | 19.01 km/l | 1488.75 CC | 1.48 | 0.26 | \$12,580.46 |
| **Std Dev** | 3.77 yrs | 4.60 km/l | 496.22 CC | 0.72 | 0.57 | \$8,830.05 |
| **Min** | 2012 | 9.00 km/l | 0 CC | 1 | 0 | \$1,800.00 |
| **25%** | 2015 | 15.70 km/l | 1197 CC | 1 | 0 | \$6,199.22 |
| **50% (Median)** | 2018 | 18.50 km/l | 1497 CC | 1 | 0 | \$10,928.90 |
| **75%** | 2021 | 22.50 km/l | 1956 CC | 2 | 0 | \$17,119.13 |
| **Max** | 2024 | 32.00 km/l | 2755 CC | 5 | 3 | \$55,000.00 |

---

## 6. DATA PREPROCESSING

Data preprocessing forms the backbone of any robust machine learning system. In regression problems, failure to properly handle missing values, disparate scales, or unencoded categorical variables degrades model convergence and induces severe bias.

### 6.1 Missing Value Analysis and Imputation
The dataset underwent a comprehensive missing value diagnostic. Out of 10,000 rows, exactly 498 records in the `service_history` column contained `NaN` entries (4.98% of the dataset), while all remaining 12 columns possessed 100% non-null integrity.
- **Domain Rationale:** In real-world automotive trade, an omitted or missing service history is not missing at random (MAR); rather, it indicates the absence of documented service records.
- **Imputation Strategy:** All missing entries in `service_history` were imputed with the explicit category string `'None'`, completing the four logical service tiers: `['Authorized Dealer', 'Partial', 'Independent Garage', 'None']`.

### 6.2 Duplicate and Inconsistent Record Verification
The dataset was screened for duplicate rows using `df.duplicated().sum()`. Exactly 0 duplicate rows were detected, confirming full uniqueness of every vehicle record.

### 6.3 Feature Engineering
To provide direct semantic representations of vehicle condition and aging without introducing data leakage, two domain-specific features were engineered:
1. **Vehicle Age (`car_age`):**
   $$\text{car\_age} = 2024 - \text{make\_year}$$
   This explicitly represents the elapsed calendar years since manufacture, facilitating linear depreciation modeling.
2. **Accident Status Indicator (`accident_status`):**
   $$\text{accident\_status} = \begin{cases} 1 & \text{if } \text{accidents\_reported} > 0 \\ 0 & \text{if } \text{accidents\_reported} = 0 \end{cases}$$
   This captures the sharp discrete penalty applied by buyers to any vehicle possessing an accident history, regardless of whether 1 or 2 minor incidents occurred.

### 6.4 Leakage-Free Preprocessing Pipeline Architecture
To eliminate data leakage, data splitting occurred **prior** to fitting any transformations. The dataset was divided into an 80% training set (8,000 samples) and a 20% testing set (2,000 samples) using a fixed `random_state=42`.

The transformations were encapsulated in a Scikit-Learn `ColumnTransformer`:
1. **Numerical Pipeline:**
   - Numerical features: `['make_year', 'mileage_kmpl', 'engine_cc', 'owner_count', 'accidents_reported', 'car_age', 'accident_status']`
   - Transformation: `SimpleImputer(strategy='median')` followed by `StandardScaler()`, standardizing features to zero mean and unit variance:
     $$z = \frac{x - \mu}{\sigma}$$
2. **Categorical Pipeline:**
   - Categorical features: `['brand', 'model', 'fuel_type', 'transmission', 'color', 'service_history', 'insurance_valid']`
   - Transformation: `SimpleImputer(strategy='constant', fill_value='None')` followed by `OneHotEncoder(handle_unknown='ignore', sparse_output=False)`.
   - This converted the 7 categorical attributes into 71 binary indicator columns.

Total processed feature dimensionality: **78 input features**. The transformer was fit exclusively on `X_train_raw` and subsequently transformed both `X_train_raw` and `X_test_raw`. The fitted transformer was serialized to `models/preprocessing_pipeline.pkl`.

---

## 7. EXPLORATORY DATA ANALYSIS (EDA)

Fourteen comprehensive visual evaluations were executed to analyze market distributions, pricing dynamics, and correlations. All 14 generated plots are preserved in the `graphs/` directory.

### Key EDA Observations:

1. **Dataset Overview (`01_dataset_overview.png`):**
   A structured dashboard card encapsulating dataset dimensions (10,000 x 13), target range (\$1,800 to \$55,000), and manufacturer coverage.
2. **Car Brand Distribution (`02_car_brand_distribution.png`):**
   Maruti Suzuki dominates market volume with 2,239 vehicles (22.4%), followed by Hyundai with 1,819 units (18.2%), reflecting real-world mass-market market shares.
3. **Manufacturing Year Distribution (`03_car_make_year_distribution.png`):**
   Vehicle production years span uniformly from 2012 to 2024, averaging approximately 750–850 vehicles per calendar year, providing a balanced sample for longitudinal depreciation analysis.
4. **Mileage Distribution (`04_mileage_distribution.png`):**
   Fuel economy follows a Gaussian distribution centered at a mean of 19.01 km/l (median 18.5 km/l), spanning 9.0 to 32.0 km/l.
5. **Engine Capacity Distribution (`05_engine_capacity_distribution.png`):**
   Distinct modal peaks exist at 998cc, 1197cc, 1497cc, 1956cc, and 2755cc. A distinct cluster at 0 CC corresponds to Electric Vehicles (EVs).
6. **Fuel Type Distribution (`06_fuel_type_distribution.png`):**
   Petrol vehicles represent the primary segment (55.2%), followed by Diesel (26.5%), CNG (11.2%), and Electric (7.1%).
7. **Transmission Distribution (`07_transmission_distribution.png`):**
   Manual transmissions represent 65.3% (6,529 units) of the inventory, while Automatics comprise 34.7% (3,471 units).
8. **Target Price Distribution (`08_price_distribution.png`):**
   Selling price exhibits a realistic moderate right skew, with a minimum price floor of \$1,800, a median of \$10,928.90, and an upper tail extending to \$55,000 for luxury SUVs.
9. **Average Price by Brand (`09_avg_price_by_brand.png`):**
   Toyota commands the highest brand valuation (\$25,359 average), driven by premium models (Fortuner, Innova Crysta), whereas Maruti Suzuki exhibits the lowest average (\$7,842), corresponding to budget compact hatchbacks.
10. **Average Price by Fuel Type (`10_avg_price_by_fuel_type.png`):**
    Electric vehicles exhibit the highest mean price (\$12,754), followed closely by Diesel (\$12,698), Petrol (\$12,525), and CNG (\$12,180).
11. **Price vs Manufacturing Year (`11_price_vs_manufacturing_year.png`):**
    A clear monotonic upward trend confirms consistent annual depreciation. Median prices increase from ~\$4,200 for 2012 models to ~\$21,500 for 2024 models.
12. **Price vs Mileage (`12_price_vs_mileage.png`):**
    An inverse correlation is observed. High-mileage vehicles (>24 km/l) are predominantly low-cost entry-level commuter cars, whereas high-displacement luxury cars exhibit lower mileage (10–14 km/l) but high prices.
13. **Price vs Engine Capacity (`13_price_vs_engine_capacity.png`):**
    A strong positive correlation exists ($r = +0.67$); larger engine displacement strongly signifies higher vehicle market class and initial purchase price.
14. **Correlation Heatmap (`14_correlation_heatmap.png`):**
    Quantitative feature correlations with `price_usd`:
    - `engine_cc`: $+0.67$ (Strong positive)
    - `make_year`: $+0.32$ (Moderate positive)
    - `mileage_kmpl`: $-0.28$ (Moderate negative)
    - `owner_count`: $-0.15$ (Weak negative)
    - `accidents_reported`: $-0.11$ (Negative penalty)

---

## 8. PROPOSED METHODOLOGY

The implemented machine learning workflow adheres to the standard CRISP-DM (Cross-Industry Standard Process for Data Mining) methodology:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Data Understanding & Ingestion                          │
│    • Load 10,000 records from Dataset/used_cars.csv        │
│    • Validate 13 columns schema and data integrity          │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Data Cleaning & Feature Engineering                     │
│    • Impute missing service_history as 'None'              │
│    • Compute car_age = 2024 - make_year                    │
│    • Compute accident_status = I(accidents_reported > 0)    │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Leakage-Free Train-Test Partitioning                     │
│    • 80:20 Split (X_train: 8,000, X_test: 2,000)           │
│    • random_state=42 for deterministic reproducibility     │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Preprocessing Pipeline Fit (Strictly on Train Split)     │
│    • Numerical: Median Imputer + StandardScaler             │
│    • Categorical: OneHotEncoder(handle_unknown='ignore')    │
│    • Serialize preprocessing_pipeline.pkl                  │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Model Training & Serialization                           │
│    • Train Linear Regression, Decision Tree, Random Forest, │
│      and Gradient Boosting Regressors                      │
│    • Save all models to models/                             │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Model Evaluation on 2,000 Test Samples                   │
│    • Calculate MAE, MSE, RMSE, and R² scores               │
│    • Select best model -> models/best_model.pkl            │
│    • Generate 5 visual diagnostic plots to graphs/          │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Deployment via Streamlit Dashboard (CARPRICE AI)         │
│    • 5 Interactive Pages: Home, Predict, Analytics,         │
│      Performance, About                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. MACHINE LEARNING ALGORITHMS

### 9.1 Linear Regression (Ordinary Least Squares)
- **Principle:** Linear Regression assumes a linear functional form connecting the target $y$ to a linear combination of input features $x$:
  $$\hat{y} = \beta_0 + \sum_{j=1}^{p} \beta_j x_j$$
  Model parameters $\beta$ are estimated by minimizing the sum of squared residuals:
  $$\hat{\beta} = \arg\min_{\beta} \|y - X\beta\|_2^2 = (X^T X)^{-1} X^T y$$
- **Role in Project:** Serves as the parametric foundation. Because car prices in this market reflect linear compounding of base model valuation, engine size scaling, annual depreciation decrements, and condition penalties, Linear Regression provides exceptional performance when all categorical factors are one-hot encoded.

### 9.2 Decision Tree Regressor
- **Principle:** A non-parametric supervised learning algorithm that segments the continuous feature space into $M$ disjoint hyper-rectangles $R_1, R_2, \dots, R_M$. The optimal split at each node is chosen to minimize Mean Squared Error (variance reduction):
  $$\text{MSE}(R_m) = \frac{1}{N_m} \sum_{i \in R_m} (y_i - \bar{y}_m)^2$$
- **Hyperparameters:** `max_depth=12`, `min_samples_split=6`, `random_state=42`.
- **Role in Project:** Captures non-linear thresholds and rule-based interactions without assuming feature linearity.

### 9.3 Random Forest Regressor
- **Principle:** An ensemble bagging technique that constructs an ensemble of $B$ de-correlated decision trees $\{T_b\}_{b=1}^B$. Each tree is trained on an independent bootstrap sample of the training data, and split nodes evaluate a random subset of $m \approx \sqrt{p}$ features. The final prediction aggregates individual tree predictions:
  $$\hat{y}_{\text{RF}} = \frac{1}{B} \sum_{b=1}^{B} T_b(x)$$
- **Hyperparameters:** `n_estimators=100`, `max_depth=16`, `min_samples_split=4`, `random_state=42`, `n_jobs=-1`.
- **Role in Project:** Mitigates the high variance and overfitting tendencies of individual decision trees.

### 9.4 Gradient Boosting Regressor
- **Principle:** An ensemble boosting framework that sequentially builds trees in an additive stage-wise manner. At step $m$, a new decision tree $h_m(x)$ is trained to predict the negative gradient of the loss function (the pseudo-residuals) computed from the previous ensemble $F_{m-1}(x)$:
  $$r_{im} = -\left[\frac{\partial L(y_i, F(x_i))}{\partial F(x_i)}\right]_{F=F_{m-1}}$$
  The model is updated via:
  $$F_m(x) = F_{m-1}(x) + \gamma \cdot h_m(x)$$
  where $\gamma$ is the shrinkage rate (learning rate).
- **Hyperparameters:** `n_estimators=150`, `learning_rate=0.1`, `max_depth=5`, `random_state=42`.
- **Role in Project:** Highly effective at minimizing residual errors through iterative gradient descent.

---

## 10. EXPERIMENTAL RESULTS & DISCUSSION

All four regression algorithms were trained on the identical 8,000-sample training dataset and evaluated on the held-out 2,000-sample testing dataset.

### 10.1 Evaluation Metrics Formulation

1. **Mean Absolute Error (MAE):**
   $$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$$
   Measures average prediction error magnitude in original USD currency without disproportionately penalizing large outliers.
2. **Mean Squared Error (MSE):**
   $$\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$
   Penalizes large errors quadratically.
3. **Root Mean Squared Error (RMSE):**
   $$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$$
   Translates quadratic error penalties back to original USD currency units.
4. **Coefficient of Determination ($R^2$ Score):**
   $$R^2 = 1 - \frac{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{\sum_{i=1}^{n} (y_i - \bar{y})^2}$$
   Measures the proportion of total variance in selling price explained by the model ($1.00$ represents perfect prediction).

---

## 11. MODEL EVALUATION & COMPARISON

### 11.1 Actual Experimental Results Table

The quantitative benchmarks obtained from the test dataset are documented below (saved to `results/model_comparison.csv`):

| Rank | Model Name | MAE ($ USD) | MSE | RMSE ($ USD) | $R^2$ Score |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 🥇 | **Linear Regression** | **\$465.98** | **443,048.38** | **\$665.62** | **0.9946** |
| 🥈 | **Gradient Boosting Regressor** | \$602.55 | 810,180.96 | \$900.10 | 0.9900 |
| 🥉 | **Random Forest Regressor** | \$801.60 | 1,285,807.49 | \$1,133.93 | 0.9842 |
| 4 | **Decision Tree Regressor** | \$1,368.00 | 3,749,177.64 | \$1,936.28 | 0.9539 |

### 11.2 Discussion of Findings

1. **Superiority of Linear Regression:**
   Linear Regression achieved the highest accuracy ($R^2 = 0.9946$) and lowest error ($\text{MAE} = \$465.98$, $\text{RMSE} = \$665.62$). In this automotive market formulation, pricing is governed by an underlying additive depreciation and specification schedule:
   $$\text{Price} = \text{BasePrice}(\text{Brand}, \text{Model}) + \alpha(\text{Engine CC}) - \beta(\text{Age}) - \gamma(\text{Mileage}) + \delta(\text{Condition})$$
   Once the categorical variables are projected into one-hot space, ordinary least squares estimates these coefficients with sub-\$500 average deviation.
2. **Gradient Boosting Performance:**
   Gradient Boosting achieved second place with an exceptional $R^2$ of 0.9900 and RMSE of \$900.10. Its sequential shallow trees accurately captured non-linear interactions between service history and vehicle age.
3. **Random Forest and Decision Tree Comparison:**
   Random Forest ($R^2 = 0.9842$, RMSE = \$1,133.93) demonstrated substantial variance reduction over the single Decision Tree ($R^2 = 0.9539$, RMSE = \$1,936.28), reducing test MAE from \$1,368.00 down to \$801.60.
4. **Residual Analysis (`eval_02_residual_plot.png`):**
   Residual analysis for the best model confirms:
   - Residual errors are centered closely around zero ($\mu_{\text{error}} \approx -\$2.40$).
   - Errors display homoscedasticity across the entire predicted price spectrum (\$2,000 to \$50,000).
   - The actual vs predicted scatter plot (`eval_01_actual_vs_predicted.png`) aligns tightly along the ideal $y = x$ reference line.

---

## 12. SYSTEM ARCHITECTURE & DEPLOYMENT

The best model (`models/best_model.pkl`) and preprocessing pipeline (`models/preprocessing_pipeline.pkl`) were integrated into an interactive web application built with Streamlit.

### 12.1 Web Application Structure (`app.py`)
The application features a modern dark navy theme (`#0b1120`, `#0f172a`) with cyan (`#06b6d4`) and blue (`#38bdf8`) accents. It provides five responsive navigation pages:

1. **Page 1: Home (`🏠 Home`):**
   - High-impact dashboard banner highlighting 10,000 verified records, 13 features, and 99.46% model accuracy.
   - Comprehensive project overview cards and algorithm breakdowns.
2. **Page 2: Price Prediction (`🔮 Price Prediction`):**
   - Interactive valuation form featuring brand-dependent dynamic model selection (e.g., selecting 'Tata' dynamically restricts models to Nexon, Harrier, Safari, Punch, Altroz, Tiago).
   - Numerical sliders for make year, mileage, engine capacity, owner count, and accident history.
   - Quick preset buttons for instant testing (Maruti Swift budget commuter, Toyota Fortuner luxury SUV, MG ZS EV electric).
   - Valuation output card presenting the predicted price in USD, confidence bounds ($\pm 1\text{ RMSE}$), vehicle configuration badges, and condition insights.
3. **Page 3: Analytics Dashboard (`📊 Analytics Dashboard`):**
   - Four top-level KPI metric cards.
   - Six interactive Plotly charts: Brand market distribution, fuel type donut share, price histogram with box marginal, annual depreciation curves, engine capacity scatter plot, and numerical correlation heatmap.
4. **Page 4: Model Performance (`⚡ Model Performance`):**
   - Benchmark comparison table loaded directly from `results/model_comparison.csv`.
   - Side-by-side Plotly bar charts comparing MAE, RMSE, and $R^2$ across all four algorithms.
   - High-resolution Actual vs Predicted scatter plots and residual diagnostic distributions.
5. **Page 5: About Project (`ℹ️ About Project`):**
   - Problem statement, academic curriculum objectives, full technical stack breakdown, and undergraduate team presentation credits.

---

## 13. CONCLUSION

This project successfully developed and deployed **CARPRICE AI**, a machine learning regression system for used car market valuation. By enforcing leakage-free preprocessing, deriving domain-specific features (`car_age`, `accident_status`), and conducting rigorous empirical benchmarking across four distinct regression algorithms on 10,000 verified records, the system achieved:
- **$R^2$ Score of 0.9946** (99.46% variance explained)
- **Mean Absolute Error (MAE) of \$465.98 USD**
- **Root Mean Squared Error (RMSE) of \$665.62 USD**

The resulting web application demonstrates that supervised regression models can effectively demystify used automobile pricing, offering an objective, transparent, and accurate valuation tool for consumers, dealerships, and financial lenders.

---

## 14. FUTURE SCOPE & REFERENCES

### 14.1 Future Scope
1. **Multi-Currency & Geolocation Integration:** Incorporate live currency conversion APIs (e.g., INR, EUR, GBP) and localized state/city taxation indices to adjust for geographic supply-demand variations.
2. **Deep Learning for Damage Assessment:** Integrate computer vision models (e.g., YOLOv8 or ResNet-50) allowing users to upload vehicle photos to automatically detect exterior dents, paint degradation, and panel scratches.
3. **Real-Time Market Web Scraping:** Establish automated pipelines to periodically ingest live pricing data from online automotive portals (e.g., CarDekho, Cars24, Autotrader) to dynamically update model coefficients.
4. **Cloud Containerization & MLOps:** Package the entire application within Docker containers and deploy via continuous integration/continuous delivery (CI/CD) pipelines to cloud platforms (AWS, Google Cloud Run).

### 14.2 Academic References
1. Pedregosa, F., et al. (2011). "Scikit-learn: Machine Learning in Python." *Journal of Machine Learning Research*, 12, 2825–2830.
2. Breiman, L. (2001). "Random Forests." *Machine Learning*, 45(1), 5–32.
3. Friedman, J. H. (2001). "Greedy Function Approximation: A Gradient Boosting Machine." *Annals of Statistics*, 29(5), 1189–1232.
4. McKinney, W. (2010). "Data Structures for Statistical Computing in Python." *Proceedings of the 9th Python in Science Conference*, 51–56.
5. Streamlit Inc. (2024). "Streamlit Documentation: The Fastest Way to Build Data Apps." https://docs.streamlit.io/

