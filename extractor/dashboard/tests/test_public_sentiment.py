import requests

def test_api():
    """Test public sentiment API response."""
    response = requests.get("http://localhost:5020/api/social_sentiment?keyword=ESG")
    assert response.status_code == 200
    data = response.json()
    assert "twitter" in data
    assert "reddit" in data
    assert "news" in data
    assert isinstance(data["overall_sentiment"], float)

if __name__ == "__main__":
    test_api()
    print("✅ API Test Passed!")
