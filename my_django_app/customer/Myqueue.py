try: from Queue import Queue, Full, Empty
except: from queue import Queue, Full, Empty
from datetime import datetime



class MyQueue(Queue):
    "Wrapper around Queue that discards old items instead of blocking."
    def __init__(self, maxsize=10):
        assert type(maxsize) is int, "maxsize should be an integer"
        Queue.__init__(self, maxsize)

    def put(self, item):
        "Put an item into the queue, possibly discarding an old item."
        try:
            Queue.put(self, (datetime.now(), item), False)
        except Full:
            # If we're full, pop an item off and add on the end.
            Queue.get(self, False)
            Queue.put(self, (datetime.now(), item), False)

    def put_nowait(self, item):
        "Put an item into the queue, possibly discarding an old item."
        self.put(item)

    def get(self):
        "Get a tuple containing an item and the datetime it was entered."
        try:
            return Queue.get(self, False)
        except Empty:
            return None

    def get_nowait(self):
        "Get a tuple containing an item and the datetime it was entered."
        return self.get()


def main():
    "Simple test method, showing at least spec #4 working."
    queue = MyQueue(10)
    for i in range(1, 12):
        queue.put("Test item number %u" % i)

    while not queue.empty():
        time_and_data = queue.get()
        print("%s => %s" % time_and_data)


if __name__ == "__main__":
    main()