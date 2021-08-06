# yep arithmetic coding
# https://www.cbloom.com/algs/statisti.html#A1.0

class Coder():
  def __init__(self, ob = []):
    self.PRECISION = 8 
    self.SHIFT = self.PRECISION - 1
    self.MAX_VALUE = (1 << self.PRECISION) - 1 # [1] * PRECISION

    self.low = 0
    self.high =  self.MAX_VALUE
    self.ob = ob
    # print("after by _:  0.%s 0.%s" % (format(self.low, '08b'), format(self.high, '08b'))) 
  def getCoded(self):
    # after all, don't forget to send the rest of low or high:
    # low:  0b01..1
    # high: 0b10..0
    # looks like it's better to send "high" with zeros...
    # but do we need all of them??
    assert (self.high >> self.SHIFT) == 1
    return self.ob + [self.high >> self.SHIFT] + [0] * self.PRECISION

  # should produce < (-math.log2(p_x) + 2) bits...    
  # probably make p_0 rational
  def code(self, p_0, x):

    assert self.low < self.high 
    assert self.low  >= 0 and self.low  <= self.MAX_VALUE
    assert self.high >= 0 and self.high <= self.MAX_VALUE
    
    # [0, p_0) or [p_0, 1)
    split = int(self.low + (self.high - self.low) * p_0)
    if x == 0:
      self.high = split
    elif x == 1:
      self.low = split
    # print("after by %d:  0.%s 0.%s" % (x, format(self.low, '08b'), format(self.high, '08b'))) 

    # bits that will never change
    while (self.low >> self.SHIFT) == (self.high >> self.SHIFT):
      assert (self.low >> self.SHIFT) <= 1
      self.ob.append(self.low >> self.SHIFT)
      # print(">> %d" % (self.low >> self.SHIFT))
      # get rid of MSB, then shift
      # (1 << SHIFT) - 1 == [1] * SHIFT 
      self.low =   (self.low  & ((1 << self.SHIFT) - 1)) << 1
      self.high = ((self.high & ((1 << self.SHIFT) - 1)) << 1) | 1
      # print("after trans! %s %s" % (bin(self.low), bin(self.high)))
