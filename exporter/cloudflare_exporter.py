import os
import time
import requests
from prometheus_client import start_http_server, Gauge
from dotenv import load_dotenv

# Load environment variables from .env
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

CLOUDFLARE_API_KEY = os.getenv("CFLARE_API_KEY")
ZONE_ID = os.getenv("CFLARE_ZONE_ID")

BASE_URL = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/analytics/dashboard"

headers = {
    "Authorization": f"Bearer {CLOUDFLARE_API_KEY}",
    "Content-Type": "application/json"
}

# Prometheus metrics
cf_total_requests = Gauge('cloudflare_total_requests', 'Total number of requests')
cf_cache_hit_ratio = Gauge('cloudflare_cache_hit_ratio', 'Cache hit ratio')
cf_waf_blocked = Gauge('cloudflare_waf_blocked_requests', 'WAF blocked requests')
cf_bot_traffic_ratio = Gauge('cloudflare_bot_traffic_ratio', 'Bot traffic percentage')

def fetch_metrics():
    try:
        response = requests.get(BASE_URL, headers=headers, params={
            "since": "-30 minutes"
        })
        data = response.json()["result"]

        cf_total_requests.set(data["totals"]["requests"]["all"])
        cf_cache_hit_ratio.set(data["totals"]["requests"]["cached"] / data["totals"]["requests"]["all"])
        cf_waf_blocked.set(data["totals"]["threats"]["all"])
        cf_bot_traffic_ratio.set(data["totals"]["bot_management"]["score"]["bot"] / data["totals"]["requests"]["all"])
        print("✅ Metrics updated")

    except Exception as e:
        print(f"❌ Error fetching Cloudflare metrics: {e}")

if __name__ == "__main__":
    start_http_server(8000)
    print("🚀 Cloudflare Exporter running on port 8000")
    while True:
        fetch_metrics()
        time.sleep(60)
