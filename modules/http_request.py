class http_request:
    def __init__(self, type, url, session, proxy={}, data={}):
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