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

class CharacterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._setupUI()
        self._data = []

    def _setupUI(self):
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
#        hbox.addLayout(vbox)
        
        label = QLabel("Character")
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName('CharacterList')
        vbox.addWidget(label)

        fbox = QFormLayout()

        self.name = QLineEdit()
        self.age = QLineEdit()

        self.gender = QComboBox(self)
        self.gender.addItem("Male")
        self.gender.addItem("Female")
        self.gender.addItem("Gay")
        self.gender.addItem("Lesbian")
        self.gender.addItem("Trans Man")
        self.gender.addItem("Trans Woman")
        self.gender.addItem("Intersex")

        self.function = QComboBox(self)
        self.function.addItem("Primary")
        self.function.addItem("Secondary")
        self.function.addItem("Extra")
        
        self.physicalDescription = QTextEdit()
        self.mbty = QTextEdit()
        
        self.fear = QLineEdit()
        self.motivation = QLineEdit()
        self.kryptonite = QLineEdit()
        self.misbelief = QLineEdit()
        self.lesson = QLineEdit()
        self.bestThing = QLineEdit()
        self.worstThing = QLineEdit()
        self.lookDown = QLineEdit()
        self.feelAlive = QLineEdit()
        self.feelLoved = QLineEdit()
        self.valueMost = QLineEdit()
        self.favorites = QLineEdit()
        self.objectPartWith = QLineEdit()
        self.typicalOutfit = QLineEdit()
        self.nicknames = QLineEdit()
        self.methodManipulation = QLineEdit()
        self.dailyRoutine = QLineEdit()
        self.gotoCure = QLineEdit()
        self.dissatisfaction = QLineEdit()
        self.beliefHappyness = QLineEdit()
        self.turnDreamReality = QLineEdit()
        self.feelAccomplishDream = QLineEdit()
#        self.backstoryChangedEverything = QLineEdit()
        self.beliefChange = QLineEdit()
        self.struggleHoldBelief = QLineEdit()
        self.newBelief = QLineEdit()

        fbox.addRow(QLabel("Name"), self.name)
        fbox.addRow(QLabel("Age"), self.age)
        fbox.addRow(QLabel("Gender"), self.gender)
        fbox.addRow(QLabel("Function"), self.function)
        fbox.addRow("Physical Description", self.physicalDescription)
        fbox.addRow("MBTY / Enneagram Personality Type", self.mbty)
#        vbox.addWidget(fbox)
#        vbox.addWidget(QLabel("Label"))
        
        fbox1 = QFormLayout()
#        fbox1.addRow("Physical Description", self.physicalDescription)
#        fbox1.addRow("MBTY / Enneagram Personality Type", self.mbty)

        grp01 = QGroupBox('Character | main aspects')
        grp01.setLayout(fbox)
        vbox.addWidget(grp01)
        
        grp02 = QGroupBox('Internal')
        fbox1.addRow("Greatest Fear", self.fear)
        fbox1.addRow("Motivation", self.motivation)
        fbox1.addRow("Kryptonite", self.kryptonite)
        fbox1.addRow("Misbelief about the world", self.misbelief)
        fbox1.addRow("Lesson needed to learn", self.lesson)
        fbox1.addRow("Best thing in life", self.bestThing)
        fbox1.addRow("Worst thing in life", self.worstThing)
        fbox1.addRow("What thing she looks down for", self.lookDown)
        fbox1.addRow("What makes them feel alive", self.feelAlive)
        fbox1.addRow("What makes them feel loved", self.feelLoved)
        fbox1.addRow("What are the three things value the most", self.valueMost)
        grp02.setLayout(fbox1)
        grp02.setLayout(fbox1)
        
        fbox2 = QFormLayout()
        grp03 = QGroupBox('External')
        fbox2.addRow("Favorite book, movie, and band", self.favorites)
        fbox2.addRow("Object can't bear part with? why?", self.objectPartWith)
        fbox2.addRow("Typical Outfit", self.typicalOutfit)
        fbox2.addRow("Nicknames", self.nicknames)
        fbox2.addRow("Method of manipulation", self.methodManipulation)
        fbox2.addRow("Daily Routine", self.dailyRoutine)
        fbox2.addRow("Go to cure for a bad day", self.gotoCure)
        grp03.setLayout(fbox2)
        
        fbox3 = QFormLayout()
        grp04 = QGroupBox('Goals')
        
        fbox3.addRow("Dissatisfaction", self.dissatisfaction)
        fbox3.addRow("Belief that brings happyness", self.beliefHappyness)
        fbox3.addRow("Turn dream reality", self.turnDreamReality)
        fbox3.addRow("Feel accomplish dream", self.feelAccomplishDream)
