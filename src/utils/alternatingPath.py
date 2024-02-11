from src.dataStructures import Edge, Flower
from src.enums.edge import EdgeType
from src.utils.edge import findConnectingEdge


def findAlternatingPath(end: Flower, pathSoFar: list[Edge], visitedVertices: list[Flower], currentVertex: Flower, mustUseBlocked: bool, roots: list[Flower]) -> tuple[list[Edge], list[Flower]]:
  """
  Finds alternating path (between L and M edges) from given vertex. If it needs to choose a elected edge, it has
  only one possibility, but for blocking it has multiple. Thus it tries both.
  If no path is found, Error is raised.
  """
  if currentVertex == end:
    return (pathSoFar, visitedVertices)
  
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

def getVerticesOnAlternatingPath(alternatingPathOuterVertices: list[Flower]) -> list[Flower]:
  result = []
  for fl in alternatingPathOuterVertices:
    outer = fl.getTotalOuterFlower()
    if outer not in result:
      result.append(outer)

  return result

def findSubtrees(alternatingPathOuterVertices: list[Flower], blockedEdges: list[Edge]) -> tuple[list[Flower], list[Edge]]:
  # Go through the alternating path, find the outerFlower and add the children, which are not in alternatingPath
  # Returns also a list of edges, which must be made unblocked.
  subtrees: list[Flower] = []
  connectingEdges: list[Edge] = []

  for fl in alternatingPathOuterVertices:
    for child in fl.children:
      if child in alternatingPathOuterVertices:
        continue
      assert child not in subtrees
      subtrees.append(child)

      edgeToBeUnblocked = findConnectingEdge(fl, child, blockedEdges)
      connectingEdges.append(edgeToBeUnblocked)

  return (subtrees, connectingEdges)
