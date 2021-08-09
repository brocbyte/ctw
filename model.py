#!/usr/bin/env python3    
class Node():
  def __init__(self, symbols = 2, parent = None):
    self.symbols = 2
    self.c = [0] * 2
    self.parent = parent
    self.child = [None] * 2
  # def getPe():
  # def getPw():

class CTW():
  def __init__(self, context_bits = 3, prevx = None):
    if prevx == None:
      prevx = [0] * context_bits
    self.context_bits = context_bits
    self.root = Node()
    self.prevx = prevx

  def update(self, x):
    node = self.root
    node.c[x] += 1
    for i in range(len(self.prevx) - 1, -1, -1):
      last = self.prevx[i]
      if node.child[last] == None:
        node.child[last] = Node(parent = node)
      node = node.child[last] 
      node.c[x] += 1
    self.prevx = self.prevx[1:]
    self.prevx.append(x)

  def printTree(self, node = None, suff = []):
    if node == None:
      node = self.root
    print("node %s: (%d %d)" % (str(suff), node.c[0], node.c[1])) 
    for i in range(2):
      if node.child[i] != None:
        self.printTree(node = node.child[i], suff = [i] + suff)




context = [0, 1, 0]
h = [0, 1, 1, 0, 1, 0, 0]

model = CTW(prevx = context)
for x in h:
  model.update(x) 
model.printTree()
