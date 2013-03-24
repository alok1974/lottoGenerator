import sys
import os
import functools
from PyQt4 import QtCore, QtGui

APP_STYLE = ("WindowsVista" if sys.platform.startswith('win')  else "Plastique")
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))




TITLE = "LOTTO GENERATOR"
LOTTO_TYPE = ['Lotto Max', 'Lotto 649']

class StyleSheet(object):
    STYLESHEET_OPTIONS = ['dark', 'soft', 'maya', 'nuke',]

    def __init__(self, *args, **kwargs):
        super(StyleSheet, self).__init__(*args, **kwargs)
        self.prefFile = os.path.join(ROOT_DIR, 'prefs', 'currStyle')
        self.style = ''

    def _createPrefs(self):
        with open(self.prefFile, 'w') as f:
            f.write('theme:')

    def _readPrefs(self):
        if not os.path.exists(self.prefFile):
            self._createPrefs()

        with open(self.prefFile, 'r') as f:
            s = f.readlines()

        self.style= s[0].split(':')[1]

        return self.style

    def _writePrefs(self, pref=''):
        if not os.path.exists(self.prefFile):
            self._createPrefs()

        with open(self.prefFile, 'w') as f:
            f.write('theme:%s:' % pref)

    def setColor(self, widget, app=None, init=False):
        self._readPrefs()

        if not self.style:
            if app:
                pass
                app.setStyle(QtGui.QStyleFactory.create(APP_STYLE))

            widget.setStyleSheet("")

            return

        if self.style not in self.STYLESHEET_OPTIONS:
            raise Exception('"%s" type of stylesheet option does not exist !!' % self.style)

        p = os.path.join(ROOT_DIR, 'styleSheets', str(self.style))

        if not os.path.exists(p):
            raise Exception('Style Path - %s does not exist !!' % p)

        with open(p, 'r') as f:
            s = f.read()

        iconDir = str(os.path.abspath(os.path.join(ROOT_DIR, 'icons', 'styleSheet_icons')))

        if not os.path.exists(iconDir):
            raise Exception('icon path - %s not found' % iconDir)

        s = s.replace('FULLPATH', iconDir)

        if app:
            app.setStyle(QtGui.QStyleFactory.create("Plastique"))

        widget.setStyleSheet(s)

