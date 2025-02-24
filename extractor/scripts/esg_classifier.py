import re
import json
import pytesseract
import pdfplumber
from PIL import Image
from transformers import pipeline
from collections import defaultdict

# Load ESG classification rules from an external JSON file
with open("esg_keywords.json", "r", encoding="utf-8") as f:
    ESG_KEYWORDS = json.load(f)

# Load NLP model for text classification
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF, including OCR for scanned documents."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

            # OCR if text extraction fails
            for img in page.images:
                img_obj = Image.open(img["stream"])
                text += pytesseract.image_to_string(img_obj)
    
    return text.strip()

def classify_esg_content(text):
    """Classifies ESG-related text into categories and subcategories."""
    esg_results = defaultdict(list)
    
    for category, subcategories in ESG_KEYWORDS.items():
        for subcategory, keywords in subcategories.items():
            for keyword in keywords:
                if re.search(rf"\b{keyword}\b", text, re.IGNORECASE):
                    esg_results[category].append(subcategory)
    
    # AI-based ESG classification
    labels = ["Environmental", "Social", "Governance"]
    ai_result = classifier(text, labels, multi_label=True)
    
    for label, score in zip(ai_result["labels"], ai_result["scores"]):
        if score > 0.5:
            esg_results[label].append(f"AI-Identified ESG Content (Score: {score:.2f})")
    
    return dict(esg_results)

def process_pdf(pdf_path):
    """Extracts text, classifies ESG content, and returns structured ESG data."""
    text = extract_text_from_pdf(pdf_path)
    esg_classification = classify_esg_content(text)
    
    return {
        "file": pdf_path,
        "classified_esg_content": esg_classification
    }

if __name__ == "__main__":
    pdf_file = "inputpdf/sample_report.pdf"
    results = process_pdf(pdf_file)
    print(json.dumps(results, indent=4))