#        fbox3.addRow("Backstory changed everything", self.backstoryChangedEverything)
        

        grp04.setLayout(fbox3)

        fbox4 = QFormLayout()
        grp05 = QGroupBox('Backstory scene that changed everything')
        fbox4.addRow("What they go believing and how they change", self.beliefChange) 
        fbox4.addRow("How they struggle to hold to old belief", self.struggleHoldBelief) 
        fbox4.addRow("New belief", self.newBelief) 

        grp05.setLayout(fbox4)

        vbox.addWidget(grp02)
        vbox.addWidget(grp03)
        vbox.addWidget(grp04)
        vbox.addWidget(grp05)

        vbox.addStretch()
#        self.setLayout(vbox)
        self.setLayout(vbox)



class CharacterListWidget(QWidget):
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()
        label = QLabel("Characters")
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName('CharacterList')
        vbox.addWidget(label)

        # CREATE THE TABLE
        self.table = QTableView(self)  # SELECTING THE VIEW
        self.table.setGeometry(0, 0, 1200, 900)
        self.model = QStandardItemModel(self)  # SELECTING THE MODEL - FRAMEWORK THAT HANDLES QUERIES AND EDITS
        self.table.setModel(self.model)  # SETTING THE MODEL
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.load()
        self.populate()

        self.table.doubleClicked.connect(self.on_click)

        vbox.addWidget(self.table)
        vbox.addStretch()
        self.setLayout(vbox)


    def on_click(self, signal):
        row = signal.row()  # RETRIEVES ROW OF CELL THAT WAS DOUBLE CLICKED
        column = signal.column()  # RETRIEVES COLUMN OF CELL THAT WAS DOUBLE CLICKED
        cell_dict = self.model.itemData(signal)  # RETURNS DICT VALUE OF SIGNAL
        cell_value = cell_dict.get(0)  # RETRIEVE VALUE FROM DICT

        index = signal.sibling(row, 0)
        index_dict = self.model.itemData(index)
        index_value = index_dict.get(0)
        print(
            'Row {}, Column {} clicked - value: {}\nColumn 1 contents: {}'.format(row, column, cell_value, index_value))

    def load(self):
#        filename, filter = QFileDialog.getOpenFileName(self, 'Open file', '~/')
        filename = "save/sample.char"
        with open(filename, 'r') as json_data:
            json_data = json.load(json_data)
            print(json_data)
            print('*'*80)
            self._data = json_data


    def populate(self):
        # GENERATE A 4x10 GRID OF RANDOM NUMBERS.
        # VALUES WILL CONTAIN A LIST OF INT.
        # MODEL ONLY ACCEPTS STRINGS - MUST CONVERT
        values = []
            
        header= ['name','age','gender','function','hash']
        self.model.setHorizontalHeaderLabels(header)

        for item in self._data:
            print(item)
            line = [item['name'],item['age'],item['gender'],item['function'],item['hash']]

            row = []
            for val in line:
                cell = QStandardItem(str(val))
                row.append(cell)
            self.model.appendRow(row)

        self.show()

    def addDock(self):
      self.dockItems = QDockWidget("Dockable", self)
      self.listWidget = QListWidget()
      self.listWidget.addItem("item1")
      self.listWidget.addItem("item2")
      self.listWidget.addItem("item3")
		
      self.dockItems.setWidget(self.listWidget)
      self.dockItems.setFloating(False)
      self.addDockWidget(Qt.RightDockWidgetArea, self.dockItems)

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
        self._character = CharacterWidget()
        self._tab03 = QWidget()
        self._tab04 = QWidget()

        self.tabs.addTab(self._grid,"List Characters")
        self.tabs.addTab(self._character,"Character  - main")
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
        
        self.setWindowTitle('Character Sheets') 

        MainAppIcon = QIcon(appIcon)
        self.setWindowIcon(MainAppIcon)
        self.setGeometry(0,0, 1920,1080)

        self.showMaximized()

        self.show()

    def _getData(self):
        items = self._grid.getItems()
        movie_name = self._movie.getName()

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

    def loadData(self, data):
            print(data)
            self.setName(data['movie']['name'])

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
