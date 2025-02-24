from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Load ESG data
def load_esg_data():
    with open("esg_comparison.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/api/esg", methods=["GET"])
def get_esg_data():
    """Serve ESG comparison data as JSON."""
    esg_data = load_esg_data()
    return jsonify(esg_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
