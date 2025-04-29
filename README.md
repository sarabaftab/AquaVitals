# AquaVitals

## Documentation

### 🔍 Overview

**AquaVitals** is a full-stack AI-powered tool that predicts weekly fish survival rates using environmental features such as rainfall, temperature, and water transparency. Built using a Flask backend and a lightweight HTML/JS frontend, it delivers real-time predictions through a user-friendly interface. The backend integrates weather APIs and XGBoost regression models for spring temperature, transparency, and survival. Will be deployed very soon!

---

### 🏗️ System Architecture

- **Frontend**

  - Built with HTML, CSS, and JavaScript
  - Uses Litepicker for intuitive date range selection
  - Collects user input (date range, fish count)
  - Displays predictions in a readable table

- **Backend (Flask)**
  - Two primary endpoints:
    - `POST /process_dates`: Fetches rainfall & temperature forecast from external APIs
    - `POST /predict`: Chains predictions through XGBoost models to output:
      - Spring temperature
      - Morning & afternoon transparency
      - Fish survival rate and risk level
  - Models loaded via `.joblib` files from the `src/models/` directory

---

## 📁 Project Structure.

```
PI515-AI/
├── Data/
│   └── Raw/
│       ├── Main_Data.xlsx
│       └── Main_Data_edited.xlsx
│
├── Output/
├── Plots/
│
├── app/
│   │
│   ├── js/
│   │   ├── predict.js
│   │   └── script.js
│   │
│   ├── css/
│   │   ├── predict.css
│   │   └── script.css
│   │
│   ├── models/
│   │   └── am_transparency_model.joblib
│   │   └── pm_transparency_model.joblib
│   │   └── fish_survial_model.joblib
│   │   └── spring_temp_model.joblib
│   │
│   ├── about.html
│   ├── index.html
│   └── predict.html
│
├── src/
│   ├── __pycache__/
│   │
│   ├── Data_Preparation/
│   │   ├── fish_survival_data_preparation.ipynb
│   │   ├── fish_survival_data_preparation.py
│   │   ├── Spring_temp_data_preparation.py
│   │   ├── Spring_temp_data_preparation.ipynb
│   │   ├── Transparency_data_preparation.ipynb
│   │   └── Transparency_data_preparation.py
│   │
│   ├── models/
│   │   └── am_transparency_model.joblib
│   │   └── pm_transparency_model.joblib
│   │   └── fish_survial_model.joblib
│   │   └── spring_temp_model.joblib
│   │
│   ├── notebooks/
│   │   ├── fish_survival_model.ipynb
│   │   ├── spring_temp_model.ipynb
│   │   └── transparency_model.ipynb
│   │
│   ├── py/
│   │   ├── fish_survival_model.py
│   │   ├── spring_temp_model.py
│   │   └── transparency_model.py
│   │
│   ├── chained_model.ipynb
│   ├── DNN.ipynb
│   └── EDA.ipynb
│
├── README.md
```

## 🔗 Chained Model Architecture

The system follows a sequential prediction flow:

1. **Input Features**

   - Max/Min Air Temperature
   - Dec/Calmar Rain
   - Season, Day of Year
   - Time Series Features (Lag, Rolling Avg)  
     ↓

2. **Model 1: Predict Spring Temp (F)**

   - Uses input features to predict water temperature  
     ↓

3. **Model 2: Predict Transparency (AM/PM)**

   - Uses input features + predicted Spring Temp (F)  
     ↓

4. **Model 3: Predict Fish Survival Rate**
   - Uses input features + predicted Spring Temp + predicted Transparency

---

## 📌 Why Focus on RMSE and MAPE?

In our evaluation, we emphasize **RMSE (Root Mean Squared Error)** and **MAPE (Mean Absolute Percentage Error)** rather than R² for the following reasons:

- **Narrow Target Range**: The target variable — fish survival rate — lies in a very tight range (~99.2–100). This means that even small prediction errors can lead to very low or even negative R² values, making it a misleading metric in this context.
- **RMSE** gives a good indication of the absolute prediction error magnitude in the same units as the target variable.
- **MAPE** provides a scale-independent metric that shows how close predictions are in percentage terms — ideal for understanding model performance when values are close together.

> ✅ A low RMSE and MAPE indicate that the predictions are accurate and consistent, even when R² may not reflect this due to the lack of target variance.

---

## 📊 Model Performance Summary

### 🌤️ Spring Temp (F) Prediction Model (XGBoost)

- **Best Parameters**: `learning_rate=0.1`, `max_depth=4`, `n_estimators=1000`, `subsample=0.8`
- **Train Set**:
  - RMSE: **0.2974**
  - MAPE: **0.0041**
  - R²: **0.9924**
- **Dev Set**:
  - RMSE: **0.3500**
  - MAPE: **0.0047**
  - R²: **0.9896**
- **Test Set**:
  - RMSE: **0.3607**
  - MAPE: **0.0048**
  - R²: **0.9886**

---

### 🌫️ AM Transparency Prediction Model (XGBoost)

- **Best Parameters**: `learning_rate=0.1`, `max_depth=4`, `n_estimators=1000`, `subsample=0.8`
- **Train Set**:
  - RMSE: **2.0794**
  - MAPE: **0.1079**
  - R²: **0.9992**
- **Dev Set**:
  - RMSE: **5.5312**
  - MAPE: **0.1333**
  - R²: **0.9955**
- **Test Set**:
  - RMSE: **6.6780**
  - MAPE: **0.1466**
  - R²: **0.9915**

---

### 🌫️ PM Transparency Prediction Model (XGBoost)

- **Best Parameters**: `learning_rate=0.1`, `max_depth=4`, `n_estimators=1000`, `subsample=1.0`
- **Train Set**:
  - RMSE: **1.6149**
  - MAPE: **0.0869**
  - R²: **0.9994**
- **Dev Set**:
  - RMSE: **9.7851**
  - MAPE: **0.1048**
  - R²: **0.9766**
- **Test Set**:
  - RMSE: **3.8432**
  - MAPE: **0.1167**
  - R²: **0.9949**

---

### 🐟 Fish Survival Rate Prediction Model (XGBoost)

- **Best Parameters**: `learning_rate=0.1`, `max_depth=2`, `n_estimators=1000`, `subsample=1.0`
- **Train Set**:
  - RMSE: **0.2166**
  - MAPE: **0.0004**
  - R²: **0.3048**
- **Dev Set**:
  - RMSE: **0.6415**
  - MAPE: **0.0006**
  - R²: **0.0210**
- **Test Set**:
  - RMSE: **0.1934**
  - MAPE: **0.0004**
  - R²: **-0.1350**

---

# ⚙️ How to Run Locally

1. Clone the repository

   ```bash
   git clone [https://github.com/yourusername/aquavitals.git]
   cd aquavitals
   ```

2. Create and activate a virtual environment

   **macOS/Linux:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   **Windows:**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask app

   ```bash
   python app.py
   ```

5. Open the app in your browser
   Go to:
   ```
   http://localhost:5000
   ```

✅ **Note:** Ensure all .joblib model files are present in the src/models/ directory before running the app.

---
