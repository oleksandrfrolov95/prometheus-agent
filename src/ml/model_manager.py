import logging
import os
from sklearn.ensemble import IsolationForest
import joblib

class ModelManager:
    def __init__(self, model_config):
        self.logger = logging.getLogger(__name__)
        self.model_config = model_config
        self.model = None
        self.model_path = "data/model.joblib"

    def load_model_if_exists(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.logger.info(f"Loaded model from {self.model_path}.")
        else:
            self.logger.info("No existing model found; a new model will be created.")

    def train(self, df):
        if df.empty:
            self.logger.warning("Training data is empty. Cannot train a model.")
            return
        # Simple example: treat all columns as features, ignoring time index.
        X = df.values
        contamination = self.model_config.get("contamination", 0.05)
        self.model = IsolationForest(
            n_estimators=100, 
            contamination=contamination, 
            random_state=42
        )
        self.model.fit(X)
        self.logger.info("Model training completed.")

    def save_model(self):
        if self.model is None:
            self.logger.warning("No model to save.")
            return
        joblib.dump(self.model, self.model_path)
        self.logger.info(f"Saved model to {self.model_path}.")
