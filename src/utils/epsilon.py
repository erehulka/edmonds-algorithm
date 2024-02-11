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
    onEvenDepth1 = isInTreeOnEvenDepth(edge.v1, treeRoots)
    onEvenDepth2 = isInTreeOnEvenDepth(edge.v2, treeRoots)

    # It must connect separate flowers
    if edge.v1.getTotalOuterFlower() == edge.v2.getTotalOuterFlower():
      continue
    # If one end is in a dumbbell and the other one at an even level in some tree, we can add only what the edge can take
    if (isInDumbbell(edge.v1, dumbbells) and onEvenDepth2) or (isInDumbbell(edge.v2, dumbbells) and onEvenDepth1):
      edgeEpsilon = edge.getEpsilon()
      if edgeEpsilon < epsilon:
        epsilon = edgeEpsilon
    # If both ends are at an even level in some tree (may be the same one), we can add only half what it can take
    if onEvenDepth1 and onEvenDepth2:
      edgeEpsilon = edge.getEpsilon() / 2
      if edgeEpsilon < epsilon:
        epsilon = edgeEpsilon
  
  assert epsilon < sys.float_info.max

  return epsilon