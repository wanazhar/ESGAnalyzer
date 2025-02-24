from esg_data_classifier import classify_esg_content
from esg_sentiment_analysis import analyze_sentiment

def aggregate_esg_data(text):
    categories = classify_esg_content(text)
    sentiment = analyze_sentiment(text)
    return {"categories": categories, "sentiment": sentiment}
