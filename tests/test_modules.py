from modules.http_request import http_request
from modules.get_proxies import get_proxy_list
from modules.reddit_nav import reddit_reutrn_subreddit_topics, reddit_read_topic, reddit_user_history
from modules.reddit_nav_json import reddit_reutrn_subreddit_topics_json, reddit_read_topic_json, reddit_user_history_json, reddit_crawl_user_history_json
from modules.reddit_parse import parse_reddit_topic_list, parse_reddit_user_history, parse_reddit_topic_page
from modules.reddit_parse_json import parse_reddit_topic_list_json, parse_reddit_user_history_json, parse_reddit_topic_page_json
from modules.session_manager import ua_generate, new_session

from pathlib import Path
import pytest
import logging
import requests
import time
import random
import json

log = logging.getLogger(__name__)

def output_path(file_name):
    script_dir = Path(__file__).parent
    output_path = script_dir / "modules_outputs" / file_name
    return output_path

@pytest.fixture(scope="session")
def generate_working_proxies(pytestconfig):
    my_working_proxies = pytestconfig.cache.get("my_working_proxies", None)
    
    if my_working_proxies is None:
        test_session = requests.session()
        proxy_url = 'https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt'
        my_proxy_request = get_proxy_list(proxy_url, test_session)
        my_working_proxies = my_proxy_request.working_proxies
        pytestconfig.cache.set("my_working_proxies", my_proxy_request.working_proxies) 
    return my_working_proxies

#########
##TESTS##
#########

def test_http_request():
    test_session = requests.session()
    my_http_request = http_request('get', 'https://www.example.com', test_session)
    output_path("http_request.html").write_text(my_http_request(), encoding="utf-8")    

def test_get_proxies():
    test_session = requests.session()
    proxy_url = 'https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt'
    my_proxy_request = get_proxy_list(proxy_url, test_session)
    output_path("get_proxies.html").write_text("\n".join(my_proxy_request.working_proxies), encoding="utf-8")    

def test_flush_proxies():
    #"C:\Users\joncu\Dev\RedditExcavator\.pytest_cache\v\my_working_proxies"
    base_dir = Path(__file__).parents[1]
    file = base_dir / ".pytest_cache" / "v" / "my_working_proxies"
    if file.exists():
        file.unlink()
        print("File deleted.")
    else:
        print("File does not exist.")

def test_reddit_read_topic(generate_working_proxies):
    test_session = requests.session()
    #my_working_proxies = generate_working_proxies.config.cache.get("my_working_proxies", None)
    my_working_proxies = generate_working_proxies
    selected_proxy = random.choice(my_working_proxies)
    log.info(f'I selected this proxy: {selected_proxy}')
    my_read_topic = reddit_read_topic(test_session, {'https': selected_proxy}, 'smarthome', '1kfph4j')
    if my_read_topic.response.status_code != 200:
        pytest.fail(f"HTTP FAIL - Status Code: {my_read_topic.response.status_code}")
    log.info(f'Status Code of Request: {my_read_topic.response.status_code}')
    output_path("reddit_read_topic.html").write_text(my_read_topic(),  encoding="utf-8")
    assert my_read_topic   

def test_reddit_read_topic_json(generate_working_proxies):
    test_session = requests.session()
    #my_working_proxies = generate_working_proxies.config.cache.get("my_working_proxies", None)
    my_working_proxies = generate_working_proxies
    selected_proxy = random.choice(my_working_proxies)
    log.info(f'I selected this proxy: {selected_proxy}')
    my_read_topic = reddit_read_topic_json(test_session, {'https': selected_proxy}, 'NoStupidQuestions', '1py98mz')
    if my_read_topic.response.status_code != 200:
        pytest.fail(f"HTTP FAIL - Status Code: {my_read_topic.response.status_code}")
    log.info(f'Status Code of Request: {my_read_topic.response.status_code}')
    output_path("reddit_read_topic_json.json").write_text(my_read_topic(),  encoding="utf-8")
    assert my_read_topic   

def test_reddit_user_history(generate_working_proxies):
    test_session = requests.session()
    #my_working_proxies = generate_working_proxies.config.cache.get("my_working_proxies", None)
    my_working_proxies = generate_working_proxies
    selected_proxy = random.choice(my_working_proxies)
    log.info(f'I selected this proxy: {selected_proxy}')
    my_user_history = reddit_user_history(test_session, {'https': selected_proxy}, "Hlord369")
    if my_user_history.response.status_code != 200:
        pytest.fail(f"HTTP FAIL - Status Code: {my_user_history.response.status_code}")
    log.info(f'Status Code of Request: {my_user_history.response.status_code}')
    output_path("reddit_user_history.html").write_text(my_user_history(), encoding="utf-8")
    assert my_user_history  

def test_reddit_user_history_json(generate_working_proxies):
    test_session = requests.session()
    #my_working_proxies = generate_working_proxies.config.cache.get("my_working_proxies", None)
    my_working_proxies = generate_working_proxies
    selected_proxy = random.choice(my_working_proxies)
    log.info(f'I selected this proxy: {selected_proxy}')
    my_user_history = reddit_user_history_json(test_session, {'https': selected_proxy}, "Hlord369")
    if my_user_history.response.status_code != 200:
        pytest.fail(f"HTTP FAIL - Status Code: {my_user_history.response.status_code}")
    log.info(f'Status Code of Request: {my_user_history.response.status_code}')
    output_path("reddit_user_history_json.json").write_text(my_user_history(), encoding="utf-8")
    assert my_user_history 

