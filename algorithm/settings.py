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
import inspect

URL_LOTTO_649 = r"http://diffusion.loto-quebec.com/sw3/stats/asp/stats.asp?cProduit=4&pRequest=3&l=1"
URL_LOTTO_MAX = r"http://diffusion.loto-quebec.com/sw3/stats/asp/stats.asp?cProduit=38&pRequest=3&l=1"
URL_QUEBEC_649 = r"http://diffusion.loto-quebec.com/sw3/stats/asp/stats.asp?cProduit=5&pRequest=3&l=1"

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.join(__file__)), '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from gui import DEF_SETTING

class Settings(object):
    def __init__(self, * args, **kwargs):
        # Call order of methods should be maintained
        self._setUserVariables(**kwargs)
        self._setDefaults()
        self._assertData()

    def _setDefaults(self):
        # Default Variables for Lotto
        self.url = (URL_LOTTO_MAX if self.isMax else URL_LOTTO_649)
        self.numbersInDraw = (7 if self.isMax else 6)
        self.rowsInATicket = (3 if self.isMax else 1)
        self.nbWinningDraw = self.rowsInATicket * self.nbTickets
        self.useAtmosphericNoise = False
        self.outStr = ''

    def _setUserVariables(self, **kwargs):
        # User Defined Variables
        self.isMax = False
        if 'lottoIsMax' in kwargs:
            self.isMax = kwargs['lottoIsMax']

        self.nbTickets = 1
        if 'nbTickets' in kwargs:
            self.nbTickets = kwargs['nbTickets']

        self.write = False
        if 'write' in kwargs:
            self.write = kwargs['write']

        if self.write:
            self.writeDirPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
            if 'writeDirPath' in kwargs:
                userPath = kwargs['writeDirPath']

                if not os.path.exists(userPath):
                    os.mkdir(userPath)

                self.writeDirPath = userPath

        self.maxLoops = DEF_SETTING['maxLoops']
        if 'maxLoops' in kwargs:
            self.maxLoops = kwargs['maxLoops']

        self.logAnatomy = False
        if 'logAnatomy' in kwargs:
            self.logAnatomy = kwargs['logAnatomy']

        self.useNonWeightedRandom = False
        if 'useNonWeightedRandom' in kwargs:
            self.useNonWeightedRandom = kwargs['useNonWeightedRandom']

        self.scrapType = 0
        if 'scrapType' in kwargs:
            self.scrapType = kwargs['scrapType']

        self.extraFileName = ''
        if 'extraFileName' in kwargs:
            self.extraFileName = kwargs['extraFileName']

        self.doSevenJumps = False
        if 'doSevenJumps' in kwargs:
            self.doSevenJumps = kwargs['doSevenJumps']

        self.forcedNumbers = []
        if 'forcedNumbers' in kwargs:
            if len(kwargs['forcedNumbers']) != len(set(kwargs['forcedNumbers'])):
                raise Exception("Forced Number list does not have unique numbers !!")
            self.forcedNumbers = kwargs['forcedNumbers']

        self.nbFromForcedRandom = 0
        if 'nbFromForcedRandom' in kwargs and self.forcedNumbers:
            if kwargs['nbFromForcedRandom'] > len(self.forcedNumbers):
                raise Exception('nbFromForcedRandom cannot be greater than total numbers in forcedNumbers !!')

            self.nbFromForcedRandom = kwargs['nbFromForcedRandom']

        self.applyDrawSum = True
        if 'applyDrawSum' in kwargs:
            self.applyDrawSum = kwargs['applyDrawSum']

        self.applyDigitSum = False
        if 'applyDigitSum' in kwargs:
            self.applyDigitSum = kwargs['applyDigitSum']

        self.applyEvens = True
        if 'applyEvens' in kwargs:
            self.applyEvens = kwargs['applyEvens']

        self.applyLows = False
        if 'applyLows' in kwargs:
            self.applyLows = kwargs['applyLows']

        self.drsmMin = DEF_SETTING['drsmMin'][int(self.isMax)]
        if 'drawSumMin' in kwargs:
            self.drsmMin = kwargs['drawSumMin']

        self.drsmMax = DEF_SETTING['drsmMax'][int(self.isMax)]
        if 'drawSumMax' in kwargs:
            self.drsmMax = kwargs['drawSumMax']

        self.dgsmMin = DEF_SETTING['dgsmMin'][int(self.isMax)]
        if 'digitSumMin' in kwargs:
            self.dgsmMin = kwargs['digitSumMin']

        self.dgsmMax = DEF_SETTING['dgsmMax'][int(self.isMax)]
        if 'digitSumMax' in kwargs:
            self.dgsmMax = kwargs['digitSumMax']

        self.evens = DEF_SETTING['nbEvens'][int(self.isMax)]
        if 'nbEvens' in kwargs:
            self.evens = kwargs['nbEvens']

        self.lows = DEF_SETTING['nbLows'][int(self.isMax)]
        if 'nbLows' in kwargs:
            self.lows = kwargs['nbLows']

    def _assertData(self):
        if self.forcedNumbers != [] and self.nbFromForcedRandom == 0:
            self.nbFromForcedRandom = len(self.forcedNumbers)

        if self.nbFromForcedRandom > self.numbersInDraw:
            raise Exception('You cannot force more than %s numbers for this Lotto Type' % self.numbersInDraw)
