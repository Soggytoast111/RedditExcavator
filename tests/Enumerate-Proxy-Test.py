import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import requests
import main
import random
from concurrent.futures import ThreadPoolExecutor


def check_proxy(proxy):
    try:
        # Use a reliable test URL like http://www.httpbin.org/ip to check if the IP changes
        response = requests.get('http://www.httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=5)
        if response.status_code == 200 and response.json().get('origin') != 'YOUR_REAL_IP': # Replace with your actual IP for comparison
            print(f"Proxy {proxy} is working and changing IP.")
            return True
        else:
            print(f"Proxy {proxy} returned status {response.status_code} or did not change IP.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Proxy {proxy} failed: {e}")
        return False

user_agents = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17']

session_headers = {'user-agent': random.choice(user_agents),
                   'Accept': 'application/json',
                   'Accept-Language': 'en-US',
                   'Connection': 'keep-alive'
                    }

proxy_list_response = main.get_proxy_list('https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt', session_headers)
proxy_list = proxy_list_response.proxy_list

with ThreadPoolExecutor(max_workers=10) as executor: # Adjust max_workers as needed
    results = executor.map(check_proxy, proxy_list)

working_proxies = [proxy for proxy, is_working in zip(proxy_list, results) if is_working]
print(f"\nWorking Proxies: {working_proxies}")