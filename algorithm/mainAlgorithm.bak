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
import time
import random

from settings import Settings
from scrap import ScrapLottoData
from randomGenerator import WeightedRandomGenerator
from  output import Output


class MainAlgorithm(Settings):
    def __init__(self, * args, **kwargs):
        super(MainAlgorithm, self).__init__(*args, **kwargs)
        self.sm = None
        self.dsm = None
        self.nbEven = None
        self.nbLow = None
        self.validation = False
        self.gen = None
        self.nbSevenJumps = 0

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

        for k,v in rowsJumpData.iteritems():
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
        op = not self.isMax
        rules = self.rules
        SR_S = rules['SR_S'][op]
        SR_E = rules['SR_E'][op]
        DSR_S = rules['DSR_S'][op]
        DSR_E = rules['DSR_E'][op]
        NB_EVENS = rules['NB_EVENS'][op]
        NB_LOWS = rules['NB_LOWS'][op]

        self._setDrawAnatomy()
        rule1 = SR_S <= self.sm <= SR_E
        rule2 = self.nbEven in NB_EVENS
        rule3 = self.nbLow in NB_LOWS
        rule4 = DSR_S <= self.dsm <= DSR_E

        if self.doSevenJumps:
            rule5 = self.nbSevenJumps>0
        else:
            rule5 = self.nbSevenJumps==0

        self.validation =  rule1 and rule2 and rule5

    def runAlg(self):
        lottoData = None
        if not self.useAtmosphericNoise:
            ld = ScrapLottoData(url=self.url, scrapType=self.scrapType)
            lottoData = ld.getLottoData()

        wr = WeightedRandomGenerator(lottoData)

        allGen = []
        for k in range(self.nbWinningDraw):
            self.validation = False
            self.winningDraw = None
            while not self.validation:
                self.winningDraw = self._getDraw(wr)
                self._validateDraw()

            self.validation = False

            if self.winningDraw not in allGen:
                allGen.append(self.winningDraw)

        self.gen = allGen
        self.output()

    def output(self):
        op = Output(isMax=self.isMax, rowsInATicket=self.rowsInATicket, logAnatomy=self.logAnatomy,
                    forcedNumbers=self.forcedNumbers, extraFileName=self.extraFileName)
        self.outStr, self.outStrDisp = op._makeOutPutString(self.gen)

        if self.display:
            print self.outStrDisp

        if self.write:
            outDir = os.path.join(self.writeDirPath, "output")
            if not os.path.exists(outDir):
                os.mkdir(outDir)

            p = os.path.join(outDir, op._getFileName())
            f = open(p, 'w')
            f.write(self.outStr)
            f.close()

if __name__ == '__main__':
    s = time.time()
    ma = MainAlgorithm(lottoIsMax=False, nbTickets=2, write=True)
    ma.runAlg()
    print 'ran in %s seconds . . . ' % (time.time() - s)
