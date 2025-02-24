import requests

def test_esg_social_sentiment():
    """Test ESG social sentiment API."""
    test_data = {"company": "Tesla"}
    response = requests.post("http://localhost:5020/api/social_sentiment", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert "overview" in data
    assert "greenwashing_alerts" in data

if __name__ == "__main__":
    test_esg_social_sentiment()
    print("✅ ESG Social Sentiment Test Passed!")
