from Constants import Constants


class Bed(object):
    def __init__(self,x,y) -> None:
        super().__init__()
        self.x=x
        self.y=y
        self.empty=True

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def isEmpty(self):
        return self.empty

    def taken(self):
        self.empty=True

class Hospital(object):
    def __init__(self) -> None:
        super().__init__()
        self.x=1000
        self.y=110
        self.width=100
        self.height=606
        self.sickNumber=0# 病人数
        self.emptyBeds=[]

        if Constants.BED_COUNT == 0:
            self.width = 0;
            self.height = 0;
        column = Constants.BED_COUNT // 100;
        for col in range(column):
            row=0
            while row<=610:
                self.emptyBeds.append(Bed(self.x+col*6,self.y+row))
                row+=6

    def takeSick(self):
        if len(self.emptyBeds)>0:
            self.sickNumber+=1
            return self.emptyBeds.pop()
        return None

hospital=Hospital()




