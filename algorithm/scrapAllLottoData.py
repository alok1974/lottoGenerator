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

from BeautifulSoup import BeautifulSoup
import urllib2
import re

import matplotlib.pyplot as plt
# Set Lotto Type
# 0 : Lotto Max
# 1 : Lotto 649
# 2 : Lotto Quebec 649
LOTTO_TYPE = 1
# Set Start and End Years
START_YEAR = 2010
END_YEAR = 2012

PRODUCT = {0: ('max', 38, 7), 1: ('649', 4, 6), 2: ('quebec49', 5, 6)}


def _writeHeader():
    s = ''
    s += '-' * 45
    s += '\n'
    s += 'Data for Lotto %s, ' % PRODUCT[LOTTO_TYPE][0].capitalize()
    s += 'From: %s  To: %s\n' % (START_YEAR, END_YEAR)
    s += '-' * 45
    s += '\n'

    return s

def _getAllLottoData():
    if END_YEAR < START_YEAR:
        raise Exception('End Year is less than the Start Year')

    allData = {}

    data = _writeHeader()

    newLine = PRODUCT[LOTTO_TYPE][2] + 1

    places = [[], [] , [], [], [], [], []]

    sumsData = {}

    totalYears = END_YEAR - START_YEAR + 1
    for i in range(totalYears):

        yr = str(i + START_YEAR)

        url = r"http://diffusion.loto-quebec.com/sw3/res/asp/index.asp?l=1&pVertige=0&pRequest=11&cProduit=%s&pMois=0&pAnnee=%s&x=112&y=12" % (PRODUCT[LOTTO_TYPE][1], yr)

        try:
            webData = urllib2.urlopen(url).read()
        except:
            raise Exception('No connection or web page does not exists')

        soup = BeautifulSoup(webData)

        if len([(re.search('No results available for this lottery for the dates selected.', str(t)).group(0)) for t in soup.findAll("i")]) > 0:
            data += '\n\nNo results available for lottery for year %s\n\n' % yr
            continue

        dateData = [re.search('>(\S+)<',str(t)).group(1) for t in soup.findAll("td", "stats_date")]
        rawData = [int(re.search('\d{1,2}',str(t)).group(0)) for t in soup.findAll("u")]

        if len(dateData) != len(rawData) / float(newLine):
            data += '\n\nData lists unequal for year %s, maybe due to max millions draw details on other page.\n \n' % yr
            continue

        data += ':%s:\n' % yr
        sm = 0
        j = newLine - 2

        sums = []

        for i, d in enumerate(rawData):

            places[i%newLine].append(d)

            if i == 0:
                data += '%s   ' % dateData[0]


            data += '%02d' % d
            sm += d

            if i == j:
                data += ' ('
                j += newLine

            elif (i+1)%newLine==0 and i!=0:
                sm -= d
                data += ')         %s\n' % sm
                sums.append(sm)
                sm = 0

            else:
                data += ', '

            if (i+1)%newLine==0 and i != len(rawData) - 1:
                data += '%s   ' % dateData[(i / newLine) + 1]

        sumsData[yr] = sums
    return data, places, sumsData

def _getMeanModeMedianOfSums():
    data, places, sums =  _getAllLottoData()

    mean = {}
    mode = {}
    median = {}
    allMean = 0
    allMode = 0
    allMedian = 0

    allSums = []
    for y, s in sums.iteritems():
        mean[y] = sum(s) / len(s)

        if len(s)%2==1:
            index = ((len(s) + 1) / 2) - 1
            median[y] = sorted(s)[index]
        else:
            highIndex = len(s) / 2
            median[y] = ((s[highIndex - 1]) + (s[highIndex])) / 2

        modeDict = {}
        for n in s:
            if not modeDict.has_key(n):
                modeDict[n] = 0

            modeDict[n] += 1

        maxModeTupleList = [(v, n) for n, v in modeDict.iteritems()]


        mode[y] = max(maxModeTupleList)[1]

    return mean, mode, median


if __name__ == '__main__':
    #pth = os.path.abspath(os.path.join(inspect.getfile(inspect.currentframe()), os.path.pardir))
    #print pth
    #data, places, sums =  _getAllLottoData()

    print _getMeanModeMedianOfSums()
    #print data
    #print places

    #ones = places[4]
    #
    #draw = 1
    #
    #d = [places[0][draw], places[1][draw], places[2][draw], places[3][draw], places[4][draw], places[5][draw], ]
    #
    #plt.plot(d, 'r--')
    ##plt.axis([0, 6, 0, 20])
    #plt.show()
    #
    #dStr = ''
    #for p in places:
    #    dStr += ','.join([str(d) for d in p])
    #    dStr += '\n'
    #
    #f = open(os.path.join(pth, "placesData.txt"), 'w')
    #f.write(dStr)
    #f.close()

    #f = open(os.path.join(pth, "allLottoData.txt"), 'w')
    #f.write(data)
    #f.close()
    #print 'done writing'
