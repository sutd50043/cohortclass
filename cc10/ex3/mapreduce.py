'''
Works for both python v2 and v3
'''

import sys
if sys.version_info[0] == 3:
    from functools import reduce
else:
    pass


def flatMap(f,l):
    ll = map(f,l)
    return reduce(lambda x,y:x+y, ll, [])


def lift_if(p,x):
    if p(x):
        return [x]
    else:
        return []

def filter(p,l):
    return flatMap(lambda x:lift_if(p,x), l)


def merge(kvls1, kvls2):
    if len(kvls1) == 0: return kvls2
    elif len(kvls2) == 0: return kvls1
    else:
        ((k1,vl1), tl1) = (kvls1[0], kvls1[1:])
        ((k2,vl2), tl2) = (kvls2[0], kvls2[1:])
        if k1 == k2: return [(k1,vl1+vl2)]+merge(tl1,tl2)
        elif k1 < k2: return [(k1,vl1)]+merge(tl1,kvls2)
        else: return [(k2,vl2)]+merge(kvls1, tl2)

def shuffle(kvs):
    kvls = map(lambda kv: [(kv[0], [kv[1]])], kvs)
    return reduce(merge, kvls, [])


def reduceByKey(f, kvs, acc):
    s = shuffle(kvs)
    return map(lambda p: (p[0], reduce(f,p[1],acc)), s)


def reduceByKey2(agg, kvs):
    s = shuffle(kvs)
    return map(agg, s)
