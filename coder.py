# yep arithmetic coding
# https://marknelson.us/posts/2014/10/19/data-compression-with-arithmetic-coding.html

class Coder():
  def __init__(self, ob = []):
    self.low = 0
    self.high = 0xffffffff
    self.ob = ob

  # probably make p_0 rational
  def code(self, p_0, x):
    # should produce < (-math.log2(p_x) + 2) bits...    
    p_x = p_0 if x == 0 else 1 - p_0
    # [0, p_0) or [p_0, 1)
    (lower, upper) = (0, p_0) if x == 0 else (p_0, 1)
    # print(str(self.high) + " < " + str(0x80000000 + (1 << 32)))
    assert self.low < self.high 
    # assert self.low  >= 0 and self.low  <= 0x100000000
    # assert self.high >= 0 and self.high <= 0x100000000

    rng = self.high - self.low + 1
    self.high = int(self.low + (rng * upper))
    self.low = int(self.low + (rng * lower))
    print("%d -- %8x %8x -- %8x" % (x, self.low, self.high, rng)) 

    pending_bits = 0

    while 1:
      if self.high < (0x80000000 + (1 << 32)):
        self.ob.append(0)
        while pending_bits >= 0:
          self.ob.append(1)
          pending_bits -= 1

        self.low <<= 1
        self.high <<= 1
        self.high |= 1

        #self.low &= 0xffffffff
        #self.high &= 0xffffffff
      elif self.low >= (0x80000000 + (1 << 32)):
        self.ob.append(1)
        while pending_bits >= 0:
          self.ob.append(0)
          pending_bits -= 1

        self.low <<= 1
        self.high <<= 1
        self.high |= 1

        #self.low &= 0xffffffff
        #self.high &= 0xffffffff
      elif self.low >= 0x40000000 and self.high < (0xC0000000 + (1 << 32)):
        pending_bits += 1
        self.low <<= 1
        self.low &= 0x7FFFFFFF
        self.high <<= 1
        self.high |= 0x80000001

        #self.low &= 0xffffffff
        #self.high &= 0xffffffff
      else:
        break
