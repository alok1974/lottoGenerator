###########################################################################################
###########################################################################################
##                                                                                       ##
##  Alok's Lotto Generator V 1.0 (c) 2013 Alok Gandhi (alok.gandhi2002@gmail.com)        ##
##                                                                                       ##
##                                                                                       ##
##  This file is part of Alok's Lotto Generator.                                         ##
##                                                                                       ##
##  This software is free software: you can redistribute it and/or modify                ##
##  it under the terms of the GNU General Public License, Version 3, 29 June 2007        ##
##  as published by the Free Software Foundation,                                        ##
##                                                                                       ##
##  This software is distributed in the hope that it will be useful,                     ##
##  but WITHOUT ANY WARRANTY; without even the implied warranty of                       ##
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                        ##
##  GNU General Public License for more details.                                         ##
##                                                                                       ##
##  You should have received a copy of the GNU General Public License                    ##
##  along with this software.  If not, see <http://www.gnu.org/licenses/>.               ##
##                                                                                       ##
###########################################################################################
###########################################################################################

import os
import sys
import json
import time
import urllib2
import functools
from Tkinter import Tk
from PyQt4 import QtCore, QtGui

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.join(__file__)), '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from gui import *
from widgets import *


from styleSheet import StyleSheet
import msgHandler
from logger import Logger
from algorithm.mainAlgorithm import MainAlgorithm

TITLE = "Alok's Lotto Generator"
LOTTO_TYPE = ['Lotto 649', 'Lotto MAX']
MAX_NUMBERS = (6, 7)
OUT_FOLDER = 'output'

# Separate worker thread for Running Algorithm
class RunAlgTask(QtCore.QThread):
    def __init__(self, parent=None, *args, **kwargs):
        QtCore.QThread.__init__(self, parent)
        self.result = ''
        self.lottoIsMax          =  kwargs['lottoIsMax']
        self.writeDirPath        =  kwargs['writeDirPath']
        self.write               =  kwargs['write']
        self.scrapType           =  kwargs['scrapType']
        self.logAnatomy          =  kwargs['logAnatomy']
        self.nbTickets           =  kwargs['nbTickets']
        self.doSevenJumps        =  kwargs['doSevenJumps']
        self.forcedNumbers       =  kwargs['forcedNumbers']
        self.nbFromForcedRandom  =  kwargs['nbFromForcedRandom']
        self.applyDrawSum        =  kwargs['applyDrawSum']
        self.applyDigitSum       =  kwargs['applyDigitSum']
        self.applyEvens          =  kwargs['applyEvens']
        self.applyLows           =  kwargs['applyLows']
        self.drawSumMin          =  kwargs['drawSumMin']
        self.drawSumMax          =  kwargs['drawSumMax']
        self.digitSumMin         =  kwargs['digitSumMin']
        self.digitSumMax         =  kwargs['digitSumMax']
        self.nbEvens             =  kwargs['nbEvens']
        self.nbLows              =  kwargs['nbLows']

    # Call this to launch the thread
    def runRat(self):
        self.start()

    # This run method is called by Qt as a result of calling start()
    def run(self):
        ma = MainAlgorithm(
                            qThread             = self                     ,
                            lottoIsMax          = self.lottoIsMax          ,
                            writeDirPath        = self.writeDirPath        ,
                            write               = self.write               ,
                            scrapType           = self.scrapType           ,
                            logAnatomy          = self.logAnatomy          ,
                            nbTickets           = self.nbTickets           ,
                            doSevenJumps        = self.doSevenJumps        ,
                            forcedNumbers       = self.forcedNumbers       ,
                            nbFromForcedRandom  = self.nbFromForcedRandom  ,
                            applyDrawSum        = self.applyDrawSum        ,
                            applyDigitSum       = self.applyDigitSum       ,
                            applyEvens          = self.applyEvens          ,
                            applyLows           = self.applyLows           ,
                            drawSumMin          = self.drawSumMin          ,
                            drawSumMax          = self.drawSumMax          ,
                            digitSumMin         = self.digitSumMin         ,
                            digitSumMax         = self.digitSumMax         ,
                            nbEvens             = self.nbEvens             ,
                            nbLows              = self.nbLows              ,
                        )

        self.result = ma.runAlg()

