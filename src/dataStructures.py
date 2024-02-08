from __future__ import annotations
import sys
from typing import List, Optional


class Tree:
  root: Flower

  def __init__(self, root: Flower):
    self.root = root

  def getNoVertexWithZeroCharge(self) -> Optional[Flower]:
    return self.root.getNoVertexWithZeroCharge()

  @staticmethod
  def findLCA(K: Flower, H: Flower) -> Flower:
    node1: Optional[Flower] = K
    node2: Optional[Flower] = H

    # Find depths of both nodes
    depth1 = K.depth()
    depth2 = H.depth()

    # Make sure node1 is deeper
    if depth2 > depth1:
        node1, node2 = node2, node1
        depth1, depth2 = depth2, depth1

    assert node1 is not None
    assert node2 is not None
    # Move node1 to the same depth as node2
    while depth1 > depth2:
        assert node1.parent is not None
        node1 = node1.parent
        depth1 -= 1

    # Move both nodes up until they meet
    while node1 != node2:
        assert node1 is not None
        assert node2 is not None
        node1 = node1.parent
        node2 = node2.parent

    if node1 is None:
       raise ValueError("FAIL when finding LCA! Flowers may not be in the same tree.")

    return node1
  
  @staticmethod
  def getSubtreesNotInAlternatingPath(root: Flower, alternatingPath: list[Flower]) -> list[Flower]:
    result: list[Flower] = []
    nextInPath: Optional[Flower] = None
    for child in root.children:
        if child not in alternatingPath:
            result.append(child)
        else:
           nextInPath = child
    if nextInPath is not None:
       result.extend(Tree.getSubtreesNotInAlternatingPath(nextInPath, alternatingPath))

    return result
    

class Flower:
  parent: Optional['Flower']
  parentEdge: Optional[Edge]
  children: List['Flower']
  outerFlower: Optional['Flower']
  innerFlowers: List['Flower']
  charge: float

  def __init__(self, parent: Optional['Flower'], parentEdge: Optional[Edge], children: List['Flower'], innerFlowers: List['Flower']) -> None:
    self.parent = parent
    self.parentEdge = parentEdge
    self.children = children
    self.innerFlowers = innerFlowers
    self.charge = 0
    self.outerFlower = None

  def isOnlyVertex(self) -> bool:
    return len(self.innerFlowers) == 0
  
  def getTotalCharge(self) -> float:
    if self.outerFlower is None:
      return self.charge
    
    return self.charge + self.outerFlower.getTotalCharge()
  
  def getTotalOuterFlower(self) -> 'Flower':
    if self.outerFlower is None:
      return self
    
    return self.outerFlower.getTotalOuterFlower()
  
  def depth(self) -> int:
    if self.parent is None:
      return 0
    
    return 1 + self.parent.depth()
  
  def getPathToPredecessor(self, flower: 'Flower') -> List['Flower']:
    if self == flower:
      return [self]
    
    if self.parent == None:
      raise ValueError("There is no path between selected flowers. One is not the predecessor of other.")
    
    assert self.parent is not None
    return [self] + self.parent.getPathToPredecessor(self.parent)
  
  def getAllLowestLevelFlowers(self) -> List['Flower']:
    if len(self.innerFlowers) == 0:
      return [self]
    
    result: List['Flower'] = []
    for inner in self.innerFlowers:
      result.extend(inner.getAllLowestLevelFlowers())

    return result
  
  def getAllSuccessors(self) -> list['Flower']:
    result = [self]
    for child in self.children:
      result.extend(child.getAllSuccessors())

    return result
  
  def changeSubtreeIntoDumbbells(self) -> list[Dumbbell]:
    if self.depth() % 2 == 1:
      assert len(self.children) == 1
      assert self.children[0].parentEdge is not None
      return [Dumbbell(self, self.children[0], self.children[0].parentEdge)] + self.children[0].changeSubtreeIntoDumbbells()
    
    # Otherwise if I am in even depth
    result: list[Dumbbell] = []
    for child in self.children:
      result.extend(child.changeSubtreeIntoDumbbells())

    return result
  
  def getNoVertexWithZeroCharge(self) -> Optional['Flower']:
    if self.charge == 0 and len(self.innerFlowers) > 0:
      return self
    for child in self.children:
      response = child.getNoVertexWithZeroCharge()
      if response is not None:
        return response
      
    return None
  
  def getRoot(self) -> 'Flower':
    if self.parent is None:
      return self
    
    return self.parent.getRoot()
  
  def getMinEpsilon(self, level: int) -> float:
    epsilon = sys.float_info.max
    for child in self.children:
      childEpsilon = child.getMinEpsilon(level + 1)
      if childEpsilon < epsilon:
        epsilon = childEpsilon

    if level % 2 == 1 and self.charge < epsilon:
      epsilon = self.charge
    
    return epsilon

  def changeChargeByEpsilon(self, level: int, epsilon: float) -> None:
    if level % 2 == 0:
      self.charge += epsilon
    else:
      self.charge -= epsilon

    for child in self.children:
      child.changeChargeByEpsilon(level + 1, epsilon)


class Edge:
  v1: Flower
  v2: Flower
  capacity: float
  textRepr: str

  def __init__(self, v1: Flower, v2: Flower, capacity: float, textRepr: str):
    self.v1 = v1
    self.v2 = v2
    self.capacity = capacity
    self.textRepr = textRepr

  def getCurrentCharge(self) -> float:
    return self.v1.getTotalCharge() + self.v2.getTotalCharge()
  
  def getEpsilon(self) -> float:
    return self.capacity - self.getCurrentCharge()


class Dumbbell:
  f1: Flower
  f2: Flower
  edge: Edge

  def __init__(self, f1: Flower, f2: Flower, edge: Edge):
    self.f1 = f1
    self.f2 = f2
    self.edge = edge

  def makeIntoSubTree(self, edge: Edge) -> Flower:
    # Find out which edge end is actually in the dumbbell.
    endVertex: Flower = edge.v1
    endVertexOuter: Flower = endVertex.getTotalOuterFlower()
    if endVertexOuter != self.f1 and endVertexOuter != self.f2:
      endVertex = edge.v2
      endVertexOuter = endVertex.getTotalOuterFlower()
    
    # Find out what is the flower conencted by the edge
    if endVertexOuter == self.f1:
      self.f1.children = [self.f2]
      self.f2.children = []
      self.f2.parent = self.f1
      return self.f1
    elif endVertexOuter == self.f2:
      self.f2.children = [self.f1]
      self.f1.children = []
      self.f1.parent = self.f2
      return self.f2
    else:
      raise ValueError("Unknown error when connecting dumbbell via edge.")
    
  def containsFlower(self, flower: Flower) -> bool:
    return self.f1 == flower or self.f2 == flower