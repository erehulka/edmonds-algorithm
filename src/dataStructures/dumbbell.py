from src.dataStructures.edge import Edge
from src.dataStructures.flower import Flower


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