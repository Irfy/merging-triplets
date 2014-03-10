#!/usr/bin/python

from __future__ import print_function

import sys
import math
import getopt
from string import split
from copy import deepcopy
from collections import namedtuple

Mergable = namedtuple('Mergable', 'i j t max_merges')

def triplet_merge(t1, t2):
    for k in xrange(3):
        k_ = (k + 1) % 3
        if (t1[k] == t2[k] and t1[k_] == t2[k_]):
            k__ = (k_ + 1) % 3
            t = range(3)
            t[k] = t1[k]
            t[k_] = t1[k_]
            t[k__] = t1[k__] | t2[k__]
            return tuple(t)
    return None

def get_mergables(data):
    mergables = []
    for i in xrange(len(data)-1):
        for j in xrange(i+1, len(data)):
            triplet = triplet_merge(data[i], data[j])
            if triplet:
                mergables.append(Mergable(i, j, triplet, 0))
    return mergables

def memodict(f):
    """ Memoization decorator for a function taking a single argument """
    class memodict(dict):
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret 
    return memodict().__getitem__

def merge(data_m):
    data, m = data_m
    data = list(data)
    data[m.i] = m.t
    del data[m.j]
    return data

merge = memodict(merge)

def find_best_merge(data, lookahead, last_m):
    mergables = get_mergables(data)
    debug(lookahead, 'after ({0},{1}): {2} mergables, data: {3}'.format(last_m.i, last_m.j, len(mergables), data))
    if not mergables:
        return None
    if lookahead == 0:
        return mergables[0]

    max_merges = 0
    max_m = mergables[0]
    for m in mergables:
        data_ = merge((tuple(data), m))
        if lookahead == 1:
            mergables_ = get_mergables(data_)
            debug(lookahead-1, 'after ({0},{1}): {2} mergables, data:'.format(m.i, m.j, len(mergables_)), data_)
            if len(mergables_) > max_merges:
                max_merges = len(mergables_)
                max_m = m
        else:
            m_ = find_best_merge(data_, lookahead-1, m)
            if m_ is None:
                continue
            m_max_merges = m_.max_merges+1
            if m_max_merges > max_merges:
                max_merges = m_max_merges
                max_m = m
    max_m = Mergable(max_m.i, max_m.j, max_m.t, max_merges)
    if True or max_merges > 10:
        debug (lookahead, "lookahead: {0}, max_m: {1}".format(lookahead, max_m))
    return max_m
    
def print_verbose(lookahead, *args):
    lvl = global_lookahead + 1 - lookahead
    digits = int(math.log10(global_lookahead+1))+1
    arrows = '-> ' * (lvl-1) + '->'
    if lookahead == -1:
        lvl = 'X'
    else:
        lvl -= 1
    print('lvl {0: >{1}} {2}'.format(lvl, digits, arrows), *args)

def print_nothing(*args):
    None

global_lookahead = 3
debug = print_nothing

for arg in sys.argv[1:]:
    if arg == '-v':
        debug = print_verbose
    elif arg == '-h':
        print("{} [-v] [-h] [<lookahead>] < triplet_file".format(sys.argv[0]))
        print("-v turns on verbose output, -h prints this help, <lookahead> sets a lookahead different from {}".format(global_lookahead))
        sys.exit(0)
    else:
        global_lookahead = int(arg)
        if global_lookahead < 0:
            raise ValueError("lookahead may not be negative")

data = map(tuple, map (lambda triplet: map (int, triplet), map (split, sys.stdin.readlines())))

m = Mergable(None,None,None,None)
while True:
    m = find_best_merge(data, global_lookahead, m)
    if not m:
        break
    #print("best merge is {}\n".format(m))
    data = merge((tuple(data), m))
#print("ended with %d triplets: %s" % (len(data), data))
print(len(data))
