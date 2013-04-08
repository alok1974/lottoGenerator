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
import time
import random

from settings import Settings
from scrap import ScrapLottoData
from randomGenerator import WeightedRandomGenerator
from  output import Output
from PyQt4 import QtCore, QtGui

class MainAlgorithm(Settings):
    def __init__(self, qThread=None, * args, **kwargs):
        super(MainAlgorithm, self).__init__(*args, **kwargs)
        self.sm = None
        self.dsm = None
        self.nbEven = None
        self.nbLow = None
        self.validation = False
        self.gen = None
        self.nbSevenJumps = 0
        self.qThread = qThread

    def _getDraw(self, wr):
        winningDraw = []

        nbNumsToget = self.numbersInDraw - self.nbFromForcedRandom

        if self.useAtmosphericNoise:
            winningDraw.extend(wr.getNaturalRandom(min=1, max=49, nbNumbers=nbNumsToget))
        else:
            for i in range(nbNumsToget):
                while True:
                    if self.useNonWeightedRandom:
                        num = wr.getNonWeightedRandom()
                    else:
                        num = wr.getRandomNumber()

                    if num not in winningDraw:
                        break

                winningDraw.append(num)

        for i in range(self.nbFromForcedRandom):

            randomIndex = random.randint(0, len(self.forcedNumbers) - 1)
            random.shuffle(self.forcedNumbers)
            forcedNumber = self.forcedNumbers[randomIndex]

            ctr = 0
            while forcedNumber in winningDraw and ctr < 20:
                randomIndex = random.randint(0, len(self.forcedNumbers) - 1)
                random.shuffle(self.forcedNumbers)
                forcedNumber = self.forcedNumbers[randomIndex]
                ctr += 1

            winningDraw.append(forcedNumber)

        return winningDraw

    @staticmethod
    def _getSevenJumps(inDraw):
        nbSevenJumps = 0
        rows = [([(i + 1) + (7 * j) for j in range(7)]) for i in range(7)]
        rowsJumpData = dict([(i + 1, 0)for i in range(7)])

        for n in inDraw:
            for index, r in enumerate(rows):
                if n in r:
                    rowsJumpData[index + 1] += 1

        for k, v in rowsJumpData.iteritems():
            if v > 1:
                nbSevenJumps += 1

        return nbSevenJumps

    def _setDrawAnatomy(self):
        self.sm = sum(self.winningDraw)
        self.dsm = sum([(n%10 + n/10) for n in self.winningDraw])
        self.nbEven = len([n for n in self.winningDraw if n%2 == 0])
        self.nbLow = len([n for n in self.winningDraw if n < 26 ])
        self.nbSevenJumps = self._getSevenJumps(self.winningDraw)

    def _validateDraw(self):
        SR_S = self.drsmMin
        SR_E = self.drsmMax
        DSR_S = self.dgsmMin
        DSR_E = self.dgsmMax
        NB_EVENS = self.evens
        NB_LOWS = self.lows

        self._setDrawAnatomy()

        drsmRule = (SR_S <= self.sm <= SR_E if self.applyDrawSum else True)
        dgsmRule = (DSR_S <= self.dsm <= DSR_E if self.applyDigitSum else True)
        evensRule = (self.nbEven in NB_EVENS if self.applyEvens else True)
        lowsRule = (self.nbLow in NB_LOWS if self.applyLows else True)
        doSevenJumps = (self.nbSevenJumps>0 if self.doSevenJumps else self.nbSevenJumps==0)

        self.validation =  drsmRule and dgsmRule and evensRule and lowsRule and doSevenJumps

    def runAlg(self):
        lottoData = None
        if not self.useAtmosphericNoise:
            ld = ScrapLottoData(url=self.url, scrapType=self.scrapType)
            lottoData = ld.getLottoData()

        wr = WeightedRandomGenerator(lottoData)

        allGen = []
        ctr = 0
        mainCtr = 0
        for k in range(self.nbWinningDraw):
            self.validation = False
            self.winningDraw = None
            while not self.validation:
                if ctr > self.maxLoops:
                    if self.qThread:
                        self.qThread.emit(QtCore.SIGNAL("ranOutofLoops()"))
                    return 'Could not generate draw !!'
                self.winningDraw = self._getDraw(wr)
                self._validateDraw()
                if self.qThread:
                    self.qThread.emit(QtCore.SIGNAL("update(int)"), mainCtr)
                ctr += 1
                mainCtr += 1

            self.validation = False
            ctr = 0

            if self.winningDraw not in allGen:
                allGen.append(self.winningDraw)

        self.gen = allGen

        if self.qThread:
            self.qThread.emit(QtCore.SIGNAL("finished()"))

        return self.output()

    def output(self):
        op = Output(
                        isMax=self.isMax,
                        rowsInATicket=self.rowsInATicket,
                        logAnatomy=self.logAnatomy,
                        forcedNumbers=self.forcedNumbers,
                        extraFileName=self.extraFileName,
                        applyDrawSum=self.applyDrawSum,
                        applyDigitSum=self.applyDigitSum,
                        applyEvens=self.applyEvens,
                        applyLows=self.applyLows,

                   )

        self.outStr, self.outStrDisp = op._makeOutPutString(self.gen)

        if self.write:
            p = os.path.join(self.writeDirPath, op._getFileName())
            f = open(p, 'w')
            f.write(self.outStr)
            f.close()

        return self.outStrDisp

if __name__ == '__main__':
    s = time.time()
    ma = MainAlgorithm(lottoIsMax=False, nbTickets=2, write=True)
    ma.runAlg()
    print 'ran in %s seconds . . . ' % (time.time() - s)
