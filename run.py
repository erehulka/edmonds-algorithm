import sys

from src.utils.parseFile import parseFileAndReturnInstance


def run(file: str) -> None:
  instance = parseFileAndReturnInstance(file)
  instance.run()

  for edge in instance.selectedEdges:
    print(edge.textRepr)

if __name__ == '__main__':
  assert len(sys.argv) > 1
  run(sys.argv[1])
