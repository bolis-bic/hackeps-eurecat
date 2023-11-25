FROM python:3.9.14-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY save.py save.py
CMD ["python3", "-u", "save.py"]