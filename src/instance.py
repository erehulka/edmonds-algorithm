from re import A
from typing import List
from src.dataStructures import Dumbbell, Edge, Flower, Tree
from src.enums.edge import EdgeType
from src.utils.alternatingPath import findAlternatingPath, findSubtrees, getVerticesOnAlternatingPath
from src.utils.edge import findConnectingEdge
from src.utils.epsilon import calculateEpsilon
from src.utils.typeOfFlower import isInTreeOnEvenDepth


class Instance:
  trees: List[Tree]
  dumbbells: List[Dumbbell]
  selectedEdges: List[Edge]
  blockingEdges: List[Edge]
  otherEdges: List[Edge]

  def __init__(self) -> None:
    self.trees = []
    self.dumbbells = []
    self.selectedEdges = []
    self.blockingEdges = []
    self.otherEdges = []

  def action(self) -> None:
    # First change the epsilon, if epsilon is 0, some action has to be performed.
    epsilon: float = calculateEpsilon(self.trees, self.otherEdges, self.dumbbells)
    treeRoots = list(map(lambda x: x.root, self.trees))

    if epsilon > 0:
      # Change the charges
      for root in treeRoots:
        root.changeChargeByEpsilon(0, epsilon)
    else:
      # Move through the instance, find out if something has to be done, if yes, perform it
      # If some not-vertex bubble in some tree has charge 0, perform P1.
      for tree in self.trees:
        flower = tree.getNoVertexWithZeroCharge()
        if flower is not None:
          self.P1(flower)
          return
      
      for edge in self.otherEdges:
        if edge.getCurrentCharge() >= edge.capacity:
          outerFlower1 = edge.v1.getTotalOuterFlower()
          outerFlower2 = edge.v2.getTotalOuterFlower()

          # If at least one of the flowers is not in a tree on even level, skip this action and try again
          if not isInTreeOnEvenDepth(outerFlower1, treeRoots) and not isInTreeOnEvenDepth(outerFlower2, treeRoots):
            continue

          # If some edge is full between some bubble on an even level and a dumbbell, perform P2.
          for dumbbell in self.dumbbells:
            if dumbbell.containsFlower(outerFlower1) and isInTreeOnEvenDepth(outerFlower2, treeRoots):
              # Meaning that the other flower is on even level
              self.P2(outerFlower2, dumbbell, edge)
              return
            elif dumbbell.containsFlower(outerFlower2) and isInTreeOnEvenDepth(outerFlower1, treeRoots):
              self.P2(outerFlower1, dumbbell, edge)
              return
            
          # If some edge between flowers in one tree has been filled, perform P3.
          if outerFlower1.getRoot() == outerFlower2.getRoot() and outerFlower1.depth() % 2 == 0 and outerFlower2.depth() % 2 == 0:
            self.P3(edge)
            return

          # Otherwise perform P4
          if isInTreeOnEvenDepth(outerFlower1, treeRoots) and isInTreeOnEvenDepth(outerFlower2, treeRoots):
            self.P4(edge)
            return    

  def run(self) -> None:
    # Repeat until all instances are dumbbells
    while len(self.trees) > 0:
      self.action()
    
  def P1(self, flower: Flower) -> None:
    print(f"P1 on {flower.getAllLowestLevelFlowers()}")
    """
    Performs an action, where for a flower on odd level the charge fell to 0. The steps are mentioned below.

    (P1) Zelenej bubline na nepárnej úrovni klesol náboj na 0. Nech K je kvet, ktorému patrí nulová bublina. 
    Z definície kvetu, K obsahuje nepárny počet kvetov K1, . . . , K2r+1, pričom stopka je vo K1. Keďže K je 
    na nepárnej úrovni, má jedného rodiča a jedného syna, ktorý je napojený na stopku. Nech hrana do rodiča 
    ide z kvetu Kt a bez ujmy na všeobecnosti nech t je nepárne. Potom cesta K1,K2,...,Kt má nepárny počet 
    kvetov a môže nahradiť K v strome. Dvojice vrcholov Kt+1,Kt+2 až K2r,K2r+1 tvoria činky. Plné hrany medzi 
    Kt a Kt+1 a K1,K2r+1 sa dajú odobrať z L, lebo v novom strome bude jedna z nich na nepárnej úrovni a druhá 
    v činke, takže pri najbližšej operácii posun prestanú byť plné.
    """
    if len(flower.children) != 1:
      raise ValueError(f"P1: The flower does not have exactly one child. Real number: {len(flower.children)}")
    
    assert flower.outerFlower is None
    
    # Find out from which inner flower Kt the edge goes to the parent. Get index.
    flowerIndexToParent = 0
    assert flower.parentEdge is not None
    for inner in flower.innerFlowers:
      lowLevelFlowers = inner.getAllLowestLevelFlowers()
      if flower.parentEdge.v1 in lowLevelFlowers or flower.parentEdge.v2 in lowLevelFlowers:
        break
      flowerIndexToParent += 1

    if flowerIndexToParent >= len(flower.innerFlowers):
      raise ValueError("Parent edge not found")

    # NOTE, the index i actually represents the inner flower K{i+1}, since we are indexing from one.

    # Get the path with the odd length. It should be from K{i+1} to K1.
    # If i+1 is odd (i is even), then the path is K{i+1}, K{i}, ..., K1 and the path of new dumbbells is K{i+2}, ..., K{t}
    # If i+1 is even, then it is K{i+1}, K{i+2}, ..., Kt, K1 where Kt is the last inner flower and the path of dumbbells is K2, ..., Ki
    newPath: List[Flower]
    dumbbellPath: List[Flower]
    if flowerIndexToParent % 2 == 0:
      newPath = flower.innerFlowers[:flowerIndexToParent+1]
      newPath.reverse()
      dumbbellPath = flower.innerFlowers[flowerIndexToParent+1:]
    else:
      newPath = flower.innerFlowers[flowerIndexToParent:] + [flower.innerFlowers[0]]
      dumbbellPath = flower.innerFlowers[1:flowerIndexToParent]

    # Change the odd path for the flower in the tree, change the child of the parent to Kt and
    # change the parent of the child to K1
    for i in range(len(newPath) - 1):
      newPath[i].children = [newPath[i+1]]
      newPath[i+1].parent = newPath[i]
      newPath[i+1].parentEdge = findConnectingEdge(newPath[i+1], newPath[i], self.blockingEdges + self.selectedEdges)

    newPath[0].parent = flower.parent
    newPath[0].parentEdge = flower.parentEdge
    assert flower.parent is not None
    flower.parent.children.remove(flower)
    flower.parent.children.append(newPath[0])

    newPath[-1].children = flower.children
    flower.children[0].parent = newPath[-1]
    assert flower.children[0].parentEdge is not None
    # parentEdge should stay the same

    # For each of the inner flowers, set outerFlower to None
    for inner in flower.innerFlowers:
      inner.outerFlower = None

    # Find the dumbbells on the even path, and put them into new dumbbells
    for i in range(0, len(dumbbellPath), 2):
      self.dumbbells.append(Dumbbell(dumbbellPath[i], dumbbellPath[i+1], findConnectingEdge(dumbbellPath[i], dumbbellPath[i+1], self.selectedEdges)))
      
    # Unblock the two connecting edges to a new dumbbell
    if len(dumbbellPath) > 0:
      e1 = findConnectingEdge(dumbbellPath[0], newPath[0], self.blockingEdges)
      e1.type = EdgeType.OTHER
      self.blockingEdges.remove(e1)
      self.otherEdges.append(e1)

      e2 = findConnectingEdge(dumbbellPath[-1], newPath[-1], self.blockingEdges)
      e2.type = EdgeType.OTHER
      self.blockingEdges.remove(e2)
      self.otherEdges.append(e2)

  def P2(self, flower: Flower, dumbbell: Dumbbell, edge: Edge) -> None:
    print(f"P2 on {flower} {dumbbell} and edge {edge}")
    """
    Connects a dumbbell to a flower in some tree.

    (P2) Naplnila sa hrana e medzi kvetom K na párnej úrovni a činkou H. Nech sa činka H skladá z kvetov 
    H1 a H2 tak, že e vedie do nejakého vrchola vo H1. Hrana e sa pridá do L a činka H sa pripojí k 
    príslušnému stromu tak, že K (na párnej úrovni) bude mať syna H1 (na nepárnej úrovni) a ten bude mať 
    jedného syna H2 (na párnej úrovni).
    """

    assert flower.depth() % 2 == 0

    # Remove the dumbbell from dumbbells.
    self.dumbbells.remove(dumbbell)

    # Transform the dumbbell into a subtree.
    subtree: Flower = dumbbell.makeIntoSubTree(edge)

    # Connect this subtree to the flower
    flower.children.append(subtree)
    subtree.parent = flower
    subtree.parentEdge = edge

    # Add the edge to blocking
    self.blockingEdges.append(edge)
    self.otherEdges.remove(edge)
    edge.type = EdgeType.BLOCKED

  def P3(self, edge: Edge) -> None:
    print(f"P3 on {edge}")
    """
    Naplnila sa hrana spájajúca kvety K a H v jednom strome. Zjavne K aj H sú na párnej úrovni. Nech W je LCA 
    K a H. Keďže W má aspoň 2 synov, musí byť tiež na párnej úrovni. Nech K, K1, ... K2k+1, W a H, H1, ... H2r+1, W
    sú cesty v strome. Z parity vrcholov vyplýva, že ich môžeme obaliť novou bublinou a dostaneme kvet Z na párnej
    úrovni, ktorého stopka je stopka W. Synovia Z budú všetci synovia zahrnutých kvetov. Títo ostanú na nepárnej úrovni.
    """

    edge.type = EdgeType.BLOCKED
    self.blockingEdges.append(edge)
    self.otherEdges.remove(edge)

    K = edge.v1.getTotalOuterFlower()
    H = edge.v2.getTotalOuterFlower()

    if K.depth() % 2 != 0 or H.depth() % 2 != 0:
      raise ValueError("One of the flowers is not on even level")
    
    # Find LCA of K and H
    W = Tree.findLCA(K, H)

    # Get the paths from K to W and H to W and reverse one of them.
    KtoW = K.getPathToPredecessor(W)
    HtoW = H.getPathToPredecessor(W)
    WtoH: List[Flower] = HtoW
    WtoH.reverse()
    KtoW = KtoW[:-1]
    innerFlowers: List[Flower] = WtoH + KtoW

    # Get the list of all the children, so children of all inner flowers, not in the new flower.
    children: List[Flower] = []
    for inner in innerFlowers:
      for child in inner.children:
        if child not in innerFlowers:
          children.append(child)
    children = list(set(children))

    # Now we have the new flower so we can create it.
    newFlower = Flower(W.parent, W.parentEdge, children, innerFlowers)
    newFlower.textRepr = str(innerFlowers)

    # Change the parent child to the new flower, and the children parents to the new flower.
    for child in children:
      child.parent = newFlower
      assert child.parentEdge is not None
      # parentEdge stays the same
    if W.parent != None:
      assert W.parent is not None
      W.parent.children.remove(W)
      W.parent.children.append(newFlower)
    newFlower.parentEdge = W.parentEdge
    
    # If this is a new root of the tree, change the root accordingly.
    if newFlower.parent is None:
      for tree in self.trees:
        if tree.root == W:
          tree.root = newFlower
          break

    # Set outerFlower of all inner flowers and delete children
    for flower in innerFlowers:
      flower.children = []
      flower.outerFlower = newFlower
      flower.parent = None

  def P4(self, edge: Edge) -> None:
    print(f"P4 on {edge}")
    """
    Naplnila sa hrana e spájajúca kvety K a H v 2 rôznych stromoch T1 a T2. Toto je vlastne jadro
    celého algoritmu, v ktorom zväčšíme párovanie M. Urobíme to tak, že nájdeme alternujúcu cestu, 
    ktorá spája stopku koreňa stromu T1 so stopkou koreňa T2. Keďže sa naplnila hrana, obidva kvety 
    K a H museli byť na párnej úrovni, takže existuje cesta K, K1, ..., K2r v strome T1 a 
    H, H1, ..., H2q v strome T2, kde K2r a H2q sú korene príslušných stromov. Obidve cesty sú tvorené
    hranami z pôvodného grafu G a striedajú sa v nich hrany z M a L, pričom hrana z M spája stopky
    susedných kvetov. Aby sme cesty v stromoch mohli doplniť na alternujúce cesty v grafe G, stačí
    si uvedomiť nasledujúce tvrdenie:

    Lema 3.13: Nech K je kvet, u je jeho stopka a v je jeho ľubovoľný vrchol. Potom existuje alternujúca
    cesta z u do v, ktorá je celá obsiahnutá v K a ak je neprázdna, tak začína hranou z L a končí hranou
    z M.

    S pomocou Lemy 3.13 teraz vieme nájsť alternujúcu cestu medzi stopkou K2r a stopkou H2q.
    Na tejto ceste vymeníme príslušnosť hrán medzi L a M, čím zvýšime počet hrán v párovaní M. Stromy
    T1 a T2 následne rozoberieme: Kvety K2i-1 a K2i (a rovnako pre H) budú po výmene hrán na alternujúcej
    ceste tvoriť činky. Aby sme videli prečo, stačí si uvedomiť, že cesta z dôkazu Lemy 3.13 pretína každý
    vnútorný kvet buď ani raz, alebo dvakrát a to jednou hranou z M a jednou z L. Preto to výmene hrán z M a L
    ostane zachovaná podmienka že každú bublinu pretína práve jedna hrana z M a stopka stromu sa presunie do 
    vrcholu v z Lemy 3.13. Rovnako vytvoria činku kvety K a H. Zvyšné časti stromov tvoria činky prirodzeným spôsobom.
    """

    # Special case - if both flowers are representing vertices and are not in trees, just add selected edge and add to dumbbells
    if edge.v1.outerFlower == None and edge.v2.outerFlower == None and edge.v1.parent is None and len(edge.v1.children) == 0 and edge.v2.parent is None and len(edge.v2.children) == 0:
      edge.type = EdgeType.SELECTED
      self.otherEdges.remove(edge)
      self.selectedEdges.append(edge)
      edge.type = EdgeType.SELECTED
      self.dumbbells.append(Dumbbell(edge.v1, edge.v2, edge))
      toRemoveTrees: list[Tree] = []
      for tree in self.trees:
        if tree.root == edge.v1 or tree.root == edge.v2:
          toRemoveTrees.append(tree)
      for tree in toRemoveTrees:
        self.trees.remove(tree)
      return

    # Make this edge blocked, it should be other before
    edge.type = EdgeType.BLOCKED
    self.otherEdges.remove(edge)
    self.blockingEdges.append(edge)

    # Find alternating path between the stem of T1 and T2 through the edge
    stem1 = edge.v1.getTotalOuterFlower().getRoot().getStem()
    stem2 = edge.v2.getTotalOuterFlower().getRoot().getStem()
    alternatingPath: List[Edge] = findAlternatingPath(end=stem2, pathSoFar=[], currentVertex=stem1, mustUseBlocked=True, visitedVertices=[stem1], roots=[edge.v1.getTotalOuterFlower().getRoot(), edge.v2.getTotalOuterFlower().getRoot()])
    alternatingPathVertices = getVerticesOnAlternatingPath(alternatingPath)
    # Find out what are the outer flowers of this path. Also save the edges connecting these flowers
    alternatingOuterFlowers = findSubtrees(alternatingPath, self.blockingEdges + self.selectedEdges)

    # This path has first edge from L and last from L as well.
    # Exchange these edges between L and M.
    addToM = True
    for edge in alternatingPath:
      if addToM:
        self.blockingEdges.remove(edge)
        self.selectedEdges.append(edge)
        edge.type = EdgeType.SELECTED
      else:
        self.selectedEdges.remove(edge)
        self.blockingEdges.append(edge)
        edge.type = EdgeType.BLOCKED
      addToM = not addToM

    # Destructurize the tree into dumbbells
    # First, make each pair from the path into dumbbells
    assert len(alternatingPathVertices) % 2 == 0
    for i in range(0, len(alternatingPathVertices), 2):
      dumbbell = Dumbbell(alternatingPathVertices[i], alternatingPathVertices[i+1], findConnectingEdge(alternatingPathVertices[i], alternatingPathVertices[i+1], self.selectedEdges))
      
      # Change the stems to new connecting vertices.
      dumbbell.changeStemsInInner()

      self.dumbbells.append(dumbbell)

      # Remove parent and children
      dumbbell.f1.parent = None
      dumbbell.f2.parent = None
      dumbbell.f1.children = []
      dumbbell.f2.children = []
    
    # Then, process the other part of the tree
    # We need to find the subtrees, which are not a part of the alternating path
    if len(alternatingOuterFlowers) > 0:
      for subtree in alternatingOuterFlowers:
        dumbbells = subtree.changeSubtreeIntoDumbbells()
        for db in dumbbells:
          db.f1.parent = None
          db.f2.parent = None
          db.f1.children = []
          db.f2.children = []
        self.dumbbells.extend(dumbbells)

    # Finally delete the trees so only dumbbells will be left.
    toRemoveTrees = []
    stemOuter1 = stem1.getTotalOuterFlower()
    stemOuter2 = stem2.getTotalOuterFlower()
    for tree in self.trees:
      if tree.root == stemOuter1 or tree.root == stemOuter2:
        toRemoveTrees.append(tree)
    for tree in toRemoveTrees:
        self.trees.remove(tree)
