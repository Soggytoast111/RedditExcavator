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
            topic_object["author"] = title["data-author"]
            scraped_data.append(topic_object)     
        self.scraped_data = scraped_data

class parse_reddit_user_history():
    def __init__(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        titles = soup.find_all(class_="thing")
        times = soup.find_all("time")
        scraped_data = []
        for index, title in enumerate(titles):
            topic_object = {}
            topic_object["topic_name"] = title["data-permalink"]
            topic_object["link_code"] = title["data-fullname"]
            topic_object["timestamp"] = times[index]["datetime"]
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