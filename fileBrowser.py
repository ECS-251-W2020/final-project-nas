from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import os

from ui import main

#
# Class that allows the addition of column we use to provide
# if the file is sharded or not
#
class ExtraColumnModel(QtWidgets.QFileSystemModel):

    # Adds a column to the display
    def columnCount(self, parent = QtCore.QModelIndex()):
        return super(ExtraColumnModel, self).columnCount()+1

    # Sets the name of the column
    def headerData(self, section, o, role):
        if o == QtCore.Qt.Horizontal and section == self.columnCount() - 1:
            return "Sharded"
        return super(ExtraColumnModel, self).headerData(section, o, role)

    # Stores the data to be added to the column
    def data(self, index, role):

        # Filename of the column we need 
        filename = super(ExtraColumnModel, self).data(index, QtWidgets.QFileSystemModel.Roles.FileNameRole)

        # if its the last column
        if index.column() == self.columnCount() - 1:

            # if filename has digit in it at the end
            if role == QtCore.Qt.DisplayRole and filename[-1].isdigit():
                return "True"
            elif role == QtCore.Qt.DisplayRole:
                return "False"

        # if the first column
        elif index.column() == 0:
            if role == QtCore.Qt.DisplayRole and filename[-1].isdigit():
                return filename[:-1]

        return super(ExtraColumnModel, self).data(index, role)

#
# Main class that gets all the files and creates context menus for them
# if the file is sharded or not
#
class MyFileBrowser(main.Ui_MainWindow, QtWidgets.QMainWindow):

    # Initialize the class with our custom context menu
    def __init__(self, maya=False):
        super(MyFileBrowser, self).__init__()
        self.setupUi(self)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.populate()

    # Populate using 
    def populate(self):
        path = "/Users/aakaashkapoor/Desktop/final-project-nas/directory"
        self.model = ExtraColumnModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        print(self.model)
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)

    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction("Open file")
        open.triggered.connect(self.open_file)
        open = menu.addAction("Push Changes")
        open.triggered.connect(self.open_file)
        filename = self.model.fileName(self.treeView.currentIndex())
        filename = "hi.txt"

        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_file(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        print("Tried to open file:", file_path)
        # os.startfile(file_path)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    fb = MyFileBrowser()
    fb.show()
    app.exec_()