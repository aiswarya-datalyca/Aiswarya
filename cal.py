
# importing libraries 
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 
  
"""
class Window(QMainWindow): 
  
    def __init__(self): 
        super().__init__() 
  
        # setting title 
        self.setWindowTitle("Python ") 
  
        # setting geometry 
        self.setGeometry(100, 100, 600, 400) 
  
        # calling method 
        self.UiComponents() 
  
        # showing all the widgets 
        self.show() 
  
    # method for components 
    def UiComponents(self): 
  
        # creating a QCalendarWidget object 
        calender = QCalendarWidget(self) 
  
        # setting geometry to the calender 
        calender.setGeometry(50, 50, 400, 250) 
        # format 
        format = QTextCharFormat() 
        format.setFont(QFont('Times', 15)) 
        # date 
        date = QDate(2020, 6, 10) 
  
        # setting date text format 
        calender.setDateTextFormat(date,format) 
        #calender.setDateEditAcceptDelay(2000)    
        calender.setGridVisible(True)
        calender.clicked[date].connect(self.showDate)
# create pyqt5 app 
App = QApplication(sys.argv) 
  
# create the instance of our Window 
window = Window() 
  
# start the app 
sys.exit(App.exec()) 

"""
class selectedDate(QWidget):
    def __init__(self):
        super(selectedDate, self).__init__()
        self.layout = QVBoxLayout(self)
        self.selection = QLineEdit("Click to Enter Date", self)
        self.layout.addWidget(self.selection)
        self.layout.addWidget(self.selection)
        self.selection.installEventFilter(self)
        #self.show()

    def mousePressEvent(self, e):
        self.myCal()
        super(selectedDate, self).mousePressEvent(e)

    def eventFilter(self, object, e):
        if self.layout.indexOf(object) != -1:
            if e.type() == e.MouseButtonPress:
                print ("hello")
                pass

        return super(selectedDate, self).eventFilter(object, e)



    def myCal(self):
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.clicked[QDate].connect(self.showDate)

        # create a new window that contains the calendar
        self.calendarWindow = QWidget()
        hbox = QHBoxLayout()
        hbox.addWidget(self.cal)
        self.calendarWindow.setLayout(hbox)
        self.calendarWindow.setGeometry(300, 300, 415, 350)
        self.calendarWindow.setWindowTitle('Calendar')
        # open this new window
        self.calendarWindow.show()

    def showDate(self, date):
        self.selection.setText(date.toString())

app = QApplication(sys.argv)
top = selectedDate()
app.exec_()
