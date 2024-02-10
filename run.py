import sys

from src.utils.parseFile import parseFileAndReturnInstance


def run(file: str) -> None:
  instance = parseFileAndReturnInstance(file)
  instance.run()

  totalWeight = 0.0
  for edge in instance.selectedEdges:
    totalWeight += edge.capacity
    print(edge.textRepr)
  print("Total weight", totalWeight)

if __name__ == '__main__':
  assert len(sys.argv) > 1
  run(sys.argv[1])
