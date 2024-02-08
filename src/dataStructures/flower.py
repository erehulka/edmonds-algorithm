import sys
from typing import List, Optional
from src.dataStructures.dumbbell import Dumbbell

from src.dataStructures.edge import Edge


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
