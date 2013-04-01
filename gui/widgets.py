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
import functools
from PyQt4 import QtCore, QtGui
from logger import Logger

from styleSheet import StyleSheet

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.join(__file__)), '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from gui import *

class ProgressWidget(QtGui.QDialog):
    def __init__(self, *args, **kwargs):
        super(ProgressWidget, self).__init__(*args, **kwargs)
        self.setModal(True)
        self._closedByProcess = False
        self._initUI()

    def _initUI(self):
        self.pic = QtGui.QLabel(self)
        self.pic.setGeometry(0, 0, 200, 100)
        self. pic.setPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(ROOT_DIR, 'icons', 'pbar', '1.png'))))
        self.setWindowTitle('Generating Draw')

    def _update(self, iter):
        iter = ((iter/ 100)%31) + 1
        self. pic.setPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(ROOT_DIR, 'icons', 'pbar', '%s.png' % iter))))

    def closeWindow(self):
        self._closedByProcess = True
        self.close()

    def closeEvent(self, event):
        if not self._closedByProcess:
            event.ignore()

class SettingsWidget(QtGui.QDialog):
    def __init__(self, isLottoMax=False, settings=[], *args, **kwargs):
        super(SettingsWidget, self).__init__(*args, **kwargs)
        self.setModal(True)
        StyleSheet().setColor(self)

        self._isLottoMax = isLottoMax
        self._settings = settings

        self._hLineMap = {}
        self._vLineMap = {}
        self._checkBox01Map = {}
        self._checkBox02Map = {}
        self._nbEvens = []
        self._nbLows = []

        self._initData()
        self._initUI()
        self._initWidgets()
        self._connections()

    def _initUI(self):
        # Labels
        self._drawSumLabel = QtGui.QLabel('Draw Sum')
        self._drawSumMinLabel = QtGui.QLabel('Min')
        self._drawSumMaxLabel = QtGui.QLabel('Max')

        self._digitSumLabel = QtGui.QLabel('Digit Sum')
        self._digitSumMinLabel = QtGui.QLabel('Min')
        self._digitSumMaxLabel = QtGui.QLabel('Max')

        self._nbEvensLabel = QtGui.QLabel('Number of Evens')
        self._nbLowsLabel = QtGui.QLabel('Number of Lows')

        # Spinboxes
        self._drawSumMinSpinBox = QtGui.QSpinBox()
        self._drawSumMinSpinBox.setStyleSheet("QSpinBox {background-color : \
                                              rgb(76, 78, 101); font-size: 30px;}")
        self._drawSumMinSpinBox.setRange(SPN_BX_RANGE['drsm_spnbx_min'][int(self._isLottoMax)],
                                         SPN_BX_RANGE['drsm_spnbx_max'][int(self._isLottoMax)])

        self._drawSumMinSpinBox.lineEdit().setReadOnly(True)
        self._drawSumMinSpinBox.lineEdit().setEnabled(False)


        self._drawSumMaxSpinBox = QtGui.QSpinBox()
        self._drawSumMaxSpinBox.setStyleSheet("QSpinBox {background-color : \
                                              rgb(76, 78, 101); font-size: 30px;}")
        self._drawSumMaxSpinBox.setRange(SPN_BX_RANGE['drsm_spnbx_min'][int(self._isLottoMax)],
                                         SPN_BX_RANGE['drsm_spnbx_max'][int(self._isLottoMax)])

        self._drawSumMaxSpinBox.lineEdit().setReadOnly(True)
        self._drawSumMaxSpinBox.lineEdit().setEnabled(False)

        self._digitSumMinSpinBox = QtGui.QSpinBox()
        self._digitSumMinSpinBox.setStyleSheet("QSpinBox {background-color : \
                                              rgb(69, 98, 104); font-size: 30px;}")
        self._digitSumMinSpinBox.setRange(SPN_BX_RANGE['dgsm_spnbx_min'][int(self._isLottoMax)],
                                         SPN_BX_RANGE['dgsm_spnbx_max'][int(self._isLottoMax)])

        self._digitSumMinSpinBox.lineEdit().setReadOnly(True)
        self._digitSumMinSpinBox.lineEdit().setEnabled(False)

        self._digitSumMaxSpinBox = QtGui.QSpinBox()
        self._digitSumMaxSpinBox.setStyleSheet("QSpinBox {background-color : \
                                              rgb(69, 98, 104); font-size: 30px;}")
        self._digitSumMaxSpinBox.setRange(SPN_BX_RANGE['dgsm_spnbx_min'][int(self._isLottoMax)],
                                         SPN_BX_RANGE['dgsm_spnbx_max'][int(self._isLottoMax)])

        self._digitSumMaxSpinBox.lineEdit().setReadOnly(True)
        self._digitSumMaxSpinBox.lineEdit().setEnabled(False)


        # Line Edits
        self._nbEvensLineEdit = QtGui.QLineEdit()
        self._nbEvensLineEdit.setText(NO_NUM_STRING)
        self._nbEvensLineEdit.setStyleSheet("QLineEdit {background-color : \
                                              rgb(97, 91, 83); color : \
                                              rgb(40, 40, 40); font-size: 16px;}")
        self._nbEvensLineEdit.setMinimumSize(50, 50)




        self._nbLowsLineEdit = QtGui.QLineEdit()
        self._nbLowsLineEdit.setText(NO_NUM_STRING)
        self._nbLowsLineEdit.setStyleSheet("QLineEdit {background-color : \
                                              rgb(97, 91, 83); color : \
                                              rgb(40, 40, 40); font-size: 16px;}")
        self._nbLowsLineEdit.setMinimumSize(50, 50)



        # Buttons
        self._okBtn = QtGui.QPushButton('OK')
        self._okBtn.setStyleSheet("QPushButton {background-color : \
                                        rgb(110, 122, 74); min-height : 120px}")

        self._defaultsBtn = QtGui.QPushButton('Defaults')
        self._defaultsBtn.setStyleSheet("QPushButton {background-color : \
                                        rgb(94, 57, 69); min-height : 120px}")

        # Lines
        lines = {'nb': (6, 2), 'type': (QtGui.QFrame.HLine, QtGui.QFrame.VLine),
                    'storeIn' : (self._hLineMap, self._vLineMap)}

        for i in range(2):
            nbLines, type, storeIn = (lines['nb'][i], lines['type'][i], lines['storeIn'][i])

            for j in range(nbLines):
                _line = QtGui.QFrame()
                _line.setGeometry(QtCore.QRect(170, 90, 118, 8))
                _line.setFrameShape(type)
                _line.setFrameShadow(QtGui.QFrame.Sunken)
                _line.setStyleSheet("QFrame {background-color : rgb(97, 91, 83);}")
                storeIn[j+1] = _line


        # Grid Layout
        self._grid = QtGui.QGridLayout()
        self._grid.setSpacing(15)

        # Column 01
        self._grid.addWidget(self._hLineMap[1], 0, 0)
        self._grid.addWidget(self._drawSumLabel, 1, 0)


        self._hLayout01 = QtGui.QHBoxLayout()
        self._hLayout01.addWidget(self._drawSumMinLabel)
        self._hLayout01.addWidget(self._drawSumMinSpinBox)
        self._grid.addLayout(self._hLayout01, 2, 0)

        self._hLayout02 = QtGui.QHBoxLayout()
        self._hLayout02.addWidget(self._drawSumMaxLabel)
        self._hLayout02.addWidget(self._drawSumMaxSpinBox)
        self._grid.addLayout(self._hLayout02, 3, 0)

        self._grid.addWidget(self._hLineMap[2], 4, 0)
        self._grid.addWidget(self._digitSumLabel, 5, 0)

        self._hLayout03 = QtGui.QHBoxLayout()
        self._hLayout03.addWidget(self._digitSumMinLabel)
        self._hLayout03.addWidget(self._digitSumMinSpinBox)
        self._grid.addLayout(self._hLayout03, 6, 0)

        self._hLayout04 = QtGui.QHBoxLayout()
        self._hLayout04.addWidget(self._digitSumMaxLabel)
        self._hLayout04.addWidget(self._digitSumMaxSpinBox)
        self._grid.addLayout(self._hLayout04, 7, 0)

        # Column 02
        self._grid.addWidget(self._vLineMap[1], 0, 1, 8, 1)

        # Column 03
        self._grid.addWidget(self._hLineMap[3], 0, 2)

        self._grid.addWidget(self._nbEvensLabel, 1, 2)
        self._checkBox01Layout = QtGui.QHBoxLayout()
        for i in range(7):
            nbStr = '%s' % str(i + 1).zfill(2)
            self._nbCheckBox = QtGui.QCheckBox(nbStr)
            self._nbCheckBox.setStyleSheet("QCheckBox::indicator::checked \
                                           {background-color: rgb(20, 180, 20);}")
            self._checkBox01Map[nbStr] = self._nbCheckBox
            self._checkBox01Layout.addWidget(self._nbCheckBox)

        self._grid.addLayout(self._checkBox01Layout, 2, 2)
        self._grid.addWidget(self._nbEvensLineEdit, 3, 2)

        self._grid.addWidget(self._hLineMap[4], 4, 2)

        self._grid.addWidget(self._nbLowsLabel, 5, 2)
        self._checkBox02Layout = QtGui.QHBoxLayout()
        for i in range(7):
            nbStr = '%s' % str(i + 1).zfill(2)
            self._nbCheckBox = QtGui.QCheckBox(nbStr)
            self._nbCheckBox.setStyleSheet("QCheckBox::indicator::checked \
                                           {background-color: rgb(20, 180, 20);}")
            self._checkBox02Map[nbStr] = self._nbCheckBox
            self._checkBox02Layout.addWidget(self._nbCheckBox)

        self._grid.addLayout(self._checkBox02Layout, 6, 2)
        self._grid.addWidget(self._nbLowsLineEdit, 7, 2)

        # Column 04
        self._grid.addWidget(self._vLineMap[2], 0, 3, 8, 1)

        # Column 05
        self._grid.addWidget(self._hLineMap[5], 0, 4)
        self._grid.addWidget(self._defaultsBtn, 1, 4, 3, 1)
        self._grid.addWidget(self._hLineMap[6], 4, 4)
        self._grid.addWidget(self._okBtn, 5, 4, 3, 1)

        self.setWindowTitle("Settings")
        self.setLayout(self._grid)
        self.setGeometry(100, 100, 10, 10)

    def _initData(self, calledFromDefaults=False):
        if calledFromDefaults:
            self._nbEvens = DEF_SETTING['nbEvens'][int(self._isLottoMax)][:]
            self._nbLows = DEF_SETTING['nbLows'][int(self._isLottoMax)][:]
        else:
            self._nbEvens = self._settings['nbEvens'][:]
            self._nbLows = self._settings['nbLows'][:]

    def _initWidgets(self, calledFromDefaults=False):
        if calledFromDefaults:
            self._drawSumMinSpinBox.setValue(DEF_SETTING['drsmMin'][int(self._isLottoMax)])
            self._drawSumMaxSpinBox.setValue(DEF_SETTING['drsmMax'][int(self._isLottoMax)])
            self._digitSumMinSpinBox.setValue(DEF_SETTING['dgsmMin'][int(self._isLottoMax)])
            self._digitSumMaxSpinBox.setValue(DEF_SETTING['dgsmMax'][int(self._isLottoMax)])
        else:
            self._drawSumMinSpinBox.setValue(self._settings['drsmMin'])
            self._drawSumMaxSpinBox.setValue(self._settings['drsmMax'])
            self._digitSumMinSpinBox.setValue(self._settings['dgsmMin'])
            self._digitSumMaxSpinBox.setValue(self._settings['dgsmMax'])

        for index, checkBox in self._checkBox01Map.iteritems():
            if int(index) in self._nbEvens:
                checkBox.setChecked(True)
            else:
                checkBox.setChecked(False)

        for index, checkBox in self._checkBox02Map.iteritems():
            if int(index) in self._nbLows:
                checkBox.setChecked(True)
            else:
                checkBox.setChecked(False)

        self._updateNbEvensLineEdit()
        self._updateNbLowsLineEdit()

    def _updateNbEvensLineEdit(self):
        if not self._nbEvens:
            self._nbEvensLineEdit.setText(NO_NUM_STRING)
            return

        s = '[%s]' % ', '.join(sorted([str(n) for n in self._nbEvens]))
        self._nbEvensLineEdit.setText(s)

    def _updateNbLowsLineEdit(self):
        if not self._nbLows:
            self._nbLowsLineEdit.setText(NO_NUM_STRING)
            return

        s = '[%s]' % ', '.join(sorted([str(n) for n in self._nbLows]))
        self._nbLowsLineEdit.setText(s)

    def _connections(self):
        self._okBtn.clicked.connect(self.close)
        self._defaultsBtn.clicked.connect(self._defaultsBtnOnClicked)
        self._connectCheckBox01()
        self._connectCheckBox02()

    def _connectCheckBox01(self):
        for index, checkBox in self._checkBox01Map.iteritems():
            checkBox.clicked.connect(functools.partial(self._connectCheckBox01MappedSlot, checkBox, int(index)))

    def _connectCheckBox01MappedSlot(self, item, nbItem):
        if item.checkState()==2:
            self._nbEvens.append(nbItem)
        elif item.checkState()==0:
            self._nbEvens.remove(nbItem)

        self._updateNbEvensLineEdit()

    def _connectCheckBox02(self):
        for index, checkBox in self._checkBox02Map.iteritems():
            checkBox.clicked.connect(functools.partial(self._connectCheckBox02MappedSlot, checkBox, int(index)))

    def _connectCheckBox02MappedSlot(self, item, nbItem):
        if item.checkState()==2:
            self._nbLows.append(nbItem)
        elif item.checkState()==0:
            self._nbLows.remove(nbItem)

        self._updateNbLowsLineEdit()

    def _defaultsBtnOnClicked(self):
        self._initData(calledFromDefaults=True)
        self._initWidgets(calledFromDefaults=True)

    def _updateSettings(self):
        self._settings['drsmMin'] = self._drawSumMinSpinBox.value()
        self._settings['drsmMax'] = self._drawSumMaxSpinBox.value()
        self._settings['dgsmMin'] = self._digitSumMinSpinBox.value()
        self._settings['dgsmMax'] = self._digitSumMaxSpinBox.value()
        self._settings['nbEvens'] = self._nbEvens[:]
        self._settings['nbLows'] = self._nbLows[:]

    def closeEvent(self, event):
        self._updateSettings()

