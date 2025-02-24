import requests

def test_esg_data_aggregation():
    """Test ESG data aggregation API."""
    response = requests.get("http://localhost:5020/api/esg_data_aggregator?company=Tesla")
    assert response.status_code == 200
    data = response.json()
    assert "aggregated_esg_scores" in data
    assert isinstance(data["aggregated_esg_scores"], dict)

if __name__ == "__main__":
    test_esg_data_aggregation()
    print("✅ ESG Data Aggregation API Test Passed!")
