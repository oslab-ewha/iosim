import conf
from queued_request import QueuedRequest

class Disk:
    def __init__(self, storage):
        self.n_io_read = 0
        self.n_io_write = 0
        self.disk_queue = []                                    # QueuedRequest object
        self.stor = storage
        self.lba_last = 0
        self.processing_residual = 0
        self.simtime = conf.ts_start

    def read(self, nblks, lba_start, lba_end):
        self.n_io_read += nblks
        queued_request = QueuedRequest(nblks, lba_start, lba_end, True)
        self.disk_queue.append(queued_request)

    def write(self, nblks, lba_start, lba_end):
        self.n_io_write += nblks
        queued_request = QueuedRequest(nblks, lba_start, lba_end, False)
        self.disk_queue.append(queued_request)

    def process_queue(self, simtime_max):                                                # process disk_queue (time limit is arriving time of next request)
        while True:
            if self.disk_queue:                                                         # when disk queue is not empty, process first request in the queue
                req = self.disk_queue[0]
            else:                                                                       # when disk queue is empty (No requests to process)
                self.simtime = simtime_max
                return

            proctime = req.calc_processing_time(self.lba_last) - self.processing_residual
            end_time = self.simtime + proctime

            if end_time <= simtime_max:                                              # when the request is finished in the time range of this term
                self.simtime = end_time
                self.stor.add_blk_done(self.simtime, req.nblks, req.is_read)
                self.disk_queue.pop(0)
                self.lba_last = req.lba_end
                self.processing_residual = 0
            else:                                                                       # when the request is not finished in the time range of this term
                self.processing_residual += simtime_max - self.simtime
                self.simtime = simtime_max
                break

    def process_rest(self):                                                             # handle rest requests in disk queue after all requests came in
        self.process_queue(conf.ts_end)

    def report(self):
        print("Disk Read:{}, Disk Write:{}".format(self.n_io_read, self.n_io_write))