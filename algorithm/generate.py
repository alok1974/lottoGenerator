# Algorithm to generate Canada Lotto Tickets
# Author: Alok Gandhi

#######################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################
from alg import MainAlgorithm

def generateTickets():
    lottoIsMax = False
    writeDirPath = r'C:\Users\Alok\Desktop'
    display = True
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
                        display=display,
                        write=write,
                        scrapType=scrapType,
                        logAnatomy=logAnatomy,
                        nbTickets=nbTickets,
                        doSevenJumps=doSevenJumps,
                        #forcedNumbers=forcedNumbers,
                        #nbFromForcedRandom=nbFromForcedRandom,
                       )
    ma.runAlg()

if __name__ == '__main__':
    generateTickets()
