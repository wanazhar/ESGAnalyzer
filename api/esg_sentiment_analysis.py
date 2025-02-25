from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Returns sentiment score for ESG-related text."""
    try:
        return analyzer.polarity_scores(text)
    except Exception as e:
        return {"error": str(e), "compound": 0, "pos": 0, "neu": 0, "neg": 0} 