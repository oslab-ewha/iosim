import conf
from cache_policy_lru import CachePolicyLRU

class Cache:
    def __init__(self, disk):
        self.pool = {}
        self.n_blks_cached = 0
        self.n_hits = 0
        self.n_miss = 0
        self.disk = disk
        self.policy = CachePolicyLRU()

    def load(self, lba_base, nblks):
        for i in range(nblks):
            lba = lba_base + i
            if lba in self.pool:
                self.policy.hit(lba)
                self.n_hits += 1
            else:
                self.n_miss += 1
                self.disk.read(lba)
                if self.is_cacheable(lba, True):
                    self.replace_cache(lba)
        return False

    def store(self, lba_base, nblks):
        for i in range(nblks):
            lba = lba_base + i
            if self.is_cacheable(lba, False):
                if not lba in self.pool:
                    self.replace_cache(lba)
                if self.is_writethrough(lba):
                    self.disk.write(lba)
            else:
                self.disk.write(lba)

    def __insert(self, lba):
        lba_replaced = 0

        if self.n_blks_cached == conf.size_cache:
            lba_replaced = self.policy.replace()
            self.pool.pop(lba_replaced, None)
        else:
            self.n_blks_cached += 1

        self.pool[lba] = True
        self.policy.insert(lba)

        return lba_replaced

    def replace_cache(self, lba):
        lba_replaced = self.__insert(lba)
        if lba_replaced > 0:
            if not self.is_writethrough(lba_replaced):
                self.disk.write(lba_replaced)

    def is_cacheable(self, lba, is_read):
        return True

    def is_writethrough(self, lba):
        return False
