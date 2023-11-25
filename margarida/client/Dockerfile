FROM python:3.9.18-slim

WORKDIR /script

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./client_mqtt.py ./client_mqtt.py

ENTRYPOINT [ "python3", "-u", "client_mqtt.py" ]