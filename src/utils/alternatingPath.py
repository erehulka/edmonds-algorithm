from src.dataStructures import Edge, Flower
from src.enums.edge import EdgeType


def findAlternatingPath(end: Flower, pathSoFar: list[Edge], visitedVertices: list[Flower], currentVertex: Flower, mustUseBlocked: bool) -> list[Edge]:
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
        if nextVertex in visitedVertices:
          continue
        try:
          return findAlternatingPath(end, pathSoFar + [edge], visitedVertices + [nextVertex], nextVertex, not mustUseBlocked)
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
    
    return findAlternatingPath(end, pathSoFar + [usedEdge], visitedVertices + [nextVertex], nextVertex, not mustUseBlocked)

  raise ValueError("Invalid Path")