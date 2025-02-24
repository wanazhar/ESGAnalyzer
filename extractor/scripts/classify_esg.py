import os
import re
import json
import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")

INPUT_FOLDER = "extracted_esg"
OUTPUT_FOLDER = "classified_esg"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ESG_KEYWORDS = {
    "Environmental": {
        "Water Usage": ["water consumption", "wastewater", "water recycling"],
        "Carbon Emissions": ["CO2 emissions", "carbon footprint"],
        "Energy Efficiency": ["renewable energy", "solar power"]
    },
    "Social": {
        "Diversity & Inclusion": ["gender equality", "workplace diversity"],
        "Labor Rights": ["worker rights", "fair labor"],
        "Community Impact": ["charity", "philanthropy"]
    },
    "Governance": {
        "Board Ethics": ["business ethics", "anti-corruption"],
        "Transparency": ["corporate governance", "stakeholder rights"]
    }
}

def classify_text(text):
    """Classify text into ESG segments based on keywords."""
    classified_data = {"Environmental": [], "Social": [], "Governance": []}
    sentences = sent_tokenize(text)

    for sentence in sentences:
        for category, subcategories in ESG_KEYWORDS.items():
            for subcategory, keywords in subcategories.items():
                if any(re.search(rf"\b{keyword}\b", sentence, re.IGNORECASE) for keyword in keywords):
                    classified_data[category].append({"subcategory": subcategory, "sentence": sentence})

    return classified_data

def process_all_extracted_texts():
    """Read extracted ESG text files and classify them."""
    for text_file in os.listdir(INPUT_FOLDER):
        if text_file.endswith(".txt"):
            input_path = os.path.join(INPUT_FOLDER, text_file)
            output_path = os.path.join(OUTPUT_FOLDER, text_file.replace(".txt", ".json"))

            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()

            classified_data = classify_text(text)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(classified_data, f, indent=4)

            print(f"Classified ESG data saved: {output_path}")

# Run classification
process_all_extracted_texts()
