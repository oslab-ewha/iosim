from accbit import AccBit
import conf

class ReqHist:
    def __init__(self):
        self.reqs = []

    def append(self, req):
        if req.ts > conf.ts_intv:
            ts_old = req.ts - conf.ts_intv
            self.__clearOutOldReqs(ts_old)
        accbit = self.__getAccBit(req)
        self.reqs.append(req)
        return accbit

    def __getAccBit(self, req):
        accbit = AccBit()
        for r in self.reqs:
            if r.isOverlappedBy(req):
                accbit.setHit(req.is_read)
            elif r.isSeqAccessedBy(req):
                accbit.setSeq(req.is_read)
        if not accbit.has_hit and not accbit.has_seq:
            accbit.setRnd(req.is_read)
        return accbit

    def __clearOutOldReqs(self, ts):
        idx = 0
        for req in self.reqs:
            if req.ts >= ts:
                break
            idx += 1
        self.reqs = self.reqs[idx:]
