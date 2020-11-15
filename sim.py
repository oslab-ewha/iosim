from trace_reader import TraceReader
import storage

class Simulator:
    def run(self):
        reader = TraceReader()
        stor = storage.get()

        for req in reader:
            stor.request(req)

        self.report(stor)

    def report(self, stor):
        totals = stor.cache.n_hits + stor.cache.n_miss
        hit = stor.cache.n_hits / totals * 100
        print("Cache Hit: {}%({}/{})".format(format(hit, ".2f"), stor.cache.n_hits, totals))
        print("Disk I/O: Read:{}, Write:{}".format(stor.disk.n_io_read, stor.disk.n_io_write))
