FROM python:3.10-slim

WORKDIR /app

COPY cloudflare_exporter.py .

RUN pip install flask prometheus_client requests python-dotenv

CMD ["python", "cloudflare_exporter.py"]