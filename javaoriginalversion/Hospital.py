from javaoriginalversion.Bed import Bed
from javaoriginalversion.Constants import Constants

class Hospital (object):

    def __init__(self) -> None:
        super().__init__()
        self.x = 800
        self.y = 110
        self.width=100
        self.height = 606
        self.beds=[]
        if Constants.BED_COUNT == 0:
          self.width = 0
          self.height = 0
        column = Constants.BED_COUNT // 100;
        width = column * 6
        for  i in range(column):
            j=10
            while j<=610:
               bed = Bed(800 + i * 6, 100 + j)
               self.beds.append(bed)
               j+=6

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getX(self):
        return self.x

    def getY(self) :
        return self.y


    def pickBed(self):
        for  bed in self.beds:
            if bed.isEmpty()==True:
                return bed
        return None;

hospital = Hospital()

