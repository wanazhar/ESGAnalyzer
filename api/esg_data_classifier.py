import json

def classify_esg_content(text):
    """Classifies ESG content into Environmental, Social, and Governance categories."""
    categories = {
        "Environmental": ["carbon", "climate", "sustainability", "pollution"],
        "Social": ["diversity", "human rights", "labor", "community"],
        "Governance": ["compliance", "board", "ethics", "audit"]
    }
    result = {"Environmental": [], "Social": [], "Governance": []}

    for key, words in categories.items():
        for word in words:
            if word in text.lower():
                result[key].append(word)

    return json.dumps(result, indent=4)
