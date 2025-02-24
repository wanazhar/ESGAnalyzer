import pdfplumber
import os
import json

INPUT_DIR = "inputpdf"

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        return " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def process_pdfs():
    """Parses multiple PDFs and extracts ESG-related content."""
    esg_data = {}
    
    for file in os.listdir(INPUT_DIR):
        if file.endswith(".pdf"):
            pdf_text = extract_text_from_pdf(os.path.join(INPUT_DIR, file))
            esg_data[file] = pdf_text  # Store extracted text per file
    
    return esg_data

if __name__ == "__main__":
    parsed_data = process_pdfs()
    with open("backend/esg_parsed_data.json", "w") as f:
        json.dump(parsed_data, f, indent=4)
    print("✅ ESG Data extracted and saved!")
