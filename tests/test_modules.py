from modules.http_request import http_request
from modules.get_proxies import get_proxy_list

from pathlib import Path
import logging
import requests
import time

log = logging.getLogger(__name__)

def output_path(file_name):
    script_dir = Path(__file__).parent
    output_path = script_dir / "modules_outputs" / file_name
    return output_path

def test_http_request():
    test_session = requests.session()
    my_http_request = http_request('get', 'https://www.example.com', test_session)
    output_path("http_request.html").write_text(my_http_request(), encoding="utf-8")    

def test_get_proxies():
    test_session = requests.session()
    proxy_url = 'https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt'
    my_proxy_request = get_proxy_list(proxy_url, test_session)
    time.sleep(10)
    output_path("get_proxies.html").write_text("\n".join(my_proxy_request.working_proxies), encoding="utf-8")    