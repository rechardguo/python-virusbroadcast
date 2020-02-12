import random

from javaoriginalversion.City import city
from javaoriginalversion.Constants import Constants


class PersonPool (object):

    def __init__(self) -> None:
        super().__init__()
        self.personList=[]
        for i in range(Constants.CITY_PERSON_SIZE):
         x = 100 * random.gauss(0,1) + city.getCenterX()
         y = 100 * random.gauss(0,1) + city.getCenterY()
         if x > 700:
          x = 700
         from javaoriginalversion.Person import Person
         self.personList.append(Person(city, x, y))



    def getPersonList(self) :
        return self.personList


    def getPeopleSize(self,state)->int :
        if state == -1:
            return Constants.CITY_PERSON_SIZE;
        i = 0;
        for  person in self.personList:
            if person.getState() == state:
                i+=1
        return i;



personPool=PersonPool()

