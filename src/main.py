import logging

from src.ingestion.prometheus_ingestor import PrometheusIngestor
from src.storage.storage_manager import StorageManager
from src.ml.model_manager import ModelManager
from src.ml.anomaly_detection import AnomalyDetector
from src.reporting.reporting_manager import ReportingManager
from src.utils.helpers import load_config

def main():
    # 1. Load configuration
    config = load_config("config/config.yaml")
    prometheus_url = config["prometheus"]["url"]
    time_window = config["prometheus"]["time_window"]
    step = config["prometheus"]["step"]

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("prometheus-agent")

    # 2. Ingest data from Prometheus
    ingestor = PrometheusIngestor(prometheus_url)
    all_metrics_data = ingestor.fetch_all_metrics_data(time_window=time_window, step=step)

    # 3. Persist raw data
    storage = StorageManager(config["storage"])
    storage.save_raw_metrics(all_metrics_data)

    # 4. Load or train ML model
    model_mgr = ModelManager(config["model"])
    model_mgr.load_model_if_exists()
    model_mgr.train(all_metrics_data)
    model_mgr.save_model()

    # 5. Detect anomalies
    anomaly_detector = AnomalyDetector(model_mgr.model, config["model"])
    anomalies = anomaly_detector.detect(all_metrics_data)

    # 6. Store anomalies
    storage.save_anomalies(anomalies)

    # 7. Reporting
    reporting_mgr = ReportingManager(config["reporting"])
    reporting_mgr.publish(anomalies)

    logger.info("Prometheus Agent run completed.")

if __name__ == "__main__":
    main()
