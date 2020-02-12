import math
import random
from javaoriginalversion.Constants import Constants
from javaoriginalversion.Hospital import hospital
from javaoriginalversion.MoveTarget import MoveTarget
from javaoriginalversion.State import State


class Person(object):
    def __init__(self,city,x,y) -> None:
        super().__init__()
        self.city=city
        self.x=x
        self.y=y
        self.infectedTime = 0
        self.confirmedTime = 0
        self.targetXU=100 * random.gauss(0,1) + self.x
        self.targetYU=100 * random.gauss(0,1) + self.y
        self.moveTarget=None
        self.state = State.NORMAL
        self.sig = 1
        self.SAFE_DIST = 2
        self.targetSig = 50

    def wantMove(self) :
        value = self.sig * random.gauss(0,1) + Constants.u;
        return value > 0;


    def getState(self) :
        return self.state

    def setState(self,state):
        self.state = state

    def getX(self) :
        return self.x

    def setX(self,x):
        self.x = x

    def getY(self) :
        return self.y

    def setY(self,y):
        self.y = y

    def isInfected(self):
        return self.state >= State.SHADOW

    def beInfected(self,worldTime) :
        self.state = State.SHADOW
        self.infectedTime = worldTime

    def distance(self,person):
        return math.sqrt(math.pow(self.x - person.getX(), 2) + math.pow(self.y - person.getY(), 2));

    def freezy(self) :
        self.state = State.FREEZE

    def moveTo(self,x,y):
        self.x += x;
        self.y += y;

    def action(self) :
        if self.state == State.FREEZE:
            return
        if not self.wantMove():
            return
        if self.moveTarget == None or self.moveTarget.isArrived():
            targetX = self.targetSig * random.gauss(0,1) + self.targetXU
            targetY = self.targetSig * random.gauss(0,1) + self.targetYU
            self.moveTarget = MoveTarget(targetX,targetY)

        dX = self.moveTarget.getX() - self.x;
        dY = self.moveTarget.getY() - self.y;
        length = math.sqrt(math.pow(dX, 2) + math.pow(dY, 2));

        if length < 1:
            self.moveTarget.setArrived(True);
            return

        udX = dX // length;
        if udX == 0 and dX != 0:
            if dX > 0:
                udX = 1
            else :
                udX = -1
        udY = dY // length
        if udY == 0 and udY != 0:
            if dY > 0:
                udY = 1
            else:
                udY = -1

        if self.x > 700:
            self.moveTarget = None;
            if udX > 0:
                udX = -udX
        self.moveTo(udX, udY)

    def update(self,worldTime):
        #TODO:找时间改为状态机
        if self.state >= State.FREEZE:
            return
        if self.state == State.CONFIRMED and worldTime - self.confirmedTime >= Constants.HOSPITAL_RECEIVE_TIME:
            bed = hospital.pickBed() #查找空床位
            if bed != None:
                #安置病人
                self.state = State.FREEZE;
                self.x = bed.getX();
                self.y = bed.getY();
                bed.setEmpty(False);
        if worldTime - self.infectedTime > Constants.SHADOW_TIME and self.state == State.SHADOW:
            self.state = State.CONFIRMED #潜伏者发病
            self.confirmedTime = worldTime #刷新时间

        self.action()
        from javaoriginalversion.PersonPool import personPool
        people = personPool.getPersonList()
        if self.state >= State.SHADOW:
            return
        for  person in people:
            if person.getState() == State.NORMAL:
                continue;
            r=random.randrange(0,1)
            if r < Constants.BROAD_RATE and self.distance(person) < self.SAFE_DIST:
                self.beInfected(worldTime)


