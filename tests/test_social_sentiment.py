from api.social_sentiment_api import get_social_sentiment

def test_social_sentiment(client):
    response = client.post("/api/social_sentiment", json={"company": "Tesla"})
    assert response.status_code == 200
