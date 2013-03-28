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

from PyQt4 import QtCore, QtGui
from logger import Logger

NO_PATH_STRING = '        < using no path >'
NO_NUM_STRING = '    < no numbers selected >'
RADIO_BTN = ['Last Six Months', 'All Months', 'Both']

class MainWidgetUI(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWidgetUI, self).__init__(*args, **kwargs)
        self._checkBoxMap = {}
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

        self._setSumsBtn = QtGui.QPushButton('Set Sums')
        self._setSumsBtn.setStyleSheet("QPushButton {background-color :\
                                             rgb(89, 76, 62);}")

        self._setRulesBtn = QtGui.QPushButton('Set Rules')
        self._setRulesBtn.setStyleSheet("QPushButton {background-color :\
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
        self._grid.setRowMinimumHeight(0, 5)
        self._grid.setRowMinimumHeight(1, 20)

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
        #self._hFolderLayout.addStretch(100)
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
        self._grid.addWidget(self._hLineMap[5], 6, 2)
        self._grid.addWidget(self._setSumsBtn, 7, 2)
        self._grid.addWidget(self._setRulesBtn, 8, 2)

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
        #self._grid.addWidget(self._forcedNumbersDisplayLabel, 5, 4)
        self._grid.addWidget(self._forcedNumbersLineEdit, 6, 4)
        #self._grid.addWidget(self._hLineMap[7], 6, 4)
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

        #self._hBtnLayout = QtGui.QHBoxLayout()
        #self._hBtnLayout.addWidget(self._generateBtn)
        #self._hBtnLayout.addWidget(self._resetBtn)
        #self._grid.addLayout(self._hBtnLayout, 7, 6)
        self._grid.addWidget(self._generateBtn, 7, 6)
        self._grid.addWidget(self._cancelBtn, 8, 6)

        #-----------------------------------------------------------------------

        self._mainLayout = QtGui.QVBoxLayout(self)
        self._mainLayout.addLayout(self._grid)
