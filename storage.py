from cache import Cache
from disk import Disk

class Storage:
    def __init__(self):
        self.cache = Cache()
        self.disk = Disk()

        self.n_accs = 0
        self.n_accs_read = 0
        self.n_accs_write = 0

    def request(self, req):
        for i in range(req.nblks):
            lba = req.lba + i
            if req.is_read:
                self.request_blk_read(lba)
            else:
                self.request_blk_write(lba)

    def request_blk_read(self, lba):
        self.n_accs += 1
        self.n_accs_read += 1
        if not self.cache.fetch(lba):
            self.disk.read(lba)
            if self.is_cacheable(lba, True):
                self.replace_cache(lba)

    def request_blk_write(self, lba):
        if self.is_cacheable(lba, False):
            self.replace_cache(lba)
            if self.is_writethrough(lba):
                self.disk.write(lba)
        else:
            self.disk.write(lba)

    def replace_cache(self, lba):
        lba_replaced = self.cache.insert(lba)
        if lba_replaced > 0:
            if not self.is_writethrough(lba_replaced):
                self.disk.write(lba_replaced)

    def is_cacheable(self, lba, is_read):
        return True

    def is_writethrough(self, lba):
        return False
