from flask import Flask, jsonify
from api.esg_sentiment_analysis import analyze_sentiment
from api.esg_compliance_checker import check_compliance

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to ESG Analyzer API!"})

@app.route("/api/sentiment", methods=["POST"])
def sentiment_analysis():
    request_data = request.get_json()
    text = request_data.get("text", "")
    return jsonify(analyze_sentiment(text))

@app.route("/api/compliance", methods=["POST"])
def compliance_check():
    request_data = request.get_json()
    text = request_data.get("text", "")
    return jsonify(check_compliance(text))

if __name__ == "__main__":
    app.run(debug=True)
