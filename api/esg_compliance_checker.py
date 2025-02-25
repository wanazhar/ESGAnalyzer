import json

# Standard regulatory requirements for ESG reporting
REGULATORY_REQUIREMENTS = {
    "GRI": ["carbon emissions", "water usage", "diversity"],
    "SASB": ["board independence", "executive pay", "supply chain"],
    "TCFD": ["climate risk", "energy transition", "scenario analysis"]
}

def check_compliance(text):
    """
    Checks ESG report compliance with global sustainability standards.
    
    Args:
        text (str): The ESG report text to analyze
        
    Returns:
        str: JSON formatted string with compliance results for each standard
    """
    try:
        if not text or not isinstance(text, str):
            return json.dumps({"error": "Invalid input: text must be a non-empty string"})
            
        compliance_results = {key: [] for key in REGULATORY_REQUIREMENTS}

        for standard, requirements in REGULATORY_REQUIREMENTS.items():
            for req in requirements:
                if req.lower() in text.lower():
                    compliance_results[standard].append(req)

        return json.dumps(compliance_results, indent=4)
    except Exception as e:
        return json.dumps({"error": f"Compliance check failed: {str(e)}"})
