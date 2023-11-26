import time
import paho.mqtt.client as mqtt
import socket
import logging
import signal
import sys

from os import environ


def _init_logging():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def _init_signal_handler():

    def signal_handler(sig, frame):
        logging.info(f"Received signal {sig}. Exiting gracefully.")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def _on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Successfully connected")
    else:
        logging.info("Failed connection to host")
        exit(-1)


def _on_message(client, user_data, message):
    msg = message.payload.decode("utf-8")
    logging.debug(f"Received message from topic {message.topic} {msg}")


def _connect_client(
    client: mqtt.Client,
    host: str,
    port: int = 1883,
    max_retries: int = 10,
) -> bool:
    logging.info(f"Connecting to service '{host}:{port}'")

    retries = 0
    while retries < max_retries:
        try:
            client.connect(environ.get("BROKER_ADDRESS"), port)
            return True
        except socket.gaierror:
            logging.error(
                f"Unable to resolve MQTT broker service hostname '{host}'. Retrying in 1 second..."
            )
            retries += 1
            time.sleep(1)
    logging.error(
        f"Exceeded maximum number of connection retries '{max_retries}'")
    return False


def main():
    _init_signal_handler()
    _init_logging()

    client = mqtt.Client(environ.get("GROUP"))

    client.username_pw_set(environ.get("USER"), environ.get("PASSWORD"))

    client.on_connect = _on_connect
    client.on_message = _on_message

    _connect_client(client, environ.get("BROKER_ADDRESS"),
                    int(environ.get("BROKER_ADDRESS_PORT")))

    client.subscribe(environ.get("TOPIC"))

    client.loop_forever()


if __name__ == "__main__":
    main()
