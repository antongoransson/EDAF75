import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from database import Database

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Krusty Cookie'
        self.left = 50
        self.top = 50
        self.width = 900
        self.height = 600
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()


class MyTableWidget(QWidget):
    CUSTOMER, ADDRESS = range(2)
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.db = parent.db
        # self.createTable()
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1,"Tab 1")
        self.tabs.addTab(self.tab2,"Tab 2")
        self.tabs.addTab(self.tab3,"Tab 3")

        # Create first tab
        self.creatTab1()
        self.tab1.setLayout(self.tab1.layout)

        # Create second tab
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

        self.tab2.setLayout(self.tab2.layout)

        #Create tab 3
        self.tab3.layout = QVBoxLayout()
        self.pushButton1 = QPushButton("PyQt5 button")
        self.pushButton1.clicked.connect(self.on_click)
        self.tab3.layout.addWidget(self.pushButton1)
        self.tab3.setLayout(self.tab3.layout)


        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    # def createTable(self):
    #
    #     # Create table
    #     self.tableWidget = QTableWidget()
    #     self.tableWidget.setColumnCount(1)
    #     self.tableWidget.resize(400, 250)
    #     movies = self.db.get_customers()
    #     for i in range (len(movies)):
    #         self.currentRowCount = self.tableWidget.rowCount() #necessary even when there are no rows in the table
    #         self.tableWidget.insertRow(self.currentRowCount)
    #         self.tableWidget.setItem(i, 0 , QTableWidgetItem(movies[i]))
    #     self.tableWidget.setHorizontalHeaderLabels(["Movie Name"])
    #     header = self.tableWidget.horizontalHeader()
    #     header.setSectionResizeMode(0, QHeaderView.Stretch)
    #     # self.tableWidget.move(100, 100)
    #
    #     # table selection change
    #     self.tableWidget.doubleClicked.connect(self.on_click)

    def creatTab1(self):
        self.tab1.layout = QVBoxLayout()
        # self.tab1.layout.addWidget(self.tableWidget)
        self.h_layout = QHBoxLayout()
        self.horizontalGroupBox = QGroupBox("Select column to filter on")
        self.h__search_layout = QHBoxLayout()
        self.horizontal_searchGroupBox = QGroupBox("Search")

        self.search_box = QLineEdit(self)
        self.search_box.resize(280,40)
        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.search_movie)
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_search)
        self.search_box.returnPressed.connect(self.search_button.click)

        self.h__search_layout.addWidget(self.search_box)
        self.h__search_layout.addWidget(self.search_button)
        self.h__search_layout.addWidget(self.reset_button)
        self.horizontal_searchGroupBox.setLayout(self.h__search_layout)

        self.modal_button = QPushButton('Add Customer', self)
        self.modal_button.clicked.connect(self.modal_onclick)

        self.cb = QComboBox()
        self.cb.addItems(["C", "C++", "Java", "C#", "Python"])
        self.cb.currentIndexChanged.connect(self.selectionchange)
        # self.h_layout.addWidget(self.cb_text)
        self.h_layout.addWidget(self.cb)
        self.horizontalGroupBox.setLayout(self.h_layout)


        self.dataGroupBox = QGroupBox("Customers")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)

        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)

        model = self.createCustomerModel(self)
        self.model = model
        self.dataView.setModel(model)
        self.update_view()

        self.tab1.layout.addWidget(self.dataGroupBox)
        self.tab1.layout.addWidget(self.modal_button)
        self.tab1.layout.addWidget(self.horizontalGroupBox)
        self.tab1.layout.addWidget(self.horizontal_searchGroupBox)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    @pyqtSlot()
    def on_click1(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")

    @pyqtSlot()
    def modal_onclick(self):
        name, address, ok = DateDialog.getInfo()
        if (ok):
            self.db.insert_customer(name, address)
            self.update_view()

    @pyqtSlot()
    def reset_search(self):
        self.update_view()

    def update_view(self):
        self.model.setRowCount(0)
        customers = self.db.get_customers()
        # self.tableWidget.setHorizontalHeaderLabels(["Movie Name"])
        customers.sort(key=lambda tup: tup.name, reverse= True)
        for customer in customers:
            self.addCustomer(self.model, customer.name, customer.address)

    @pyqtSlot()
    def search(self):
        textboxValue = self.search_box.text()
        items = self.tableWidget.findItems(self.search_box.text(), Qt.MatchContains)
        if items:
            results = '\n'.join('row %d column %d' % (item.row() + 1, item.column() + 1) for item in items)
        else:
            results = 'Found Nothing'
        QMessageBox.information(self, 'Search Results', results)
        # QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")

    @pyqtSlot()
    def search_movie(self):
        customer = self.db.get_customer(self.search_box.text())
        print(customer)
        if (len(customer) > 0):
            self.model.setRowCount(0)
            self.addCustomer(self.model, customer[0].name, customer[0].address)
        else:
            self.search_box.setText("")
        # QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)

    @pyqtSlot()
    def selectionchange(self):
        text = self.cb.currentText()
        print(text)

    def createCustomerModel(self, parent):
        model = QStandardItemModel(0, 2, parent)
        model.setHeaderData(self.CUSTOMER, Qt.Horizontal, "Customer")
        model.setHeaderData(self.ADDRESS, Qt.Horizontal, "Address")
        return model

    def addCustomer(self, model, customer, address):
        model.insertRow(0)
        model.setData(model.index(0, self.CUSTOMER), customer)
        model.setData(model.index(0, self.ADDRESS), address)


class DateDialog(QDialog):
    def __init__(self, parent = None):
        super(DateDialog, self).__init__(parent)

        layout = QVBoxLayout(self)

        # nice widget for editing the date
        # self.datetime = QDateTimeEdit(self)
        # self.datetime.setCalendarPopup(True)
        # self.datetime.setDateTime(QDateTime.currentDateTime())
        self.textbox = QLineEdit(self)
        self.textbox1 = QLineEdit(self)

        self.h_layout1 = QHBoxLayout()
        self.horizontalGroupBox1 = QGroupBox("Customer name")

        self.h_layout1.addWidget(self.textbox)
        self.horizontalGroupBox1.setLayout(self.h_layout1)

        self.h_layout2 = QHBoxLayout()
        self.horizontalGroupBox2 = QGroupBox("Address name")

        self.h_layout2.addWidget(self.textbox1)
        self.horizontalGroupBox2.setLayout(self.h_layout2)


        layout.addWidget(self.horizontalGroupBox1)
        layout.addWidget(self.horizontalGroupBox2)
        # layout.addWidg    et(self.datetime)
        # layout.addWidget(self.textbox)
        # layout.addWidget(self.textbox1)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # get current date and time from the dialog
    def dateTime(self):
        return self.datetime.dateTime()

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getInfo(parent = None):
        dialog = DateDialog(parent)
        result = dialog.exec_()
        # date = dialog.dateTime()
        return dialog.textbox.text(), dialog.textbox1.text(), result == QDialog.Accepted  # (date.date(), date.time(), result == QDialog.Accepted)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
