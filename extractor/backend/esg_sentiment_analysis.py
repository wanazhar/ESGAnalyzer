import json
from openai import OpenAI
import os
from textblob import TextBlob  # Additional sentiment analysis model

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_sentiment(text):
    """Analyze sentiment using AI & TextBlob for accuracy."""
    prompt = f"""
    Analyze the sentiment of this ESG-related text. Rate as:
    - Positive 😊
    - Neutral 😐
    - Negative 😠
    Provide a short summary of the sentiment. Text:

    {text}

    Return JSON format: {{"sentiment": "...", "summary": "..."}}.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    ai_sentiment = json.loads(response.choices[0].message.content)

    # Backup sentiment analysis with TextBlob
    textblob_sentiment = TextBlob(text).sentiment.polarity
    if textblob_sentiment > 0:
        textblob_result = "Positive 😊"
    elif textblob_sentiment < 0:
        textblob_result = "Negative 😠"
    else:
        textblob_result = "Neutral 😐"

    return {**ai_sentiment, "textblob_sentiment": textblob_result}

def analyze_all_esg_sentiments():
    """Perform AI-driven sentiment analysis on ESG reports."""
    with open("backend/esg_sorted_data.json") as f:
        esg_data = json.load(f)

    for entry in esg_data:
        sentiment_analysis = analyze_sentiment(entry["text"])
        entry.update(sentiment_analysis)

    with open("backend/esg_sentiment_data.json", "w") as f:
        json.dump(esg_data, f, indent=4)

if __name__ == "__main__":
    analyze_all_esg_sentiments()
