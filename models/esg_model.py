import joblib

class ESGModel:
    def __init__(self):
        self.model = joblib.load("esg_model.pkl")

    def predict_esg_score(self, features):
        return self.model.predict([features])[0]
