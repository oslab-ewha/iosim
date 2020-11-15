from trace_reader import TraceReader
from storage import Storage

class Simulator:
    def run(self):
        reader = TraceReader()
        storage = Storage()

        for req in reader:
            storage.request(req)

        self.report(storage)

    def report(self, storage):
        totals = storage.cache.n_hits + storage.cache.n_miss
        hit = storage.cache.n_hits / totals * 100
        print("Cache Hit: {}%({}/{})".format(format(hit, ".2f"), storage.cache.n_hits, totals))
        print("Disk I/O: Read:{}, Write:{}".format(storage.disk.n_io_read, storage.disk.n_io_write))
