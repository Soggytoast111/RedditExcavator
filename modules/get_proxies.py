import requests
from modules.http_request import http_request 
from concurrent.futures import ThreadPoolExecutor

class get_proxy_list(http_request):
    def __init__(self, url, session):
        super().__init__('get', url, session)
        self.proxy_list = self.response.text.split('\n')
        with ThreadPoolExecutor(max_workers=10) as executor: # Adjust max_workers as needed
            results = executor.map(self.comb_proxy_list, self.proxy_list)
        working_proxies = [proxy for proxy, is_working in zip(self.proxy_list, results) if is_working]
        self.working_proxies = working_proxies

    def comb_proxy_list(self, proxy):
        try:
            response = requests.get('http://www.httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=2.5)
            if response.status_code == 200 and response.json().get('origin') != 'YOUR_REAL_IP': # Replace with your actual IP for comparison
                print(f"Proxy {proxy} is working and changing IP.")
                return True
            else:
                print(f"Proxy {proxy} returned status {response.status_code} or did not change IP.")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Proxy {proxy} failed: {e}")
            return False