from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from dialog import Dialog

class RecipeTab(QWidget):
    RECIPE, = range(1)
    RAW_MATERIAL, AMOUNT, AMOUNT_LEFT = range(3)

    def __init__(self, db, parent = None):
        super(RecipeTab, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.db = db
        self.h_layout = QHBoxLayout()
        self.h__op_layout = QHBoxLayout()
        self.horizontal_opGroupBox = QGroupBox("Handle Recipes")

        self.modal_button = QPushButton('Add', self)
        # self.modal_button.clicked.connect(self.modal_onclick)
        self.remove_button = QPushButton('Remove', self)
        self.remove_button.clicked.connect(self.remove_recipe)

        self.h__op_layout.addWidget(self.modal_button)
        self.h__op_layout.addWidget(self.remove_button)
        self.horizontal_opGroupBox.setLayout(self.h__op_layout)

        self.dataGroupBox = QGroupBox()
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)
        self.dataView.setSortingEnabled(True)
        self.dataView.clicked.connect(self.view_onclick)

        self.rm_dataView = QTreeView()
        self.rm_dataView.setRootIsDecorated(False)
        self.rm_dataView.setAlternatingRowColors(True)
        self.rm_dataView.setSortingEnabled(True)
        self.rm_dataView.clicked.connect(self.rmview_onclick)
        # self.rm_dataView.selectionChanged.connect(self.test)

        self.rm_button_labels=['Add', 'Update', 'Remove']
        self.rm_buttons_onclick = [self.add_onclick, self.update_onclick, self.remove_onclick]
        self.rm_buttons = [0] * 3
        hbox = QHBoxLayout()
        for i in range(len(self.rm_buttons)):
            self.rm_buttons[i] = QPushButton(self.rm_button_labels[i], self)
            self.rm_buttons[i].clicked.connect(self.rm_buttons_onclick[i])
            self.rm_buttons[i].setEnabled(i == 0)
            hbox.addWidget(self.rm_buttons[i])

        self.search_box = QLineEdit(self)
        self.search_box.resize(280, 40)
        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.search_raw_m)
        self.search_box.returnPressed.connect(self.search_button.click)
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_search)
        dataLayout = QHBoxLayout()

        vbox = QVBoxLayout()

        h_searchbox = QHBoxLayout()
        vbox.addWidget(self.rm_dataView)

        h_searchbox.addWidget(self.search_box)
        h_searchbox.addWidget(self.search_button)
        h_searchbox.addWidget(self.reset_button)
        vbox.addLayout(hbox)
        vbox.addLayout(h_searchbox)
        dataLayout.addWidget(self.dataView)
        dataLayout.addLayout(vbox)
        # dataLayout.addWidget(self.rm_dataView)
        self.dataGroupBox.setLayout(dataLayout)

        self.recipe_model = self.createRecipeModel(self)

        self.rm_model = self.createRawMaterialModel(self)
        self.dataView.setModel(self.recipe_model)

        self.rm_dataView.setModel(self.rm_model)
        self.update_recipe_view()
        self.update_raw_material_view()

        self.layout.addWidget(self.dataGroupBox)
        # self.layout.addWidget(self.horizontal_opGroupBox)


    @pyqtSlot()
    def add_onclick(self):
        raw_material, amount, ok = Dialog.getInfo(['Raw material', 'Amount'], 'Add')
        if (ok):
            self.db.insert_raw_material(raw_material, amount)
            self.update_raw_material_view()

    @pyqtSlot()
    def remove_onclick(self):
        index = self.rm_dataView.selectedIndexes()[0]
        item = index.model().itemFromIndex(index)
        self.db.delete_raw_material(item.text())
        self.update_raw_material_view()

    @pyqtSlot()
    def update_onclick(self):
        rm_index, _, amount_index = self.rm_dataView.selectedIndexes()
        raw_m = rm_index.model().itemFromIndex(rm_index)
        amount = amount_index.model().itemFromIndex(amount_index)
        amount, ok = Dialog.getInfo(['Amount'], [amount.text()], 'Update')
        if (ok):
            item = rm_index.model().itemFromIndex(rm_index)
            self.db.update_raw_material(item.text(), amount)
            self.update_raw_material_view()

    @pyqtSlot()
    def view_onclick(self):
        index = self.dataView.selectedIndexes()[0]
        recipe = index.model().itemFromIndex(index).text()
        self.update_raw_material_view(recipe)
        self.search_box.setText("")

    @pyqtSlot()
    def rmview_onclick(self):
        for b in self.rm_buttons:
            b.setEnabled(True)

    @pyqtSlot()
    def remove_recipe(self):
        index = self.dataView.selectedIndexes()[0]
        item = index.model().itemFromIndex(index)
        self.db.delete_customer(item.text())
        self.update_recipe_view()


    @pyqtSlot()
    def search_raw_m(self):
        self.dataView.clearSelection()
        self.disable_buttons()
        raw_m = self.db.get_raw_materials(self.search_box.text())
        self.rm_model.setRowCount(0)
        if (len(raw_m) > 0):
            for r in raw_m:
                self.addRawMaterial(self.rm_model, r.raw_material, '-', r.amount)
        else:
            self.search_box.setText("")
            self.addRawMaterial(self.rm_model, 'No results found', '', '')
        self.rm_dataView.resizeColumnToContents(0)

    @pyqtSlot()
    def reset_search(self):
        self.rm_dataView.clearSelection()
        self.dataView.clearSelection()
        self.update_raw_material_view()
        self.search_box.setText("")
        self.search_box.setFocus()

    def disable_buttons(self):
        for i in [1, 2]:
            self.rm_buttons[i].setEnabled(False)

    @pyqtSlot()
    def test(self):
        index = self.dataView.selectedIndexes()
        print(index)

    def update_recipe_view(self):
        self.recipe_model.setRowCount(0)
        recipes = self.db.get_all_recipes()
        recipes.sort(reverse = True)
        for recipe in recipes:
            self.addRecipe(self.recipe_model, recipe)
        self.dataView.resizeColumnToContents(0)

    def update_raw_material_view(self, recipe = None):
        self.rm_model.setRowCount(0)
        self.disable_buttons()
        if recipe is None:
            raw_materials =  self.db.get_all_raw_materials()
        else:
            raw_materials = self.db.get_recipe_items(recipe)
        raw_materials.sort(key=lambda tup: tup.raw_material, reverse= True)
        for rm in raw_materials:
            self.addRawMaterial(self.rm_model, rm.raw_material, rm.amount, rm.amount_left)
        self.rm_dataView.resizeColumnToContents(0)
        for i in [1, 2]:
            self.rm_dataView.header().setSectionResizeMode(i, QHeaderView.Stretch);

    def createRecipeModel(self, parent):
        model = QStandardItemModel(0, 1, parent)
        model.setHeaderData(self.RECIPE, Qt.Horizontal, "Recipe")
        return model

    def createRawMaterialModel(self, parent):
        model = QStandardItemModel(0, 3, parent)
        model.setHeaderData(self.RAW_MATERIAL, Qt.Horizontal, "Raw material")
        model.setHeaderData(self.AMOUNT, Qt.Horizontal, "Amount")
        model.setHeaderData(self.AMOUNT_LEFT, Qt.Horizontal, "Amount left")
        return model

    def addRecipe(self, model, recipe):
        model.insertRow(0)
        model.setData(model.index(0, self.RECIPE), recipe)

    def addRawMaterial(self, model, raw_material, amount, amount_left):
        model.insertRow(0)
        model.setData(model.index(0, self.RAW_MATERIAL), raw_material)
        model.setData(model.index(0, self.AMOUNT), amount)
        model.setData(model.index(0, self.AMOUNT_LEFT), amount_left)
