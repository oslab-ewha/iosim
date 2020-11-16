from accbit import AccBit
import logger
import conf

class AccBmpCol:
    def __init__(self):
        self.bits = []
        for i in range(conf.height):
            self.bits.append(AccBit())

    def access(self, req, accbit):
        if req.lba > conf.lba_max:
            logger.error("too large lba: {}, max:{}".format(req.lba, conf.lba_max))
            exit(1)

        idx = int((req.lba - 1) / float(conf.lba_max) * conf.height)
        self.bits[idx].merge(accbit)

    def bitcol(self):
        bitcol = []
        for b in self.bits:
            bitcol.append(b.getval())
        return bitcol
