class City(object):
    def __init__(self,centerX,centerY) -> None:
        super().__init__()
        self.centerX=centerX
        self.centerY=centerY

    def getCenterX(self):
        return self.centerX

    def setCenterX(self,centerX):
        self.centerX = centerX

    def getCenterY(self) :
        return self.centerY

    def setCenterY(self,centerY) :
        self.centerY = centerY
city=City(400,400)
