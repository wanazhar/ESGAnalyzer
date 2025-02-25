"""
ESG Analyzer - Data Extraction Pipeline
This script runs the complete ESG data extraction and analysis pipeline
"""
import sys
import os

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from extractor.scripts import extract_text
    from extractor.scripts import classify_esg
    from extractor.scripts import store_data
except ImportError as e:
    print(f"Error importing required modules: {str(e)}")
    print("Make sure all required packages are installed and the directory structure is correct")
    sys.exit(1)

def run_pipeline():
    """Run the complete ESG data extraction and analysis pipeline"""
    try:
        print("📥 Extracting text from PDFs...")
        extract_text.process_all_pdfs()
        
        print("🔍 Classifying ESG content...")
        classify_esg.process_all_extracted_texts()
        
        print("💾 Storing ESG data in the database...")
        store_data.store_data()
        
        print("✅ ESG Analysis Pipeline Completed!")
        return True
    except Exception as e:
        print(f"❌ Error in ESG Analysis Pipeline: {str(e)}")
        return False

if __name__ == "__main__":
    run_pipeline()
