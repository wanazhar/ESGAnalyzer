import requests

def test_esg_compliance():
    """Test ESG compliance checker API."""
    test_data = {"report": "GHG Emissions, Board Oversight, Human Rights"}
    response = requests.post("http://localhost:5020/api/check_compliance", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert "missing" in data
    assert "suggestions" in data

if __name__ == "__main__":
    test_esg_compliance()
    print("✅ ESG Compliance Checker Test Passed!")
