from src.dataStructures import Edge, Flower, Tree
from src.enums.edge import EdgeType
from src.instance import Instance


def parseFileAndReturnInstance(fileName: str) -> Instance:
  result = Instance()

  with open(fileName, 'r') as file:
    firstLine = file.readline()
    values = firstLine.split()
    vertices = int(values[0])

    for i in range(vertices):
      flower = Flower(None, None, [], [])
      flower.textRepr = str(i + 1)
      result.trees.append(Tree(flower))
    
    for line in file:
      values = line.split()
      v1 = result.trees[int(values[0]) - 1].root
      v2 = result.trees[int(values[1]) - 1].root
      capacity = int(values[2])
      edge = Edge(v1, v2, capacity, f"{values[0]} {values[1]}", EdgeType.OTHER)
      result.otherEdges.append(edge)
      v1.edges.append(edge)
      v2.edges.append(edge)

  return result