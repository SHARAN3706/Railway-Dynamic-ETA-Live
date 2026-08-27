import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb

def train_eta_model():
    print(">>> Loading generated telemetry dataset...")
    df = pd.read_csv("train_telemetry_dataset.csv")

    features = [
        "distance_km",
        "current_speed",
        "preceding_gap_km",
        "signal_aspect",
        "congestion_index",
        "weather_impact",
        "speed_restriction"
    ]
    target = "actual_time_mins"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(">>> Training XGBoost Regressor for dynamic ETA forecasting...")
    model = xgb.XGBRegressor(
        n_estimators=150,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Evaluation
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print("-" * 50)
    print("Model Performance Metrics:")
    print(f"Mean Absolute Error (MAE): {mae:.2f} minutes")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f} minutes")
    print(f"R-Squared Accuracy: {r2 * 100:.2f}%")
    print("-" * 50)

    joblib.dump(model, "ml_engine/eta_xgboost_model.pkl")
    print(">>> Model saved successfully: ml_engine/eta_xgboost_model.pkl")

if __name__ == "__main__":
    train_eta_model()