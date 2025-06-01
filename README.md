# EdgeWatch

**EdgeWatch** is a containerized monitoring stack that collects and visualizes real-time analytics from Cloudflare. It includes a custom Python-based Prometheus exporter and a Grafana dashboard to monitor metrics such as:

- Total requests
- Cache hit ratio
- Bandwidth served and saved
- WAF threat detection
- HTTP 4xx/5xx error breakdown

## 🚀 Features

- Cloudflare GraphQL API integration
- Prometheus for time-series storage
- Grafana dashboard for visualization
- Docker Compose setup for easy deployment
- Lightweight and production-ready

## 📦 Stack Overview

- **Exporter:** Python + Prometheus client
- **Database:** Prometheus
- **Dashboard:** Grafana
- **Deployment:** Docker Compose

## 📁 Project Structure

EdgeWatch/
├── cloudflare-exporter/
│ ├── cloudflare_exporter.py
│ ├── Dockerfile
│ ├── .env
├── prometheus/
│ ├── prometheus.yml
├── docker-compose.yml
├── requirements.txt

🌐 Domain Setup (Optional)
To use a custom domain (e.g. edgewatch.yourdomain.com) with HTTPS:

Install Nginx + Certbot on your server

Reverse proxy http://localhost:3000 via Nginx

Issue a certificate with Let's Encrypt

📊 Sample Metrics Visualized
Total Requests vs Cached Requests

Bandwidth Served vs Saved

Cache Hit Ratio Over Time

HTTP Error Breakdown (4xx/5xx)

Threats Blocked by WAF

🧩 License
MIT © 2025 — Akshay Kulkarni

<img width="1388" alt="image" src="https://github.com/user-attachments/assets/da6db5be-01bb-4de0-85ee-a9f874bc7b2c" />
<img width="1341" alt="image" src="https://github.com/user-attachments/assets/fd6db1b5-4c65-4951-bdcc-46935a2adb2b" />

