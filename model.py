#!/usr/bin/env python3    
import math
import numpy as np

class Node():
  def __init__(self, parent = None):
    self.parent = parent
    self.child = [None] * 2
    self.depth = parent.depth + 1 if parent != None else 0
    self.c = [0] * 2
    self.pe = 0.0
    self.pw = 0.0


class CTW():
  def __init__(self, context_bits = 3, prevx = None):
    if prevx is None:
      prevx = [0] * context_bits
    self.context_bits = context_bits
    self.root = Node()
    self.prevx = prevx

  def update(self, x, reverse, tmp):
    node = self.root

    for i in range(len(self.prevx), -1, -1):
      # in root node we skip this, only for non-duplication
      if i != len(self.prevx):
        # go one step Dipper
        last = self.prevx[i]
        if node.child[last] is None:
          node.child[last] = Node(parent = node)
        node = node.child[last] 

      # update node
      if not reverse:
        node.pe += math.log(node.c[x] + 0.5) - math.log(sum(node.c) + 1.0)
        node.c[x] += 1
      else:
        node.c[x] -= 1
        node.pe -= math.log(node.c[x] + 0.5) - math.log(sum(node.c) + 1.0)


    # node is leaf
    assert node.depth == self.context_bits
    node.pw = node.pe
    # back-propagate!
    while node.parent != None:
      node = node.parent
      assert node.depth < self.context_bits
      pw0s = node.child[0].pw if node.child[0] != None else 0.0
      pw1s = node.child[1].pw if node.child[1] != None else 0.0
      node.pw = math.log(0.5) + np.logaddexp(node.pe, pw0s + pw1s)
    if not tmp:
      self.prevx = self.prevx[1:]
      self.prevx.append(x)

  def getLogPx(self, x):
    pw = self.root.pw

    # dummy x-update
    self.update(x, reverse = False, tmp = True)
    pwx = self.root.pw

    # restore everything
    self.update(x, reverse = True, tmp = True)

    # log (/) = -
    return pwx - pw

  def printTree(self, node = None, suff = []):
    if node is None:
      node = self.root
    print("node %s: (%d %d), %.6f %.6f" % (str(suff), node.c[0], node.c[1], math.exp(node.pe), math.exp(node.pw)))
    for i in range(2):
      if node.child[i] != None:
        self.printTree(node = node.child[i], suff = [i] + suff)
