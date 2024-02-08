from re import A
from typing import List
from src.dataStructures.dumbbell import Dumbbell
from src.dataStructures.edge import Edge
from src.dataStructures.flower import Flower
from src.dataStructures.tree import Tree


class Instance:
  _trees: List[Tree]
  _dumbbells: List[Dumbbell]
  _soloFlowers: List[Flower]
  _selectedEdges: List[Edge]
  _blockingEdges: List[Edge]

  def action(self) -> None:
    # 1: Prejdi inštanciu, ak zistíš že treba dačo vykonať, tak to vykonaj.
    # If some not-vertex bubble in some tree has charge 0, perform P1.

    # 2. Zisti hodnotu epsilon o ktorú sa dajú náboje zmeniť
    # 3: V prípade, že sa nič nevykonalo, zmeň náboje.
    pass

  def run(self) -> None:
    # Opakuj action pokým nie sú všetky kvetiny v dumbbelloch (kým sú trees a soloFlowers neprázdne)
    while len(self._trees) > 0 and len(self._soloFlowers) > 0:
      self.action()
    
  def P1(self, flower: Flower) -> None:
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
    
    # Find out from which inner flower Kt the edge goes to the parent. Get index.
    flowerIndexToParent = 0
    for inner in flower.innerFlowers:
      assert flower.parentEdge is not None
      lowLevelFlowers = inner.getAllLowestLevelFlowers()
      if flower.parentEdge.v1 in lowLevelFlowers or flower.parentEdge.v2 in lowLevelFlowers:
        break
      flowerIndexToParent += 1

    # NOTE, the index i actually represents the inner flower K{i+1}, since we are indexing from one.

    # Get the path with the odd length. It should be from K{i+1} to K1.
    # If i+1 is odd (i is even), then the path is K{i+1}, K{i}, ..., K1
    # If i+1 is even, then it is K{i+1}, K{i+2}, ..., Kt, K1 where Kt is the last inner flower
    newPath: List[Flower]
    if flowerIndexToParent % 2 == 0:
      newPath = flower.innerFlowers[0:flowerIndexToParent+1]
      newPath.reverse()
    else:
      newPath = flower.innerFlowers[flowerIndexToParent:] + [flower.innerFlowers[0]]

    # Change the odd path for the flower in the tree, change the child of the parent to Kt and
    # change the parent of the child to K1
    for i in range(len(newPath) - 1):
      newPath[i].children = [newPath[i+1]]
      newPath[i+1].parent = newPath[i]

    newPath[0].parent = flower.parent
    assert flower.parent is not None
    flower.parent.children.remove(flower)
    flower.parent.children.append(newPath[0])

    newPath[-1].children = flower.children
    flower.children[0].parent = newPath[-1]

    # For each of the inner flowers, set outerFlower to None
    for inner in flower.innerFlowers:
      inner.outerFlower = None

    # Find the dumbbells on the even path, and TODO
      
  def P2(self, flower: Flower, dumbbell: Dumbbell, edge: Edge) -> None:
    """
    Connects a dumbbell to a flower in some tree.

    (P2) Naplnila sa hrana e medzi kvetom K na párnej úrovni a činkou H. Nech sa činka H skladá z kvetov 
    H1 a H2 tak, že e vedie do nejakého vrchola vo H1. Hrana e sa pridá do L a činka H sa pripojí k 
    príslušnému stromu tak, že K (na párnej úrovni) bude mať syna H1 (na nepárnej úrovni) a ten bude mať 
    jedného syna H2 (na párnej úrovni).
    """

    # Remove the dumbbell from dumbbells.
    self._dumbbells.remove(dumbbell)

    # Transform the dumbbell into a subtree.
    subtree: Flower = dumbbell.makeIntoSubTree(edge)

    # Connect this subtree to the flower
    flower.children.append(subtree)
    subtree.parent = flower

    # Add the edge to blocking
    self._blockingEdges.append(edge)

  def P3(self, edge: Edge) -> None:
    """
    Naplnila sa hrana spájajúca kvety K a H v jednom strome. Zjavne K aj H sú na párnej úrovni. Nech W je LCA 
    K a H. Keďže W má aspoň 2 synov, musí byť tiež na párnej úrovni. Nech K, K1, ... K2k+1, W a H, H1, ... H2r+1, W
    sú cesty v strome. Z parity vrcholov vyplýva, že ich môžeme obaliť novou bublinou a dostaneme kvet Z na párnej
    úrovni, ktorého stopka je stopka W. Synovia Z budú všetci synovia zahrnutých kvetov. Títo ostanú na nepárnej úrovni.
    """

    K = edge.v1.getTotalOuterFlower()
    H = edge.v2.getTotalOuterFlower()

    if K.depth() % 2 != 0 or H.depth() % 2 != 0:
      raise ValueError("One of the flowers is not on even level")
    
    # Find LCA of K and H
    W = Tree.findLCA(K, H)

    # Get the paths from K to W and H to W and reverse one of them.
    KtoW = K.getPathToPredecessor(W)
    HtoW = K.getPathToPredecessor(W)
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
    flower = Flower(W.parent, W.parentEdge, children, innerFlowers)

    # Change the parent child to the new flower, and the children parents to the new flower.
    for child in children:
      child.parent = flower
    if W.parent != None:
      assert W.parent is not None
      W.parent.children.remove(W)
      W.parent.children.append(flower)

    # Set outerFlower of all inner flowers.
    for flower in innerFlowers:
      flower.outerFlower = flower

  def P4(self, edge: Edge) -> None:
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

    # Find alternating path between the stem of T1 and T2 through the edge
    alternatingPath: List[Edge] = [] # TODO
    
    # Find out what are the outer flowers of this path. Also save the edges connecting these flowers
    alternatingOuterFlowers: List[Flower] = []
    alternatingOuterFlowersEdges: List[Edge] = []
    for edge in alternatingPath:
      outerFlower1 = edge.v1.getTotalOuterFlower()
      outerFlower2 = edge.v2.getTotalOuterFlower()
      if outerFlower1 not in alternatingOuterFlowers:
        alternatingOuterFlowers.append(outerFlower1)
      if outerFlower2 not in alternatingOuterFlowers:
        alternatingOuterFlowers.append(outerFlower2)
      if outerFlower1 != outerFlower2:
        alternatingOuterFlowersEdges.append(edge)

    # This path has first edge from L and last from L as well.
    # Exchange these edges between L and M.
    addToM = True
    for edge in alternatingPath:
      if addToM:
        self._blockingEdges.remove(edge)
        self._selectedEdges.append(edge)
      else:
        self._selectedEdges.remove(edge)
        self._blockingEdges.append(edge)
      addToM = not addToM

    # Destructurize the tree into dumbbells
    # First, make each pair from the path into dumbbells
    assert len(alternatingOuterFlowers) % 2 == 0
    for i in range(0, len(alternatingOuterFlowers), 2):
      self._dumbbells.append(Dumbbell(alternatingOuterFlowers[i], alternatingOuterFlowers[i+1], alternatingOuterFlowersEdges[i]))
    
    # Then, process the other part of the tree
    # We need to find the subtrees, which are not a part of the alternating path
    subtrees: list[Flower] = Tree.getSubtreesNotInAlternatingPath(alternatingOuterFlowers[0], alternatingOuterFlowers) + Tree.getSubtreesNotInAlternatingPath(alternatingOuterFlowers[-1], alternatingOuterFlowers)
    for subtree in subtrees:
      self._dumbbells.extend(subtree.changeSubtreeIntoDumbbells())

    # Finally delete the trees so only dumbbells will be left.
    for tree in self._trees:
      if tree.root == alternatingOuterFlowers[0] or tree.root == alternatingOuterFlowers[-1]:
        self._trees.remove(tree)
