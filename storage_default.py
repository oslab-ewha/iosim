from cache import Cache
from disk import Disk

class StorageDefault:
    def __init__(self):
        self.disk = Disk()
        self.cache = Cache(self.disk)

        self.n_accs = 0
        self.n_accs_read = 0
        self.n_accs_write = 0
        self.n_prefetch = 0

    def request(self, req):
        if req.is_read:
            self.request_blk_read(req)
        else:
            self.request_blk_write(req)

    def request_blk_read(self, req):
        self.n_accs += 1
        self.n_accs_read += 1

        self.cache.load(req.pid, req.lba, req.nblks)

    def request_blk_write(self, req):
        self.n_accs += 1
        self.n_accs_write += 1

        self.cache.store(req.pid, req.lba, req.nblks)

    def prefetch(self, pid, lba_base, nblks):
        self.cache.load(pid, lba_base, nblks)
        self.n_prefetch += nblks

    def report(self):
        print("Req Read:{}, Req Write:{}".format(self.n_accs_read, self.n_accs_write))
        print("# of prefetch: {}".format(self.n_prefetch))
        self.cache.report()
        self.disk.report()
