from cache import Cache
from disk import Disk
import conf

class StorageDefault:
    def __init__(self):
        self.disk = Disk(self)
        self.cache = Cache(self.disk)

        self.n_accs = 0
        self.n_accs_read = 0
        self.n_accs_write = 0
        self.n_prefetch = 0
        self.n_prefetch_blk = 0

        self.ts_start = 0
        self.total_read = 0
        self.total_write = 0
        self.total_rw = 0
        self.n_timeslots = 0
        self.data_read = []
        self.data_write = []
        self.data_rw = []
        self.max_read = 0
        self.max_write = 0
        self.max_rw = 0

    def flush(self):
        self.cache.flush()

    def request(self, req):
        if req.is_read:
            self.request_blk_read(req)
        else:
            self.request_blk_write(req)

    def request_blk_read(self, req):
        self.n_accs += 1
        self.n_accs_read += 1

        n_cache_hit, n_disk_io = self.cache.load(req.pid, req.lba, req.nblks)
        if n_disk_io:                                                     # A case of disk access
            last_lba = req.lba + req.nblks
            self.disk.read(n_disk_io, req.lba, last_lba)
        if n_cache_hit:                                                   # A case of cache hit
            self.add_blk_done(req.ts, n_cache_hit, req.is_read)

    def request_blk_write(self, req):
        self.n_accs += 1
        self.n_accs_write += 1

        n_cache_hit, n_disk_io = self.cache.store(req.pid, req.lba, req.nblks)
        if n_disk_io:                                                   # A case of disk access
            last_lba = req.lba + req.nblks
            self.disk.write(n_disk_io, req.lba, last_lba)
        if n_cache_hit:                                                  # A case of cache hit
            self.add_blk_done(req.ts, n_cache_hit, req.is_read)

    def prefetch(self, req):
        n_cache_hit, n_disk_io = self.cache.prefetch(req.pid, req.lba + req.nblks, req.nblks)
        self.n_prefetch += 1
        self.n_prefetch_blk += req.nblks
        last_lba = req.lba + 2* req.nblks
        if req.is_read:
            self.disk.read(n_disk_io, req.lba + req.nblks, last_lba)
        else:
            self.disk.write(n_disk_io, req.lba + req.nblks, last_lba)
        if n_cache_hit:
            self.add_blk_done(req.ts, n_cache_hit, req.is_read)

    def add_blk_done(self, ts, nblks, is_read):
        time_range = int(ts / conf.time_slot) * conf.time_slot                          # calculate the time range
        while len(self.data_rw) <=  time_range:
            self.data_read.append(0)
            self.data_write.append(0)
            self.data_rw.append(0)
        if is_read:
            self.data_read[time_range] += nblks * 512
        else:
            self.data_write[time_range] += nblks * 512
        self.data_rw[time_range] += nblks * 512

    def calc_bandwidth(self):
        self.n_timeslots = len(self.data_rw)                                            # total number of time slots
        self.total_read = sum(self.data_read) / conf.time_slot
        self.total_write = sum(self.data_write) / conf.time_slot
        self.total_rw = sum(self.data_rw) / conf.time_slot
        self.max_read = max(self.data_read) / conf.time_slot
        self.max_write = max(self.data_write) / conf.time_slot
        self.max_rw = max(self.data_rw) / conf.time_slot

    def report(self):
        print("Req Read:{}, Req Write:{}".format(self.n_accs_read, self.n_accs_write))
        print("# of prefetch: {}".format(self.n_prefetch))
        if self.n_prefetch != 0:
            hit = self.cache.n_hits_prefetch / self.n_prefetch_blk * 100
        else:
            hit = 0
        print("Prefetch Accuracy : {}%({}/{})".format(format(hit, ".2f"), self.cache.n_hits_prefetch, self.n_prefetch_blk))
        self.cache.report()
        self.disk.report()
        try:
            self.calc_bandwidth()
            print("Total Bandwidth (Average, Maximum): {} MB/s, {} MB/s".format(format((self.total_read + self.total_write) / self.n_timeslots  / (1024*1024), ".2f"), format(self.max_rw / (1024*1024), ".2f")))
            print("Read Bandwidth (Average, Maximum): {} MB/s, {} MB/s".format(format(self.total_read / self.n_timeslots / (1024*1024), ".2f"), format(self.max_read / (1024*1024), ".2f")))
            print("Write Bandwidth (Average, Maximum): {} MB/s, {} MB/s".format(format(self.total_write / self.n_timeslots / (1024*1024), ".2f"), format(self.max_write / (1024*1024), ".2f")))
        except(ZeroDivisionError):
            print("Time range is too small to calculate bandwidth")