from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from dialog import Dialog

class CustomerTab(QWidget):
    CUSTOMER, ADDRESS = range(2)

    def __init__(self, db, parent = None):
        super(CustomerTab, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.db = db

        h_layout = QHBoxLayout()
        horizontalGroupBox = QGroupBox("Select column to filter on")
        h_searchlayout = QHBoxLayout()
        horizontal_searchGroupBox = QGroupBox("Search")
        h_button_layout = QHBoxLayout()
        horizontal_handle_customers_GroupBox = QGroupBox("Handle Customers")

        self.search_box = QLineEdit(self)
        self.search_box.resize(280, 40)
        search_button = QPushButton('Search', self)
        search_button.clicked.connect(self.search_customer)
        reset_button = QPushButton('Reset', self)
        reset_button.clicked.connect(self.reset_search)
        self.search_box.returnPressed.connect(search_button.click)

        h_searchlayout.addWidget(self.search_box)
        h_searchlayout.addWidget(search_button)
        h_searchlayout.addWidget(reset_button)
        horizontal_searchGroupBox.setLayout(h_searchlayout)

        modal_button = QPushButton('Add', self)
        modal_button.clicked.connect(self.modal_onclick)
        remove_button = QPushButton('Remove', self)
        remove_button.clicked.connect(self.remove_customer)

        h_button_layout.addWidget(modal_button)
        h_button_layout.addWidget(remove_button)
        horizontal_handle_customers_GroupBox.setLayout(h_button_layout)

        self.cb = QComboBox()
        self.cb.addItems(['Name', 'Address'])
        self.cb.currentIndexChanged.connect(self.selectionchange)

        h_layout.addWidget(self.cb)
        horizontalGroupBox.setLayout(h_layout)

        dataGroupBox = QGroupBox()
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)
        self.dataView.setSortingEnabled(True)
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        dataGroupBox.setLayout(dataLayout)

        self.model = self.createCustomerModel(self)
        self.dataView.setModel(self.model)
        self.update_view()

        self.layout.addWidget(dataGroupBox)
        self.layout.addWidget(horizontal_handle_customers_GroupBox)
        self.layout.addWidget(horizontalGroupBox)
        self.layout.addWidget(horizontal_searchGroupBox)

    # @pyqtSlot()
    # def on_click(self):
    #     print("\n")
    #     for currentQTableWidgetItem in self.tableWidget.selectedItems():
    #         print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    @pyqtSlot()
    def modal_onclick(self):
        name, address, ok = Dialog.getInfo(['Customer name', 'Address'], 'Add Customer')
        if (ok):
            self.db.insert_customer(name, address)
            self.update_view()


    @pyqtSlot()
    def remove_customer(self):
        index = self.dataView.selectedIndexes()[0]
        item = index.model().itemFromIndex(index)
        self.db.delete_customer(item.text())
        self.update_view()

    @pyqtSlot()
    def reset_search(self):
        self.update_view()
        self.search_box.setText("")
        self.search_box.setFocus()

    def update_view(self):
        self.model.setRowCount(0)
        customers = self.db.get_all_customers()
        customers.sort(key=lambda tup: tup.name, reverse= True)
        for customer in customers:
            self.addCustomer(self.model, customer.name, customer.address)
        # self.dataView.resizeColumnToContents(0)
        self.dataView.header().setSectionResizeMode(0, QHeaderView.Stretch);
        self.dataView.header().setSectionResizeMode(1, QHeaderView.Stretch);

    # @pyqtSlot()
    # def search(self):
    #     textboxValue = self.search_box.text()
    #     items = self.tableWidget.findItems(self.search_box.text(), Qt.MatchContains)
    #     if items:
    #         results = '\n'.join('row %d column %d' % (item.row() + 1, item.column() + 1) for item in items)
    #     else:
    #         results = 'Found Nothing'
    #     QMessageBox.information(self, 'Search Results', results)
    #     # QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
    #     self.textbox.setText("")

    @pyqtSlot()
    def search_customer(self):
        customers = self.db.get_customers(self.search_box.text(),self.cb.currentText().lower())
        self.model.setRowCount(0)
        if (len(customers) > 0):
            for c in customers:
                self.addCustomer(self.model, c.name, c.address)
        else:
            self.search_box.setText("")
            self.addCustomer(self.model, "No results found", "")
        self.dataView.resizeColumnToContents(0)

    @pyqtSlot()
    def selectionchange(self):
        text = self.cb.currentText()
        self.search_box.setFocus()

    def createCustomerModel(self, parent):
        model = QStandardItemModel(0, 2, parent)
        # self.dataView.setStyleSheet("font: 20pt")
        model.setHeaderData(self.CUSTOMER, Qt.Horizontal, "Customer")
        model.setHeaderData(self.ADDRESS, Qt.Horizontal, "Address")
        return model

    def addCustomer(self, model, customer, address):
        model.insertRow(0)
        model.setData(model.index(0, self.CUSTOMER), customer)
        model.setData(model.index(0, self.ADDRESS), address)
