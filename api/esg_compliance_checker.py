import json

REGULATORY_REQUIREMENTS = {
    "GRI": ["carbon emissions", "water usage", "diversity"],
    "SASB": ["board independence", "executive pay", "supply chain"],
    "TCFD": ["climate risk", "energy transition", "scenario analysis"]
}

def check_compliance(text):
    """Checks ESG report compliance with global sustainability standards."""
    compliance_results = {key: [] for key in REGULATORY_REQUIREMENTS}

    for standard, requirements in REGULATORY_REQUIREMENTS.items():
        for req in requirements:
            if req in text.lower():
                compliance_results[standard].append(req)

    return json.dumps(compliance_results, indent=4)
