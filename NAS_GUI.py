from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
import sys 
import os
import subprocess

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        
        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()
       #self.createProgressBar()
        #self.exit_GUI()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 2, 1)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        mainLayout.addWidget(self.bottomRightGroupBox, 1, 0)
       #mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Welcome to NAS")
        self.changeStyle('Windows')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Files")

        radioButton1 = QRadioButton("File 1")
        radioButton2 = QRadioButton("File 2")
        radioButton3 = QRadioButton("File 3")
        radioButton1.setChecked(True)
        
        #check for ip entry
        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.Password)
        
        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        #check

        checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        #layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)
        
    #function for exiting
    def exit_GUI(self):
        print("GUI closed")
        sys.exit()
    #
    
    #function for calling another python script
    
    def call_client(self):
        subprocess.call("python3 1.py",shell=True)
        
   #function for creating top right box(submit and quit buttons)
    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Submission section")

        defaultPushButton = QPushButton("Submit")
        defaultPushButton.clicked.connect(self.call_client)
        #defaultPushButton.setDefault(True)

        togglePushButton = QPushButton("Quit")
        togglePushButton.clicked.connect(self.exit_GUI)
        #togglePushButton.setDefault(True)
        #togglePushButton.setCheckable(True)
        #togglePushButton.setChecked(True)

        flatPushButton = QPushButton("NAS")
        flatPushButton.setFlat(True)

        layout = QVBoxLayout()
        layout.addWidget(defaultPushButton)
        layout.addWidget(togglePushButton)
        layout.addWidget(flatPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

       # tab1 = QWidget()
       # tableWidget = QTableWidget(10, 10)

        #tab1hbox = QHBoxLayout()
        #tab1hbox.setContentsMargins(5, 5, 5, 5)
        #tab1hbox.addWidget(tableWidget)
        #tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        #textEdit = QTextEdit()
        textEdit = QLabel()

       #textEdit.setText("Welcome to the world of NAS")
        textEdit.setText("We aim to provide a peer-to-peer data sharing platform\n ,NAS, which promises transparent management of distributed\n, fragmented and replicated data on a local network\n as well as effective space utilization on different\n systems present on the network")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        #self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "About NAS")

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Enter Server IP address")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)

        lineEdit = QLineEdit('')
        lineEdit.setEchoMode(QLineEdit.Normal)

        #spinBox = QSpinBox(self.bottomRightGroupBox)
        #spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        #slider = QSlider(Qt.Horizontal, self.bottomRightGroupBox)
        #slider.setValue(40)

        #scrollBar = QScrollBar(Qt.Horizontal, self.bottomRightGroupBox)
        #scrollBar.setValue(60)

        #dial = QDial(self.bottomRightGroupBox)
        #dial.setValue(30)
        #dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        #layout.addWidget(spinBox, 1, 0, 1, 2)
        layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        #layout.addWidget(slider, 3, 0)
        #layout.addWidget(scrollBar, 4, 0)
        #layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

   # def createProgressBar(self):
   #     self.progressBar = QProgressBar()
   #     self.progressBar.setRange(0, 10000)
   #     self.progressBar.setValue(0)

    #    timer = QTimer(self)
   #     timer.timeout.connect(self.advanceProgressBar)
   #     timer.start(1000)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
