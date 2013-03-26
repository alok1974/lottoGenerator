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

import sys
import os
from PyQt4 import QtCore, QtGui
from logger import Logger


APP_STYLE = ("WindowsVista" if sys.platform.startswith('win')  else "Plastique")
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

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
            raise Exception('"%s" type of stylesheet option does not exist !!'
                            % self.style)

        p = os.path.join(ROOT_DIR, 'styleSheets', str(self.style))

        if not os.path.exists(p):
            raise Exception('Style Path - %s does not exist !!' % p)

        s = ''
        with open(p, 'r') as f:
            s = f.read()
        #
        #imageDir = str(os.path.abspath(os.path.join(ROOT_DIR, 'icons')))
        #s = s.replace('FULLPATH', imageDir)

        if app:
            app.setStyle(QtGui.QStyleFactory.create("Plastique"))

        widget.setStyleSheet(s)