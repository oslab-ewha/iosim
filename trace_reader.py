import csv
from trace_context import TraceContext
from bioreq import BIOReq
import conf

class TraceReader:
    def __init__(self):
        self.contexts = {}
        self.reader = None
        self.__load()

    def __load(self):
        try:
            f = open(conf.path, "r")
        except IOError:
            logger.error("trace file not found: {}".format(conf.path))
            exit(1)

        self.reader = csv.reader(f, delimiter = ',')
        return True

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            row = next(self.reader)
            if row[3] == 'I':
                return self.__getBIOReq(row)

    def __getBIOReq(self, row):
        req = BIOReq(row)
        ctx = TraceContext(row)
        if ctx in self.contexts:
            req.context = self.contexts[ctx]
        else:
            self.contexts[ctx] = ctx
            req.context = ctx

        req.context.add(req)
        return req
