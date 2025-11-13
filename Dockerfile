FROM python:3.12.9-slim

WORKDIR /app


COPY requirements.txt ./requirements.txt
# Install dependencies first so this layer can be reused when src changes but requirements does not
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
# Copy model, should be changed in F10
COPY output/model.joblib ./output/model.joblib

# Gunicorn needs this to resolve the imports correctly
ENV PYTHONPATH=/app/src



# Use gunicorn to run in production mode
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:8081", "src.serve_model:app" ]
