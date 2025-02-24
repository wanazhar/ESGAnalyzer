from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load precomputed ESG data
esg_data = pd.read_csv("data/aggregated_esg_data.csv")

@app.route("/api/esg_data", methods=["GET"])
def get_esg_data():
    """Retrieve ESG data for a company."""
    company = request.args.get("company")
    result = esg_data[esg_data["company"].str.lower() == company.lower()]

    if result.empty:
        return jsonify({"error": "Company not found"}), 404

    return jsonify(result.to_dict(orient="records")[0])

if __name__ == "__main__":
    app.run(debug=True, port=5009)
