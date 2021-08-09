#!/usr/bin/env python3
import math

enwik4 = open("enwik4", 'rb').read()[:100]


def bitgen(x):
  for c in x:
    for i in range(8):
      yield int((c & (0x80 >> i)) != 0) 


from coder import Coder
import itertools
import numpy as np


'''
p_0 = 0.009
n = 80000 
k = int(n * (1 - p_0))

def rand_bin_array(K, N):
  arr = np.zeros(N)
  arr[:K]  = 1
  np.random.shuffle(arr)
  return arr

seqs = [rand_bin_array(k, n)]

# seqs = list(map(list, itertools.product([0, 1], repeat = n)))
print(seqs)

errors = 0

for seq in seqs:
  enc = Coder()
  for x in seq:
    enc.code(p_0, x)
  coded = enc.getCoded()

  dec = Coder(ob = coded)
  decoded = []
  try:
    while 1:
      x = dec.code(p_0)
      decoded.append(x)
      # feels wrong, but...
      if len(decoded) == len(seq):
        break
  except StopIteration:
    pass
  if len ([i for i, j in zip(seq, decoded) if i == j]) != len(seq):
     print("orig: " + str(seq)) 
     print("code: " + str(coded)) 
     print("deco: " + str(decoded) + "\n") 
     errors += 1
print("TOTAL ERRS: %d" % errors)

exit(0)
'''





bg = bitgen(enwik4)
context_bits = 16 
H = 0.0

from model import CTW
ctw = CTW(context_bits = context_bits)

enc = Coder()

try:
  while 1:
    pwn = ctw.getLogPn()

    # dummy 0-update
    ctw.update(0)
    pwn0 = ctw.getLogPn()
    ctw.save_load(save = False)

    # dummy 1-update
    ctw.update(1)
    pwn1 = ctw.getLogPn()
    ctw.save_load(save = False)

    p_0 = math.exp(pwn0 - pwn)
    p_1 = math.exp(pwn1 - pwn)
    print("p_0: " + str(p_0))

    assert (p_0 + p_1 - 1 < 1e-1)

    x = next(bg)
    ctw.update(x)
    ctw.save_load(save = True)

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
