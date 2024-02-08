from src.dataStructures import Edge, Flower, Tree
from src.instance import Instance


def parseFileAndReturnInstance(fileName: str) -> Instance:
  result = Instance()

  with open(fileName, 'r') as file:
    firstLine = file.readline()
    values = firstLine.split()
    vertices = int(values[0])

    for i in range(vertices):
      result.trees.append(Tree(Flower(None, None, [], [])))
    
    for line in file:
      values = line.split()
      v1 = result.trees[int(values[0]) - 1].root
      v2 = result.trees[int(values[1]) - 1].root
      capacity = int(values[2])
      result.otherEdges.append(Edge(v1, v2, capacity, f"{values[0]} {values[1]}"))

  return result