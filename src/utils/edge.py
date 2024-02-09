from src.dataStructures import Edge, Flower


def findConnectingEdge(f1: Flower, f2: Flower, edges: list[Edge]) -> Edge:
  allInner1 = f1.getAllLowestLevelFlowers()
  allInner2 = f2.getAllLowestLevelFlowers()
  for edge in edges:
    if (edge.v1 in allInner1 and edge.v2 in allInner2) or (edge.v2 in allInner1 and edge.v1 in allInner2):
      return edge
    
  raise ValueError("No edge has been found")