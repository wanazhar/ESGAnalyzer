"""
ESG Analyzer - Main Application
Flask-based API for ESG analysis and sentiment tracking
"""
import logging
from flask import Flask, jsonify, request
from api.esg_sentiment_analysis import analyze_sentiment
from api.esg_compliance_checker import check_compliance
from config import Config

# Setup configuration and logging
Config.setup_logging()
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def home():
    """Home endpoint returning a welcome message"""
    logger.info("Home endpoint accessed")
    return jsonify({
        "message": "Welcome to ESG Analyzer API!",
        "version": "1.0.0",
        "endpoints": {
            "/api/sentiment": "Analyze ESG sentiment in text",
            "/api/compliance": "Check ESG compliance against standards"
        }
    })

@app.route("/api/sentiment", methods=["POST"])
def sentiment_analysis():
    """Endpoint for analyzing sentiment in ESG-related text"""
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        text = request_data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided for analysis"}), 400
            
        logger.info(f"Performing sentiment analysis on text ({len(text)} chars)")
        results = analyze_sentiment(text)
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/compliance", methods=["POST"])
def compliance_check():
    """Endpoint for checking ESG compliance against standards"""
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        text = request_data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided for compliance check"}), 400
            
        logger.info(f"Performing compliance check on text ({len(text)} chars)")
        results = check_compliance(text)
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error in compliance check: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    try:
        # Validate configuration before starting
        Config.validate()
        logger.info(f"Starting ESG Analyzer API in {'DEBUG' if Config.DEBUG else 'PRODUCTION'} mode")
        app.run(debug=Config.DEBUG)
    except Exception as e:
        logger.critical(f"Failed to start application: {str(e)}")
