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

import time

class Output(object):
    def __init__(self, **kwargs):
        self.isMax=False
        if 'isMax' in kwargs:
            self.isMax = kwargs['isMax']

        self.rowsInATicket = 1
        if 'rowsInATicket' in kwargs:
            self.rowsInATicket = kwargs['rowsInATicket']

        self.logAnatomy = False
        if 'logAnatomy' in kwargs:
            self.logAnatomy = kwargs['logAnatomy']

        self.extraFileName = ''
        if 'extraFileName' in kwargs:
            self.extraFileName = kwargs['extraFileName']

        self.forcedNumbers = []
        if 'forcedNumbers' in kwargs:
            self.forcedNumbers = kwargs['forcedNumbers']

    def _getDrawSum(self, inDraw):
        return sum(inDraw)

    def _getNbEvens(self, inDraw):
        return len([n for n in inDraw if n%2 == 0])

    def _getSevenJumps(self, inDraw):
        nbSevenJumps = 0
        rows = [([(i + 1) + (7 * j) for j in range(7)]) for i in range(7)]
        rowsJumpData = dict([(i + 1, 0)for i in range(7)])

        for n in inDraw:
            for index, r in enumerate(rows):
                if n in r:
                    rowsJumpData[index+1] += 1

        for k,v in rowsJumpData.iteritems():
            if v > 1:
                nbSevenJumps += 1

        return nbSevenJumps

    def _getForcedNumbersInDraw(self, inDraw):
        return [n for n in self.forcedNumbers if n in inDraw]

    def _makeOutPutString(self, inGenerated):
        ctr = 1
        outStr = ''
        outStrDisp = ''
        nbDashes = (22 + (4 * int(self.isMax)))

        for index, winningDraw in enumerate(inGenerated):
            if index%self.rowsInATicket == 0:
                outStr += 'Ticket %02d\n'%ctr
                outStr += '-' * nbDashes
                outStr += '\n'

                outStrDisp += 'Ticket %02d\n'%ctr
                outStrDisp += '-' * (nbDashes + 10)
                outStrDisp += '\n'

                ctr += 1

            outStr += '%s\n'%', '.join([str('%02d'%n) for n in sorted(winningDraw)])
            outStrDisp += '%s\n'%', '.join([str('%02d'%n) for n in sorted(winningDraw)])
            if self.logAnatomy:
                outStrDisp += 'Sum : %s, ' % self._getDrawSum(winningDraw)
                outStrDisp += 'Evens : %s\n' % self._getNbEvens(winningDraw)
                outStrDisp += 'nbSeven Jumps : %s\n' % self._getSevenJumps(winningDraw)
                outStrDisp += 'Forced Numbers : %s\n' % self._getForcedNumbersInDraw(winningDraw)

                if self.isMax:
                    outStr += '-' * nbDashes
                    outStr += '\n'

                    outStrDisp += '-' * (nbDashes + 10)
                    outStrDisp += '\n'


            if index%self.rowsInATicket == (self.rowsInATicket - 1):
                outStr += '-' * nbDashes
                outStr += '\n'
                outStr += '\n'

                outStrDisp += '-' * (nbDashes + 10)
                outStrDisp += '\n'
                outStrDisp += '\n'

        return outStr, outStrDisp

    def _getTimeStamp(self):
        t = time.asctime()
        return '_'.join(t.split()[:-2] + t.split()[-1:] + ['h'] + time.asctime().split()[3].split(":"))

    def _getFileName(self):
        tp = ('Max' if self.isMax else '649')
        extraFileName = ('%s_' % self.extraFileName if self.extraFileName else '')
        return '%sLotto_%s_Winning_Ticket_%s.txt' % (extraFileName, tp, self._getTimeStamp())
