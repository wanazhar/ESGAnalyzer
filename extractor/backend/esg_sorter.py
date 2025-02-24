import json
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_text_with_ai(text):
    """Use AI to classify ESG data into Environmental, Social, or Governance."""
    prompt = f"""
    Read the following ESG-related text and classify it into:
    - Environmental (E)
    - Social (S)
    - Governance (G)
    Also, suggest the most relevant subcategory. Text:

    {text}

    Return JSON format: {{"category": "...", "subcategory": "..."}}.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)

def classify_parsed_data():
    """Classify extracted ESG content from parsed JSON."""
    with open("backend/esg_parsed_data.json") as f:
        esg_data = json.load(f)

    for entry in esg_data:
        ai_classification = classify_text_with_ai(entry["text"])
        entry.update(ai_classification)

    with open("backend/esg_sorted_data.json", "w") as f:
        json.dump(esg_data, f, indent=4)

if __name__ == "__main__":
    classify_parsed_data()
