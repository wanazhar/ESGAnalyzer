from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model
model = joblib.load("models/esg_forecast_model.pkl")

@app.route("/api/esg_forecast", methods=["POST"])
def predict_esg():
    """Predicts future ESG score based on input features."""
    data = request.json
    features = np.array([
        data["year"], 
        data["carbon_emissions"], 
        data["water_usage"], 
        data["diversity_score"], 
        data["board_independence"]
    ]).reshape(1, -1)

    predicted_score = model.predict(features)[0]
    return jsonify({"predicted_esg_score": round(predicted_score, 2)})

if __name__ == "__main__":
    app.run(debug=True, port=5007)
