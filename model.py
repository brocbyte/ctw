#!/usr/bin/env python3    
class Node():
  def __init__(self, parent = None, depth = 0):
    self.c = [0] * 2
    self.parent = parent
    self.child = [None] * 2
    self.depth = depth
    self.pe = 1
    self.pw = 1
    

class CTW():
  def __init__(self, context_bits = 3, prevx = None):
    if prevx == None:
      prevx = [0] * context_bits
    self.context_bits = context_bits
    self.root = Node()
    self.prevx = prevx

  def update(self, x):
    node = self.root
    node.pe = (node.c[x] + 0.5) / (node.c[0] + node.c[1] + 1) * node.pe
    node.c[x] += 1
    for i in range(len(self.prevx) - 1, -1, -1):
      last = self.prevx[i]
      if node.child[last] == None:
        node.child[last] = Node(parent = node, depth = node.depth + 1)
      node = node.child[last] 
      node.pe = (node.c[x] + 0.5) / (node.c[0] + node.c[1] + 1) * node.pe
      node.c[x] += 1

    # node is leaf
    # back-propagate!
    node.pw = node.pe
    while node.parent != None:
      node = node.parent
      pw0s = node.child[0].pw if node.child[0] != None  else 1
      pw1s = node.child[1].pw if node.child[1] != None  else 1
      node.pw = 0.5 * (node.pe + pw0s * pw1s)

    self.prevx = self.prevx[1:]
    self.prevx.append(x)

  def printTree(self, node = None, suff = []):
    if node == None:
      node = self.root
    print("node %s: (%d %d), %.6f %.6f" % (str(suff), node.c[0], node.c[1], node.pe, node.pw)) 
    for i in range(2):
      if node.child[i] != None:
        self.printTree(node = node.child[i], suff = [i] + suff)




context = [0, 1, 0]
h = [0, 1, 1, 0, 1, 0, 0]

model = CTW(prevx = context)
for x in h:
  model.update(x) 
model.printTree()
