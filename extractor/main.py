import scripts.extract_text
import scripts.classify_esg
import scripts.store_data

print("📥 Extracting text from PDFs...")
scripts.extract_text.process_all_pdfs()

print("🔍 Classifying ESG content...")
scripts.classify_esg.process_all_extracted_texts()

print("💾 Storing ESG data in the database...")
scripts.store_data.store_data()

print("✅ ESG Analysis Pipeline Completed!")
