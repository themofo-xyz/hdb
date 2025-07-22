from proxyscrape import create_collector, get_proxyscrape_resource
import time
import ipaddress
import requests
import warnings

# Suppress warnings from requests
warnings.filterwarnings("ignore")

# Create a custom ProxyScrape API resource
proxyscrape_resource = get_proxyscrape_resource(proxytype='all', timeout=5000, ssl='all', anonymity='all', country='all')

# Create a collector
resource_types = ['https', 'http', 'socks4', 'socks5']
collector = create_collector('my-collector', resource_types=resource_types, resources=[proxyscrape_resource])

# Log resource types
print(f"Fetching proxies from resource types: {resource_types}, custom resource: proxyscrape_all")

# Retry fetching proxies
attempts = 3
proxies = None
for attempt in range(1, attempts + 1):
    print(f"Attempt {attempt}/{attempts}: Fetching proxies...")
    try:
        proxies = collector.get_proxies()
        if proxies:
            print(f"Found {len(proxies)} proxies.")
            break
        else:
            print("No proxies found in this attempt.")
    except Exception as e:
        print(f"Error fetching proxies: {e}")
    if attempt < attempts:
        print("Retrying in 5 seconds...")
        time.sleep(5)

# Function to test proxy type (optional)
def test_proxy_type(host, port, timeout=2):
    proxy_url = f"http://{host}:{port}"
    proxies = {"http": proxy_url, "https": proxy_url}
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=timeout, verify=False)
        if response.status_code == 200:
            return 'http'
    except requests.RequestException:
        pass
    try:
        response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=timeout, verify=False)
        if response.status_code == 200:
            return 'https'
    except requests.RequestException:
        pass
    return 'unknown'

# Process proxies
if proxies:
    fixed_proxies = []
    http_ports = [80, 8080, 8561, 3128, 8000]  # Common HTTP ports
    allowed_types = {'http', 'https', 'socks4', 'socks5'}
    
    for proxy in proxies:
        try:
            ipaddress.ip_address(proxy.host)
            port = int(proxy.port)
            
            # Assign type based on port or original type
            if port == 443:
                proxy_type = 'https'
            elif port in http_ports:
                proxy_type = 'http'
            elif port in [1080, 9050]:
                proxy_type = 'socks5'
            else:
                proxy_type = proxy.type if proxy.type in allowed_types else 'unknown'
            
            # Skip unknown proxies
            if proxy_type == 'unknown':
                continue
            
            # Optional: Test proxy (uncomment to enable)
            # tested_type = test_proxy_type(proxy.host, proxy.port)
            # if tested_type in allowed_types:
            #     proxy_type = tested_type
            # else:
            #     continue
            
            proxy_dict = {'host': proxy.host, 'port': port, 'type': proxy_type}
            fixed_proxies.append(proxy_dict)
        except ValueError:
            continue
        except (TypeError, ValueError):
            continue
    
    https_proxies = [p for p in fixed_proxies if p['type'] == 'https']
    print(f"Found {len(https_proxies)} HTTPS proxies out of {len(fixed_proxies)} total proxies.")
    
    with open('proxy.txt', 'w') as f:
        for proxy in fixed_proxies:
            proxy_line = f"{proxy['type']} {proxy['host']} {proxy['port']}"
            print(proxy_line)
            f.write(proxy_line + '\n')
    print("Proxies saved to proxy.txt")
else:
    print("No proxies found after all attempts. Check your internet connection or try again later.")

print("Happy hunting!")