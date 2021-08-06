#!/usr/bin/env python3
import math

enwik4 = open("enwik4", 'rb').read()


def bitgen(x):
  for c in x:
    for i in range(8):
      yield int((c & (0x80 >> i)) != 0) 


from coder import Coder

p_0 = 0.115
l = [1, 0, 0, 1, 0, 1, 0, 0]
print("orig: " + str(l))
ones = sum(l)
zeros = len(l) - ones

enc = Coder()
for x in l:
  enc.code(p_0, x)

coded = enc.getCoded()
# print("coded: " + str(coded))

dec = Coder(ob = coded)
decoded = []

try:
  while 1:
    x = dec.code(p_0)
    decoded.append(x)
except StopIteration:
  pass
    

print("deco: " + str(decoded))


# print("real: %d bits, should: < %.2f" % (len(enc.getCoded()), ones * -math.log2(1 - p_0) + zeros * -math.log2(p_0) + 2.0))

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
