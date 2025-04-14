import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_percentage_error
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
import numpy as np
from joblib import dump
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

from data_preparation.Transparency_data_preparation import create_transparency_pipeline, prepare_am_transparency_data, prepare_pm_transparency_data

def evaluate_xgb(X_train, y_train, X_dev, y_dev):
    print("Evaluating XGBoost Regressor...")

    param_grid = {
        'algo__n_estimators': [1000],
        'algo__max_depth': [2, 3, 4],
        'algo__learning_rate': [0.01, 0.05, 0.1],
        'algo__subsample': [0.8, 1.0],
    }
    

    pipeline = create_transparency_pipeline()

    pipeline_with_algo = Pipeline(steps=[
        ('preprocessor', pipeline),
        ('algo', XGBRegressor(objective='reg:squarederror', random_state=42))
    ])

    grid_search = GridSearchCV(
        pipeline_with_algo, param_grid,
        cv=5, scoring='neg_mean_squared_error', verbose=1
    )
    grid_search.fit(X_train, y_train)
    best_estimator = grid_search.best_estimator_

    try:
        model = best_estimator.named_steps["algo"]
        preprocessor = best_estimator.named_steps["preprocessor"]
        feature_names = preprocessor.get_feature_names_out()
        importances = model.feature_importances_

        feature_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": importances
        }).sort_values(by="Importance", ascending=False)

        print("\nTop 10 Most Important Features:")
        print(feature_df.head(10))
    except Exception as e:
        print("Could not extract feature importances:", e)

    y_pred = best_estimator.predict(X_dev)
    rmse = np.sqrt(mean_squared_error(y_dev, y_pred))
    mape = mean_absolute_percentage_error(y_dev, y_pred)
    r2 = r2_score(y_dev, y_pred)

    print("Grid searching is done!")
    print("Best score (neg MSE):", grid_search.best_score_)
    print("Best hyperparameters:")
    print(grid_search.best_params_)

    return best_estimator, rmse, mape, r2

def evaluate_metrics(y_true, y_pred, label, target):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    mean_target = np.mean(y_true)
    print(f"\n📊 {label} Set Performance for {target}:")
    print(f"Mean of y_{label.lower()}: {mean_target:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAPE: {mape:.4f}")
    print(f"R²: {r2:.4f}")
    return rmse, mape, r2

def main():
    for target in ["AM Transparency", "PM Transparency"]:
        print(f"\n🚀 Evaluating model for: {target}")

        if target == "AM Transparency":
            X_train, X_dev, X_test, y_train, y_dev, y_test = prepare_am_transparency_data()
            model_filename = "models/am_transparency_model.joblib"
        else:
            X_train, X_dev, X_test, y_train, y_dev, y_test = prepare_pm_transparency_data()
            model_filename = "models/pm_transparency_model.joblib"

        best_model, dev_rmse, dev_mape, dev_r2 = evaluate_xgb(X_train, y_train, X_dev, y_dev)

        print("✅ Data Split Shapes:")
        print("  X_train:", X_train.shape)
        print("  X_dev:", X_dev.shape)
        print("  X_test:", X_test.shape)
        print("  y_train:", y_train.shape)
        print("  y_dev:", y_dev.shape)
        print("  y_test:", y_test.shape)

        y_train_pred = best_model.predict(X_train)
        y_dev_pred = best_model.predict(X_dev)
        y_test_pred = best_model.predict(X_test)

        evaluate_metrics(y_train, y_train_pred, "Train", target)
        evaluate_metrics(y_dev, y_dev_pred, "Dev", target)
        evaluate_metrics(y_test, y_test_pred, "Test", target)

        dump(best_model, model_filename)
        print(f"✅ Model saved as: {model_filename}")

if __name__ == "__main__":
    main()
