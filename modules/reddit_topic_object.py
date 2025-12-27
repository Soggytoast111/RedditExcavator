from datetime import datetime

def check_and_convert_time(time):
    if not len(time) == 13:
        dt_obj = datetime.fromisoformat(time)
        unix_seconds = dt_obj.timestamp()
        unix_millis = int(unix_seconds * 1000)
        return unix_millis
    else:
        return time

class reddit_topic_object():
    def __init__(self, link_code, time_submitted, author, comment_count):
        self.topic_object = {
            link_code:{
                "time_submitted":check_and_convert_time(time_submitted),
                "author":author,
                "comment_count":comment_count
            }
        }
