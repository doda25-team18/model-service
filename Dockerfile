FROM python:3.12.9-slim

WORKDIR /app

COPY src ./src
COPY requirements.txt ./requirements.txt
COPY output/model.joblib ./output/model.joblib

RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "python", "src/serve_model.py" ]
