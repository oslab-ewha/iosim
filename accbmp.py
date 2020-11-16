from reqhist import ReqHist
from accbmpcol import AccBmpCol
import conf

class AccBmp:
    def __init__(self):
        self.ts_last = 0
        self.bitcols = []
        self.__add_empty_bitcols(conf.width - 1)
        self.accbmpcol = AccBmpCol()
        self.reqhist = ReqHist()

    def access(self, req):
        accbit = self.reqhist.append(req)
        self.accbmpcol.access(req, accbit)

    def advance_ts(self, ts):
        diff_ts = ts - self.ts_last
        if diff_ts < conf.ts_intv:
            return
        n_emptys = int(diff_ts / conf.ts_intv)
        if n_emptys > 0:
            if n_emptys > conf.width - 1:
                n_emptys = conf.width - 1
            self.bitcols[0:n_emptys] = []
            self.__add_empty_bitcols(n_emptys)
        while self.ts_last + conf.ts_intv < ts:
            self.ts_last += conf.ts_intv

    def __add_empty_bitcols(self, n):
        bmpcol = AccBmpCol()
        for i in range(n):
            self.bitcols.append(bmpcol.bitcol())

    def bitmap(self):
        bmp = []
        for bc in self.bitcols:
            bmp.append(bc)
        bmp.append(self.accbmpcol.bitcol())
        return bmp
