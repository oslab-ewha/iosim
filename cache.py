import conf
from cache_policy_lru import CachePolicyLRU

class Cache:
    def __init__(self):
        self.pool = {}
        self.n_blks_cached = 0
        self.n_hits = 0
        self.n_miss = 0
        self.policy = CachePolicyLRU()

    def fetch(self, lba):
        if lba in self.pool:
            self.policy.hit(lba)
            self.n_hits += 1
            return True

        self.n_miss += 1
        return False

    def insert(self, lba):
        lba_replaced = 0

        if self.n_blks_cached == conf.size_cache:
            lba_replaced = self.policy.replace()
            self.pool.pop(lba_replaced, None)
        else:
            self.n_blks_cached += 1

        self.pool[lba] = True
        self.policy.insert(lba)

        return lba_replaced
