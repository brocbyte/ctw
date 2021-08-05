#!/usr/bin/env python3
import math

print(math.log2(0.5))

enwik4 = open("enwik4", 'rb').read()


def bitgen(x):
  for c in x:
    for i in range(8):
      yield int((c & (0x80 >> i)) != 0) 

from collections import defaultdict
lookup = defaultdict(lambda: [1, 2])

bg = bitgen(enwik4)
BACK_BITS = 8 
HH = 0.0

try:
  prevx = [-1]*BACK_BITS
  while 1:
    x = next(bg)
    px = tuple(prevx)

    p_1 = lookup[px][0] / lookup[px][1]
    p_x = p_1 if x == 1 else 1 - p_1 
    H = -math.log2(p_x)
    HH += H    

    lookup[px][0] += x == 1
    lookup[px][1] += 1
     
    prevx.append(x)
    prevx = prevx[-BACK_BITS:]

except StopIteration:
  pass

print("%.2f bytes of entropy" % (HH / 8))
