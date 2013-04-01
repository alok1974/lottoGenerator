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
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class StyleSheet(object):
    def __init__(self, *args, **kwargs):
        super(StyleSheet, self).__init__(*args, **kwargs)

    def setColor(self, widget, app=None):
        p = os.path.abspath(os.path.join(ROOT_DIR, 'styleSheets', 'stylesheet'))

        if not os.path.exists(p):
            raise Exception('Style Path - %s does not exist !!' % p)

        s = ''
        with open(p, 'r') as f:
            s = f.read()

        if app:
            app.setStyle(QtGui.QStyleFactory.create("Plastique"))

        widget.setStyleSheet(s)
