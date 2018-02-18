import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from database import Database
from customertab import CustomerTab

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class App(QMainWindow):

    def __init__(self , db):
        super().__init__()
        self.title = 'Krusty Cookies'
        self.left = 50
        self.top = 50
        self.width = 1800
        self.height = 1000
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.show()


class TabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.db = parent.db
        # Initialize tab screen

        self.tabs = QTabWidget()
        self.tab1 = CustomerTab(db, self)
        # self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1,"Tab 1")
        self.tabs.addTab(self.tab2,"Tab 2")
        self.tabs.addTab(self.tab3,"Tab 3")

        # Create first tab
        # self.creatTab1()
        self.tab1.setLayout(self.tab1.layout)

        # Create second tab
        self.createTab2()
        self.tab2.setLayout(self.tab2.layout)

        #Create tab 3
        self.tab3.layout = QVBoxLayout()
        self.pushButton1 = QPushButton("PyQt5 button")
        self.tab3.layout.addWidget(self.pushButton1)
        self.tab3.setLayout(self.tab3.layout)
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.tab1.search_box.setFocus()
        self.setLayout(self.layout)


    def createTab2(self):
        self.tab2.layout = QVBoxLayout()

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)

        self.tab2.layout.addWidget(self.textbox)

        # Create a button in the window
        self.button = QPushButton('Show text', self)
        self.button.move(20,80)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click1)
        self.tab2.layout.addWidget(self.button)

    @pyqtSlot()
    def on_click1(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = Database("db.db")
    ex = App(db)
    sys.exit(app.exec_())
