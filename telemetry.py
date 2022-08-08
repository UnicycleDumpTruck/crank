"""Send log messages to remote log aggregation servers."""
import threading
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
    logger.warning("Failed to read Splunk telemetry environmental variables.")


def send_log_message(message):
    message_thread = threading.Thread(target=send_msg, args=(message,))
    message_thread.start()

def send_msg(message):
    """Send a message to log aggregation server."""
    payload = {"event": message, "sourcetype": SPLUNK_SOURCETYPE}
    try:
        r = requests.post(SPLUNK_URL, headers={'Authorization': SPLUNK_AUTH},
                          json=payload, verify=False)
        logger.debug(r.text)
    except Exception as e:
        logger.warning(f"Error sending message to Splunk: {e}")

if __name__ == "__main__":
    send_log_message(sys.argv[1])
