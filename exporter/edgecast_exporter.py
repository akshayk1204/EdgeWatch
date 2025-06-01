from prometheus_client import start_http_server, Gauge
import random
import time

# Define metrics
cache_hit_ratio = Gauge('edgecast_cache_hit_ratio', 'Cache Hit Ratio from Edgecast')
cache_miss_ratio = Gauge('edgecast_cache_miss_ratio', 'Cache Miss Ratio from Edgecast')
requests_total = Gauge('edgecast_requests_total', 'Total number of requests served')
waf_blocked_requests_total = Gauge('edgecast_waf_blocked_requests_total', 'Total WAF blocked requests')
bot_traffic_percentage = Gauge('edgecast_bot_traffic_percentage', 'Estimated Bot Traffic Percentage')

def fetch_edgecast_data():
    # Simulate real data here — replace with actual Edgecast API calls later
    data = {
        'hit_ratio': round(random.uniform(0.7, 0.95), 2),
        'requests_total': random.randint(1000, 5000),
        'waf_blocked': random.randint(50, 200),
        'bot_traffic': round(random.uniform(0.1, 0.4), 2),
    }
    data['miss_ratio'] = round(1.0 - data['hit_ratio'], 2)
    return data

def update_metrics():
    while True:
        metrics = fetch_edgecast_data()
        
        # Set Prometheus metrics
        cache_hit_ratio.set(metrics['hit_ratio'])
        cache_miss_ratio.set(metrics['miss_ratio'])
        requests_total.set(metrics['requests_total'])
        waf_blocked_requests_total.set(metrics['waf_blocked'])
        bot_traffic_percentage.set(metrics['bot_traffic'])

        print(f"[Edgecast Exporter] Updated metrics: {metrics}")
        time.sleep(30)

if __name__ == '__main__':
    print("Starting Edgecast Exporter on port 8000...")
    start_http_server(8000)
    update_metrics()
