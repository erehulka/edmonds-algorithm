from typing import Optional
from src.dataStructures.flower import Flower


class Tree:
  root: Flower

  def getNoVertexWithZeroCharge(self) -> Optional[Flower]:
    return self.root.getNoVertexWithZeroCharge()

  @staticmethod
  def findLCA(K: Flower, H: Flower) -> Flower:
    node1: Optional[Flower] = K
    node2: Optional[Flower] = H

    # Find depths of both nodes
    depth1 = K.depth()
    depth2 = H.depth()

    # Make sure node1 is deeper
    if depth2 > depth1:
        node1, node2 = node2, node1
        depth1, depth2 = depth2, depth1

    assert node1 is not None
    assert node2 is not None
    # Move node1 to the same depth as node2
    while depth1 > depth2:
        assert node1.parent is not None
        node1 = node1.parent
        depth1 -= 1

    # Move both nodes up until they meet
    while node1 != node2:
        assert node1 is not None
        assert node2 is not None
        node1 = node1.parent
        node2 = node2.parent

    if node1 is None:
       raise ValueError("FAIL when finding LCA! Flowers may not be in the same tree.")

    return node1
  
  @staticmethod
  def getSubtreesNotInAlternatingPath(root: Flower, alternatingPath: list[Flower]) -> list[Flower]:
    result: list[Flower] = []
    nextInPath: Optional[Flower] = None
    for child in root.children:
        if child not in alternatingPath:
            result.append(child)
        else:
           nextInPath = child
    if nextInPath is not None:
       result.extend(Tree.getSubtreesNotInAlternatingPath(nextInPath, alternatingPath))

    return result
    
    