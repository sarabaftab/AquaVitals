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

from data_preparation.Spring_temp_data_preparation import create_spring_temp_pipeline, prepare_spring_temp_data

def evaluate_xgb(X_train, y_train, X_dev, y_dev):
    print("Evaluating XGBoost Regressor...")

    param_grid = {
        'algo__n_estimators': [1000],
        'algo__max_depth': [2, 3, 4],
        'algo__learning_rate': [0.01, 0.05, 0.1],
        'algo__subsample': [0.8, 1.0],
    }

    pipeline = create_spring_temp_pipeline()

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

def evaluate_metrics(y_true, y_pred, label):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    mean_target = np.mean(y_true)
    print(f"\n📊 {label} Set Performance:")
    print(f"Mean of y_{label.lower()}: {mean_target:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAPE: {mape:.4f}")
    print(f"R²: {r2:.4f}")
    return rmse, mape, r2

def main():
    print("\n🚀 Evaluating model for: Spring Temp (F)")
    X_train, X_dev, X_test, y_train, y_dev, y_test = prepare_spring_temp_data()

    best_model, _, _, _ = evaluate_xgb(X_train, y_train, X_dev, y_dev)

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

    evaluate_metrics(y_train, y_train_pred, "Train")
    evaluate_metrics(y_dev, y_dev_pred, "Dev")
    evaluate_metrics(y_test, y_test_pred, "Test")

    # ✅ Save model
    dump(best_model, "models/spring_temp_model.joblib")
    print("✅ Model saved as: models/spring_temp_model.joblib")

if __name__ == "__main__":
    main()
