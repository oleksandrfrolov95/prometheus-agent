import logging
import requests
import json
import pandas as pd

class ReportingManager:
    def __init__(self, reporting_config):
        self.logger = logging.getLogger(__name__)
        self.reporting_config = reporting_config

        # Only Teams webhook is used
        self.teams_webhook_url = reporting_config.get("teams_webhook_url", "")

    def publish(self, anomalies: pd.DataFrame):
        if anomalies.empty:
            self.logger.info("No anomalies to report.")
            return

        anomaly_count = len(anomalies)
        self.logger.warning(f"Reporting {anomaly_count} anomalies...")

        # Send Teams notification (if configured)
        if self.teams_webhook_url:
            self.send_to_teams(anomalies)
        else:
            self.logger.warning("Teams webhook URL not configured; skipping notification.")

    def send_to_teams(self, anomalies: pd.DataFrame):
        anomaly_count = len(anomalies)
        anomalies_preview = anomalies.head(5).to_dict(orient='records')
        message_text = (
            f"**Prometheus Agent Anomaly Alert**\n\n"
            f"Detected **{anomaly_count}** anomalies.\n\n"
            f"Sample Anomalies:\n\n"
        )
        payload = {"text": message_text}
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(self.teams_webhook_url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                self.logger.info("Successfully sent anomalies to Microsoft Teams.")
            else:
                self.logger.error(f"Failed to send message to Teams. HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.logger.exception("Error sending message to Teams:", exc_info=e)
