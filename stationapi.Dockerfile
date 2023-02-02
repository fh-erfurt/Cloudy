FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt .
COPY app/stationapi.py /app/main.py

RUN pip install -r requirements.txt