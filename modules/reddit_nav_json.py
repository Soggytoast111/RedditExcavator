from modules.http_request import http_request 
from modules.reddit_parse_json import parse_reddit_user_history_json
import json

class reddit_reutrn_subreddit_topics_json(http_request):
    def __init__(self, session, proxy, subreddit, previous_last_request_ID=''):
        super().__init__('get', f'https://old.reddit.com/r/{subreddit}/new.json?limit=100{'&after='+ previous_last_request_ID if previous_last_request_ID else ''}', session, proxy=proxy)
        
class reddit_user_history_json(http_request):
    def __init__(self, session, proxy, username, previous_last_request_ID=''):
        super().__init__('get', f'https://old.reddit.com/user/{username}/overview.json?limit=100{'&after='+ previous_last_request_ID if previous_last_request_ID else ''}&sort=new', session, proxy=proxy)
        ##IF self.response.status_code == 403, generate new Auth Token and try again

class reddit_read_topic_json(http_request):
    def __init__(self, session, proxy, subreddit, post_id):
        super().__init__('get', f'https://old.reddit.com/r/{subreddit}/comments/{post_id}.json', session, proxy=proxy)
        ##IF self.response.status_code == 403, generate new Auth Token and try again

class reddit_crawl_user_history_json():
    def __init__(self, session, proxy, username):
        page_json = {"data": {"after": 0}}
        self.processed_pages = []
        while not page_json["data"]["after"] == "null":
            user_history_page = reddit_user_history_json(session, proxy, username, user_history_page["data"]["after"])
            self.last_status_code = user_history_page.status_code()
            page_json = json.dumps(user_history_page())
            processed_page = parse_reddit_user_history_json(user_history_page(), self.last_status_code)
            self.processed_pages.append(processed_page) 
    pass

class reddit_crawl_subreddit_topics():
    pass
