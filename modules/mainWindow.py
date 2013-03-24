import sys
import os
import functools
from Tkinter import Tk
from PyQt4 import QtCore, QtGui

from widgets import MainWidgetUI, StyleSheet, NO_NUM_STRING, NO_PATH_STRING

from logger import Logger


TITLE = "ALOK'S LOTTO GENERATOR"
LOTTO_TYPE = ['Lotto Max', 'Lotto 649']

class MainWidget(MainWidgetUI):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)

        self._outPutDir = ''

        self._initData()
        self._initUI()
        self._initWidgets()

    def _initData(self):
        self._lottoTypes = LOTTO_TYPE
        self._forcedNumbers = []
        self._outDir = ''

    def _initUI(self):
        self._setupUI()

    def _initWidgets(self):

        self._lottoTypeComboBox.addItems(self._lottoTypes)
        self._lottoTypeComboBox.setEditable(True)
        self._lottoTypeComboBox.lineEdit().setReadOnly(True)
        self._lottoTypeComboBox.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        for i in range(self._lottoTypeComboBox.count()):
            self._lottoTypeComboBox.setItemData(i, QtCore.Qt.AlignCenter,
                                                QtCore.Qt.TextAlignmentRole)

        self._nbTicketsSpinBox.setRange(1, 1000)
        self._nbTicketsSpinBox.setValue(1)

        self._updateForcedNumberLineEdit()

        self._connectSignals()

    def _updateForcedNumberLineEdit(self):
        if not self._forcedNumbers:
            self._forcedNumbersLineEdit.setText(NO_NUM_STRING)
            return

        self._forcedNumbers.sort()

        s = ', '.join([str(n).zfill(2) for n in self._forcedNumbers])
        self._forcedNumbersLineEdit.setText(s)


    def _connectSignals(self):
        self._generateBtn.clicked.connect(self._generateBtnOnClicked)
        self._clearTextBtn.clicked.connect(self._clearTextBtnOnClicked)
        self._selectOutPathBtn.clicked.connect(self._selectOutPathBtnOnClicked)
        self._clearOutPathBtn.clicked.connect(self._clearOutPathBtnOnClicked)
        self._copyBtn.clicked.connect(self._copyBtnOnClicked)
        self._noNumberCheckBox.clicked.connect(self._noNumberCheckBoxOnClicked)

        self._cancelBtn.clicked.connect(self._cancelBtnOnClicked)

        self._connectCheckBoxes()

    def _noNumberCheckBoxOnClicked(self):
        for _, checkBox in self._checkBoxMap.iteritems():
            checkBox.setCheckState(0)

        self._forcedNumbers = []
        self._updateForcedNumberLineEdit()

    def _connectCheckBoxes(self):
        for index, checkBox in self._checkBoxMap.iteritems():
            checkBox.clicked.connect(functools.partial(self._checkBoxClickedMappedSlot, checkBox, int(index)))

    def _checkBoxClickedMappedSlot(self, item, nbItem):
        if item.checkState()==2:
            self._forcedNumbers.append(nbItem)

        self._updateForcedNumberLineEdit()

        self._noNumberCheckBox.setCheckState(0)


    def _selectOutPathBtnOnClicked(self):
        fg = QtGui.QFileDialog()
        fg.setFileMode(QtGui.QFileDialog.Directory)
        fg.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        fg.setOption(QtGui.QFileDialog.ShowDirsOnly)
        f = str(fg.getExistingDirectory(self, 'Select Output Folder',
                                        os.path.dirname(os.path.abspath(__file__)),
                                        QtGui.QFileDialog.ShowDirsOnly))

        if not f:
            return

        self._outPutDirLineEdit.setText(f)
        self._outPutDirLineEdit.setCursorPosition(0)
        self._outPutDirLineEdit.setToolTip(f)

    def _clearOutPathBtnOnClicked(self):
        self._outPutDirLineEdit.setText(NO_PATH_STRING)
        self._outPutDirLineEdit.setCursorPosition(0)
        self._outPutDirLineEdit.setToolTip('')


    def _generateBtnOnClicked(self):
        s = ''
        s += str(self._lottoTypeComboBox.currentText())
        s += '\n\n'
        s += str(self._nbTicketsSpinBox.value())

        self._displayTextEdit.clear()

        self._displayTextEdit.setText(s)

    def _clearTextBtnOnClicked(self):
        self._displayTextEdit.clear()

    def _copyBtnOnClicked(self):
        text = str(self._displayTextEdit.toPlainText())

        if not text:
            return

        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append('%s' % text)
        r.destroy()

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

        self.setWindowTitle(TITLE)

        StyleSheet().setColor(self._mainWidget)
        StyleSheet().setColor(self, app= QtCore.QCoreApplication.instance())

        self.move(50, 50)

def run():
    app = QtGui.QApplication(sys.argv)
    am = MainWindow()
    am.show()
    am.raise_()
    app.exec_()

if __name__ == '__main__':
    run()
