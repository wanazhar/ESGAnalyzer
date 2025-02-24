import os
import fitz  # PyMuPDF for PDF parsing
import pytesseract
from PIL import Image
import json

INPUT_FOLDER = "input_pdfs"
OUTPUT_FOLDER = "extracted_esg"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF, including OCR for images."""
    doc = fitz.open(pdf_path)
    extracted_text = ""

    for page in doc:
        extracted_text += page.get_text("text") + "\n"
        
        # Extract text from images
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image = Image.open(base_image["image"])
            extracted_text += pytesseract.image_to_string(image) + "\n"

    return extracted_text.strip()

def process_all_pdfs():
    """Extract text from all PDFs in the input folder."""
    for pdf_file in os.listdir(INPUT_FOLDER):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_FOLDER, pdf_file)
            text = extract_text_from_pdf(pdf_path)
            
            output_path = os.path.join(OUTPUT_FOLDER, pdf_file.replace(".pdf", ".txt"))
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            
            print(f"Extracted ESG text saved: {output_path}")

# Run extraction
process_all_pdfs()
