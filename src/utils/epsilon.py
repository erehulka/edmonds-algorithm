import sys
from src.dataStructures import Dumbbell, Edge, Tree
from src.utils.typeOfFlower import isInDumbbell, isInTreeOnEvenDepth


def calculateEpsilon(trees: list[Tree], otherEdges: list[Edge], dumbbells: list[Dumbbell]) -> float:
  epsilon: float = sys.float_info.max
  for tree in trees:
    treeEpsilon = tree.root.getMinEpsilon(0)
    if treeEpsilon < epsilon:
      epsilon = treeEpsilon

  assert epsilon > 0 and epsilon < sys.float_info.max

  for edge in otherEdges:
    # It must connect separate flowers
    if edge.v1.getTotalOuterFlower() == edge.v2.getTotalOuterFlower():
      continue
    # If one end is in a dumbbell and the other one at an even level in some tree, we can add only what the edge can take
    if (isInDumbbell(edge.v1, dumbbells) and isInTreeOnEvenDepth(edge.v2, trees)) or (isInDumbbell(edge.v2, dumbbells) and isInTreeOnEvenDepth(edge.v1, trees)):
      edgeEpsilon = edge.getEpsilon()
      if edgeEpsilon < epsilon:
        epsilon = edgeEpsilon
    # If both ends are at an even level in some tree (may be the same one), we can add only half what it can take
    if isInTreeOnEvenDepth(edge.v1, trees) and isInTreeOnEvenDepth(edge.v2, trees):
      edgeEpsilon = edge.getEpsilon() / 2
      if edgeEpsilon < epsilon:
        epsilon = edgeEpsilon

  return epsilon