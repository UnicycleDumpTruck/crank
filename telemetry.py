"""Send log messages to remote log aggregation servers."""
import threading
import requests
import os
from loguru import logger

# Sensitive data stored in environmental variables
# On Ubuntu, put variables in /etc/environment
SPLUNK_URL = os.environ.get('SPLUNK_URL')
SPLUNK_SOURCETYPE = os.environ.get('SPLUNK_SOURCETYPE')
SPLUNK_AUTH = os.environ.get('SPLUNK_AUTH')

if not all((SPLUNK_URL, SPLUNK_SOURCETYPE, SPLUNK_AUTH)):
    logger.warning("Failed to read Splunk telemetry environmental variables.")

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = os.environ.get('INFLUXDB_BUCKET')
org = os.environ.get('INFLUXDB_ORG')
token = os.environ.get('INFLUXDB_TOKEN')
url = os.environ.get('INFLUXDB_URL')

client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("exhibit_boot").tag("location", "Power2Play").field("exhibit_name", "crank")
try:
    write_api.write(bucket=bucket, org=org, record=p)
except Exception as e:
    logger.warning(f"Error sending boot point to InfluxDB: {e}")

def send_point_in_thread(max_rpm, balls_dropped, temperature):
    logging_thread = threading.Thread(target=send_point, args=(max_rpm, balls_dropped, temperature))
    logging_thread.start()

def send_point(max_rpm, balls_dropped, temperature):
    try:
        p = influxdb_client.Point("crank_session").tag("location", "Power2Play").field("max_rpm", max_rpm).field("balls_dropped", balls_dropped).field("temperature", temperature)
        write_api.write(bucket=bucket, org=org, record=p)
    except Exception as e:
        logger.warning(f"Error sending point to InfluxDB: {e}")

def send_log_message(message):
    message_thread = threading.Thread(target=send_msg, args=(message,))
    message_thread.start()

def send_msg(message):
    """Send a message to log aggregation server."""
    payload = {"event": message, "sourcetype": SPLUNK_SOURCETYPE}
    try:
        r = requests.post(SPLUNK_URL, headers={'Authorization': SPLUNK_AUTH},
                          json=payload, verify=False)
        logger.debug(f"Splunk response: {r.text}")
    except Exception as e:
        logger.warning(f"Error sending message to Splunk: {e}")
