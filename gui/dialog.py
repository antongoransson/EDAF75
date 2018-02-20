from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Dialog(QDialog):
    def __init__(self, fields, default_vals, title, parent):
        super(Dialog, self).__init__(parent)

        if default_vals is None:
            default_vals = ['' for field in fields]
        layout = QVBoxLayout(self)
        self.fields = fields
        self.setWindowTitle(title)
        self.resize(600, 600)

        self.layouts = [QHBoxLayout() for field in fields]
        self.group_boxes = [QGroupBox(field) for field in fields]
        self.textboxes = [QLineEdit(self) for x in range(len(fields))]
        for i in range(len(fields)):
            self.textboxes[i].setText(default_vals[i])
            self.layouts[i].addWidget(self.textboxes[i])
            self.group_boxes[i].setLayout(self.layouts[i])

        for gb in self.group_boxes:
            layout.addWidget(gb)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getInfo(fields, default_vals = None, title = 'Dialog', parent = None):
        dialog = Dialog(fields, default_vals, title, parent)
        result = dialog.exec_()
        return_val = [textbox.text() for textbox in dialog.textboxes]
        return_val.append(result == QDialog.Accepted)
        return return_val
        # return dialog.textbox.text(), dialog.textbox1.text(), result == QDialog.Accepted