class MainWidgetUI(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWidgetUI, self).__init__(*args, **kwargs)


    def _setupUI(self):

        #-----------------------------------------------------------------------

        # Labels
        self._lottoTypeLabel = QtGui.QLabel('Select Lotto Type')
        self._nbTicketsLabel = QtGui.QLabel('Number of Tickets to Generate')
        self._displayLabel = QtGui.QLabel('Ouput')
        self._scrapTypeLabel = QtGui.QLabel('Generate Based on Results')

        #-----------------------------------------------------------------------

        # Edits and ComboBoxes
        self._lottoTypeComboBox = QtGui.QComboBox()
        self._lottoTypeComboBox.setMinimumSize(100, 100)
        self._lottoTypeComboBox.setStyleSheet("QComboBox {background-color : rgb(76, 78, 101); font-size: 30px;}")

        self._nbTicketsSpinBox = QtGui.QSpinBox()
        self._nbTicketsSpinBox.setMinimumSize(100, 100)
        self._nbTicketsSpinBox.setStyleSheet("QSpinBox {background-color : rgb(69, 98, 104); font-size: 30px;}")

        self._displayTextEdit = QtGui.QTextEdit()
        self._displayTextEdit.setReadOnly(True)
        self._displayTextEdit.setStyleSheet("QTextEdit {background-color : rgb(97, 91, 83); color : rgb(40, 40, 40); font-size: 16px;}")

        self._outPutDirLineEdit = QtGui.QLineEdit()
        self._outPutDirLineEdit.setReadOnly(True)
        self._outPutDirLineEdit.setText('        < out put path >')
        self._outPutDirLineEdit.setStyleSheet("QLineEdit {background-color : rgb(97, 91, 83); color : rgb(40, 40, 40); font-size: 16px;}")
        self._outPutDirLineEdit.setMinimumSize(50, 50)

        #-----------------------------------------------------------------------

        # Check Boxes
        self._sevenJumpsCheckBox = QtGui.QCheckBox("Do Seven Jumps")
        self._sevenJumpsCheckBox.setStyleSheet("QCheckBox {font-size: 16px;}")

        self._writeToFileCheckBox = QtGui.QCheckBox("Write Results to File")
        self._writeToFileCheckBox.setStyleSheet("QCheckBox {font-size: 16px;}")

        #-----------------------------------------------------------------------

        # Lines
        self._line01 = QtGui.QFrame()
        self._line01.setGeometry(QtCore.QRect(170, 90, 118, 8))
        self._line01.setFrameShape(QtGui.QFrame.HLine)
        self._line01.setFrameShadow(QtGui.QFrame.Sunken)
        self._line01.setStyleSheet("QFrame {background-color : rgb(97, 91, 83);}")

        self._line02 = QtGui.QFrame()
        self._line02.setGeometry(QtCore.QRect(170, 90, 118, 8))
        self._line02.setFrameShape(QtGui.QFrame.HLine)
        self._line02.setFrameShadow(QtGui.QFrame.Sunken)
        self._line02.setStyleSheet("QFrame {background-color : rgb(97, 91, 83);}")

        self._line03 = QtGui.QFrame()
        self._line03.setGeometry(QtCore.QRect(170, 90, 118, 8))
        self._line03.setFrameShape(QtGui.QFrame.HLine)
        self._line03.setFrameShadow(QtGui.QFrame.Sunken)
        self._line03.setStyleSheet("QFrame {background-color : rgb(97, 91, 83);}")

        self._line04 = QtGui.QFrame()
        self._line04.setGeometry(QtCore.QRect(170, 90, 118, 8))
        self._line04.setFrameShape(QtGui.QFrame.HLine)
        self._line04.setFrameShadow(QtGui.QFrame.Sunken)
        self._line04.setStyleSheet("QFrame {background-color : rgb(97, 91, 83);}")

        self._line05 = QtGui.QFrame()
        self._line05.setGeometry(QtCore.QRect(170, 90, 118, 8))
        self._line05.setFrameShape(QtGui.QFrame.HLine)
        self._line05.setFrameShadow(QtGui.QFrame.Sunken)
        self._line05.setStyleSheet("QFrame {background-color : rgb(97, 91, 83);}")

        self._line06 = QtGui.QFrame()
        self._line06.setGeometry(QtCore.QRect(170, 90, 118, 8))
        self._line06.setFrameShape(QtGui.QFrame.HLine)
        self._line06.setFrameShadow(QtGui.QFrame.Sunken)
        self._line06.setStyleSheet("QFrame {background-color : rgb(97, 91, 83);}")

        self._line07 = QtGui.QFrame()
        self._line07.setGeometry(QtCore.QRect(170, 90, 118, 8))
        self._line07.setFrameShape(QtGui.QFrame.HLine)
        self._line07.setFrameShadow(QtGui.QFrame.Sunken)
        self._line07.setStyleSheet("QFrame {background-color : rgb(97, 91, 83);}")

        self._line08 = QtGui.QFrame()
        self._line08.setGeometry(QtCore.QRect(170, 90, 118, 8))
        self._line08.setFrameShape(QtGui.QFrame.HLine)
        self._line08.setFrameShadow(QtGui.QFrame.Sunken)
        self._line08.setStyleSheet("QFrame {background-color : rgb(97, 91, 83);}")


        #-----------------------------------------------------------------------

        # Buttons
        self._generateBtn = QtGui.QPushButton('Generate')
        self._generateBtn.setStyleSheet("QPushButton {background-color : rgb(110, 122, 74);}")

        self._cancelBtn = QtGui.QPushButton('Cancel')
        self._cancelBtn.setStyleSheet("QPushButton {background-color : rgb(94, 57, 69);}")

        self._clearTextBtn = QtGui.QPushButton('Clear Text')
        self._clearTextBtn.setStyleSheet("QPushButton {background-color : rgb(57, 77, 94);}")

        self._copyBtn = QtGui.QPushButton('Copy')
        self._copyBtn.setStyleSheet("QPushButton {background-color : rgb(57, 90, 94);}")

        self._selectOutPathBtn = QtGui.QPushButton('Select Output Dir')
        self._selectOutPathBtn.setStyleSheet("QPushButton {background-color : rgb(89, 65, 62);}")
        #self._selectOutPathBtn.setMaximumHeight(20)


        #-----------------------------------------------------------------------

        # Radio Buttons
        self._sixMonthRadioBtn = QtGui.QRadioButton('Last Six Months')
        self._sixMonthRadioBtn.setStyleSheet("QRadioButton {/*background-color : rgb(69, 98, 104)*/; font-size: 16px;}")
        self._sixMonthRadioBtn.setChecked(True)

        self._allMonthRadioBtn = QtGui.QRadioButton('All Months')
        self._allMonthRadioBtn.setStyleSheet("QRadioButton {/*background-color : rgb(69, 98, 104)*/; font-size: 16px;}")

        self._bothRadioBtn = QtGui.QRadioButton('Both')
        self._bothRadioBtn.setStyleSheet("QRadioButton {/*background-color : rgb(69, 98, 104)*/; font-size: 16px;}")

