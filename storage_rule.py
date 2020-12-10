from storage_default import StorageDefault
import conf

class StorageRuleBased(StorageDefault):
    def __init__(self):
        super().__init__()
        self.last_blks_proc = {}
        self.last_blks = []

    def request_blk_read(self, req):
        super().request_blk_read(req)

        if conf.per_process_rule:
            is_seq = self.__is_sequential_proc(req)
        else:
            is_seq = self.__is_sequential(req.lba, self.last_blks)

        if is_seq:
                self.prefetch(req.pid, req.lba + req.nblks, req.nblks)

        lba_last = req.lba + req.nblks
        if conf.per_process_rule:
            self.__set_last_blk(lba_last, self.__get_proc_last_blks(req.pid))
        else:
            self.__set_last_blk(lba_last, self.last_blks)

    def __is_sequential_proc(self, req):
        last_blks = self.__get_proc_last_blks(req.pid)
        return self.__is_sequential(req.lba, last_blks)

    def __is_sequential(self, lba, last_blks):
        for blk in last_blks:
            if lba == blk:
                return True
        return False

    def __get_proc_last_blks(self, pid):
        if not pid in self.last_blks_proc:
            self.last_blks_proc[pid] = []

        return self.last_blks_proc[pid]

    def __set_last_blk(self, lba, last_blks):
        if len(last_blks) >= conf.n_refhist:
            last_blks.pop(0)
        last_blks.append(lba)
