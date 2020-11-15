class TraceContext:
    def __init__(self, row):
        self.pid = int(row[2])
        self.command = row[7]
        self.refcnts = 0
        self.nread = 0
        self.nwrite = 0

    def __hash__(self):
        return hash((self.pid, self.command))

    def __eq__(self, other):
        if not isinstance(other, TraceContext):
            return NotImplemented

        return self.pid == other.pid and self.command == other.command

    def __str__(self):
        return "{}({}): {}(r:{},w:{})".format(self.command, self.pid, self.refcnts, self.nread, self.nwrite)

    def add(self, access):
        self.refcnts += 1
        if access.is_read:
            self.nread += 1
        else:
            self.nwrite += 1
