#!/usr/bin/python

import os
import sys
import random
import json
from PySide6 import QtGui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6 import QtCore, QtWidgets, QtGui

from exportbs import *

# https://www.pythoncentral.io/pyside-pyqt-tutorial-the-qlistwidget/
# https://www.youtube.com/watch?v=m_LXqG8VoDA
# https://www.youtube.com/watch?v=Sl-5-gnn8mk 
# https://www.youtube.com/channel/UCPme28sMOcWS50CgtTWUZIw
#  https://www.pythoncentral.io/pyside-pyqt-tutorial-qlistview-and-qstandarditemmodel/
#  https://github.com/tonytony2020/Qt-Python-Binding-Examples/blob/master/list_tree_and_table/listview_dnd/listview.py
# http://www2.hawaii.edu/~takebaya/cent110/gui/qtablewidget.html
# https://realpython.com/python-pyqt-database/
# https://www.daniweb.com/programming/software-development/threads/468891/displaying-images-in-qlistview-with-same-thumbnail-size-keeping-aspect-rat
# https://www.programcreek.com/python/example/108101/PyQt5.QtWidgets.QListView
# https://www.learnpyqt.com/tutorials/modelview-architecture/
# ui->tableView->setModel(model);
# ui->tableView->setColumnHidden(5, true);

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class CharacterListWidget(QWidget):
    _parent = ''
    _items = []
    def __init__(self):
        super().__init__()
        self.setUI()

    def setParent(self, parent):
        self._parent = parent

    def getItems(self):
        items = []
        for item in self._items:
            items.append(item['item'].serialize())
        return items

    def export(self):
        pass

    def setUI(self):
        vbox = QVBoxLayout()

        label = QLabel("Characters")
        vbox.addWidget(label)
        
        self.table = QTableWidget(1,5)
        self.columnLabels = ["Character","Role","Age","Gender","hash"]
        self.table.setHorizontalHeaderLabels(self.columnLabels)
        vbox.addWidget(self.table)


        with open('save/sample.char') as f:
            read_data = f.read()
            data = json.loads(read_data)
            print(data)
            f.close()

        self.model = TableModel(data)
#        self.table.setModel(self.model)

        self.table.setColumnHidden(4, True)

        self.setLayout(vbox)

    def load(self):
        filename, filter = QFileDialog.getOpenFileName(self, 'Open file', '~/')
        with open(filename, 'r') as json_data:
            json_data = json.load(json_data)
            print(json_data)
            print('*'*80)
            self._parent.loadData(json_data)

