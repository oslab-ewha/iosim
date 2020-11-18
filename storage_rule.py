from storage_default import StorageDefault

class StorageRuleBased(StorageDefault):
    def __init__(self):
        super().__init__()
        self.last_blks = {}

    def request_blk_read(self, req):
        super().request_blk_read(req)
        last_blk = self.get_last_blk(req.pid)
        if last_blk == req.lba:
            self.prefetch(req.pid, last_blk + req.nblks, req.nblks)
        self.last_blks[req.pid] = req.lba + req.nblks

    def get_last_blk(self, pid):
        if pid in self.last_blks:
            return self.last_blks[pid]
        else:
            self.last_blks[pid] = 0
            return 0
