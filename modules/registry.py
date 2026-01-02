class registry():
    def __init__(self):
        self["processed_users"] = set()
        self["processed_topics"] = set()

    def update_users(self, user):
        self["processed_users"].add(user)
    
    def update_topics(self, topic):
        self["processed_topics"].add(topic)