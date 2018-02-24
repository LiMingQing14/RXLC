import re

template = """{
    "major_version": {pmajor_version},
    "minor_version": {pminor_version}
}"""

def func(matched):
    data = {'major_version': 4, 'minor_version': 5}
    return str(data[matched.group('value')])

if __name__ == '__main__':
    # print template
    # print re.sub('{p(?P<value>\w+)}', func, template)

    import json

    class T(json.JSONEncoder):
        def __init__(self, md5, size):
            json.JSONEncoder.__init__(self)
            self.md5 = md5
            self.size = size

        # @staticmethod
        # def default(o):
        #     return {'md5': o.md5, 'size': o.size}
        def default(self):
            return {'md5': self.md5, 'size': self.size}

    class Ts(dict):
        def __init__(self):
            dict.__init__(self)

        def add(self, t):
            # dict.__setitem__(self, t.md5, t)
            self[t.md5] = t

    assets = Ts()
    assets.add(T("A", 1))
    assets.add(T("B", 2))

    class UserEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, T):
                return obj.default()
            return json.JSONEncoder.default(self, obj)

    _json = {
        'version': 0,
        'assets': assets
    }
    # print json.dumps(_json, default = T.default, indent = 4)
    # print json.dumps(_json, cls = UserEncoder, indent = 4)
    # print json.dumps(_json)

    class L:
        def __init__(self, a, b):
            self._a = a
            self._b = b

        def __repr__(self):
            return "(%d-%d)" % (self._a, self._b)

        def set(self, a, b):
            self._a = a
            self._b = b

    class M:
        def __init__(self):
            self._list = []

        def __iter__(self):
            return self._list.__iter__()

        def __repr__(self):
            ret = [repr(x) for x in self._list]
            return ','.join(ret)

        # def append(self, item):
        #     self._list.append(item)

        # def __getattribute__(self, *args, **kwargs):
        #     print("__getattribute__() is called")
        #     return object.__getattribute__(self, *args, **kwargs)

        def __getattr__(self, name):
            # print("__getattr__() is called ")
            # return name + " from getattr"
            return getattr(self._list, name)

        # def __get__(self, instance, owner):
        #     print("__get__() is called", instance, owner)
        #     return self

    m = M()
    m.append(L(1, 1))
    m.append(L(2, 2))
    m.append(L(3, 3))

    n = M()
    n.append(L(11, 11))
    n.append(L(12, 12))
    n.append(L(13, 13))

    # print(m)
    # print(n)
    # m.extend(n)
    # print(m)
    # print(n)

    # print(len(m))

    class Celsius(object):
        def __init__(self, temperature = 0):
            self._temperature = temperature

        def to_fahrenheit(self):
            return (self.temperature * 1.8) + 32

        @property
        def temperature(self):
            print("Getting value")
            return self._temperature

        @temperature.setter
        def temperature(self, value):
            if value < -273:
                raise ValueError("Temperature below -273 is not possible")
            print("Setting value")
            self._temperature = value

    # c = Celsius()
    # print c._temperature
    # c.temperature = 37.77777777777
    # print c.to_fahrenheit()
    # print c._temperature

    # print __file__
    # import os
    # print os.getcwd()
    # print os.path.abspath(os.path.join(os.getcwd(), '..'))

    class L(object):
        def __init__(self):
            super(L, self).__init__()
            self.__list = []

        def __getattr__(self, name):
            return getattr(self.__list, name)

        def __len__(self):
            return self.__list.__len__()

        def __repr__(self):
            return ','.join([str(x) for x in self.__list])

    l1 = L()
    l2 = L()

    # l1.append(1)
    # l1.append(2)
    l2.append(3)
    l2.append(4)
    ll = l1 or l2
    print ll == l1
    print ll == l2