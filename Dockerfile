FROM python:3.12.9-slim

WORKDIR /app


COPY requirements.txt ./requirements.txt
# Install dependencies first so this layer can be reused when src changes but requirements does not
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

RUN mkdir -p /app/models

ENV MODEL_DIR=/app/models
ENV MODEL_VERSION=model-7
ENV MODEL_REPO=doda25-team18/model-service
# Gunicorn needs this to resolve the imports correctly
ENV PYTHONPATH=/app/src
ENV MODEL_SERVICE_PORT=8081
# This is needed to show the logs
ENV PYTHONUNBUFFERED=1

# Use gunicorn to run in production mode
ENTRYPOINT [ "sh", "-c", "gunicorn --capture-output --log-level info --bind 0.0.0.0:${MODEL_SERVICE_PORT} src.serve_model:app" ]