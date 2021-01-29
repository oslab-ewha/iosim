import conf

class QueuedRequest:
    def __init__(self, nblks, lba_start, lba_end, is_read):
        self.nblks = nblks
        self.is_read = is_read
        self.lba_start = lba_start
        self.lba_end = lba_end

    def calc_processing_time(self, lba_last):
        if lba_last == self.lba_start:
            return self.nblks * conf.disk_transmission_time
        else:
            return conf.disk_setup_time + self.nblks * conf.disk_transmission_time