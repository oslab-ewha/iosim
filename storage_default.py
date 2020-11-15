from cache import Cache
from disk import Disk

class StorageDefault:
    def __init__(self):
        self.disk = Disk()
        self.cache = Cache(self.disk)

        self.n_accs = 0
        self.n_accs_read = 0
        self.n_accs_write = 0

    def request(self, req):
        if req.is_read:
            self.request_blk_read(req.lba, req.nblks)
        else:
            self.request_blk_write(req.lba, req.nblks)

    def request_blk_read(self, lba, nblks):
        self.n_accs += 1
        self.n_accs_read += 1

        self.cache.load(lba, nblks)

    def request_blk_write(self, lba, nblks):
        self.n_accs += 1
        self.n_accs_write += 1

        self.cache.store(lba, nblks)
