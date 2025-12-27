from bs4 import BeautifulSoup

class parse_reddit_topic_list():
    def __init__(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        titles = soup.find_all(class_="thing")
        scraped_data = []
        for title in titles:
            topic_object = {}
            topic_object["topic_name"] = title["data-permalink"]
            topic_object["link_code"] = title["data-fullname"]
            topic_object["timestamp"] = title["data-timestamp"]
            topic_object["comment_count"] = title["data-comments-count"]
            topic_object["author"] = title["data-author"]
            scraped_data.append(topic_object)     
        self.scraped_data = scraped_data

class parse_reddit_user_history():
    def __init__(self, html_content, author):
        soup = BeautifulSoup(html_content, "html.parser")
        titles = soup.find_all(class_="thing")
        times = soup.find_all("time")
        comment_counts = soup.find_all(class_="bylink may-blank")
        scraped_data = []
        posted_count = 0
        for index, title in enumerate(titles):
            if topic_object["id"][:8] == "thing_t1": 
                topic_object = {}
                topic_object["topic_name"] = title["data-permalink"]
                topic_object["link_code"] = title["data-fullname"]
                topic_object["timestamp"] = times[index]["datetime"]
                topic_object["comment_count"] = comment_counts[index-posted_count].get_text().strip()
                topic_object["author"] = author
                scraped_data.append(topic_object)     
            elif topic_object["id"][:8] == "thing_t3":
                posted_count += 1
                topic_object = {}
                topic_object["topic_name"] = title["data-permalink"]
                topic_object["link_code"] = title["data-fullname"]
                topic_object["timestamp"] = title["data-timestamp"]
                topic_object["comment_count"] = title["data-comments-count"]
                topic_object["author"] = author
                scraped_data.append(topic_object) 
        self.scraped_data = scraped_data

class parse_reddit_topic_page():
    def __init__(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        titles = soup.find_all(class_="author")
        scraped_data = []
        for title in titles:
            topic_object = {}
            topic_object["topic_participant"] = title.get_text().strip()
            scraped_data.append(topic_object)     
        self.scraped_data = scraped_data