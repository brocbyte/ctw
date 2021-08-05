#!/usr/bin/env python3
import math

enwik4 = open("enwik4", 'rb').read()


def bitgen(x):
  for c in x:
    for i in range(8):
      yield int((c & (0x80 >> i)) != 0) 


from coder import Coder

enc = Coder()
p_0 = 0.5
for i in [0, 1, 0, 1, 0]:
  enc.code(p_0 if i == 0 else 1 - p_0, i)
print(enc.ob)

exit(0)

from collections import defaultdict
lookup = defaultdict(lambda: [0, 0])

bg = bitgen(enwik4)
BACK_BITS = 16 
H = 0.0

try:
  prevx = [-1]*BACK_BITS
  while 1:
    x = next(bg)
    px = tuple(prevx)
    # https://en.wikipedia.org/wiki/Krichevsky%E2%80%93Trofimov_estimator
    p_x = (lookup[px][x] + 0.5) / (lookup[px][0]+lookup[px][1]+1)

    H += -math.log2(p_x)

    lookup[px][x] += 1
     
    prevx.append(x)
    prevx = prevx[-BACK_BITS:]

except StopIteration:
  pass

print("%.2f bytes of entropy" % (H / 8))
