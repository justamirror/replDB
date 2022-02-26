from collections import UserDict, UserList
import collections
observed_han = {}
base = {}
def observed(db_name, type):
    def han(class_):
        observed_han[type] = class_
        base[db_name] = class_
        base[class_] = db_name
        return class_
    return han
def toInt(i):
    if not isinstance(i, int):
        raise TypeError(f"list indices must be integers or slices, not {i.__class__.__name__}")
    return int(i)
#@observed("LIST", list)
class ObservedList(collections.abc.MutableSequence):
    def __init__(self, db):
        self.__data = db
    @property
    def data(self):
        return self.__data
    @property
    def value(self):
        return list(self.data.values())
    def handle(d):
       return ((str(n), v) for (n, v) in enumerate(d))
    def __getitem__(self, i):
        return self.data[str(toInt(i))]
    def __setitem__(self, i, v):
        i = toInt(i)
        if i > len(self)-1:
            raise IndexError("list assignment index out of range")
        self.data[str(i)] = v
    def __delitem__(self, i):
        del self.data[str(i)]
    def __len__(self):
        return len(self.data)
    def insert(self, i, v):
        raise NotImplementedError("...Making this wouldnt be a good idea.")
    def append(self, value):
        self.data[len(self)] = value
    def __repr__(self):
        return str(self.value)
@observed("DICT", dict)
class ObservedDict(UserDict):
    def __init__(self, db):
        self.data = db
    @property
    def value(self):
        return self.data.data
    def handle(d):
       return d.items()