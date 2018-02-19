import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from database import Database
from customertab import CustomerTab
from recipetab import RecipeTab

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
        self.tab2 = RecipeTab(db, self)
        self.tab3 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1,"Customers")
        self.tabs.addTab(self.tab2,"Recipes")
        self.tabs.addTab(self.tab3,"Tab 3")

        # Create first tab
        self.tab1.setLayout(self.tab1.layout)

        # Create second tab
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = Database("db.db")
    ex = App(db)
    sys.exit(app.exec_())
