#!/usr/bin/env python3    
import math
class Node():
  def __init__(self, parent = None, depth = 0):
    self.parent = parent
    self.child = [None] * 2
    self.old_child = [None] * 2
    self.depth = depth

    # "serializable"
    self.c = [0] * 2
    self.old_c = [0] * 2
    self.pe = self.old_pe = 0
    self.pw = self.old_pw = 0

    

class CTW():
  def __init__(self, context_bits = 3, prevx = None):
    if prevx == None:
      prevx = [0] * context_bits
    self.context_bits = context_bits
    self.root = Node()
    self.prevx = prevx

  # idk
  def save_load(self, node = None, save = True):
    if node == None:
      node = self.root

    if save:
      node.old_c[0], node.old_c[1], node.old_pe, node.old_pw = node.c[0], node.c[1], node.pe, node.pw
      node.old_child[0], node.old_child[1] = node.child[0], node.child[1]
    else:
      node.c[0], node.c[1], node.pe, node.pw = node.old_c[0], node.old_c[1], node.old_pe, node.old_pw
      node.child[0], node.child[1] = node.old_child[0], node.old_child[1]

    for i in range(2):
      if node.child[i] != None:
        self.save_load(node.child[i])

  def update(self, x):
    node = self.root
    node.pe = math.log(node.c[x] + 0.5) - math.log(node.c[0] + node.c[1] + 1) + node.pe
    node.c[x] += 1
    for i in range(len(self.prevx) - 1, -1, -1):
      last = self.prevx[i]
      if node.child[last] == None:
        node.child[last] = Node(parent = node, depth = node.depth + 1)
      node = node.child[last] 
      node.pe = math.log(node.c[x] + 0.5) - math.log(node.c[0] + node.c[1] + 1) + node.pe
      node.c[x] += 1

    # node is leaf
    # back-propagate!
    node.pw = node.pe
    while node.parent != None:
      node = node.parent
      pw0s = node.child[0].pw if node.child[0] != None else 0
      pw1s = node.child[1].pw if node.child[1] != None else 0
      node.pw = math.log(0.5) + math.log(math.exp(node.pe) + math.exp(pw0s + pw1s))

    self.prevx = self.prevx[1:]
    self.prevx.append(x)

  def getLogPn(self):
    return self.root.pw

  def printTree(self, node = None, suff = []):
    if node == None:
      node = self.root
    print("node %s: (%d %d), %.6f %.6f" % (str(suff), node.c[0], node.c[1], node.pe, node.pw)) 
    for i in range(2):
      if node.child[i] != None:
        self.printTree(node = node.child[i], suff = [i] + suff)
