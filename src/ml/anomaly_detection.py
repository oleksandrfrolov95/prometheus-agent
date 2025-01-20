import logging
import pandas as pd

class AnomalyDetector:
    def __init__(self, model, model_config):
        self.logger = logging.getLogger(__name__)
        self.model = model
        self.model_config = model_config

    def detect(self, df):
        if df.empty or self.model is None:
            self.logger.warning("Cannot detect anomalies - either data is empty or model is None.")
            return pd.DataFrame()

        X = df.values
        predictions = self.model.predict(X)  # 1 = normal, -1 = anomaly
        df_anomalies = df.copy()
        df_anomalies["anomaly_label"] = predictions
        anomalies = df_anomalies[df_anomalies["anomaly_label"] == -1]
        self.logger.info(f"Detected {len(anomalies)} anomalies.")
        return anomalies
