import logging
import os
import pandas as pd

class StorageManager:
    def __init__(self, storage_config):
        self.logger = logging.getLogger(__name__)
        self.storage_config = storage_config
        self.type = storage_config.get("type", "local")
        self.path = storage_config.get("path", "data")

    def save_raw_metrics(self, df):
        if df.empty:
            self.logger.info("No data to save (DataFrame is empty).")
            return
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        file_path = os.path.join(self.path, "raw_metrics.parquet")
        df.to_parquet(file_path)
        self.logger.info(f"Saved raw metrics to {file_path}.")

    def save_anomalies(self, anomalies):
        if anomalies.empty:
            self.logger.info("No anomalies to save (DataFrame is empty).")
            return
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        file_path = os.path.join(self.path, "anomalies.parquet")
        anomalies.to_parquet(file_path)
        self.logger.info(f"Saved anomalies to {file_path}.")