class MainWidget(MainWidgetUI):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)

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
        self._nbFromForced = 0
        self._logAnatomy = True
        self._logSettings = False
        self._iter = 0
        self._start = 0
        self._end = 0

        self._settings = {
                            'drsmMin': DEF_SETTING['drsmMin'][int(self._isLottoMax)],
                            'drsmMax': DEF_SETTING['drsmMax'][int(self._isLottoMax)],
                            'dgsmMin': DEF_SETTING['dgsmMin'][int(self._isLottoMax)],
                            'dgsmMax': DEF_SETTING['dgsmMax'][int(self._isLottoMax)],
                            'nbEvens': DEF_SETTING['nbEvens'][int(self._isLottoMax)],
                            'nbLows': DEF_SETTING['nbLows'][int(self._isLottoMax)],
                         }

        self._rules = {'drsmRule': DEF_RULES['drsmRule'], 'dgsmRule' : DEF_RULES['dgsmRule'],
                       'evensRule': DEF_RULES['evensRule'], 'lowsRule': DEF_RULES['lowsRule']}

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

        self._nbFromForcedSpinBox.setRange(0, len(self._forcedNumbers))
        self._nbFromForcedSpinBox.setValue(len(self._forcedNumbers))

        self._radioBtnMap[0].setChecked(True)
        self._noNumberCheckBox.setChecked(True)
        self._logAnatomyCheckBox.setChecked(True)

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
        self._lottoTypeComboBox.currentIndexChanged.connect(self._lottoTypeComboBoxIndexChanged)
        self._nbTicketsSpinBox.valueChanged.connect(self._nbTicketsSpinBoxValueChanged)
        self._selectOutPathBtn.clicked.connect(self._selectOutPathBtnOnClicked)
        self._clearOutPathBtn.clicked.connect(self._clearOutPathBtnOnClicked)

        self._connectRadioBtn()
        self._sevenJumpsCheckBox.clicked.connect(self._sevenJumpsCheckBoxOnClicked)
        self._logAnatomyCheckBox.clicked.connect(self._logAnatomyCheckBoxOnClicked)
        self._logSettingsCheckBox.clicked.connect(self._logSettingsCheckBoxOnClicked)
        self._settingsBtn.clicked.connect(self._settingsBtnOnClicked)
        self._rulesBtn.clicked.connect(self._rulesBtnOnClicked)

        self._noNumberCheckBox.clicked.connect(self._noNumberCheckBoxOnClicked)
        self._connectCheckBox()
        self._nbFromForcedSpinBox.valueChanged.connect(self._nbFromForcedSpinBoxValueChanged)

        self._clearTextBtn.clicked.connect(self._clearTextBtnOnClicked)
        self._copyBtn.clicked.connect(self._copyBtnOnClicked)

        self._generateBtn.clicked.connect(self._generateBtnOnClicked)
        self._resetBtn.clicked.connect(self._resetBtnOnClicked)
        self._cancelBtn.clicked.connect(self._cancelBtnOnClicked)

    def _lottoTypeComboBoxIndexChanged(self, item):
        if item==0 and len(self._forcedNumbers)==7:
            msgHandler._pop(self, 1)
            self._lottoTypeComboBox.blockSignals(True) # blocking signals so the func does not go in recursion
            self._lottoTypeComboBox.setCurrentIndex(1)
            self._isLottoMax = bool(1)
            self._lottoTypeComboBox.blockSignals(False)

            return

        self._isLottoMax = bool(item)

        self._settings = {
                            'drsmMin': DEF_SETTING['drsmMin'][int(self._isLottoMax)],
                            'drsmMax': DEF_SETTING['drsmMax'][int(self._isLottoMax)],
                            'dgsmMin': DEF_SETTING['dgsmMin'][int(self._isLottoMax)],
                            'dgsmMax': DEF_SETTING['dgsmMax'][int(self._isLottoMax)],
                            'nbEvens': DEF_SETTING['nbEvens'][int(self._isLottoMax)],
                            'nbLows': DEF_SETTING['nbLows'][int(self._isLottoMax)],
                         }

    def _nbTicketsSpinBoxValueChanged(self, value):
        self._nbTickets = value

    def _selectOutPathBtnOnClicked(self):
        fg = QtGui.QFileDialog()
        fg.setFileMode(QtGui.QFileDialog.Directory)
        fg.setOptions(QtGui.QFileDialog.ShowDirsOnly)
        fg.setOption(QtGui.QFileDialog.ShowDirsOnly)
        f = str(fg.getExistingDirectory(self, 'Select Output Folder',
                                        os.path.abspath(os.path.join(ROOT_DIR, 'output')),
                                        QtGui.QFileDialog.ShowDirsOnly))

        if not f:
            return

        # Adding folder for result output
        f = os.path.abspath(os.path.join(f, OUT_FOLDER))

        self._outDir = str(f)
        self._outPutDirLineEdit.setText(f)
        self._outPutDirLineEdit.setCursorPosition(0)
        self._outPutDirLineEdit.setToolTip(f)

    def _clearOutPathBtnOnClicked(self):
        self._outPutDirLineEdit.setText(NO_PATH_STRING)
        self._outPutDirLineEdit.setCursorPosition(0)
        self._outPutDirLineEdit.setToolTip('')
        self._outDir = ''

    def _connectRadioBtn(self):
        for index, radioBtn in self._radioBtnMap.iteritems():
            radioBtn.clicked.connect(functools.partial(self._radioBtnClickedMappedSlot, index))

    def _radioBtnClickedMappedSlot(self, index):
        self._scrapType = index

    def _sevenJumpsCheckBoxOnClicked(self, checkState):
        self._doSevenJumps = checkState

    def _logAnatomyCheckBoxOnClicked(self, checkState):
        self._logAnatomy = checkState

    def _logSettingsCheckBoxOnClicked(self, checkState):
        self._logSettings = checkState

    def _settingsBtnOnClicked(self):
        if not hasattr(self, 'sw'):
            self.sw = SettingsWidget(
                                        isLottoMax=self._isLottoMax,
                                        settings=self._settings,
                                     )
        else:
            self.sw = None
            self.sw = SettingsWidget(
                                        isLottoMax=self._isLottoMax,
                                        settings=self._settings,
                                     )

        self.sw.show()

    def _rulesBtnOnClicked(self):
        if not hasattr(self, 'rw'):
            self.rw = RulesWidget(rules=self._rules)
        else:
            self.rw = None
            self.rw = RulesWidget(rules=self._rules)

        self.rw.show()

    def _noNumberCheckBoxOnClicked(self):
        for _, checkBox in self._checkBoxMap.iteritems():
            checkBox.setCheckState(0)

        self._forcedNumbers = []
        self._updateForcedNumberLineEdit()
        self._nbFromForcedSpinBox.setRange(0, 0)
        self._nbFromForcedSpinBox.setValue(0)

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
            msgHandler._pop(self, 2, extraArgs=[maxAllowed, lottoType])
            item.blockSignals(True) # blocking signals so the func does not go in recursion
            item.setCheckState(0)
            self._forcedNumbers.remove(nbItem)
            item.blockSignals(False)
            return

        self._updateForcedNumberLineEdit()
        self._noNumberCheckBox.setCheckState(0)
        self._nbFromForcedSpinBox.setRange(0, len(self._forcedNumbers))
        self._nbFromForcedSpinBox.setValue(len(self._forcedNumbers))

    def _nbFromForcedSpinBoxValueChanged(self, value):
        self._nbFromForced = value

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

    def _isNetworkAvailable(self):
        try:
            response=urllib2.urlopen('http://www.google.com',timeout=1)#'http://74.125.113.99',timeout=1) # pinging google.com
            return True
        except urllib2.URLError as err:pass
        return False

    def _generateBtnOnClicked(self):
        if not self._isNetworkAvailable():
            msgHandler._pop(self, 3)
            return

        self._displayTextEdit.clear()
        self._displayTextEdit.setText('Processing Draw . . .')
        QtGui.QApplication.processEvents()

        kwargs = {
                    'lottoIsMax'          :  self._isLottoMax,
                    'writeDirPath'        :  self._outDir,
                    'write'               :  bool(self._outDir),
                    'scrapType'           :  self._scrapType,
                    'logAnatomy'          :  self._logAnatomy,
                    'nbTickets'           :  self._nbTickets,
                    'doSevenJumps'        :  self._doSevenJumps,
                    'forcedNumbers'       :  self._forcedNumbers,
                    'nbFromForcedRandom'  :  self._nbFromForced,
                    'applyDrawSum'        :  self._rules['drsmRule'],
                    'applyDigitSum'       :  self._rules['dgsmRule'],
                    'applyEvens'          :  self._rules['evensRule'],
                    'applyLows'           :  self._rules['lowsRule'],
                    'drawSumMin'          :  self._settings['drsmMin'],
                    'drawSumMax'          :  self._settings['drsmMax'],
                    'digitSumMin'         :  self._settings['dgsmMin'],
                    'digitSumMax'         :  self._settings['dgsmMax'],
                    'nbEvens'             :  self._settings['nbEvens'],
                    'nbLows'              :  self._settings['nbLows'],
                 }

        self._start = time.time()
        self.rat = RunAlgTask(**kwargs)
        self.rat.runRat()

        self.pw = ProgressWidget()
        self.pw.show()

        # Signals that will be emitted from Algorithm to udpate progress
        self.connect(self.rat, QtCore.SIGNAL("update(int)"), self._informOfUpdate)
        self.connect(self.rat, QtCore.SIGNAL("finished()"), self._informOfFinished)
        self.connect(self.rat, QtCore.SIGNAL("ranOutofLoops()"), self._informOfRanOutOfLoops)

    # Method called asynchronously by thread when progress should be updated
    def _informOfUpdate(self, iterations):
        self.pw._update(iterations)
        self._iter = iterations

    # Method called asynchronously by thread when it has finished
    def _informOfFinished(self):
        self._end = time.time()
        self._displayTextEdit.clear()

        s = ''
        s += 'Total Iterations : %s \n\n' % self._iter
        s += 'Total Running Time : %s (secs)\n\n' % round((self._end - self._start), 2)

        if self._logSettings:
            s += 'Using following settings: \n\n'
            s += '*' * 20
            s += '\n'
            s += 'Is Lotto Max: %s\n' % self._isLottoMax
            s += 'Nb Tickets: %s\n' % self._nbTickets
            s += 'Scrap Type: %s\n' % self._scrapType
            s += 'Do Seven Jumps: %s\n' % self._doSevenJumps
            s += 'Output Dir: "%s "\n' % self._outDir
            s += 'Forced Numbers: [%s]\n' % ', '.join([str(n).zfill(2) for n in self._forcedNumbers])
            s += 'Number of Forced Numbers to use: %s\n' % self._nbFromForced
            s += 'LogAnatomy: %s\n' % self._logAnatomy
            s += 'Draw Sum(Min, Max): (%s, %s)\n' % (self._settings['drsmMin'], self._settings['drsmMax'])
            s += 'Digit Sum(Min, Max): (%s, %s)\n' % (self._settings['dgsmMin'], self._settings['dgsmMax'])
            s += 'Nb Evens: %s\n' % self._settings['nbEvens']
            s += 'Nb Lows: %s\n' % self._settings['nbLows']
            s += 'Draw Sum Rule: %s\n' % self._rules['drsmRule']
            s += 'Digit Sum Rule: %s\n' % self._rules['dgsmRule']
            s += 'Even/Odd Rule: %s\n' % self._rules['evensRule']
            s += 'Low/High Rule: %s\n\n' % self._rules['lowsRule']
            s += '*' * 10
            s += '\n'
            s += 'Results\n'
            s += '*' * 10
            s += '\n\n\n'

        s += self.rat.result
        self._displayTextEdit.setText(s)
        self.pw.closeWindow()

    # Method called asynchronously bythread when it maximum loops have reached
    def _informOfRanOutOfLoops(self):
        self.pw.closeWindow()

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

        self.statusBar()

        resetAction = QtGui.QAction('&Reset Settings', self)
        resetAction.triggered.connect(self._mainWidget._resetBtnOnClicked)

        saveAction = QtGui.QAction('&Save Current Settings', self)
        saveAction.triggered.connect(self._onSaveAction)

        loadAction = QtGui.QAction('&Load Settings', self)
        loadAction.triggered.connect(self._onLoadAction)


        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&File')
        self._presetsMenu = fileMenu.addMenu('&Lotto Settings')
        self._presetsMenu.addAction(resetAction)
        self._presetsMenu.addAction(saveAction)
        self._presetsMenu.addAction(loadAction)

        StyleSheet().setColor(self._mainWidget)
        StyleSheet().setColor(self, app= QtCore.QCoreApplication.instance())

        self.move(50, 50)

    def _onSaveAction(self):
        saveLocation = os.path.join(ROOT_DIR, 'prefs', 'untitled.alg')

        fg = QtGui.QFileDialog()

        f = fg.getSaveFileName(self, "Save File",
                            saveLocation,
                            "Alok's Lotto Generator (*.alg)")

        if not f:
            return

        settings = self._getSettings()

        with open(f, 'wb') as file:
            json.dump(settings, file, sort_keys=True, indent=4)

        Logger.info(f)

    def _getSettings(self):
        d = {}

        w = self._mainWidget

        d['isMax'] = w._isLottoMax
        d['forcedNumbers'] = w._forcedNumbers
        d['outDir'] = w._outDir
        d['doSevenJumps'] = w._doSevenJumps
        d['scrapType'] = w._scrapType
        d['nbFromForced'] = w._nbFromForced
        d['logAnatomy'] = w._logAnatomy
        d['logSettings'] = w._logSettings
        d['drsmMin'] = w._settings['drsmMin']
        d['drsmMax'] = w._settings['drsmMax']
        d['dgsmMin'] = w._settings['dgsmMin']
        d['dgsmMax'] = w._settings['dgsmMax']
        d['drsmRule'] = w._rules['drsmRule']
        d['dgsmRule'] = w._rules['dgsmRule']
        d['evensRule'] = w._rules['evensRule']
        d['lowsRule'] = w._rules['lowsRule']

        return d

    def _onLoadAction(self):
        loadLocation = os.path.join(ROOT_DIR, 'prefs', 'untitled.alg')
        fg = QtGui.QFileDialog()
        f = str(fg.getOpenFileName(self, 'Open file', loadLocation, "Alok's Lotto Generator (*.alg)"))

        if not f:
            return

        with open(f, 'rb') as file:
            settings = json.load(file)

        Logger.info(settings)

def run():
    app = QtGui.QApplication(sys.argv)
    am = MainWindow()
    am.show()
    am.raise_()
    app.exec_()

if __name__ == '__main__':
    run()
