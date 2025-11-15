FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY smsspamcollection ./smsspamcollection
COPY output ./output

EXPOSE 8081

CMD ["python", "src/serve_model.py"]
