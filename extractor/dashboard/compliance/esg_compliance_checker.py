import json
import difflib

# Define ESG Compliance Rules (Simplified)
COMPLIANCE_RULES = {
    "SASB": ["GHG Emissions", "Water Usage", "Workforce Diversity", "Risk Management"],
    "GRI": ["Environmental Impact", "Human Rights", "Supply Chain", "Ethical Practices"],
    "TCFD": ["Climate Risk Disclosure", "Carbon Emission Goals", "Board Oversight"]
}

def check_compliance(esg_report):
    """Check ESG report against compliance standards."""
    flagged_issues = {}

    for standard, requirements in COMPLIANCE_RULES.items():
        missing_disclosures = [req for req in requirements if req not in esg_report]
        if missing_disclosures:
            flagged_issues[standard] = missing_disclosures

    return flagged_issues

def suggest_improvements(flagged_issues):
    """Suggest improvements based on missing disclosures."""
    suggestions = {}
    
    for standard, missing in flagged_issues.items():
        suggestions[standard] = [f"Consider adding {req} to improve {standard} compliance." for req in missing]
    
    return suggestions

# Example ESG Report (for testing)
sample_report = ["GHG Emissions", "Board Oversight", "Human Rights"]

# Run Compliance Check
flagged_issues = check_compliance(sample_report)
improvement_suggestions = suggest_improvements(flagged_issues)

# Output Compliance Status
print("⚠️ Missing Disclosures:", flagged_issues)
print("✅ Improvement Suggestions:", improvement_suggestions)
