import sys
from src.dataStructures import Dumbbell, Edge, Tree
from src.utils.typeOfFlower import isInDumbbell, isInTreeOnEvenDepth


def calculateEpsilon(trees: list[Tree], otherEdges: list[Edge], dumbbells: list[Dumbbell]) -> float:
  epsilon: float = sys.float_info.max
  for tree in trees:
    treeEpsilon = tree.root.getMinEpsilon(0)
    if treeEpsilon < epsilon:
      epsilon = treeEpsilon
  
  treeRoots = list(map(lambda x: x.root, trees))

  for edge in otherEdges:
    # It must connect separate flowers
    if edge.v1.getTotalOuterFlower() == edge.v2.getTotalOuterFlower():
      continue
    # If one end is in a dumbbell and the other one at an even level in some tree, we can add only what the edge can take
    if (isInDumbbell(edge.v1, dumbbells) and isInTreeOnEvenDepth(edge.v2, treeRoots)) or (isInDumbbell(edge.v2, dumbbells) and isInTreeOnEvenDepth(edge.v1, treeRoots)):
      edgeEpsilon = edge.getEpsilon()
      if edgeEpsilon < epsilon:
        epsilon = edgeEpsilon
    # If both ends are at an even level in some tree (may be the same one), we can add only half what it can take
    if isInTreeOnEvenDepth(edge.v1, treeRoots) and isInTreeOnEvenDepth(edge.v2, treeRoots):
      edgeEpsilon = edge.getEpsilon() / 2
      if edgeEpsilon < epsilon:
        epsilon = edgeEpsilon
  
  assert epsilon < sys.float_info.max

  return epsilon