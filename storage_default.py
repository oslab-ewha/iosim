from cache import Cache
from disk import Disk
import conf

class StorageDefault:
    def __init__(self):
        self.disk = Disk()
        self.cache = Cache(self.disk)

        self.n_accs = 0
        self.n_accs_read = 0
        self.n_accs_write = 0
        self.n_prefetch = 0
        self.n_prefetch_blk = 0

        self.time_slot = 1                          # time slot to measure bandwidth
        self.simtime = 0
        self.ts_start = 0
        self.total_read = 0
        self.total_write = 0
        self.n_timeslots = 0
        self.data_read = 0
        self.data_write = 0
        self.max_read = 0
        self.max_write = 0
        self.max_total = 0

    def flush(self):
        self.cache.flush()

    def request(self, req):
        self.simtime = req.ts
        if req.ts >= self.ts_start + self.time_slot:
            self.ts_start = int(req.ts / self.time_slot) * self.time_slot
            self.calc_bandwidth()
        if req.is_read:
            self.request_blk_read(req)
        else:
            self.request_blk_write(req)
        self.add_blk_done(req.is_read, req.nblks)

    def request_blk_read(self, req):
        self.n_accs += 1
        self.n_accs_read += 1

        self.cache.load(req.pid, req.lba, req.nblks)

    def request_blk_write(self, req):
        self.n_accs += 1
        self.n_accs_write += 1

        self.cache.store(req.pid, req.lba, req.nblks)

    def prefetch(self, pid, lba_base, nblks):
        self.cache.prefetch(pid, lba_base, nblks)
        self.n_prefetch += 1
        self.n_prefetch_blk += nblks

    def add_blk_done(self, is_read, nblks):
        if is_read:
            self.data_read += nblks * 512
        else:
            self.data_write += nblks * 512

    def calc_bandwidth(self):
        self.total_read += self.data_read / self.time_slot
        self.total_write += self.data_write / self.time_slot
        avg_read = self.data_read / self.time_slot
        avg_write = self.data_write / self.time_slot
        avg_total = (self.data_read + self.data_write) / self.time_slot
        if avg_read > self.max_read:
            self.max_read = avg_read
        if avg_write > self.max_write:
            self.max_write = avg_write
        if avg_total > self.max_total:
            self.max_total = avg_total
        self.n_timeslots += 1
        self.data_read = 0
        self.data_write = 0

    def report(self):
        print("Req Read:{}, Req Write:{}".format(self.n_accs_read, self.n_accs_write))
        try:
            print("Total Bandwidth (Average, Maximum): {} MB/s, {} MB/s".format(format((self.total_read + self.total_write) / self.n_timeslots  / (1024*1024), ".2f"), format(self.max_total / (1024*1024), ".2f")))
            print("Read Bandwidth (Average, Maximum): {} MB/s, {} MB/s".format(format(self.total_read / self.n_timeslots / (1024*1024), ".2f"), format(self.max_read / (1024*1024), ".2f")))
            print("Write Bandwidth (Average, Maximum): {} MB/s, {} MB/s".format(format(self.total_write / self.n_timeslots / (1024*1024), ".2f"), format(self.max_write / (1024*1024), ".2f")))
        except(ZeroDivisionError):
            print("Time range is too small to calculate bandwidth")
        print("# of prefetch: {}".format(self.n_prefetch))
        if self.n_prefetch != 0:
            hit = self.cache.n_hits_prefetch / self.n_prefetch_blk * 100
        else:
            hit = 0
        print("Prefetch Accuracy : {}%({}/{})".format(format(hit, ".2f"), self.cache.n_hits_prefetch, self.n_prefetch_blk))
        self.cache.report()
        self.disk.report()