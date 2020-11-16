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

    def load(self, pid, lba_base, nblks):
        for i in range(nblks):
            lba = lba_base + i
            if lba in self.pool:
                self.policy.hit(lba)
                self.n_hits += 1
            else:
                self.n_miss += 1
                self.disk.read(lba)
                if self.is_cacheable(pid, lba, True):
                    self.replace_cache(pid, lba)

    def store(self, pid, lba_base, nblks):
        for i in range(nblks):
            lba = lba_base + i
            if self.is_cacheable(pid, lba, False):
                if not lba in self.pool:
                    self.replace_cache(pid, lba)
                if self.is_writethrough(pid, lba):
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

    def replace_cache(self, pid, lba):
        lba_replaced = self.__insert(lba)
        if lba_replaced > 0:
            if not self.is_writethrough(pid, lba_replaced):
                self.disk.write(lba_replaced)

    def is_cacheable(self, pid, lba, is_read):
        return True

    def is_writethrough(self, pid, lba):
        return False

    def report(self):
        totals = self.n_hits + self.n_miss
        hit = self.n_hits / totals * 100
        print("Cache Size: {}(Cached:{})".format(conf.size_cache, self.n_blks_cached))
        print("Cache Hit: {}%({}/{})".format(format(hit, ".2f"), self.n_hits, totals))
