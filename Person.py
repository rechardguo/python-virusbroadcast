import random
from enum import unique, Enum

import math

from Constants import Constants
from Hospital import hospital


@unique
class PersonStatus(Enum):
    NORMAL = 0 #未被感染
    SHADOW = 1 #潜伏者
    CONFIRMED = 2 #感染者
    FROZEN =3 #已隔离


class Person(object):
    def __init__(self,id,x,y,city) -> None:
        super().__init__()
        self.id=id
        self.x=x
        self.y=y
        self.city=city
        self.state=PersonStatus.NORMAL
        self.infectedTime = 0 # 感染时间
        self.confirmedTime = 0 # 确诊时间
        self.inHospital=False

    def __eq__(self,other):
        if isinstance(other,Person):
          return self.id==other.id
        else:
          return False

    def __ne__(self,other):
      return(not self.__eq__(other))

    def __hash__(self):
      return hash(self.id)


    def getCity(self):
        return self.city

    def getState(self):
        return self.state

    def isInfected(self):
        return self.state.value > PersonStatus.NORMAL.value

    def beShaowedInfect(self,worldTime):
        self.state=PersonStatus.SHADOW
        self.infectedTime = worldTime
        self.city.shaowed.add(self)

    def wantMove(self):
         value = random.gauss(1,1)
         return value < Constants.u

    def moveTo(self,x,y):
        self.x=x
        self.y=y

    def update(self,worldTime):
        if self.state == PersonStatus.FROZEN:
         return
        if self.state.value >= PersonStatus.SHADOW.value and worldTime - self.infectedTime >= Constants.HOSPITAL_RECEIVE_TIME:
            bed = hospital.takeSick() #查找空床位
            if bed != None :
             #安置病人
             self.state = PersonStatus.FROZEN
             self.x = bed.getX()
             self.y = bed.getY()
             return
        if worldTime - self.infectedTime > Constants.SHADOW_TIME and self.state == PersonStatus.SHADOW:
                self.state = PersonStatus.CONFIRMED #潜伏者发病
                self.confirmedTime = worldTime #刷新时间
                self.city.shaowed.remove(self)
                self.city.infected.add(self)

        #行动
        self.action();
        if self.state.value >= PersonStatus.SHADOW.value:
         return;
        # for sickPerson in self.city.infected+self.city.shaowed:
        #         randomRate = random.random()
        #         if randomRate < Constants.BROAD_RATE and self.distance(sickPerson) < Constants.SAFE_DIST :
        #             self.beInfect(worldTime)


    def distance(self,person):
        return math.sqrt(math.pow(self.x - person.x, 2) + math.pow(self.y - person.y, 2));

    def action(self):
        if self.state == PersonStatus.FROZEN:
             return
        if not self.wantMove():
             return
        dx=random.gauss(1,10)
        nx=self.x+dx
        if nx>800:
            nx=800
        dy=random.gauss(1,10)
        ny=self.y+dy
        if ny>800:
            ny=800
        self.moveTo(nx,ny)

if __name__ == '__main__':
   while True:
    print(random.random() )


#        if (moveTarget == null || moveTarget.isArrived()) {
#
#         double targetX = targetSig * new Random().nextGaussian() + targetXU;
#         double targetY = targetSig * new Random().nextGaussian() + targetYU;
#         moveTarget = new MoveTarget((int) targetX, (int) targetY);
#
#         }
#
#
# int dX = moveTarget.getX() - x;
# int dY = moveTarget.getY() - y;
# double length = Math.sqrt(Math.pow(dX, 2) + Math.pow(dY, 2));
#
# if (length < 1) {
# moveTarget.setArrived(true);
# return;
# }
# int udX = (int) (dX / length);
# if (udX == 0 && dX != 0) {
# if (dX > 0) {
# udX = 1;
# } else {
# udX = -1;
# }
# }
# int udY = (int) (dY / length);
# if (udY == 0 && udY != 0) {
# if (dY > 0) {
# udY = 1;
# } else {
# udY = -1;
# }
# }
#
# if (x > 700) {
# moveTarget = null;
# if (udX > 0) {
# udX = -udX;
# }
# }


