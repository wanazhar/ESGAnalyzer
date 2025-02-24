import requests

def test_transparency_score():
    """Test ESG transparency scoring API."""
    response = requests.get("http://localhost:5020/api/transparency_score?company=Tesla")
    assert response.status_code == 200
    data = response.json()
    assert "transparency_score" in data
    assert isinstance(data["transparency_score"], float)

if __name__ == "__main__":
    test_transparency_score()
    print("✅ ESG Transparency Score API Test Passed!")
