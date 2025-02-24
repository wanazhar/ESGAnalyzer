import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
import json
from openai import OpenAI

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update if necessary
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # API key stored externally

def extract_text_from_pdf(pdf_path):
    """Extract text and images from PDFs using AI for OCR and parsing."""
    doc = fitz.open(pdf_path)
    extracted_text = []

    for page in doc:
        text = page.get_text("text")
        if text.strip():
            extracted_text.append(text)

        # Extract images and run OCR
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_data = base_image["image"]
            pil_img = Image.open(io.BytesIO(img_data))
            ocr_text = pytesseract.image_to_string(pil_img)
            extracted_text.append(ocr_text)

    return "\n".join(extracted_text)

def classify_esg_content(text):
    """Use AI (GPT) to classify text into ESG categories."""
    prompt = f"""
    Classify the following ESG-related content into Environmental (E), Social (S), or Governance (G). 
    If possible, provide subcategories like 'Water Usage' under 'E'. Text:

    {text}

    Return JSON format: {{"category": "...", "subcategory": "..."}}
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)

def process_pdfs(input_folder="inputpdf"):
    """Extract, classify, and save ESG data."""
    esg_data = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            text = extract_text_from_pdf(pdf_path)
            classification = classify_esg_content(text)
            esg_data.append({"file": filename, "text": text, **classification})

    with open("backend/esg_parsed_data.json", "w") as f:
        json.dump(esg_data, f, indent=4)

if __name__ == "__main__":
    process_pdfs()
