"""
Минипланировщик
Используя виджеты календаря, выбора времени, отображения списка и другие,
напишите программу-ежедневник с графическим пользовательским интерфейсом на PyQT.
Класс, реализующий это приложение назовите SimplePlanner
Виджет выбора времени должен называться timeEdit и иметь тип QTimeEdit.
Календарь реализуйте через QCalendarWidget и назовите этот виджет calendarWidget.
Кнопку добавления события назовите addEventBtn.
Для отображения списка событий используйте QListWidget, назовите этот виджет eventList.
Пользователь должен иметь возможность ввести название события, выбирать дату и время.
После нажатия на кнопку «Добавить» событие должно добавляться в список событий.
События должны быть отсортированы по возрастанию даты.
Для размещения виджетов используйте различные layout.
Дату/время следует преобразовывать в текст в такой формат "2020-03-04 12:34:00"
"""

import datetime
import io
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtWidgets

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="gemometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>767</width>
    <height>348</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Минипланировщик</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QHBoxLayout" name="horizontalLayout">
    <item>
     <layout class="QVBoxLayout" name="verticalLayout">
      <item>
       <widget class="QTimeEdit" name="timeEdit"/>
      </item>
      <item>
       <widget class="QCalendarWidget" name="calendarWidget"/>
      </item>
      <item>
       <widget class="QLineEdit" name="lineEdit"/>
      </item>
      <item>
       <widget class="QPushButton" name="addEventBtn">
        <property name="text">
         <string>Добавить событие</string>
        </property>
       </widget>
      </item>
     </layout>
    </item>
    <item>
     <widget class="QListWidget" name="eventList">
      <property name="minimumSize">
       <size>
        <width>200</width>
        <height>0</height>
       </size>
      </property>
     </widget>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>767</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class Event():
    def __init__(self, datetime, title):
        self.datetime = datetime
        self.title = title

    def __str__(self):
        return f"{self.datetime} - {self.title}"


class SimplePlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)

        self.addEventBtn.clicked.connect(self.add)

        self.events = []

    def add(self):
        t = datetime.datetime(self.calendarWidget.selectedDate().year(),
                              self.calendarWidget.selectedDate().month(),
                              self.calendarWidget.selectedDate().day(),
                              self.timeEdit.time().hour(),
                              self.timeEdit.time().minute())
        title = self.lineEdit.text()
        self.events.append(Event(t, title))
        self.events.sort(key=lambda x: x.datetime)

        self.eventList.clear()
        self.eventList.addItems([str(event) for event in self.events])


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    ex = SimplePlanner()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
