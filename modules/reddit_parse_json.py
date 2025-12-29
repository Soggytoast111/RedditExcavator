import json

class parse_reddit_topic_list_json():
    def __init__(self, html_content):
        html_json = json.loads(html_content)
        scraped_data = []
        for entry in html_json["data"]["children"]:
            topic_object = {}
            topic_object["topic_name"] = entry["data"]["title"]
            topic_object["link_code"] = entry["data"]["name"]
            topic_object["permalink"] = entry["data"]["permalink"]
            topic_object["url"] = entry["data"]["url"]
            topic_object["timestamp"] = entry["data"]["created"]
            topic_object["comment_count"] = entry["data"]["num_comments"]
            topic_object["author"] = entry["data"]["author"]
            topic_object["summary"] = entry["data"]["selftext"]
            scraped_data.append(topic_object)     
        self.scraped_data = scraped_data

class parse_reddit_user_history_json():
    def __init__(self, html_content):
        html_json = json.loads(html_content)
        scraped_data = []
        for entry in html_json["data"]["children"]:
            if entry["kind"] == "t3":
                topic_object = {}
                topic_object["topic_name"] = entry["data"]["title"]
                topic_object["link_code"] = entry["data"]["name"]
                topic_object["permalink"] = entry["data"]["permalink"]
                topic_object["url"] = entry["data"]["url"]
                topic_object["timestamp"] = entry["data"]["created"]
                topic_object["comment_count"] = entry["data"]["num_comments"]
                topic_object["author"] = entry["data"]["author"]
                topic_object["summary"] = entry["data"]["selftext"]
                scraped_data.append(topic_object)     
            elif entry["kind"] == "t1":
                topic_object = {}
                topic_object["topic_name"] = entry["data"]["link_title"]
                topic_object["link_code"] = entry["data"]["link_id"]
                topic_object["permalink"] = entry["data"]["link_permalink"]
                topic_object["url"] = entry["data"]["link_url"]
                topic_object["timestamp"] = entry["data"]["created"]
                topic_object["comment_count"] = entry["data"]["num_comments"]
                topic_object["author"] = entry["data"]["author"]
                topic_object["summary"] = ""
        self.scraped_data = scraped_data

class parse_reddit_topic_page_json():
    def __init__(self, html_content):
        html_json = json.loads(html_content)
        scraped_data = []
        for comment in html_json[0]["data"]["children"]:
            topic_object = {}
            topic_object["author"] = comment["data"]["author"]
            scraped_data.append(topic_object)     
        for comment in html_json[1]["data"]["children"]:
            topic_object = {}
            topic_object["author"] = comment["data"]["author"]
            scraped_data.append(topic_object) 
        self.scraped_data = scraped_data