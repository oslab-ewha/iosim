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
        self.context = None
