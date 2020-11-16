from storage_default import StorageDefault

class StoragePrefetch(StorageDefault):
    def request_blk_read(self, req):
        super().request_blk_read(req)
        self.prefetch(req.pid, req.lba + req.nblks, req.nblks)
