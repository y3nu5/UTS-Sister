import time


class Stats:

    def __init__(self):

        self.received = 0
        self.unique_processed = 0
        self.duplicate_dropped = 0

        self.topics = set()

        self.start_time = time.time()

    def uptime(self):
        return int(time.time() - self.start_time)


stats = Stats()