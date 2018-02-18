from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Dialog(QDialog):
    def __init__(self, parent = None):
        super(Dialog, self).__init__(parent)

        layout = QVBoxLayout(self)
        self.setWindowTitle("Add customer")
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
        dialog = Dialog(parent)
        result = dialog.exec_()
        return dialog.textbox.text(), dialog.textbox1.text(), result == QDialog.Accepted
