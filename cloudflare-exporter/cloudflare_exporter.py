import os
import time
import requests
import json
import argparse
from datetime import datetime, timedelta
from prometheus_client import start_http_server, Gauge
from dotenv import load_dotenv

# Load .env variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

CLOUDFLARE_API_KEY = os.getenv("CFLARE_API_KEY")
ZONE_ID = os.getenv("CFLARE_ZONE_ID")

GRAPHQL_URL = "https://api.cloudflare.com/client/v4/graphql"
HEADERS = {
    "Authorization": f"Bearer {CLOUDFLARE_API_KEY}",
    "Content-Type": "application/json"
}

# Prometheus Metrics
cf_total_requests = Gauge('cloudflare_total_requests', 'Total number of requests')
cf_cache_hit_ratio = Gauge('cloudflare_cache_hit_ratio', 'Cache hit ratio percentage (0-100)')
cf_waf_blocked = Gauge('cloudflare_waf_blocked_requests', 'WAF blocked requests')
cf_total_bytes = Gauge('cloudflare_total_bytes', 'Total bytes served')
cf_bandwidth_saved = Gauge('cloudflare_bandwidth_saved_bytes', 'Bandwidth saved via caching')
cf_data_transferred_gb = Gauge('cloudflare_data_transferred_gb', 'Total data transferred (GB)')
cf_4xx_errors = Gauge('cloudflare_4xx_errors', '4xx Client Errors')
cf_5xx_errors = Gauge('cloudflare_5xx_errors', '5xx Server Errors')

def fetch_metrics():
    # Calculate time filter for last 24 hours
    time_filter = (datetime.utcnow() - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    query = {
        "query": f"""
        query($zoneTag: String!) {{
          viewer {{
            zones(filter: {{zoneTag: $zoneTag}}) {{
              httpRequests1hGroups(
                limit: 1,
                filter: {{ datetime_gt: "{time_filter}" }}
              ) {{
                sum {{
                  requests
                  cachedRequests
                  bytes
                  cachedBytes
                  threats
                  responseStatusMap {{
                    edgeResponseStatus
                    requests
                  }}
                }}
              }}
            }}
          }}
        }}
        """,
        "variables": {
            "zoneTag": ZONE_ID
        }
    }

    try:
        print("📡 Fetching metrics from Cloudflare API...")
        response = requests.post(
            GRAPHQL_URL,
            headers=HEADERS,
            json=query,
            timeout=15  # Increased timeout for more complex query
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("errors"):
            print(f"❌ GraphQL Errors: {json.dumps(data['errors'], indent=2)}")
            return
            
        zones = data.get("data", {}).get("viewer", {}).get("zones", [])
        if not zones:
            print("⚠️ No zones data returned - check Zone ID")
            return
            
        groups = zones[0].get("httpRequests1hGroups", [])
        if not groups:
            print("⚠️ No request groups data available")
            return
            
        http_data = groups[0].get("sum", {})
        
        # Set all metrics
        total_requests = http_data.get("requests", 0)
        cached_requests = http_data.get("cachedRequests", 0)
        cached_bytes = http_data.get("cachedBytes", 0)
        
        cf_total_requests.set(total_requests)
        cf_cache_hit_ratio.set((cached_requests / total_requests * 100) if total_requests else 0)
        cf_waf_blocked.set(http_data.get("threats", 0))
        cf_total_bytes.set(http_data.get("bytes", 0))
        cf_bandwidth_saved.set(cached_bytes)
        cf_data_transferred_gb.set(http_data.get("bytes", 0) / (1024 ** 3))

        # Process status codes
        status_map = http_data.get("responseStatusMap", [])
        status_4xx = 0
        status_5xx = 0
        
        for status in status_map:
            code = status.get("edgeResponseStatus", 0)
            count = status.get("requests", 0)
            if 400 <= code < 500:
                status_4xx += count
            elif code >= 500:
                status_5xx += count
        
        cf_4xx_errors.set(status_4xx)
        cf_5xx_errors.set(status_5xx)
        
        print(f"✅ Metrics updated - "
              f"Requests: {total_requests}, "
              f"Cached: {cached_requests} ({cached_requests/total_requests:.1%}), "
              f"4xx Errors: {status_4xx}, "
              f"5xx Errors: {status_5xx}")
        
    except Exception as e:
        print(f"🔥 Failed to fetch metrics: {str(e)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8001)
    args = parser.parse_args()

    print(f"🚀 Starting Cloudflare Prometheus Exporter on port {args.port}")
    start_http_server(args.port)

    while True:
        fetch_metrics()
        time.sleep(60)

if __name__ == "__main__":
    main()