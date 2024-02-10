from src.dataStructures import Edge, Flower
from src.enums.edge import EdgeType


def findAlternatingPath(end: Flower, pathSoFar: list[Edge], visitedVertices: list[Flower], currentVertex: Flower, mustUseBlocked: bool, roots: list[Flower]) -> list[Edge]:
  """
  Finds alternating path (between L and M edges) from given vertex. If it needs to choose a elected edge, it has
  only one possibility, but for blocking it has multiple. Thus it tries both.
  If no path is found, Error is raised.
  """
  if currentVertex == end:
    return pathSoFar
  
  if mustUseBlocked:
    for edge in currentVertex.edges:
      if edge.type == EdgeType.BLOCKED:
        nextVertex = edge.v1
        if nextVertex == currentVertex:
          nextVertex = edge.v2
        if nextVertex in visitedVertices or nextVertex.getTotalOuterFlower().getRoot() not in roots:
          continue
        try:
          return findAlternatingPath(end, pathSoFar + [edge], visitedVertices + [nextVertex], nextVertex, not mustUseBlocked, roots)
        except:
          pass
  else:
    usedEdge = None
    for edge in currentVertex.edges:
      if edge.type == EdgeType.SELECTED:
        usedEdge = edge
        break
    if usedEdge is None:
      raise ValueError("There is no edge to be chosen")
    
    nextVertex = usedEdge.v1
    if nextVertex == currentVertex:
      nextVertex = usedEdge.v2
    
    if nextVertex in visitedVertices:
      raise ValueError("There is no edge to be chosen")
    
    return findAlternatingPath(end, pathSoFar + [usedEdge], visitedVertices + [nextVertex], nextVertex, not mustUseBlocked, roots)

  raise ValueError("Invalid Path")

def hasIntersection(l1: list, l2: list) -> bool:
  set1 = set(l1)
  set2 = set(l2)
  return len(set1.intersection(set2)) > 0

def getVerticesOnAlternatingPath(alternatingPath: list[Edge]) -> list[Flower]:
  result = []
  for e in alternatingPath:
    outer1 = e.v1.getTotalOuterFlower()
    outer2 = e.v2.getTotalOuterFlower()
    if outer1 not in result:
      result.append(outer1)
    if outer2 not in result:
      result.append(outer2)

  return result

def findSubtrees(alternatingPath: list[Edge], edges: list[Edge]) -> list[Flower]:
  # Go through the alternating path, find the outerFlower and add the children, which are not in alternatingPath
  visitedFlowers: list[Flower] = []
  subtrees: list[Flower] = []

  alternatingPathVertices = getVerticesOnAlternatingPath(alternatingPath)

  for edge in alternatingPath:
    for fl in [edge.v1, edge.v2]:
      outerFlower = fl.getTotalOuterFlower()
      if outerFlower in visitedFlowers:
        continue
      visitedFlowers.append(outerFlower)
      for child in outerFlower.children:
        # If child is actually on the alternating path, continue
        if hasIntersection(alternatingPathVertices, child.getAllLowestLevelFlowers()):
          continue
        subtrees.append(child)

  return subtrees
