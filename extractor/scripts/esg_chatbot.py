import openai
import json
import random
from datetime import datetime
import requests

# Load API keys from external file
with open("config.json", "r") as config_file:
    config = json.load(config_file)
OPENAI_API_KEY = config.get("OPENAI_API_KEY")
CLAUDE_API_KEY = config.get("CLAUDE_API_KEY")
GEMINI_API_KEY = config.get("GEMINI_API_KEY")

# Define ESG prompts to improve AI responses
ESG_PROMPTS = {
    "general": "Provide a detailed analysis of current ESG trends and how they impact businesses globally.",
    "company_specific": "Analyze the ESG performance of {company} and compare it with industry competitors.",
    "industry_insights": "Discuss the key ESG challenges faced by the {industry} sector and compare with best practices.",
    "sentiment_analysis": "Summarize the public perception of {company}'s ESG efforts based on news and social media sentiment.",
    "regulatory_compliance": "Explain how {company} aligns with global ESG regulatory frameworks such as GRI, SASB, or TCFD.",
    "benchmarking": "Compare the ESG scores of {company} against industry benchmarks and sustainability leaders."
}

# Function to query OpenAI's GPT model
def query_openai(prompt: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an ESG analysis expert with deep knowledge of global sustainability standards and industry benchmarks."},
                      {"role": "user", "content": prompt}],
            api_key=OPENAI_API_KEY
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error retrieving GPT response: {str(e)}"

# Function to query Claude AI
def query_claude(prompt: str):
    try:
        response = requests.post("https://api.anthropic.com/v1/complete",
            headers={"Authorization": f"Bearer {CLAUDE_API_KEY}", "Content-Type": "application/json"},
            json={"model": "claude-2", "prompt": prompt, "max_tokens": 500}
        )
        return response.json().get("completion", "Claude API error")
    except Exception as e:
        return f"Error retrieving Claude response: {str(e)}"

# Function to query Gemini AI
def query_gemini(prompt: str):
    try:
        response = requests.post("https://api.gemini.com/v1/generate",
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"},
            json={"prompt": prompt, "max_tokens": 500}
        )
        return response.json().get("text", "Gemini API error")
    except Exception as e:
        return f"Error retrieving Gemini response: {str(e)}"

# Function to handle AI model selection and fallback
def get_esg_insight(prompt: str, model: str = "gpt-4"):
    if model == "gpt-4":
        response = query_openai(prompt)
    elif model == "claude":
        response = query_claude(prompt)
    elif model == "gemini":
        response = query_gemini(prompt)
    else:
        response = "Invalid model selection. Defaulting to GPT-4."
        response = query_openai(prompt)
    return response

# Example chatbot function
def esg_chatbot(query: str, company: str = None, industry: str = None, model: str = "gpt-4"):
    """Handles user queries related to ESG insights with AI model selection."""
    if "trends" in query.lower():
        prompt = ESG_PROMPTS["general"]
    elif "compare" in query.lower() and company:
        prompt = ESG_PROMPTS["company_specific"].format(company=company)
    elif "industry" in query.lower() and industry:
        prompt = ESG_PROMPTS["industry_insights"].format(industry=industry)
    elif "sentiment" in query.lower() and company:
        prompt = ESG_PROMPTS["sentiment_analysis"].format(company=company)
    elif "regulatory" in query.lower() and company:
        prompt = ESG_PROMPTS["regulatory_compliance"].format(company=company)
    elif "benchmark" in query.lower() and company:
        prompt = ESG_PROMPTS["benchmarking"].format(company=company)
    else:
        prompt = "Provide an overview of ESG principles and their importance in the global market."
    
    response = get_esg_insight(prompt, model)
    return response

# Example usage
if __name__ == "__main__":
    print("ESG Chatbot Online. Type 'exit' to quit.")
    while True:
        user_query = input("Ask me about ESG: ")
        if user_query.lower() == "exit":
            break
        print("\n", esg_chatbot(user_query, company="Tesla", industry="Automotive", model="claude"), "\n")
