import sys
import getopt
import logger

path = None
size_cache = 128
storage_type = 'default'

class Conf:
    def __init__(self, usage):
        self.usage = usage
        self.__parseArgs("hc:t:")

    def __parseArgs(self, optspec):
        global  path, size_cache, storage_type

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

        if len(args) < 1:
            logger.error("path required")
            exit(1)

        path = args[0]

def parse(usage_func):
    Conf(usage_func)
