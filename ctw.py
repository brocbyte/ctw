#!/usr/bin/env python3
import math

enwik4 = open("enwik4", 'rb').read()[:1000]
print(enwik4)


def bitgen(x):
  for c in x:
    for i in range(8):
      yield int((c & (0x80 >> i)) != 0) 


from coder import Coder
import itertools
import numpy as np

bg = bitgen(enwik4)
context_bits = 16 
H = 0.0

from model import CTW
ctw = CTW(context_bits = context_bits)

enc = Coder()

try:
  while 1:
    p_0 = math.exp(ctw.getLogPx(0))
    p_1 = math.exp(ctw.getLogPx(1))

    # print("p_0: " + str(p_0))
    # print("p_1: " + str(p_1))

    assert (abs(p_0 + p_1 - 1) < 1e-6)

    x = next(bg)
    ctw.update(x)

    p_x = p_0 if x == 0 else 1 - p_0
        
    enc.code(p_0, x)

    H += -math.log2(p_x)


except StopIteration:
  pass

print("%.2f bytes of entropy" % (H / 8))
exit(0)

def write_bin_from_bitstream(fn, bitstream):
  ob = []
  for i in range(0, len(bitstream), 8):
    bytie = bitstream[i:i+8]
    byte = 0
    for bit in bytie:
      byte <<= 1
      byte |= bit
    ob.append(byte)

  with open(fn, "wb") as f:
        f.write(bytes(ob))



coded = enc.getCoded()
write_bin_from_bitstream("enwik4.cmp", coded)

dec = Coder(ob = coded)
decoded = []

lookup = defaultdict(lambda: [0, 0])

try:
  prevx = [-1]*BACK_BITS
  while 1:

    px = tuple(prevx)

    p_0 = (lookup[px][0] + 0.5) / (lookup[px][0]+lookup[px][1]+1)

    x = dec.code(p_0)
    decoded.append(x)

    # feels wrong, but...
    if len(decoded) == 80000:
      break


    lookup[px][x] += 1
     
    prevx.append(x)
    prevx = prevx[-BACK_BITS:]

except StopIteration:
  pass


write_bin_from_bitstream("enwik4.mmm", decoded)