def test_reddit_subreddit_topics(generate_working_proxies):
    test_session = requests.session()
    #my_working_proxies = generate_working_proxies.config.cache.get("my_working_proxies", None)
    my_working_proxies = generate_working_proxies
    selected_proxy = random.choice(my_working_proxies)
    log.info(f'I selected this proxy: {selected_proxy}')
    my_read_topic = reddit_reutrn_subreddit_topics(test_session, {'https': selected_proxy}, 'NoStupidQuestions')
    if my_read_topic.response.status_code != 200:
        pytest.fail(f"HTTP FAIL - Status Code: {my_read_topic.response.status_code}")
    log.info(f'Status Code of Request: {my_read_topic.response.status_code}')
    output_path("reddit_subreddit_topics.html").write_text(my_read_topic(),  encoding="utf-8")
    assert my_read_topic  

def test_reddit_subreddit_topics_json(generate_working_proxies):
    test_session = requests.session()
    #my_working_proxies = generate_working_proxies.config.cache.get("my_working_proxies", None)
    my_working_proxies = generate_working_proxies
    selected_proxy = random.choice(my_working_proxies)
    log.info(f'I selected this proxy: {selected_proxy}')
    my_read_topic = reddit_reutrn_subreddit_topics_json(test_session, {'https': selected_proxy}, 'NoStupidQuestions')
    if my_read_topic.response.status_code != 200:
        pytest.fail(f"HTTP FAIL - Status Code: {my_read_topic.response.status_code}")
    log.info(f'Status Code of Request: {my_read_topic.response.status_code}')
    output_path("reddit_subreddit_topics_json.json").write_text(my_read_topic(),  encoding="utf-8")
    assert my_read_topic  

def __deprecated__test_parse_reddit_topic_list():
    html_file_path = output_path("reddit_subreddit_topics.html")
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    my_parsed_data = parse_reddit_topic_list(html_content)
    output_path("parse_reddit_topic_list.html").write_text(json.dumps(my_parsed_data.scraped_data), encoding="utf-8")  

def test_parse_reddit_topic_list_json():
    html_file_path = output_path("reddit_subreddit_topics_json.json")
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    my_parsed_data = parse_reddit_topic_list_json(html_content)
    output_path("parse_reddit_topic_list_json.json").write_text(json.dumps(my_parsed_data.scraped_data), encoding="utf-8")

def __deprecated__test_parse_reddit_user_history():
    html_file_path = output_path("reddit_user_history.html")
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    my_parsed_data = parse_reddit_user_history(html_content)
    output_path("parse_reddit_user_history.html").write_text(json.dumps(my_parsed_data.scraped_data), encoding="utf-8") 

def test_parse_reddit_user_history_json():
    html_file_path = output_path("reddit_user_history_json.json")
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    my_parsed_data = parse_reddit_user_history_json(html_content)
    output_path("parse_reddit_user_history_json.json").write_text(json.dumps(my_parsed_data.scraped_data), encoding="utf-8") 

def __deprecated__test_parse_reddit_topic_page():
    html_file_path = output_path("reddit_read_topic.html")
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    my_parsed_data = parse_reddit_topic_page(html_content)
    output_path("parse_reddit_read_topic.html").write_text(json.dumps(my_parsed_data.scraped_data), encoding="utf-8") 

def test_parse_reddit_topic_page_json():
    html_file_path = output_path("reddit_read_topic_json.json")
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    my_parsed_data = parse_reddit_topic_page_json(html_content)
    output_path("parse_reddit_read_topic_json.json").write_text(json.dumps(my_parsed_data.scraped_data), encoding="utf-8") 

def test_reddit_crawl_user_history_json(generate_working_proxies):
    test_session = requests.session()
    #my_working_proxies = generate_working_proxies.config.cache.get("my_working_proxies", None)
    my_working_proxies = generate_working_proxies
    selected_proxy = random.choice(my_working_proxies)
    log.info(f'I selected this proxy: {selected_proxy}')
    crawled_user_history = reddit_crawl_user_history_json(test_session, {'https': selected_proxy}, "Hlord369")
    retry_counter=0
    while (not crawled_user_history.last_status_code == 200) and (retry_counter < 5):
        test_session = requests.session()
        my_working_proxies = generate_working_proxies
        selected_proxy = random.choice(my_working_proxies)
        log.info(f'I selected this proxy: {selected_proxy} - on retry attempt: {retry_counter+1}')
        crawled_user_history = reddit_crawl_user_history_json(test_session, {'https': selected_proxy}, "Hlord369")
        retry_counter+=1        
                
    output_path("reddit_crawl_user_history_json.json").write_text(json.dumps(crawled_user_history["processed_pages"]), encoding="utf-8")

def test_ua_generator():
    my_device = ua_generate()

    output_path("generated_ua_test.json").write_text(json.dumps(my_device.headers.get()), encoding="utf-8")

def test_session_manager():
    url = "https://postman-echo.com/get"
    my_session = new_session()

    response = my_session.get(url=url, proxies=my_session.proxies, verify=False)    
    output_path("session_manager_test.json").write_text(response.text, encoding="utf-8")
