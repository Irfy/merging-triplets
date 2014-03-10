#!/usr/bin/python

import random
import sys
import math

t_no = 10
if len(sys.argv) > 1:
    t_no = int(sys.argv[1])
max_val = int(math.ceil(math.log(t_no, 3))+2)
for i in xrange(t_no):
    print random.randrange(max_val), random.randrange(max_val), random.randrange(max_val)
