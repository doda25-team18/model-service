FROM python:3.12.9-slim

WORKDIR /app


COPY requirements.txt ./requirements.txt
# Install dependencies first so this layer can be reused when src changes but requirements does not
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
# Copy model, should be changed in F10
COPY output ./output

# Gunicorn needs this to resolve the imports correctly
ENV PYTHONPATH=/app/src
ENV MODEL_SERVICE_PORT=8081


# Use gunicorn to run in production mode
ENTRYPOINT [ "sh", "-c", "gunicorn --bind 0.0.0.0:${MODEL_SERVICE_PORT} src.serve_model:app" ]
