import conf
from cache_policy_lru import CachePolicyLRU

class Cache:
    def __init__(self, disk):
        self.pool = {}
        self.prefetched = {}
        self.n_blks_cached_max = 0
        self.n_blks_cached = 0
        self.n_hits = 0
        self.n_miss = 0
        self.n_hits_prefetch = 0
        self.disk = disk
        self.policy = CachePolicyLRU()

    def flush(self):
        for lba in self.pool:
            if self.pool[lba]:
                self.disk.write(1, lba, lba+1)
        self.pool = {}
        self.n_blks_cached = 0

    def load(self, pid, lba_base, nblks):
        n_cache_hit = 0
        n_disk_io = 0
        for i in range(nblks):
            lba = lba_base + i
            if lba in self.pool:
                self.policy.hit(lba)
                self.n_hits += 1
                n_cache_hit += 1
                if lba in self.prefetched:
                    if not self.prefetched[lba]:
                        self.prefetched[lba] = True
                        self.n_hits_prefetch += 1
            else:                                           # disk access
                self.n_miss += 1
                n_disk_io += 1
                if self.is_cacheable(pid, lba, True):
                    n_disk_io += self.replace_cache(pid, lba)
        return n_cache_hit, n_disk_io


    def prefetch(self, pid, lba_base, nblks):
        n_cache_hit = 0
        n_disk_io = 0
        for i in range(nblks):
            lba = lba_base + i
            if not lba in self.pool:
                n_disk_io += 1
                n_disk_io += self.replace_cache(pid, lba)
                self.prefetched[lba] = False
            else:
                n_cache_hit += 1
        return n_cache_hit, n_disk_io

    def store(self, pid, lba_base, nblks):
        n_cache_hit = 0
        n_disk_io = 0
        for i in range(nblks):
            lba = lba_base + i
            if self.is_cacheable(pid, lba, False):
                if not lba in self.pool:
                    n_disk_io += self.replace_cache(pid, lba)
                n_disk_io += self.__update_cache(pid, lba)
            else:
                if lba in self.pool:
                    n_cache_hit += 1
                    n_disk_io += self.__update_cache(pid, lba)
                else:                                       # disk access
                    n_disk_io += 1
        return n_cache_hit, n_disk_io

    def __update_cache(self, pid, lba):
        self.pool[lba] = True
        if self.is_writethrough(pid, lba):
            self.pool[lba] = False
            return 1
        return 0

    def __insert(self, lba):
        lba_replaced = 0

        if self.n_blks_cached == conf.size_cache:
            lba_replaced = self.policy.replace()
        else:
            self.n_blks_cached += 1
            if self.n_blks_cached_max < self.n_blks_cached:
                self.n_blks_cached_max = self.n_blks_cached

        self.pool[lba] = False
        self.policy.insert(lba)

        return lba_replaced

    def replace_cache(self, pid, lba):
        lba_replaced = self.__insert(lba)
        if lba_replaced > 0:
            if self.pool[lba_replaced]:
                self.pool.pop(lba_replaced, None)
                self.prefetched.pop(lba_replaced, None)
                return 1
            self.pool.pop(lba_replaced, None)
            self.prefetched.pop(lba_replaced, None)
        return 0

    def is_cacheable(self, pid, lba, is_read):
        if not is_read:
            return False
        return True

    def is_writethrough(self, pid, lba):
        return False

    def report(self):
        totals = self.n_hits + self.n_miss
        hit = 0
        if totals > 0:
            hit = self.n_hits / totals * 100
        print("Cache Size: {}(Max Cached:{})".format(conf.size_cache, self.n_blks_cached_max))
        print("Cache Hit: {}%({}/{})".format(format(hit, ".2f"), self.n_hits, totals))
