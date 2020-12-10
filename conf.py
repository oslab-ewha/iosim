import sys
import getopt
import logger

path = None
size_cache = 128
storage_type = 'default'
ts_start = 0
ts_end = 100000000
ts_intv = 0.0001
width = 5
height = 10
lba_max = 0

per_process = False

# rule model
n_refhist = 1

# ml model
model_type = 'cnn'
path_model = None

class Conf:
    def __init__(self, usage):
        self.usage = usage
        self.__parseArgs("hc:t:G:u:T:L:m:M:pb:")

    def __parseArgs(self, optspec):
        global  path, size_cache, storage_type, ts_intv, width, height, lba_max, per_process, n_refhist
        global  model_type, path_model

        try:
            opts, args = getopt.getopt(sys.argv[1:], optspec)
        except getopt.GetoptError:
            logger.error("invalid option")
            self.usage()
            exit(1)

        for o, a in opts:
            if o == '-h':
                self.usage()
                exit(0)
            if o == '-c':
                size_cache = int(a)
            elif o == '-t':
                storage_type = a
            elif o == '-u':
                ts_intv = int(a)
            elif o == '-G':
                self.__parse_bmp_dim(a)
            elif o == '-T':
                self.__parse_ts_range(a)
            elif o == '-L':
                lba_max = int(a)
            elif o == '-m':
                path_model = a
            elif o == '-M':
                model_type = a
            elif o == '-p':
                per_process = True
            elif o == '-b':
                n_refhist = int(a)

        if len(args) < 1:
            logger.error("path required")
            exit(1)
        if storage_type == 'ml':
            if lba_max == 0:
                logger.error("maximum lba is required")
                exit(1)
            if path_model is None:
                logger.error("ML storage requires a path for model")
                exit(1)

        path = args[0]

    def __parse_bmp_dim(self, dim):
        global  width, height

        if 'x' in dim:
            width, height = dim.split(sep='x', maxsplit=1)
            width = int(width)
            height = int(height)

    def __parse_ts_range(self, range):
        global      ts_start, ts_end

        if not '-' in range:
            ts_start = float(range)
        else:
            start, end = range.split(sep='-', maxsplit=1)
            ts_start = float(start)
            ts_end = float(end)

def parse(usage_func):
    Conf(usage_func)
