import requests 
from pathlib import Path
import logging
import random


log = logging.getLogger(__name__)
script_dir = Path(__file__).parent
output_file = script_dir / 'output.txt'

class get_proxy_list:
    def __init__(self, url, session_headers):
        self.response = requests.get(url, headers=session_headers)
        self.proxy_list = self.response.text.split('\n')
        print(random.choice(self.proxy_list))
        print(random.choice(self.proxy_list))
        print(random.choice(self.proxy_list))
        output_file.write_text(str(self.proxy_list), encoding="utf-8")

get_proxy_list('https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt', {})