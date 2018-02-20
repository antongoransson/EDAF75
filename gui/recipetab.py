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

        dataGroupBox = QGroupBox()
        self.recipe_data_view = QTreeView()
        self.recipe_data_view.setRootIsDecorated(False)
        self.recipe_data_view.setAlternatingRowColors(True)
        self.recipe_data_view.setSortingEnabled(True)
        self.recipe_data_view.clicked.connect(self.recipe_view_onclick)

        self.raw_mat_data_view = QTreeView()
        self.raw_mat_data_view.setRootIsDecorated(False)
        self.raw_mat_data_view.setAlternatingRowColors(True)
        self.raw_mat_data_view.setSortingEnabled(True)
        self.raw_mat_data_view.clicked.connect(self.raw_mat_view_onclick)

        rm_button_labels=['Add', 'Update', 'Remove']
        rm_buttons_onclick = [self.add_onclick, self.update_onclick, self.remove_onclick]
        self.rm_buttons = [i for i in range(len(rm_button_labels))]
        hbox = QHBoxLayout()
        for i in range(len(self.rm_buttons)):
            self.rm_buttons[i] = QPushButton(rm_button_labels[i], self)
            self.rm_buttons[i].clicked.connect(rm_buttons_onclick[i])
            self.rm_buttons[i].setEnabled(rm_button_labels[i] == 'Add')
            hbox.addWidget(self.rm_buttons[i])

        self.search_box = QLineEdit(self)
        self.search_box.resize(280, 40)
        search_button = QPushButton('Search', self)
        search_button.clicked.connect(self.search_raw_mat)
        self.search_box.returnPressed.connect(search_button.click)
        reset_button = QPushButton('Reset', self)
        reset_button.clicked.connect(self.reset_search)
        dataLayout = QHBoxLayout()

        v_raw_mat_box = QVBoxLayout()

        h_searchbox = QHBoxLayout()
        v_raw_mat_box.addWidget(self.raw_mat_data_view)

        h_searchbox.addWidget(self.search_box)
        h_searchbox.addWidget(search_button)
        h_searchbox.addWidget(reset_button)
        v_raw_mat_box.addLayout(hbox)
        v_raw_mat_box.addLayout(h_searchbox)
        dataLayout.addWidget(self.recipe_data_view)
        dataLayout.addLayout(v_raw_mat_box)
        dataGroupBox.setLayout(dataLayout)

        self.recipe_model = self.createRecipeModel(self)
        self.raw_mat_model = self.createRawMaterialModel(self)

        self.recipe_data_view.setModel(self.recipe_model)
        self.raw_mat_data_view.setModel(self.raw_mat_model)
        self.update_recipe_view()
        self.update_raw_mat_view()

        self.layout.addWidget(dataGroupBox)


    @pyqtSlot()
    def add_onclick(self):
        raw_material, amount, ok = Dialog.getInfo(['Raw material', 'Amount'], 'Add')
        if (ok):
            self.db.insert_raw_material(raw_material, amount)
            self.update_raw_mat_view()

    @pyqtSlot()
    def remove_onclick(self):
        index = self.raw_mat_data_view.selectedIndexes()[0]
        item = index.model().itemFromIndex(index)
        self.db.delete_raw_material(item.text())
        self.update_raw_mat_view()

    @pyqtSlot()
    def update_onclick(self):
        rm_index, _, amount_index = self.raw_mat_data_view.selectedIndexes()
        raw_m = rm_index.model().itemFromIndex(rm_index)
        amount = amount_index.model().itemFromIndex(amount_index)
        amount, ok = Dialog.getInfo(['Amount'], 'Update', [amount.text()])
        if (ok):
            item = rm_index.model().itemFromIndex(rm_index)
            self.db.update_raw_material(item.text(), amount)
            self.update_raw_mat_view()

    @pyqtSlot()
    def recipe_view_onclick(self):
        index = self.recipe_data_view.selectedIndexes()[0]
        recipe = index.model().itemFromIndex(index).text()
        self.update_raw_mat_view(recipe)
        self.search_box.setText("")

    @pyqtSlot()
    def raw_mat_view_onclick(self):
        for b in self.rm_buttons:
            b.setEnabled(True)

    @pyqtSlot()
    def search_raw_mat(self):
        self.recipe_data_view.clearSelection()
        self.disable_buttons()
        raw_mats = self.db.get_raw_materials(self.search_box.text())
        self.raw_mat_model.setRowCount(0)
        if (len(raw_mats) > 0):
            for r in raw_mats:
                self.addRawMaterial(self.raw_mat_model, r.raw_material, '-', r.amount)
        else:
            self.search_box.setText("")
            self.addRawMaterial(self.raw_mat_model, 'No results found', '', '')
        self.raw_mat_data_view.resizeColumnToContents(0)

    @pyqtSlot()
    def reset_search(self):
        self.raw_mat_data_view.clearSelection()
        self.recipe_data_view.clearSelection()
        self.update_raw_mat_view()
        self.search_box.setText("")
        self.search_box.setFocus()

    def disable_buttons(self):
        for i in [1, 2]:
            self.rm_buttons[i].setEnabled(False)

    @pyqtSlot()
    def test(self):
        index = self.recipe_data_view.selectedIndexes()
        print(index)

    def update_recipe_view(self):
        self.recipe_model.setRowCount(0)
        recipes = self.db.get_all_recipes()
        recipes.sort(reverse = True)
        for recipe in recipes:
            self.addRecipe(self.recipe_model, recipe)
        self.recipe_data_view.resizeColumnToContents(0)

    def update_raw_mat_view(self, recipe = None):
        self.raw_mat_model.setRowCount(0)
        self.disable_buttons()
        if recipe is None:
            raw_materials =  self.db.get_all_raw_materials()
        else:
            raw_materials = self.db.get_recipe_items(recipe)
        raw_materials.sort(key = lambda raw_mat: raw_mat.raw_material, reverse = True)
        for rm in raw_materials:
            self.addRawMaterial(self.raw_mat_model, rm.raw_material, rm.amount, rm.amount_left)
        self.raw_mat_data_view.resizeColumnToContents(0)
        for i in [1, 2]:
            self.raw_mat_data_view.header().setSectionResizeMode(i, QHeaderView.Stretch);

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
