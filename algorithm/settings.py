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
import inspect

URL_LOTTO_649 = r"http://diffusion.loto-quebec.com/sw3/stats/asp/stats.asp?cProduit=4&pRequest=3&l=1"
URL_LOTTO_MAX = r"http://diffusion.loto-quebec.com/sw3/stats/asp/stats.asp?cProduit=38&pRequest=3&l=1"
URL_QUEBEC_649 = r"http://diffusion.loto-quebec.com/sw3/stats/asp/stats.asp?cProduit=5&pRequest=3&l=1"

class Settings(object):
    def __init__(self, * args, **kwargs):
        # Call order of methods should be maintained
        self._setUserVariables(**kwargs)
        self._setRules()
        self._setDefaults()
        self._assertData()


    def _setRules(self):
        # Rules for Algorithm Processes
        # first value for lotto max next value for lotto 649
        self.rules = {'SR_S': (140, 125),
                      'SR_E': (210, 170),
                      'DSR_S': (38, 38),
                      'DSR_E': (60, 60),
                      'NB_EVENS': ([5, 4, 3], [2, 3, 4]),
                      'NB_LOWS': ([4], [3]),
                      }

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

        self.display = True
        if 'display' in kwargs:
            self.display = kwargs['display']

        self.write = True
        if 'write' in kwargs:
            self.write = kwargs['write']

        self.writeDirPath = os.path.dirname(os.path.abspath(__file__))
        if 'writeDirPath' in kwargs:
            userPath = kwargs['writeDirPath']
            if os.path.exists(userPath):
                self.writeDirPath = userPath
            else:
                print 'Specified write path : %s was not found, \ndefault path: %s will be used' % (userPath, self.writeDirPath)

        self.maxLoops = 1
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

    def _assertData(self):
        if self.forcedNumbers != [] and self.nbFromForcedRandom == 0:
            self.nbFromForcedRandom = len(self.forcedNumbers)

        if self.nbFromForcedRandom > self.numbersInDraw:
            raise Exception('You cannot force more than %s numbers for this Lotto Type' % self.numbersInDraw)