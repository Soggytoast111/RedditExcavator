from modules.session_manager import new_session

class http_request:
    def __init__(self, type, url, session, proxy={}, data={}):
        self.active_session = session
        retry_count = 0
        if type == 'get':
            self.response = session.get(url=url, proxies=proxy, data=data,verify=False)
        elif type == 'post':
            self.response = session.post(url=url, proxies=proxy, data=data,verify=False)
        else:
            print('invalid type!')
        while ((self.response.status_code is not 200) and retry_count < 6):  
            session = new_session()
            self.active_session = session
            retry_count += 1
            if type == 'get':
                self.response = session.get(url=url, proxies=proxy, data=data,verify=False)
            elif type == 'post':
                self.response = session.post(url=url, proxies=proxy, data=data,verify=False)
            else:
                print('invalid type!')

    def __call__(self):
        return self.response.text
    
    def status_code(self):
        return self.response.status_code