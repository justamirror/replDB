import collections
import json
from . import key as KEYENCODE
from replit import database, db as DATABASE
from .builtins import base, observed_han
import inspect
sep = '$$'
class Counter():
    def __init__(self):
        self.c = 0
    def __str__(self):
        v = self.c
        self.c += 1
        return str(v)
c = Counter()
class _Types(collections.UserDict):
    def __init__(self, v={}):
        super().__init__(v)
    def __call__(self, v):
        if isinstance(v, str):
            self.value = json.loads(open(v).read())
        else:
            self.value = v
pslice_cache = {}

class Database(collections.UserDict):
    def __init__(self, *args):
        global _Types
        if len(args) == 1:
            self._db: database.Database = database.Database(args[0])
            self.prefix = ''
        else:
            self._db: database.Database = args[0]
            self.prefix: database.Database = args[1]
        self.types = _Types(base)
    @property
    def data(self):
        p = self._db.prefix(self.prefix)
        data = {}
        for k in p:
            k = k[len(self.prefix):]
            v = None
            if k == '$TYPE':
                continue
            #elif "$$" in k:
            #    continue
            elif k.endswith("$TYPE"):
                v = self.__getitem__(k[:-7], False)
                k = k[:-7]
            else:
                v = self.__getitem__(k, False)
            if "$$" in k:
                continue
            data[KEYENCODE.decode(k)] = v
        return data
    #def prefix(self, p)
    def __setitem__(self, oi, value):
        item = self.prefix+KEYENCODE.encode(oi)
        if value.__class__.__dict__.get('DB_TYPE'):
            self.register_type(value.__class__.DB_TYPE, value.__class__)
        if observed_han.get(value.__class__):
            self._db.set_raw(item+sep+"$TYPE", self.types[observed_han[value.__class__]])
            for key, v in observed_han[value.__class__].handle(value):
                self[oi+sep+key] = v
        elif self.types.get(value.__class__):
            self._db.set_raw(item+sep+"$TYPE", self.types[value.__class__])
            for key in value.db.keys():
               self[oi+sep+key] = value.db[key]
        else:
            self._db[item] = value
    def __delitem__(self, item):
        item = self.prefix+KEYENCODE.encode(item)
        del self._db[item]
    def __getitem__(self, item, encode=True):
        if encode:
            item = KEYENCODE.encode(item)
        item = self.prefix+item
        t = None
        try:
            t = self._db.get_raw(item+sep+"$TYPE")
        except:
            pass
        if self.types.get(t):
            db = Database(self._db, item+sep)
            argspec = inspect.getfullargspec(self.types[t])
            if argspec.varkw or len(argspec.args) > 2:
                i = self.types[t](db, **db)
            else:
                i = self.types[t](db)
            i.db = db
            return i
        return self._db[item]
    def register_type(self, value, name=None):
        if name == None:
            name = value.DB_TYPE
        self.types[name] = value
        self.types[value] = name
    def type(self, name=None):
        def type(value):
            self.register_type(value, name)
            return value
        return type
    def clear(self):
        for k in self._db.prefix(self.prefix):
            del self._db[k]


db: Database = Database(DATABASE, '')