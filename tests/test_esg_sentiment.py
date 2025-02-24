from api.esg_sentiment_analysis import analyze_sentiment

def test_analyze_sentiment():
    text = "The company is making great strides in sustainability!"
    result = analyze_sentiment(text)
    assert result["compound"] > 0
