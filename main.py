import requests 
import base64
import json
import random
from concurrent.futures import ThreadPoolExecutor
from json_loader import load_json

API_Data = load_json('API-Keys.json')
global_counter = {}

def error(message):
    raise Exception(message)

class http_session_manager:
    def __init__(self, headers):
        self.session_headers = {}
        for key in headers:
            self.session_headers[key] = headers[key]

class http_request:
    def __init__(self, type, url, session_headers, proxy={}, **params):
        self.url = url
        self.params = params
        self.proxy = proxy
        if type == 'get':
            self.response = requests.get(self.url, headers=session_headers, params=self.params, proxies=proxy, verify=False)
        elif type == 'post':
            self.response = requests.post(self.url, headers=session_headers, params=self.params, proxies=proxy, verify=False)
        else:
            print('invalid type!')

    def __call__(self):
        return self.response.text

################
###PROXY-LIST###
################

class get_proxy_list(http_request):
    def __init__(self, url, session_headers):
        super().__init__('get', url, session_headers)
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


############
###REDDIT###
############

class reddit_auth_token(http_request):
    def __init__(self, api, API_Data, session_headers={}):
        self.api = api
        if api:
            session_headers['content-type'] = 'application/x-www-form-urlencoded'
            session_headers['User-Agent'] = API_Data['app_name']
            session_headers['Authorization'] = f"Basic {str(base64.b64encode((f"{API_Data['app_ID']}:{API_Data['secret']}").encode('utf8')))[2:-1]}"
            super().__init__('post', 'https://www.reddit.com/api/v1/access_token', session_headers, grant_type='password', username=API_Data['username'], password=API_Data['password'])
        else:
            print('No API Key Needed for Proxy Requests.')

class check_and_refresh_auth_token(reddit_auth_token):
    def check_auth_code(self, API_Data):
        if (self.response.status_code == 401) and not ("auth_refresh_retried" in self):
            super().__init__(True, API_Data)
            self.auth_refresh_retried = True

class reddit_reutrn_subreddit_topics(http_request):
    def __init__(self, api, auth_token, session_headers, subreddit, proxy={}, previous_last_request_ID=''):
        self.api = api
        session_headers['Authorization'] = f'bearer {auth_token}'
        if api:
            super().__init__('get', f'https://oauth.reddit.com/r/{subreddit}/new?limit=100{'&after='+ previous_last_request_ID if previous_last_request_ID else ''}', session_headers)
        else:
            super().__init__('get', f'https://old.reddit.com/r/{subreddit}/new?limit=100{'&after='+ previous_last_request_ID if previous_last_request_ID else ''}', session_headers, proxy)
        

class reddit_user_history(http_request):
    def __init__(self, api, auth_token, session_headers, username, proxy={}, previous_last_request_ID=''):
        self.api = api
        if api:    
            session_headers['Authorization'] = f'bearer {auth_token}'
            super().__init__('get', f'https://oauth.reddit.com/user/{username}/overview?limit=100{'&after='+ previous_last_request_ID if previous_last_request_ID else ''}&sort=new', session_headers)
        else:    
            super().__init__('get', f'https://old.reddit.com/user/{username}/overview?limit=100{'&after='+ previous_last_request_ID if previous_last_request_ID else ''}&sort=new', session_headers, proxy)
        
        ##IF self.response.status_code == 403, generate new Auth Token and try again

class reddit_read_topic(http_request):
    def __init__(self, api, auth_token, session_headers, subreddit, post_id, proxy={}):
        self.api = api
        if api:
            session_headers['Authorization'] = f'bearer {auth_token}'
            super().__init__('get', f'https://oauth.reddit.com/r/{subreddit}/comments/{post_id}', session_headers)
        else:
            super().__init__('get', f'https://old.reddit.com/r/{subreddit}/comments/{post_id}', session_headers, proxy)
        ##IF self.response.status_code == 403, generate new Auth Token and try again

#################
###ARCHIVE.ORG###
#################

class get_pages_from_archive(http_request):
    def __init__(self, subreddit, session_headers):
        super().__init__('get', f'https://web.archive.org/cdx/search/cdx?url=https://www.reddit.com/r/{subreddit}&output=json', session_headers)

class handle_archive_page_list:
    def __init__(self, archive_page):
        pageJSON = json.loads(archive_page)
        self.archive_pages = []
        for item in pageJSON[1:]:
            self.archive_pages.append(item[1])

class read_archive_page(http_request):
    def __init__(self, index, archive_page_list, subreddit, session_headers):
        super().__init__('get', f'https://web.archive.org/web/{archive_page_list[index]}id_/https://www.reddit.com/r/{subreddit}', session_headers)



#########################
###THREADING AND QUEUE###
#########################
import threading
import queue

####
#Threading logic goes here
####


##########
###MAIN###
##########

proxy_list = get_proxy_list('https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt', {})
print(proxy_list())

#request = firstRedditRequest('https://www.example.com')
#request.printResponse()