class AppMainWindow(QMainWindow):
    
    def __init__(self):
        super(AppMainWindow, self).__init__()
        
        self.initUI()
       
    def initGrid(self):
 
        self.tabs = QTabWidget()

        textEdit = QTextEdit()
        self._grid = CharacterListWidget()
        self._grid.setParent(self)
        self.setCentralWidget(self.tabs)
        
        self._tab01 = QWidget()
        self._tab02 = QWidget()
        self._tab03 = QWidget()
        self._tab04 = QWidget()

        self.tabs.addTab(self._grid,"List Characters")
        self.tabs.addTab(self._tab02,"Character  - main")
        self.tabs.addTab(self._tab03,"Character - extra")
        self.tabs.addTab(self._tab04,"Reference")

    def initUI(self):               
        exitIcon = "resources/icons/exit22.png"
        newIcon = "resources/icons/document2.png"
        saveIcon = "resources/icons/document-save.png"
        openIcon = "resources/icons/document-open.png"
        exportIcon = "resources/icons/document-print.png"
        exportHtmlIcon = "resources/icons/goto.png"
        appIcon = "resources/icons/krita.png"

        self.initGrid()

        exitAction = QtGui.QAction(QIcon(exitIcon),'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        newAction = QtGui.QAction(QIcon(newIcon),'New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New Beat Sheet')
        newAction.triggered.connect(self.new)

        saveAction = QtGui.QAction(QIcon(saveIcon),'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save Beat Sheet')
        saveAction.triggered.connect(self.save)

        openAction = QtGui.QAction(QIcon(openIcon),'Open', self)
        openAction.setShortcut('Ctrl+S')
        openAction.setStatusTip('Open Beat Sheet')
        openAction.triggered.connect(self.open)

        exportAction = QtGui.QAction(QIcon(exportIcon),'Export', self)
        exportAction.setShortcut('Ctrl+E')
        exportAction.setStatusTip('Export Beat Sheet')
        exportAction.triggered.connect(self.export)

        exportHtmlAction = QtGui.QAction(QIcon(exportHtmlIcon),'Export HTML', self)
        exportHtmlAction.setShortcut('Ctrl+H')
        exportHtmlAction.setStatusTip('Export Beat Sheet (HTML)')
        exportHtmlAction.triggered.connect(self.exportHtml)

        exportOdtAction = QtGui.QAction(QIcon(exportHtmlIcon),'Export ODT', self)
        exportOdtAction.setShortcut('Ctrl+T')
        exportOdtAction.setStatusTip('Export Beat Sheet (ODT)')
        exportOdtAction.triggered.connect(self.exportOdt)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('BeatSheet')
        toolbar.addAction(exitAction)
        
        fileMenu = menubar.addMenu('&Export')
        fileMenu.addAction(exportAction)
        fileMenu.addAction(exportHtmlAction)
        fileMenu.addAction(exportOdtAction)

        toolbar.addAction(newAction)
        toolbar.addAction(saveAction)
        toolbar.addAction(openAction)
        toolbar.addAction(exportAction)
        toolbar.addAction(exportHtmlAction)
        toolbar.addAction(exportOdtAction)
        
        self.setWindowTitle('Save the Cat Beat Sheet') 

        MainAppIcon = QIcon(appIcon)
        self.setWindowIcon(MainAppIcon)
        self.setGeometry(0,0, 1920,1080)

        self.showMaximized()

        self.show()

    def _getData(self):
        items = self._grid.getItems()
        movie_name = self._movie.getName()
        movie_theme = self._movie.getTheme()
        movie_genre = self._movie.getGenre()
        movie_logline = self._grid.getLogLine()
        author_name = self._author.getName()
        author_email = self._author.getEmail()
        author_institute = self._author.getInstitute()
        
        plot_text = self._plot.getPlot()
        escaleta_text = self._escaleta.getEscaleta()
        argumento_text = self._argumento.getArgumento()
        synopsis_text = self._synopsis.getSynopsis()

        movie = {
                'movie': {'name': movie_name, 'genre': movie_genre, 'theme': movie_theme,'logline': movie_logline},
                'beat-sheet': items,
                'synopsis': synopsis_text,
                'plot': plot_text,
                'argumento': argumento_text,
                'escaleta': escaleta_text,
                'author': {'name':author_name, 'email': author_email, 'institute':author_institute }
                }
        return movie

    def setName(self, name):
        self._movie.setName(name)

    def setGenre(self, name):
        self._movie.setGenre(name)

    def setTheme(self, name):
        self._movie.setTheme(name)

    def loadData(self, data):
            print(data)
            self.setName(data['movie']['name'])
            self.setGenre(data['movie']['genre'])
            self.setTheme(data['movie']['theme'])
            self._grid.setLogLine(data['movie']['logline'])
            self._author.setName(data['author']['name'])
            self._author.setEmail(data['author']['email'])
            self._author.setInstitute(data['author']['institute'])
            self._synopsis.setSynopsis(data['synopsis'])
            self._plot.setPlot(data['plot'])
            self._argumento.setArgumento(data['argumento'])
            self._escaleta.setEscaleta(data['escaleta'])

    def load(self):
        pass

    def save(self):
        movie = self._getData()

        filename, filter = QFileDialog.getSaveFileName(parent=self, caption='Select Save the Cat file', dir='.', filter='Save the Cat Beat Sheet (*.cat)')

        if filename:
            filename, file_extension = os.path.splitext(filename)
            if file_extension != 'cat':
                filename = filename + '.cat'
            print(filename)
            with open(filename, "w") as write_file:
                json.dump(movie, write_file, sort_keys=True, indent=4)
    
    def open(self):
        #self._grid.open()
        print("Open")
        self._grid.load()
        self._load()

    def new(self):
        print("New")

    def export(self):
        data = self._getData()
        tex = BeatSheetExporterLatex()
        tex.setData(data)
        tex.setParent(self)
        tex.export()

    def exportHtml(self):
        data = self._getData()
        tex = BeatSheetExporterHtml()
        tex.setData(data)
        tex.setParent(self)
        tex.export()

    def exportOdt(self):
        data = self._getData()
        tex = BeatSheetExporterOdt()
        tex.setData(data)
        tex.setParent(self)
        tex.export()

    def _load(self):
        pass

def main():
    app = QApplication([])
    ex = AppMainWindow()
    File = QtCore.QFile("resources/stye.qss")
    File.open(QtCore.QFile.ReadOnly)
    qss = QtCore.QTextStream(File)
	#setup stylesheet
    app.setStyleSheet(qss.readAll())

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
