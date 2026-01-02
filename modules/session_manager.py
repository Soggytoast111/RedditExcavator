from modules.get_proxies import get_proxy_list
import ua_generator
import requests
import json
import random
from pathlib import Path

proxy_list_file = Path(__file__).parents[1] / ".pytest_cache" / "v" / "my_working_proxies"

def ua_generate(): 
    ua = ua_generator.generate(device='desktop', browser=['chrome', 'edge'])
    return ua

def generate_working_proxies():
    try: 
        with open(proxy_list_file, 'r') as f:
            my_working_proxies = json.load(f)   
    except:
        test_session = requests.session()
        proxy_url = 'https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt'
        my_proxy_request = get_proxy_list(proxy_url, test_session)
        my_working_proxies = my_proxy_request.working_proxies
        proxy_list_file.write_text(json.dumps(my_working_proxies), encoding="utf-8")  
    return my_working_proxies

def new_session():
    my_new_session = requests.session()
    my_working_proxies = generate_working_proxies()
    selected_proxy = random.choice(my_working_proxies)
    ua = ua_generate()
    my_new_session.headers.update(ua.headers.get())
    print(f'I selected this proxy: {selected_proxy}')
    my_new_session.proxy = selected_proxy

    return my_new_session