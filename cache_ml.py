from cache import Cache

class CacheML(Cache):
    def __init__(self,disk):
        super().__init__(disk)
        self.scores_read = {}
        self.scores_write = {}

    def is_cacheable(self, pid, lba, is_read):
        score = self.get_score(pid, True)
        if score[0] < 0.2:
            return False
        return True

    def get_score(self, pid, is_read):
        if is_read:
            if not pid in self.scores_read:
                score = [0, 0, 1]
                self.scores_read[pid] = score
            else:
                score = self.scores_read[pid]
        else:
            if not pid in self.scores_write:
                score = [0, 0, 1]
                self.scores_write[pid] = score
            else:
                score = self.scores_write[pid]
        return score
            