class RulesWidget(QtGui.QDialog):
    def __init__(self, rules={}, *args, **kwargs):
        super(RulesWidget, self).__init__(*args, **kwargs)
        self.setModal(True)

        StyleSheet().setColor(self)

        self._rules = rules

        self._hLineMap = {}

        self._initUI()
        self._initWidgets()

    def _initUI(self):
        # CheckBoxes
        self._drawSumCheckBox = QtGui.QCheckBox('  Apply Draw Sum Rule')
        self._drawSumCheckBox.setStyleSheet("QCheckBox {font-size: 16px;} \
                                            QCheckBox::indicator::checked \
                                            {background-color: rgb(200, 200, 0);}")



        self._digitSumCheckBox = QtGui.QCheckBox('  Apply Digit Sum Rule')
        self._digitSumCheckBox.setStyleSheet("QCheckBox {font-size: 16px;} \
                                            QCheckBox::indicator::checked \
                                            {background-color: rgb(200, 200, 0);}")


        self._evensCheckBox = QtGui.QCheckBox('  Apply Even/Odd Number Rule')
        self._evensCheckBox.setStyleSheet("QCheckBox {font-size: 16px;} \
                                            QCheckBox::indicator::checked \
                                            {background-color: rgb(200, 200, 0);}")


        self._lowsCheckBox = QtGui.QCheckBox('  Apply Low/High Number Rule')
        self._lowsCheckBox.setStyleSheet("QCheckBox {font-size: 16px;} \
                                            QCheckBox::indicator::checked \
                                            {background-color: rgb(200, 200, 0);}")

        # Buttons
        self._okBtn = QtGui.QPushButton('OK')
        self._okBtn.setStyleSheet("QPushButton {background-color : \
                                        rgb(110, 122, 74);}")
        self._okBtn.clicked.connect(self.close)


        self._defaultsBtn = QtGui.QPushButton('Defaults')
        self._defaultsBtn.setStyleSheet("QPushButton {background-color : \
                                        rgb(94, 57, 69);}")

        self._defaultsBtn.clicked.connect(self._defaultsBtnOnClicked)


        # Lines
        for i in range(2):
            _line = QtGui.QFrame()
            _line.setGeometry(QtCore.QRect(170, 90, 118, 8))
            _line.setFrameShape(QtGui.QFrame.HLine)
            _line.setFrameShadow(QtGui.QFrame.Sunken)
            _line.setStyleSheet("QFrame {background-color : rgb(97, 91, 83);}")
            self._hLineMap[i+1] = _line




        # Grid Layout
        self._grid = QtGui.QGridLayout()
        self._grid.setSpacing(30)

        self._grid.addWidget(self._hLineMap[1], 0, 0)
        self._grid.addWidget(self._drawSumCheckBox, 1, 0)
        self._grid.addWidget(self._digitSumCheckBox, 2, 0)
        self._grid.addWidget(self._evensCheckBox, 3, 0)
        self._grid.addWidget(self._lowsCheckBox, 4, 0)
        self._grid.addWidget(self._hLineMap[2], 5, 0)

        self._hlayout = QtGui.QHBoxLayout()
        self._hlayout.addWidget(self._okBtn)
        self._hlayout.addWidget(self._defaultsBtn)

        self._grid.addLayout(self._hlayout, 6, 0)

        self.setLayout(self._grid)
        self.setWindowTitle("Rules")
        self.setGeometry(100, 100, 10, 10)

    def _initWidgets(self):
        self._drawSumCheckBox.setChecked(self._rules['drsmRule'])
        self._digitSumCheckBox.setChecked(self._rules['dgsmRule'])
        self._evensCheckBox.setChecked(self._rules['evensRule'])
        self._lowsCheckBox.setChecked(self._rules['lowsRule'])

    def _defaultsBtnOnClicked(self):
        self._drawSumCheckBox.setChecked(DEF_RULES['drsmRule'])
        self._digitSumCheckBox.setChecked(DEF_RULES['dgsmRule'])
        self._evensCheckBox.setChecked(DEF_RULES['evensRule'])
        self._lowsCheckBox.setChecked(DEF_RULES['lowsRule'])

    def _updateRules(self):
        self._rules['drsmRule'] = bool(self._drawSumCheckBox.isChecked())
        self._rules['dgsmRule'] = bool(self._digitSumCheckBox.isChecked())
        self._rules['evensRule'] = bool(self._evensCheckBox.isChecked())
        self._rules['lowsRule'] = bool(self._lowsCheckBox.isChecked())

    def closeEvent(self, event):
        self._updateRules()


