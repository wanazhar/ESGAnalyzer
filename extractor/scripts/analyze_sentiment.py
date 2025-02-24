import os
import json
import openai
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# Load API key from config file
CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Error: {CONFIG_FILE} not found!")
        return None

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()
if config:
    openai.api_key = config.get("openai_api_key")
    llm_model = config.get("llm_model", "gpt-4")  # Default to GPT-4

# Check API key before proceeding
if not openai.api_key:
    raise ValueError("❌ OpenAI API key is missing! Set it in config.json.")

# Function to analyze sentiment using an LLM
def refine_sentiment_with_llm(text):
    """Use an LLM to refine sentiment and classify ESG-related themes."""
    prompt = f"""
    Analyze the following ESG-related news article and classify its sentiment as Positive, Negative, or Neutral.
    Then, determine which ESG category (Environmental, Social, or Governance) it falls under.
    Finally, provide a short summary (max 2 sentences) explaining why.

    Article: {text[:1000]}  # Limit text length for efficiency

    Output format:
    Sentiment: [Positive/Negative/Neutral]
    ESG Category: [Environmental/Social/Governance]
    Summary: [Short explanation]
    """

    try:
        response = openai.ChatCompletion.create(
            model=llm_model,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        return "Sentiment: Unknown\nESG Category: Unknown\nSummary: Error processing."

# (Other functions remain unchanged)
