from pathlib import Path
import logging
import main
import json_loader
import json
import ast
import pytest
import random

log = logging.getLogger(__name__)
script_dir = Path(__file__).parent
http_test_path = script_dir / "outputs" / "http_test.html"
proxy_http_test_path = script_dir / "outputs" / "proxy_http_test.html"

get_proxy_test_path = script_dir / "outputs" / "get_proxy_test.txt"

reddit_auth_test_path = script_dir / "outputs" / "reddit_auth_test.json"
reddit_return_sub_test_path = script_dir / "outputs" / "reddit_sub_return_test.json"
reddit_return_user_history_test_path = script_dir / "outputs" / "reddit_user_history_return_test.json"
reddit_read_topic_test_path = script_dir / "outputs" / "reddit_read_topic_test.json"
reddit_return_user_history_test_proxy_path = script_dir / "outputs" / "reddit_user_history_proxy.html"


proxy_reddit_read_topic_test_path = script_dir / "outputs" / "proxy_reddit_read_topic_test.html"

archive_get_pages_test_path = script_dir / "outputs" / "archive_get_pages_test.json"
handle_archive_pages_test_path = script_dir / "outputs" / "handle_archive_pages_test.json"
read_archive_page_test_path = script_dir / "outputs" / "read_archive_page_test.html"

auth_json = json_loader.load_json(reddit_auth_test_path)

##################
##HEADER / PROXY##
##################
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

###############
###HTTP TEST###
###############

def test_http_request():
    session_headers = {'content-type': 'application/x-www-form-urlencoded', 'content-type2': 'application/xxx-www-form-urlsencoded'}
    my_http_request = main.http_request('get', 'https://www.example.com', session_headers,  help='a', me='b', world='c')
    http_test_path.write_text(my_http_request(), encoding="utf-8")    

def test_http_with_proxy():
    my_proxy_request = main.get_proxy_list('https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt', session_headers)
    proxy_list = my_proxy_request.working_proxies    
    selected_proxy = random.choice(proxy_list)
    log.info(f'I selected this random Proxy From List: {selected_proxy}')
    my_proxy_http_request = main.http_request('get', 'https://icanhazip.com/', session_headers, {'https': selected_proxy})
    proxy_http_test_path.write_text(my_proxy_http_request(), encoding="utf-8")
    if my_proxy_http_request.response.status_code != 200:
        pytest.fail(f"HTTP FAIL - Status Code: {my_proxy_http_request.response.status_code}")

#####################
###PROXY-LIST TEST###
#####################

def test_get_proxies():
    my_proxy_request = main.get_proxy_list('https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt', session_headers)
    if my_proxy_request.response.status_code != 200:
        pytest.fail(f"HTTP FAIL - Status Code: {my_proxy_request.response.status_code}")    
    #log.info(f'A Random Proxy From List: {random.choice(my_proxy_request.proxy_list)}')
    get_proxy_test_path.write_text(json.dumps(my_proxy_request.working_proxies))
    assert isinstance(my_proxy_request.working_proxies, list)

##################
###REDDIT TESTS###
##################
#STATUS CODES: 
#429 - Rate Limited
#403 - ??
#401 - Expired Token?
#404 - Object not found


##########
#WITH API#
##########

def test_get_reddit_auth_token():
    mytoken = main.reddit_auth_token(True, main.API_Data) 
    if mytoken.response.status_code != 200:
        pytest.fail(f"HTTP FAIL - Status Code: {mytoken.response.status_code}")
    log.info(f'Status Code of Request: {mytoken.response.status_code}')
    reddit_auth_test_path.write_text(mytoken())
    assert mytoken

def test_return_subreddit_topics():
    my_subreddit_topics = main.reddit_reutrn_subreddit_topics(True, auth_json['access_token'], session_headers, 'AskConservatives')
    if my_subreddit_topics.response.status_code != 200:
        pytest.fail(f"HTTP FAIL - Status Code: {my_subreddit_topics.response.status_code}")
    log.info(f'Status Code of Request: {my_subreddit_topics.response.status_code}')
    reddit_return_sub_test_path.write_text(my_subreddit_topics())
    assert my_subreddit_topics

def test_return_user_history():
    my_user_history = main.reddit_user_history(True, auth_json['access_token'], session_headers, 'SportNo2179')
    if my_user_history.response.status_code != 200:
        pytest.fail(f"HTTP FAIL - Status Code: {my_user_history.response.status_code}")
    log.info(f'Status Code of Request: {my_user_history.response.status_code}')
    reddit_return_user_history_test_path.write_text(my_user_history())
    assert my_user_history    

def test_read_topic():
    my_read_topic = main.reddit_read_topic(True, auth_json['access_token'], session_headers, 'smarthome', '1kfph4j')
    if my_read_topic.response.status_code != 200:
        pytest.fail(f"HTTP FAIL - Status Code: {my_read_topic.response.status_code}")
    log.info(f'Status Code of Request: {my_read_topic.response.status_code}')
    reddit_read_topic_test_path.write_text(my_read_topic())
    assert my_read_topic   

#################
#WITH HTTP PROXY#
#################

def test_read_topic_proxy():
    selected_proxy = random.choice(proxy_list)
    log.info(f'I selected this proxy: {selected_proxy}')
    my_read_topic = main.reddit_read_topic(False, auth_json['access_token'], session_headers, 'smarthome', '1kfph4j', {'https': selected_proxy})
    if my_read_topic.response.status_code != 200:
        pytest.fail(f"HTTP FAIL - Status Code: {my_read_topic.response.status_code}")
    log.info(f'Status Code of Request: {my_read_topic.response.status_code}')
    proxy_reddit_read_topic_test_path.write_text(my_read_topic(),  encoding="utf-8")
    assert my_read_topic   

def test_return_user_history_proxy():
    selected_proxy = random.choice(proxy_list)
    log.info(f'I selected this proxy: {selected_proxy}')
    my_user_history = main.reddit_user_history(False, auth_json['access_token'], session_headers, 'SportNo2179', {'https': selected_proxy})
    if my_user_history.response.status_code != 200:
        pytest.fail(f"HTTP FAIL - Status Code: {my_user_history.response.status_code}")
    log.info(f'Status Code of Request: {my_user_history.response.status_code}')
    reddit_return_user_history_test_proxy_path.write_text(my_user_history(), encoding="utf-8")
    assert my_user_history  


#######################
###ARCHIVE.ORG TESTS###
#######################

def test_get_archive_pages():
    my_archive_pages = main.get_pages_from_archive('AskConservatives', session_headers)
    log.info(f'Status Code of Request: {my_archive_pages.response.status_code}')
    archive_get_pages_test_path.write_text(my_archive_pages())
    assert my_archive_pages

def test_my_parsed_archive():
    with archive_get_pages_test_path.open('r') as f:
        archive_response_content = f.read()
    my_parsed_archive_pages = main.handle_archive_page_list(archive_response_content)
    handle_archive_pages_test_path.write_text(str(my_parsed_archive_pages.archive_pages))
    assert my_parsed_archive_pages

def test_read_archive_page():
    with handle_archive_pages_test_path.open('r') as f:
        archive_pages_content = f.read()
    archive_pages_list = ast.literal_eval(archive_pages_content)
    my_read_archive_page = main.read_archive_page(2, archive_pages_list, 'AskConservatives', session_headers)
    read_archive_page_test_path.write_text(my_read_archive_page(),  encoding="utf-8")