import random

from Constants import Constants
from Person import Person

CITY_X=400
CITY_Y=400
class City(object):
    def __init__(self) -> None:
        super().__init__()
        self.x=CITY_X
        self.y=CITY_Y
        self.personPool=[]
        self.initPerson()
        self.infected=set() # 感染的人口
        self.shaowed=set() # 潜在感染的人口


    def initPerson(self):
        for i in range(Constants.CITY_PERSON_SIZE):
            x = random.gauss(CITY_X,110)
            y = random.gauss(CITY_Y,110)
            if x>800:
                x=800
            if y>800:
                y=800
            p=Person(i,x,y,self)
            self.personPool.append(p)
