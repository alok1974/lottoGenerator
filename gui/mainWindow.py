import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.join(__file__)), '..')))

import functools
from Tkinter import Tk
from PyQt4 import QtCore, QtGui


from widgets import MainWidgetUI, NO_NUM_STRING, NO_PATH_STRING
from styleSheet import StyleSheet
from msgHandler import _pop
from logger import Logger
from alg.generate import generateTickets


TITLE = "ALOK'S LOTTO GENERATOR"
LOTTO_TYPE = ['Lotto 649', 'Lotto MAX']
MAX_NUMBERS = (6, 7)

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
        self._isLottoMax = False
        self._nbTickets = 1
        self._doSevenJumps = False
        self._scrapType = 0

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
        self._lottoTypeComboBox.currentIndexChanged.connect(self._lottoTypeComboBoxOnClicked)
        self._nbTicketsSpinBox.valueChanged.connect(self._nbTicketsSpinBoxValueChanged)

        self._connectRadioBtn()
        self._sevenJumpsCheckBox.clicked.connect(self._sevenJumpsCheckBoxOnClicked)
        self._selectOutPathBtn.clicked.connect(self._selectOutPathBtnOnClicked)
        self._clearOutPathBtn.clicked.connect(self._clearOutPathBtnOnClicked)

        self._noNumberCheckBox.clicked.connect(self._noNumberCheckBoxOnClicked)
        self._connectCheckBox()

        self._clearTextBtn.clicked.connect(self._clearTextBtnOnClicked)
        self._copyBtn.clicked.connect(self._copyBtnOnClicked)

        self._generateBtn.clicked.connect(self._generateBtnOnClicked)
        self._resetBtn.clicked.connect(self._resetBtnOnClicked)
        self._cancelBtn.clicked.connect(self._cancelBtnOnClicked)

    def _lottoTypeComboBoxOnClicked(self, item):
        if item==0 and len(self._forcedNumbers)==7:
            _pop(self, 1)
            self._lottoTypeComboBox.blockSignals(True) # blocking signals so the func does not go in recursion
            self._lottoTypeComboBox.setCurrentIndex(1)
            self._lottoTypeComboBox.blockSignals(False)

        self._isLottoMax = bool(item)

    def _nbTicketsSpinBoxValueChanged(self, value):
        self._nbTickets = value

    def _connectRadioBtn(self):
        for index, radioBtn in self._radioBtnMap.iteritems():
            radioBtn.clicked.connect(functools.partial(self._radioBtnClickedMappedSlot, index))

    def _radioBtnClickedMappedSlot(self, index):
        self._scrapType = index

    def _sevenJumpsCheckBoxOnClicked(self, checkState):
        self._doSevenJumps = checkState

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
        self._outDir = str(f)

    def _clearOutPathBtnOnClicked(self):
        self._outPutDirLineEdit.setText(NO_PATH_STRING)
        self._outPutDirLineEdit.setCursorPosition(0)
        self._outPutDirLineEdit.setToolTip('')
        self._outDir = ''

    def _noNumberCheckBoxOnClicked(self):
        for _, checkBox in self._checkBoxMap.iteritems():
            checkBox.setCheckState(0)

        self._forcedNumbers = []
        self._updateForcedNumberLineEdit()

    def _connectCheckBox(self):
        for index, checkBox in self._checkBoxMap.iteritems():
            checkBox.clicked.connect(functools.partial(self._checkBoxClickedMappedSlot, checkBox, int(index)))

    def _checkBoxClickedMappedSlot(self, item, nbItem):
        if item.checkState()==2:
            self._forcedNumbers.append(nbItem)
        elif item.checkState()==0:
            self._forcedNumbers.remove(nbItem)

        nbForcedNumbers = len(self._forcedNumbers)
        maxAllowed = MAX_NUMBERS[int(self._isLottoMax)]
        lottoType = LOTTO_TYPE[int(self._isLottoMax)]

        if nbForcedNumbers > maxAllowed:
            _pop(self, 2, extraArgs=[maxAllowed, lottoType])
            item.blockSignals(True) # blocking signals so the func does not go in recursion
            item.setCheckState(0)
            self._forcedNumbers.remove(nbItem)
            item.blockSignals(False)
            return

        self._updateForcedNumberLineEdit()
        self._noNumberCheckBox.setCheckState(0)

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

    def _generateBtnOnClicked(self):
        s = self._displayTextEdit.toPlainText()
        s += '*' * 30
        s += '\n'
        s += 'Is Lotto Max: %s\n' % self._isLottoMax
        s += 'Nb Tickets: %s\n' % self._nbTickets
        s += 'Scrap Type: %s\n' % self._scrapType
        s += 'Do Seven Jumps: %s\n' % self._doSevenJumps
        s += 'Output Dir: "%s "\n' % self._outDir
        s += 'Forced Numbers: [%s]\n' % ', '.join([str(n).zfill(2) for n in self._forcedNumbers])
        s += '*' * 30
        s += '\n\n\n'

        #self._displayTextEdit.clear()

        self._displayTextEdit.setText(s)

    def _resetBtnOnClicked(self):
        self._noNumberCheckBox.setCheckState(2)
        self._noNumberCheckBoxOnClicked()
        self._lottoTypeComboBox.setCurrentIndex(0)
        self._nbTicketsSpinBox.setValue(1)
        for index, radioBtn in self._radioBtnMap.iteritems():
            if index==0:
                radioBtn.setChecked(True)
            else:
                radioBtn.setChecked(False)
        self._sevenJumpsCheckBox.setCheckState(0)
        self._outDir = ''
        self._outPutDirLineEdit.setText(NO_PATH_STRING)

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
