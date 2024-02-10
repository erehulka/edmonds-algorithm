from src.dataStructures import Dumbbell, Flower, Tree


def isInDumbbell(flower: Flower, dumbbells: list[Dumbbell]) -> bool:
  outerFlower = flower.getTotalOuterFlower()
  for dumbbell in dumbbells:
    if outerFlower == dumbbell.f1 or outerFlower == dumbbell.f2:
      return True
    
  return False

def isInTreeOnEvenDepth(flower: Flower, treeRoots: list[Flower]) -> bool:
  outerFlower = flower.getTotalOuterFlower()
  if outerFlower.getRoot() not in treeRoots:
    return False

  return outerFlower.depth() % 2 == 0
