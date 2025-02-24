import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load historical ESG scores dataset
data = pd.read_csv("data/esg_scores_historical.csv")

# Feature selection
features = ["year", "carbon_emissions", "water_usage", "diversity_score", "board_independence"]
X = data[features]
y = data["esg_score"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Model MAE: {mae:.2f}")

# Save model
joblib.dump(model, "models/esg_forecast_model.pkl")
