from src.dataStructures.dumbbell import Dumbbell
from src.dataStructures.flower import Flower
from src.dataStructures.tree import Tree


def isInDumbbell(flower: Flower, dumbbells: list[Dumbbell]) -> bool:
  outerFlower = flower.getTotalOuterFlower()
  for dumbbell in dumbbells:
    if outerFlower == dumbbell.f1 or outerFlower == dumbbell.f2:
      return True
    
  return False

def isInTreeOnEvenDepth(flower: Flower, trees: list[Tree]) -> bool:
  outerFlower = flower.getTotalOuterFlower()
  for tree in trees:
    if outerFlower in tree.root.getAllSuccessors():
      return outerFlower.depth() % 2 == 0
  return False