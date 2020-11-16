class BIOReq:
    def __init__(self, row):
        if 'W' in row[4]:
            self.is_read = False
        elif 'R' in row[4]:
            self.is_read = True
        else:
            self.is_read = None
        self.ts = float(row[0])
        self.pid = int(row[2])
        self.lba =  int(row[5])
        self.nblks = int(row[6])

    def isOverlappedBy(self, req):
        last = self.lba + self.nblks - 1
        if (self.lba >= req.lba and self.lba < req.lba + req.nblks) or \
           (last >= req.lba and last < req.lba + req.nblks):
            return True
        return False

    def isSeqAccessedBy(self, req):
        if self.lba + self.nblks == req.lba:
            return True
        return False
