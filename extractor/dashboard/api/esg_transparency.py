from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load precomputed transparency scores
transparency_data = pd.read_csv("data/esg_transparency_scores.csv")

@app.route("/api/esg_transparency", methods=["GET"])
def get_transparency_score():
    """Retrieve ESG Transparency Score for a company."""
    company = request.args.get("company")
    result = transparency_data[transparency_data["company"].str.lower() == company.lower()]

    if result.empty:
        return jsonify({"error": "Company not found"}), 404

    return jsonify(result[["company", "transparency_score"]].to_dict(orient="records")[0])

if __name__ == "__main__":
    app.run(debug=True, port=5008)
