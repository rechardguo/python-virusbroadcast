class Bed(object):

    def __init__(self,x,y) -> None:
        super().__init__()
        self.x=x
        self.y=y
        self.empty=True

    def isEmpty(self):
        return self.empty

    def setEmpty(self,empty):
        self.empty = empty

    def getX(self):
        return self.x

    def getY(self):
        return self.y