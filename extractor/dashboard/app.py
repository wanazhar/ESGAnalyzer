from flask import Flask, jsonify, request
import json

app = Flask(__name__)

def load_esg_data():
    """Loads ESG data from processed results."""
    with open("../output/esg_results.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/api/esg_comparison", methods=["GET"])
def get_esg_comparison():
    """Returns filtered ESG comparison data based on year and company."""
    year = request.args.get("year")
    company = request.args.get("company")
    esg_data = load_esg_data()

    filtered_data = esg_data.get("classified_esg_content", {})
    
    if year:
        filtered_data = {cat: [item for item in items if item.get("year") == year] for cat, items in filtered_data.items()}
    
    if company:
        filtered_data = {cat: [item for item in items if item.get("company") == company] for cat, items in filtered_data.items()}

    return jsonify(filtered_data)

if __name__ == "__main__":
    app.run(debug=True)
