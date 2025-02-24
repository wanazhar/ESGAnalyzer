from api.esg_data_classifier import classify_esg_content

def test_classify_esg():
    text = "Company is committed to carbon neutrality and ethical governance."
    result = classify_esg_content(text)
    assert "Environmental" in result
    assert "Governance" in result
