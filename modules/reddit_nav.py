from modules.http_request import http_request 

class reddit_reutrn_subreddit_topics(http_request):
    def __init__(self, session, proxy, subreddit, previous_last_request_ID=''):
        super().__init__('get', f'https://old.reddit.com/r/{subreddit}/new?limit=100{'&after='+ previous_last_request_ID if previous_last_request_ID else ''}', session, proxy=proxy)
        
class reddit_user_history(http_request):
    def __init__(self, session, proxy, username, previous_last_request_ID=''):
        super().__init__('get', f'https://old.reddit.com/user/{username}/overview?limit=100{'&after='+ previous_last_request_ID if previous_last_request_ID else ''}&sort=new', session, proxy=proxy)
        ##IF self.response.status_code == 403, generate new Auth Token and try again

class reddit_read_topic(http_request):
    def __init__(self, session, proxy, subreddit, post_id):
        super().__init__('get', f'https://old.reddit.com/r/{subreddit}/comments/{post_id}', session, proxy=proxy)
        ##IF self.response.status_code == 403, generate new Auth Token and try again

class reddit_crawl_user_history(reddit_reutrn_subreddit_topics):
    def __init__(self, username):
        pass
    pass

class reddit_crawl_subreddit_topics():
    pass
