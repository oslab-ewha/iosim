from storage_default import StorageDefault
from accbmp import AccBmp
from cache_ml import CacheML
import model
import conf

class StorageML(StorageDefault):
    def __init__(self):
        super().__init__()
        self.cache = CacheML(self.disk)
        self.ts = 0
        self.accbmps_proc = {}
        self.accbmp = AccBmp()
        model.load()

    def request_blk_read(self, req):
        if conf.per_process:
            if req.pid in self.accbmps_proc:
                accbmp = self.accbmps_proc[req.pid]
            else:
                accbmp = AccBmp()
                self.accbmps_proc[req.pid] = accbmp
            for pid in self.accbmps_proc:
                self.accbmps_proc[pid].advance_ts(req.ts)
        else:
            accbmp = self.accbmp
            accbmp.advance_ts(req.ts)

        accbmp.access(req)

        super().request_blk_read(req)

        score_read, score_write = model.predict(accbmp)
        self.cache.score_read = score_read
        self.cache.score_write = score_write

        if score_read[1] > 0.5:
            self.prefetch(req)