#----------------------------------------------------------------------------------

        # Grid Layout
        self._grid = QtGui.QGridLayout()
        self._grid.setSpacing(30)
        self._grid.setRowMinimumHeight(0, 5)
        self._grid.setRowMinimumHeight(1, 20)

        #----------------------------------------------------------------------------------
        # Column 01
        self._grid.addWidget(self._lottoTypeLabel, 0, 0)
        self._grid.addWidget(self._line01, 1, 0)
        self._grid.addWidget(self._lottoTypeComboBox, 2, 0)
        self._grid.addWidget(self._line02, 3, 0)
        self._grid.addWidget(self._nbTicketsLabel, 4, 0)
        self._grid.addWidget(self._nbTicketsSpinBox, 5, 0)
        self._grid.addWidget(self._line03, 6, 0)
        self._grid.addWidget(self._generateBtn, 7, 0)
        self._grid.addWidget(self._cancelBtn, 8, 0)

        #----------------------------------------------------------------------------------

        # column 02
        self._grid.addWidget(self._scrapTypeLabel, 0, 1)
        self._grid.addWidget(self._line04, 1, 1)

        self._vRadioLayout = QtGui.QVBoxLayout()
        #self._vRadioLayout.addStretch(100)

        self._vRadioLayout.addWidget(self._sixMonthRadioBtn)
        self._vRadioLayout.addWidget(self._allMonthRadioBtn)
        self._vRadioLayout.addWidget(self._bothRadioBtn)

        self._grid.addLayout(self._vRadioLayout, 2, 1)
        self._grid.addWidget(self._line05, 3, 1)
        self._grid.addWidget(self._sevenJumpsCheckBox, 4, 1)
        self._grid.addWidget(self._writeToFileCheckBox, 5, 1)
        self._grid.addWidget(self._line06, 6, 1)
        self._grid.addWidget(self._selectOutPathBtn, 7, 1)
        self._grid.addWidget(self._outPutDirLineEdit, 8 ,1)


        #----------------------------------------------------------------------------------

        # Column 03
        self._hLayout = QtGui.QHBoxLayout()
        self._hLayout.addWidget(self._clearTextBtn)
        self._hLayout.addWidget(self._copyBtn)

        self._grid.addWidget(self._displayLabel, 0, 2)
        self._grid.addWidget(self._displayTextEdit, 1, 2, 5, 1)
        self._grid.addWidget(self._line07, 6, 2)
        self._grid.addLayout(self._hLayout, 7, 2)

        #-----------------------------------------------------------------------

        self._mainLayout = QtGui.QVBoxLayout(self)
        self._mainLayout.addLayout(self._grid)

        self.setWindowTitle(TITLE)

class MainWidget(MainWidgetUI):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)

        self._initData()
        self._initUI()
        self._initWidgets()

    def _initData(self):
        self._lottoTypes = LOTTO_TYPE

    def _initUI(self):
        self._setupUI()

    def _initWidgets(self):

        self._lottoTypeComboBox.addItems(self._lottoTypes)
        self._lottoTypeComboBox.setEditable(True)
        self._lottoTypeComboBox.lineEdit().setReadOnly(True)
        self._lottoTypeComboBox.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        for i in range(self._lottoTypeComboBox.count()):
            self._lottoTypeComboBox.setItemData(i, QtCore.Qt.AlignCenter, QtCore.Qt.TextAlignmentRole)

        self._nbTicketsSpinBox.setRange(1, 1000)
        self._nbTicketsSpinBox.setValue(1)

        self._connectSignals()

    def _connectSignals(self):
        self._generateBtn.clicked.connect(self._generateBtnOnClicked)
        self._clearTextBtn.clicked.connect(self._clearTextBtnOnClicked)
        self._cancelBtn.clicked.connect(self._cancelBtnOnClicked)

    def _generateBtnOnClicked(self):
        s = ''
        s += str(self._lottoTypeComboBox.currentText())
        s += '\n\n'
        s += str(self._nbTicketsSpinBox.value())

        self._displayTextEdit.clear()

        self._displayTextEdit.setText(s)

    def _clearTextBtnOnClicked(self):
        self._displayTextEdit.clear()

    def _cancelBtnOnClicked(self):
        QtCore.QCoreApplication.instance().quit()

class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        mainWidget = QtGui.QFrame()

        self._mainWidget = MainWidget()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self._mainWidget, 100)
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

        self.setWindowTitle('Lotto Generator')

        StyleSheet().setColor(self._mainWidget)
        StyleSheet().setColor(self, app= QtCore.QCoreApplication.instance())


def run():
    app = QtGui.QApplication(sys.argv)
    am = MainWindow()
    am.show()
    am.raise_()
    app.exec_()

if __name__ == '__main__':
    run()
