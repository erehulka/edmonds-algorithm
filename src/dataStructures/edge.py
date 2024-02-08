from src.dataStructures.flower import Flower


class Edge:
  v1: Flower
  v2: Flower
  capacity: float

  def getCurrentCharge(self) -> float:
    return self.v1.getTotalCharge() + self.v2.getTotalCharge()
  
  def getEpsilon(self) -> float:
    return self.capacity - self.getEpsilon()
