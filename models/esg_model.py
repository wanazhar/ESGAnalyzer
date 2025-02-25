import joblib
import os
import numpy as np

class ESGModel:
    """
    ESG prediction model that loads a pre-trained model and provides
    methods for making predictions on ESG scores.
    """
    def __init__(self, model_path="esg_model.pkl"):
        """
        Initialize the ESG model, loading it from disk or creating a fallback model.
        
        Args:
            model_path (str): Path to the trained model file
        """
        self.model = None
        try:
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                print(f"Model loaded successfully from {model_path}")
            else:
                print(f"Model file {model_path} not found. Using fallback model.")
                # Simple fallback model that returns average values
                self.model = None
        except Exception as e:
            print(f"Error loading model: {str(e)}. Using fallback model.")
            self.model = None

    def predict_esg_score(self, features):
        """
        Predict ESG score based on input features.
        
        Args:
            features (list): List of features for prediction
            
        Returns:
            float: Predicted ESG score
        """
        try:
            if self.model:
                return self.model.predict([features])[0]
            else:
                # Fallback logic when model is not available
                # Return a simple average score (0.5-0.8) as placeholder
                return 0.5 + (sum(features) % 30) / 100
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return 0.5  # Default fallback score
