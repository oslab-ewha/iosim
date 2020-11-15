class Disk:
    def __init__(self):
        self.n_io_read = 0
        self.n_io_write = 0

    def read(self, lba):
        self.n_io_read += 1

    def write(self, lba):
        self.n_io_write += 1