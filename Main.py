#!/usr/bin/python3
import random
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPainter, QStaticText, QColor, QFont
from PyQt5.QtWidgets import QWidget, QApplication

from City import City
from Constants import Constants
from Hospital import Hospital, hospital
from Person import PersonStatus

global worldTime
worldTime=0

# 感染人数的线程
class InfecteThread(QThread):
    def __int__(self,parent=None):
        super(InfecteThread,self).__init__(parent)

    def setCity(self,city):
        self.city=city

    def run(self):
        index=0
        while True :
            if index==len(self.city.personPool):
             index=0
            movedPerson=self.city.personPool[index]
            if movedPerson!=None:
                for sickPerson in self.city.infected|self.city.shaowed:
                         if sickPerson.state == PersonStatus.FROZEN:
                            continue
                         if sickPerson==movedPerson:
                             continue
                         randomRate = random.random()
                         print(movedPerson.distance(sickPerson))
                         if randomRate < Constants.BROAD_RATE and movedPerson.distance(sickPerson) < Constants.SAFE_DIST :
                             movedPerson.beShaowedInfect(worldTime)
            index+=1


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.resize(1200, 800)
        self.setStyleSheet("background-color:black;")
        self.setWindowTitle("病毒传播模型")
        self.city=City()
        self.initInfectedPerson()
        self.timer = QTimer()
        self.timer.setInterval(100)  # 500毫秒
        self.timer.timeout.connect(self.refresh)
        self.timer.start()
        self.thread=InfecteThread()
        self.thread.setCity(self.city)
        self.thread.start()

    # 初始化感染人数
    def initInfectedPerson(self):
        personPool=self.city.personPool
        size=len(personPool)
        count=0
        while count<Constants.ORIGINAL_COUNT:
         #随机感染时间0-Constans.SHADOW_TIME以内
         infectTime=random.randint(0,Constants.SHADOW_TIME)
         index=random.randint(0,size)
         p=personPool[index]
         if not p.isInfected():
             global worldTime
             if worldTime<infectTime:
                 worldTime=infectTime
             p.beShaowedInfect(infectTime)
             count+=1

    def displayHospital(self,qp):
        # 绘制医院边界
        self.hospital=Hospital()
        qp.drawRect(self.hospital.x, self.hospital.y,
                    self.hospital.width, self.hospital.height)
        qp.setFont(QFont('Arial', 20))
        qp.setPen(QColor(0x00ff00))
        qp.drawStaticText(self.hospital.x,
                          self.hospital.y - 50,
                          QStaticText("医院"))


    def displayNumber(self,qp):
        qp.setPen(QColor(0xdddddd))
        qp.drawStaticText(16,40,QStaticText("城市总人数：%s"%Constants.CITY_PERSON_SIZE))
        qp.setPen(QColor(0xdddddd))
        healthNumber=Constants.CITY_PERSON_SIZE-len(self.city.shaowed)-len(self.city.infected)
        qp.drawStaticText(16,64,QStaticText("健康者人数：%s"%healthNumber))
        qp.setPen(QColor(0xffee00))
        qp.drawStaticText(16,88,QStaticText("潜伏者人数：%s"%len(self.city.shaowed)))
        qp.setPen(QColor(0xff0000))
        qp.drawStaticText(16, 112,QStaticText("感染者人数:%s"%len(self.city.infected)))
        qp.setPen(QColor(0x48FFFC))
        qp.drawStaticText(16, 136,QStaticText("已隔离人数:%s"%hospital.sickNumber))
        qp.setPen(QColor(0x00ff00))
        left=len(hospital.emptyBeds)
        qp.drawStaticText(16, 160,QStaticText("空余病床:%s"%left))

    def refresh(self):
        global worldTime
        worldTime+=1
        self.update() # 重绘事件，也就是触发paintEvent函数。

    '''重新实现绘制事件'''
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.displayNumber(qp)
        self.displayHospital(qp)
        self.displayPerson(qp)
        qp.end()

    def displayPerson(self,qp):
       qp.setPen(Qt.green)
       for p in self.city.personPool:
           p.update(worldTime)
           if p.getState()==PersonStatus.NORMAL:
               qp.setPen(QColor(0xdddddd))
           elif  p.getState()==PersonStatus.SHADOW:
               qp.setPen(QColor(0xffee00))
           elif  p.getState()==PersonStatus.CONFIRMED:
               qp.setPen(QColor(0xff0000))
           else:
               qp.setPen(QColor(0x48FFFC))
           qp.drawEllipse(p.x, p.y,2,2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Widget()
    form.show()
    app.exec_()


