import logging
import os
import signal
import sys

from json import loads

import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WriteOptions

INFLUXDB_URL = os.environ.get("INFLUXDB_URL")
INFLUXDB_ORG = os.environ.get("INFLUXDB_ORG")
INFLUXDB_TOKEN = os.environ.get("INFLUXDB_TOKEN")
INFLUXDB_BUCKET = os.environ.get("INFLUXDB_BUCKET")

MQTT_BROKER = os.environ.get("MQTT_BROKER")
MQTT_PORT = os.environ.get("MQTT_PORT")
MQTT_TOPIC = os.environ.get("MQTT_TOPIC")
MQTT_USERNAME = os.environ.get("MQTT_USERNAME")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")

WRITE_OPTIONS = WriteOptions(
    batch_size=1_000,
    flush_interval=1_000,
)


def init_logging():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def init_signal_handler():

    def signal_handler(sig, frame):
        logging.info(f"Received signal {sig}. Exiting gracefully.")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def get_mqtt_client(username, password, broker="localhost", port=1883):

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT Broker!")
        else:
            logging.info("Failed to connect, return code %d\n", rc)

    client = mqtt.Client("python-mqtt")
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, int(port))
    return client


def get_influxdb_client(url, token, org):
    logging.info("Connecting to InfluxDB")
    client = InfluxDBClient(url=url, token=token, org=org)
    logging.info("Connected to InfluxDB")
    return client


def save_record(message, write_api):
    payload = loads(str(message.payload)[2:-1])
    device_id, measurement = message.topic.split("/")[-2:]

    record_dict = {
        "measurement": device_id,
        "tags": {
            "measurement": measurement
        },
        "fields": {
            "value": payload["value"]
        },
        "time": int(payload["unix_timestamp"]) * 1_000_000_000,
    }
    record = Point.from_dict(record_dict)

    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=record)
    logging.debug(f"Written {record} to {INFLUXDB_BUCKET}")


def main():
    init_logging()
    init_signal_handler()

    try:
        influxdb_client = get_influxdb_client(INFLUXDB_URL, INFLUXDB_TOKEN,
                                              INFLUXDB_ORG)
        write_api = influxdb_client.write_api(write_options=WRITE_OPTIONS)

        mqtt_client = get_mqtt_client(
            username=MQTT_USERNAME,
            password=MQTT_PASSWORD,
            broker=MQTT_BROKER,
            port=MQTT_PORT,
        )
        mqtt_client.subscribe(MQTT_TOPIC)

        def on_message(client, userdata, message):
            save_record(message, write_api)

        mqtt_client.on_message = on_message
        mqtt_client.loop_forever()
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        if mqtt_client:
            mqtt_client.disconnect()
        if influxdb_client:
            influxdb_client.close()


if __name__ == "__main__":
    main()
