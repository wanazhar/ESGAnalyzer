from openai import OpenAI
import json
from cache import cache_result

API_KEY = "your_openai_key_here"  # Use external config file

def load_esg_data():
    """Loads ESG data for AI-driven insights."""
    with open("../output/esg_results.json", "r", encoding="utf-8") as f:
        return json.load(f)

@cache_result
def fetch_ai_analysis(company: str, year: str) -> dict:
    """Uses AI to generate ESG insights based on trends."""
    client = OpenAI(api_key=API_KEY)
    
    prompt = f"""
    Analyze the ESG performance of {company} in {year}.
    Compare trends with industry benchmarks and highlight key risks.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    
    return {"analysis": response["choices"][0]["message"]["content"]}
