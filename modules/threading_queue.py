import threading
import queue

class resource_queue():
    def __init__(self, consumer_function):
        self.work_queue = queue.Queue()
        num_threads = 10
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=consumer_function, args=(self.work_queue,))
            t.daemon = True # Thread dies when main thread dies
            t.start()
            threads.append(t)
        self.work_queue.join()
        for i in range(num_threads):
            self.work_queue.put(None)
        for t in threads:
            t.join()

    def add_to_queue(self, data):
        self.work_queue.put(data)