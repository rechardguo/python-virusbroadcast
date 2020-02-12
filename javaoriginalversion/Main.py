import random

import sys

import os

from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QStaticText, QFont
from PyQt5.QtWidgets import QWidget, QApplication

from javaoriginalversion.Constants import Constants
from javaoriginalversion.Hospital import hospital
from javaoriginalversion.PersonPool import personPool
from javaoriginalversion.State import State

global worldTime
worldTime=0

class PersonActionThread(QThread):
    def __int__(self,parent=None):
        super(PersonActionThread,self).__init__(parent)

    def run(self):
        while True:
         for p in personPool.getPersonList():
             p.update(worldTime)

class Widget(QWidget):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.resize(1000, 800)
            self.setStyleSheet("background-color:black;")
            self.setWindowTitle("瘟疫传播模拟")
            self.initInfected()
            self.timer = QTimer()
            self.timer.setInterval(300)
            self.timer.timeout.connect(self.refresh)
            self.timer.start()
            self.thread=PersonActionThread()
            self.thread.start()

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

        def initInfected(self):
         people = personPool.getPersonList() #获取所有的市民
         i=0
         while i< Constants.ORIGINAL_COUNT:
             person=people[random.randint(0,len(people)-1)]
             if not person.isInfected():
                 person.beInfected(worldTime)
             i+=1

        def displayHospital(self,qp):
            # 绘制医院边界
            self.hospital=hospital
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
            qp.drawStaticText(16,64,QStaticText("健康者人数：%s"%personPool.getPeopleSize(State.NORMAL)))
            qp.setPen(QColor(0xffee00))
            qp.drawStaticText(16,88,QStaticText("潜伏者人数：%s"%personPool.getPeopleSize(State.SHADOW)))
            qp.setPen(QColor(0xff0000))
            qp.drawStaticText(16, 112,QStaticText("感染者人数:%s"%personPool.getPeopleSize(State.CONFIRMED)))
            qp.setPen(QColor(0x48FFFC))
            qp.drawStaticText(16, 136,QStaticText("已隔离人数:%s"%personPool.getPeopleSize(State.FREEZE)))
            qp.setPen(QColor(0x00ff00))
            left=Constants.BED_COUNT - personPool.getPeopleSize(State.FREEZE)
            qp.drawStaticText(16, 160,QStaticText("空余病床:%s"%left))

        def displayPerson(self,qp):
            qp.setPen(Qt.green)
            for p in personPool.getPersonList():
                if p.getState()==State.NORMAL:
                    qp.setPen(QColor(0xdddddd))
                elif  p.getState()==State.SHADOW:
                    qp.setPen(QColor(0xffee00))
                elif  p.getState()==State.CONFIRMED:
                    qp.setPen(QColor(0xff0000))
                else:
                    qp.setPen(QColor(0x48FFFC))
                qp.drawEllipse(p.x, p.y,2,2)

if __name__ == "__main__":
    o_path = os.getcwd()
    print(o_path)
    app = QApplication(sys.argv)
    form = Widget()
    form.show()
    app.exec_()