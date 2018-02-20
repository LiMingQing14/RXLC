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

    class T:
        def __init__(self, md5, size):
            self.md5 = md5
            self.size = size

    class Ts:
        def __init__(self):
            self.ts = []
        def add(self, t):
            self.ts.append(t)

        @staticmethod
        def default(o):
            ret = {}
            for x in o.ts:
                ret[x.md5] = {'md5': x.md5, 'size': x.size}
            return ret

    assets = Ts()
    assets.add(T("A", 1))
    assets.add(T("B", 2))

    _json = {
        'version': 0,
        'assets': assets
    }
    print json.dumps(_json, default=Ts.default, indent =4)