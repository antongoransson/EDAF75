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
        self.modal_button.clicked.connect(self.modal_onclick)
        self.remove_button = QPushButton('Remove', self)
        self.remove_button.clicked.connect(self.remove_customer)

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

        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        dataLayout.addWidget(self.rm_dataView)
        self.dataGroupBox.setLayout(dataLayout)

        self.recipe_model = self.createRecipeModel(self)

        self.rm_model = self.createRawMaterialModel(self)
        self.dataView.setModel(self.recipe_model)
        self.rm_dataView.setModel(self.rm_model)
        self.update_recipe_view()

        self.layout.addWidget(self.dataGroupBox)
        self.layout.addWidget(self.horizontal_opGroupBox)

    @pyqtSlot()
    def modal_onclick(self):
        name, address, ok = Dialog.getInfo()
        if (ok):
            self.db.insert_customer(name, address)
            self.update_recipe_view()

    @pyqtSlot()
    def view_onclick(self):
        index = self.dataView.selectedIndexes()[0]
        recipe = index.model().itemFromIndex(index).text()
        self.update_raw_material_view(recipe)

    @pyqtSlot()
    def remove_customer(self):
        index = self.dataView.selectedIndexes()[0]
        item = index.model().itemFromIndex(index)
        self.db.delete_customer(item.text())
        self.update_recipe_view()

    def update_recipe_view(self):
        self.recipe_model.setRowCount(0)
        recipes = self.db.get_all_recipes()
        recipes.sort(reverse=True)
        for recipe in recipes:
            self.addRecipe(self.recipe_model, recipe)
        self.dataView.resizeColumnToContents(0)

    def update_raw_material_view(self, recipe):
        self.rm_model.setRowCount(0)
        raw_materials = self.db.get_recipe_items(recipe)
        raw_materials.sort(key=lambda tup: tup.raw_material, reverse= True)
        for rm in raw_materials:
            self.addRawMaterial(self.rm_model, rm.raw_material, rm.amount, rm.amount_left)
        self.rm_dataView.resizeColumnToContents(0)
        self.rm_dataView.header().setSectionResizeMode(1, QHeaderView.Stretch);
        self.rm_dataView.header().setSectionResizeMode(2, QHeaderView.Stretch);

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
