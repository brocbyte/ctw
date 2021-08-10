#!/usr/bin/env python3
import math
from coder import Coder
import itertools
import numpy as np

enwik4 = open("enwik4", 'rb').read()

def bitgen(x):
  for c in x:
    for i in range(8):
      yield int((c & (0x80 >> i)) != 0) 

bg = bitgen(enwik4)
context_bits = 48
H = 0.0

from model import CTW
ctw = CTW(context_bits = context_bits)

enc = Coder()

try:
  while 1:
    p_0 = math.exp(ctw.getLogPx(0))
    p_1 = math.exp(ctw.getLogPx(1))
    assert (abs(p_0 + p_1 - 1) < 1e-6)

    x = next(bg)

    # model
    ctw.update(x, reverse = False, tmp = False)

    # arithmetic coding 
    enc.code(p_0, x)

    # entropy measure
    p_x = p_0 if x == 0 else 1 - p_0
    H += -math.log2(p_x)


except StopIteration:
  pass

print("%.2f bytes of entropy" % (H / 8))

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
print("coded in %d bytes" % math.ceil(len(coded) / 8))

dec = Coder(ob = coded)
decoded = []

ctw = CTW(context_bits = context_bits)

try:
  while 1:
    p_0 = math.exp(ctw.getLogPx(0))
    p_1 = math.exp(ctw.getLogPx(1))

    assert (abs(p_0 + p_1 - 1) < 1e-6)

    x = dec.code(p_0)
    decoded.append(x)

    ctw.update(x, reverse = False, tmp = False)

    # feels wrong, but...
    if len(decoded) == 80000:
      break

except StopIteration:
  pass

write_bin_from_bitstream("enwik4.mmm", decoded)
