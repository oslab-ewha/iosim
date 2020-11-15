from storage_default import StorageDefault

class StoragePrefetch(StorageDefault):
    def request_blk_read(self, lba, nblks):
        super().request_blk_read(lba, nblks)
        super().request_blk_read(lba + nblks, nblks)
