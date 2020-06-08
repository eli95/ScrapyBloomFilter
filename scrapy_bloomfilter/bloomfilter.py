from .defaults import BLOOMFILTER_BIT, BLOOMFILTER_HASH_NUMBER


class HashMap(object):
    def __init__(self, m, seed):
        self.m = m
        self.seed = seed
    
    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.m - 1) & ret


class BloomFilter(object):
    def __init__(self, server, key, bit=BLOOMFILTER_BIT, hash_number=BLOOMFILTER_HASH_NUMBER):
        self.m = 1 << bit
        self.seeds = range(hash_number)
        self.server = server
        self.key = key
        self.maps = [HashMap(self.m, seed) for seed in self.seeds]
    
    def exists(self, value):
        if not value:
            return False
        exist = True
        for map in self.maps:
            offset = map.hash(value)
            exist = exist & self.server.getbit(self.key, offset)
        return exist
    
    def insert(self, value):
        for f in self.maps:
            offset = f.hash(value)
            self.server.setbit(self.key, offset, 1)
