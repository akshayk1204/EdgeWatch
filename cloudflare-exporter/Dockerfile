FROM python:3.10-slim
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY cloudflare_exporter.py .
COPY .env .env

RUN pip install flask prometheus_client requests python-dotenv

CMD ["python", "cloudflare_exporter.py"]