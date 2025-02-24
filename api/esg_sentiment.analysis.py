from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Returns sentiment score for ESG-related text."""
    return analyzer.polarity_scores(text)
