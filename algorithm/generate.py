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

from mainAlgorithm import MainAlgorithm

def generateTickets():
    lottoIsMax = False
    writeDirPath = r'C:\Users\Alok\Desktop'
    write = True
    logAnatomy = True
    nbTickets = 3
    doSevenJumps = True
    forcedNumbers = []
    nbFromForcedRandom = len(forcedNumbers)
    scrapType = 0

    ma = MainAlgorithm(
                        lottoIsMax=lottoIsMax,
                        writeDirPath=writeDirPath,
                        write=write,
                        scrapType=scrapType,
                        logAnatomy=logAnatomy,
                        nbTickets=nbTickets,
                        doSevenJumps=doSevenJumps,
                        forcedNumbers=forcedNumbers,
                        nbFromForcedRandom=nbFromForcedRandom,
                       )
    s = ma.runAlg()

    print s

if __name__ == '__main__':
    generateTickets()