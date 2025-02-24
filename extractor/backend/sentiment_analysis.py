import json
import requests

# Load config file
def load_config():
    with open("config.json") as f:
        return json.load(f)

config = load_config()

def analyze_sentiment(text, provider="openai"):
    """Analyzes ESG sentiment using the selected AI provider."""
    provider_config = config["ai_providers"].get(provider)

    if not provider_config:
        raise ValueError(f"Unsupported AI provider: {provider}")

    api_key = provider_config["api_key"]
    model = provider_config["model"]

    if provider == "openai":
        return analyze_with_openai(text, api_key, model)
    elif provider == "anthropic":
        return analyze_with_anthropic(text, api_key, model)
    elif provider == "cohere":
        return analyze_with_cohere(text, api_key, model)
    else:
        raise ValueError("Invalid AI provider selected.")

def analyze_with_openai(text, api_key, model):
    """Uses OpenAI GPT-4 for sentiment analysis."""
    import openai
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": f"Analyze sentiment: {text}"}]
    )
    return response["choices"][0]["message"]["content"]

def analyze_with_anthropic(text, api_key, model):
    """Uses Anthropic Claude for sentiment analysis."""
    url = "https://api.anthropic.com/v1/complete"
    headers = {"x-api-key": api_key, "content-type": "application/json"}
    data = {"model": model, "prompt": f"Analyze sentiment: {text}", "max_tokens": 500}
    response = requests.post(url, headers=headers, json=data)
    return response.json().get("completion", "No response")

def analyze_with_cohere(text, api_key, model):
    """Uses Cohere Command-R for sentiment analysis."""
    url = "https://api.cohere.ai/v1/generate"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"model": model, "prompt": f"Analyze sentiment: {text}", "max_tokens": 500}
    response = requests.post(url, headers=headers, json=data)
    return response.json().get("generations", [{}])[0].get("text", "No response")

def compare_esg_reports(provider="openai"):
    """Compares company ESG reports with external sources using selected AI model."""
    with open("backend/esg_parsed_data.json") as f:
        company_reports = json.load(f)

    with open("backend/esg_scraped_data.json") as f:
        external_reports = json.load(f)

    comparison_results = {}

    for company, text in company_reports.items():
        company_sentiment = analyze_sentiment(text, provider)
        external_sentiment = analyze_sentiment(" ".join(external_reports.values()), provider)

        comparison_results[company] = {
            "Company Sentiment": company_sentiment,
            "External Sentiment": external_sentiment
        }

    with open("backend/esg_comparison.json", "w") as f:
        json.dump(comparison_results, f, indent=4)

    print(f"✅ Sentiment analysis and comparison completed using {provider}!")

if __name__ == "__main__":
    compare_esg_reports(provider="anthropic")  # Change to "openai", "anthropic", or "cohere"