class MainWidgetUI(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWidgetUI, self).__init__(*args, **kwargs)
        self._radioBtnMap = {}
        self._hLineMap = {}
        self._vLineMap = {}
        self._checkBoxMap = {}

    def _setupUI(self):

        #-----------------------------------------------------------------------

        # Labels
        self._lottoTypeLabel = QtGui.QLabel('Select Lotto Type')
        self._nbTicketsLabel = QtGui.QLabel('Number of Tickets \nto Generate')
        self._displayLabel = QtGui.QLabel('Generated Results')
        self._scrapTypeLabel = QtGui.QLabel('Generate based \non results for')
        self._forcedNumbersLabel = QtGui.QLabel('Select Numbers to force')
        self._forcedNumbersDisplayLabel = QtGui.QLabel('Forced numbers')
        self._useFolderLabel = QtGui.QLabel('Output folder for \nwriting results')
        self._nbFromForcedLabel = QtGui.QLabel('How many numbers to use \nfrom forced numbers ?')


        #-----------------------------------------------------------------------

        # Edits and ComboBoxes
        self._lottoTypeComboBox = QtGui.QComboBox()
        self._lottoTypeComboBox.setMinimumSize(200, 50)
        self._lottoTypeComboBox.setStyleSheet("QComboBox {background-color : \
                                              rgb(76, 78, 101); font-size: 30px;}")

        self._nbTicketsSpinBox = QtGui.QSpinBox()
        self._nbTicketsSpinBox.setMinimumSize(200, 50)
        self._nbTicketsSpinBox.setStyleSheet("QSpinBox {background-color : \
                                             rgb(69, 98, 104); font-size: 30px;}")


        self._nbFromForcedSpinBox = QtGui.QSpinBox()
        self._nbFromForcedSpinBox.setMinimumSize(200, 50)
        self._nbFromForcedSpinBox.setStyleSheet("QSpinBox {background-color : \
                                             rgb(104, 99, 62); font-size: 30px;}")

        self._displayTextEdit = QtGui.QTextEdit()
        self._displayTextEdit.setReadOnly(True)
        self._displayTextEdit.setStyleSheet("QTextEdit {background-color :\
                                            rgb(97, 91, 83); color : \
                                            rgb(50, 0, 0); font-size: 12px;}")

        self._outPutDirLineEdit = QtGui.QLineEdit()
        self._outPutDirLineEdit.setReadOnly(True)
        self._outPutDirLineEdit.setText(NO_PATH_STRING)
        self._outPutDirLineEdit.setStyleSheet("QLineEdit {background-color : \
                                              rgb(97, 91, 83); color : \
                                              rgb(40, 40, 40); font-size: 16px;}")
        self._outPutDirLineEdit.setMinimumSize(50, 50)
        self._outPutDirLineEdit.setToolTip('')
        self._outPutDirLineEdit.setEnabled(False)

        self._forcedNumbersLineEdit = QtGui.QLineEdit()
        self._forcedNumbersLineEdit.setReadOnly(True)
        self._forcedNumbersLineEdit.setText(NO_NUM_STRING)
        self._forcedNumbersLineEdit.setStyleSheet("QLineEdit {background-color : \
                                                  rgb(97, 91, 83); color : \
                                                  rgb(40, 40, 40); font-size: 16px;}")

        self._forcedNumbersLineEdit.setMinimumSize(50, 50)

        #-----------------------------------------------------------------------

        # Check Boxes
        self._sevenJumpsCheckBox = QtGui.QCheckBox("Do Seven Jumps")
        self._sevenJumpsCheckBox.setStyleSheet("QCheckBox {font-size: 16px;}")

        self._writeToFileCheckBox = QtGui.QCheckBox("Write Results to File")
        self._writeToFileCheckBox.setStyleSheet("QCheckBox {font-size: 16px;}")

        self._logAnatomyCheckBox = QtGui.QCheckBox("Log Details in Results")
        self._logAnatomyCheckBox.setStyleSheet("QCheckBox {font-size: 16px;}")

        self._logSettingsCheckBox = QtGui.QCheckBox("Show Settings in Results")
        self._logSettingsCheckBox.setStyleSheet("QCheckBox {font-size: 16px;}")

        #-----------------------------------------------------------------------

        # Lines
        lines = {'nb': (9, 3), 'type': (QtGui.QFrame.HLine, QtGui.QFrame.VLine),
                    'storeIn' : (self._hLineMap, self._vLineMap)}

        for i in range(2):
            nbLines, type, storeIn = (lines['nb'][i], lines['type'][i], lines['storeIn'][i])

            for j in range(nbLines):
                _line = QtGui.QFrame()
                _line.setGeometry(QtCore.QRect(170, 90, 118, 8))
                _line.setFrameShape(type)
                _line.setFrameShadow(QtGui.QFrame.Sunken)
                _line.setStyleSheet("QFrame {background-color : rgb(97, 91, 83);}")
                storeIn[j+1] = _line

        #-----------------------------------------------------------------------

        # Buttons
        self._generateBtn = QtGui.QPushButton('Generate')
        self._generateBtn.setStyleSheet("QPushButton {background-color : \
                                        rgb(110, 122, 74);}")

        self._resetBtn = QtGui.QPushButton('Reset Options')
        self._resetBtn.setStyleSheet("QPushButton {background-color : \
                                        rgb(110, 122, 74);}")

        self._cancelBtn = QtGui.QPushButton('Cancel')
        self._cancelBtn.setStyleSheet("QPushButton {background-color : \
                                      rgb(94, 57, 69);}")

        self._clearTextBtn = QtGui.QPushButton('Clear')
        self._clearTextBtn.setStyleSheet("QPushButton {background-color : \
                                         rgb(57, 77, 94);}")
        self._clearTextBtn.setMinimumHeight(100)

        self._copyBtn = QtGui.QPushButton('Copy')
        self._copyBtn.setStyleSheet("QPushButton {background-color : \
                                    rgb(57, 90, 94);}")
        self._copyBtn.setMinimumHeight(100)

        self._clearOutPathBtn = QtGui.QPushButton('No Folder')
        self._clearOutPathBtn.setStyleSheet("QPushButton {background-color : \
                                            rgb(90, 69, 96);}")

        self._selectOutPathBtn = QtGui.QPushButton('Select Folder')
        self._selectOutPathBtn.setStyleSheet("QPushButton {background-color :\
                                             rgb(89, 65, 62);}")

        self._settingsBtn = QtGui.QPushButton('Settings')
        self._settingsBtn.setStyleSheet("QPushButton {background-color :\
                                             rgb(89, 76, 62);}")

        self._rulesBtn = QtGui.QPushButton('Rules')
        self._rulesBtn.setStyleSheet("QPushButton {background-color :\
                                             rgb(68, 89, 62);}")

        #-----------------------------------------------------------------------

        # Radio Buttons
        for index, t in enumerate(RADIO_BTN):
            _radioBtn =  QtGui.QRadioButton(t)
            _radioBtn.setStyleSheet("QRadioButton {/*background-color :\
                                                         rgb(69, 98, 104)*/; \
                                                         font-size: 16px;}")
            self._radioBtnMap[index] = _radioBtn

        #-----------------------------------------------------------------------

        #-----------------------------------------------------------------------

        # Grid Layout
        self._grid = QtGui.QGridLayout()
        self._grid.setSpacing(15)

        #-----------------------------------------------------------------------
        # Column 01
        self._grid.addWidget(self._hLineMap[1], 0, 0)
        self._grid.addWidget(self._lottoTypeLabel, 1, 0)
        self._grid.addWidget(self._lottoTypeComboBox, 2, 0, 1, 1)

        self._grid.addWidget(self._nbTicketsLabel, 3, 0)
        self._grid.addWidget(self._nbTicketsSpinBox, 4, 0, 1, 1)

        self._grid.addWidget(self._hLineMap[2], 5, 0)
        self._grid.addWidget(self._useFolderLabel, 6, 0)
        self._grid.addWidget(self._outPutDirLineEdit, 7, 0)

        self._hFolderLayout = QtGui.QHBoxLayout()
        self._hFolderLayout.addWidget(self._selectOutPathBtn)
        self._hFolderLayout.addWidget(self._clearOutPathBtn)

        self._grid.addLayout(self._hFolderLayout, 8, 0)

        #-----------------------------------------------------------------------

        # column 02
        self._grid.addWidget(self._vLineMap[1], 0, 1, 9, 1)

        #-----------------------------------------------------------------------

        # column 03
        self._grid.addWidget(self._hLineMap[3], 0, 2)
        self._grid.addWidget(self._scrapTypeLabel, 1, 2)

        self._vRadioLayout = QtGui.QVBoxLayout()

        for i in range(3):
            self._vRadioLayout.addWidget(self._radioBtnMap[i])

        self._grid.addLayout(self._vRadioLayout, 2, 2)
        self._grid.addWidget(self._hLineMap[4], 3, 2)
        self._grid.addWidget(self._sevenJumpsCheckBox, 4, 2)
        self._grid.addWidget(self._logAnatomyCheckBox, 5, 2)
        self._grid.addWidget(self._logSettingsCheckBox, 6, 2)
        self._grid.addWidget(self._settingsBtn, 7, 2)
        self._grid.addWidget(self._rulesBtn, 8, 2)

        #-----------------------------------------------------------------------

        # column 04
        self._grid.addWidget(self._vLineMap[2], 0, 3, 9, 1)


        #-----------------------------------------------------------------------

        # Column 05
        self._grid.addWidget(self._hLineMap[6], 0, 4)

        self._grid.addWidget(self._forcedNumbersLabel, 1, 4)

        self._numberGrid = QtGui.QGridLayout()
        self._noNumberCheckBox = QtGui.QCheckBox('None')
        self._noNumberCheckBox.setStyleSheet("QCheckBox::indicator::checked \
                                             {background-color: rgb(200, 20, 20);}")

        self._numberGrid.addWidget(self._noNumberCheckBox, 0, 0)
        for i in range(10):
            for j in range(5):
                if i==j==0:
                    continue

                nbStr = '%s' % str((j * 10) + i).zfill(2)
                self._nbCheckBox = QtGui.QCheckBox(nbStr)
                self._nbCheckBox.setStyleSheet("QCheckBox::indicator::checked \
                                               {background-color: rgb(20, 180, 20);}")
                self._checkBoxMap[nbStr] = self._nbCheckBox
                self._numberGrid.addWidget(self._nbCheckBox, i, j)

        self._grid.addLayout(self._numberGrid, 2, 4, 4, 1)
        self._grid.addWidget(self._forcedNumbersLineEdit, 6, 4)
        self._grid.addWidget(self._nbFromForcedLabel, 7, 4)
        self._grid.addWidget(self._nbFromForcedSpinBox, 8, 4)

        #-----------------------------------------------------------------------

        # column 06
        self._grid.addWidget(self._vLineMap[3], 0, 5, 9, 1)

        #-----------------------------------------------------------------------

        # Column 07
        self._hLayout = QtGui.QHBoxLayout()
        self._hLayout.addWidget(self._clearTextBtn)
        self._hLayout.addWidget(self._copyBtn)

        self._grid.addWidget(self._hLineMap[8], 0, 6)
        self._grid.addWidget(self._displayLabel, 1, 6)
        self._grid.addWidget(self._displayTextEdit, 2, 6, 3, 1)
        self._grid.addLayout(self._hLayout, 5, 6)
        self._grid.addWidget(self._hLineMap[9], 6, 6)

        self._grid.addWidget(self._generateBtn, 7, 6)
        self._grid.addWidget(self._cancelBtn, 8, 6)

        #-----------------------------------------------------------------------

        self._mainLayout = QtGui.QVBoxLayout(self)
        self._mainLayout.addLayout(self._grid)
