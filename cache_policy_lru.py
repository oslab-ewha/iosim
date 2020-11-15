class CachePolicyLRU:
    def __init__(self):
        self.lru = []

    def hit(self, lba):
        self.lru.remove(lba)
        self.lru.insert(0, lba)

    def insert(self, lba):
        self.lru.insert(0, lba)

    def replace(self):
        return self.lru.pop(-1)
