"""Send log messages to remote log aggregation servers."""
import requests
import os
import sys
from loguru import logger

# Sensitive data stored in environmental variables
# On Ubuntu, put variables in /etc/environment
SPLUNK_URL = os.environ.get('SPLUNK_URL')
SPLUNK_SOURCETYPE = os.environ.get('SPLUNK_SOURCETYPE')
SPLUNK_AUTH = os.environ.get('SPLUNK_AUTH')

if not all((SPLUNK_URL, SPLUNK_SOURCETYPE, SPLUNK_AUTH)):
    print("Failed to read Splunk telemetry environmental variables.")


def send_log_message(message):
    """Send a message to log aggregation server."""
    payload = {"event": message, "sourcetype": SPLUNK_SOURCETYPE}
    try:
        r = requests.post(SPLUNK_URL, headers={'Authorization': SPLUNK_AUTH},
                          json=payload, verify=False)
        print(r.text)
    except Exception as e:
        logger.warning(f"Error sending message to Splunk: {e}")

send_log_message("boot")

if __name__ == "__main__":
    send_log_message(sys.argv[1])
