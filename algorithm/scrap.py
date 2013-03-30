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

from BeautifulSoup import BeautifulSoup
import urllib2
import re

class ScrapLottoData(object):
    def __init__(self, **kwargs):
        self.url = None
        if 'url' in kwargs:
            self.url = kwargs['url']

        # Scrap Type 0 : Last Six months
        # Scrap Type 1 : All Months
        # Scrap Type 2 : Last Six Months * All Months

        self.scrapType = 0
        if 'scrapType' in kwargs:
            self.scrapType = kwargs['scrapType']

        self.webData = None
        self.rawData = None
        self.totalDraws = None
        self.sixMonthsData = None
        self.allMonthsData = None
        self.sixMonthsDict = None
        self.allMonthsDict = None
        self.lottoData = {}
        self.sixMonthsWeightBias = 0.5

        if not self._checkConnection():
            raise Exception('Internet Connection is not available !')


        self._preProcessData()

    def _checkConnection(self):
        try:
            response=urllib2.urlopen('http://www.google.com',timeout=1)#'http://74.125.113.99',timeout=1) # pinging google.com
            return True
        except urllib2.URLError as err:pass
        return False


    def _setWebData(self):
        try:
            self.webData = urllib2.urlopen(self.url).read()
        except:
            raise Exception("Could not open the url : %s" % self.url)

    def _atoi(self, inStr=""):
        inStr = (inStr.replace(',', '') if ',' in inStr else inStr)
        inStr = ''.join(inStr.split())
        return int(inStr)

    def _atof(self, inStr=""):
        inStr = (inStr.replace(',', '') if ',' in inStr else inStr)
        inStr = ''.join(inStr.split())
        return float(inStr)

    def _setRawData(self):
        soup = BeautifulSoup(self.webData)
        self.rawData = [int(re.search('\d{1,4}',str(t)).group(0)) for t in soup.findAll("td", "STATSNUMS")]

        nbCurrentDrawsRawString,  nbTotalDrawsRawString = [str(t) for t in soup.findAll("td", "entete_stats1")]
        self.nbCurrentDraws = self._atof(re.search(r'Past six months: <b>(\S+)', nbCurrentDrawsRawString).group(1))
        self.nbTotalDraws = self._atof(re.search(r'Since the start: <b>(\S+)', nbTotalDrawsRawString).group(1))

    def _setSixMonthsData(self):
        self.sixMonthsData = [n for i, n in enumerate(self.rawData) if i < 147 ]

    def _setSixMonthsDict(self):
        self.sixMonthsDict = dict(zip([n for i, n in enumerate(self.sixMonthsData) if i%3==0], [n for i, n in enumerate(self.sixMonthsData) if i%3==1]))

    def _setAllmonthsData(self):
        self.allMonthsData = [n for i, n in enumerate(self.rawData) if i >= 147 ]

    def _setAllMonthsDict(self):
        self.allMonthsDict = dict(zip([n for i, n in enumerate(self.allMonthsData) if i%3==0], [n for i, n in enumerate(self.allMonthsData) if i%3==1]))

    def _preProcessData(self):
        self._setWebData()
        self._setRawData()
        self._setSixMonthsData()
        self._setSixMonthsDict()
        self._setAllmonthsData()
        self._setAllMonthsDict()
        self._setLottoData()

    def _setLottoData(self):

        for k, v in self.sixMonthsDict.iteritems():
            if not self.lottoData.has_key(k):
                self.lottoData[k] = 0
            if self.scrapType==0:
                self.lottoData[k] = self.sixMonthsDict[k]
            elif self.scrapType==1:
                self.lottoData[k] = self.allMonthsDict[k]
            elif self.scrapType==2:
                self.lottoData[k] = self.sixMonthsDict[k]  * self.allMonthsDict[k]
            else:
                raise Exception("Don't know how to handle scrap type == %s !!!" % self.scrapType)


        return self.lottoData

    def getLottoData(self):
        return self.lottoData

if __name__ == '__main__':
    URL_LOTTO_649 = r"http://diffusion.loto-quebec.com/sw3/stats/asp/stats.asp?cProduit=4&pRequest=3&l=1"
    URL_LOTTO_MAX = r"http://diffusion.loto-quebec.com/sw3/stats/asp/stats.asp?cProduit=38&pRequest=3&l=1"
    URL_QUEBEC_649 = r"http://diffusion.loto-quebec.com/sw3/stats/asp/stats.asp?cProduit=5&pRequest=3&l=1"

    ld = ScrapLottoData(url=URL_LOTTO_649)
    #smd = ld.sixMonthsDict

    #print smd
    print ld.getLottoData()
    #d = {}
    #for k, v in smd.iteritems():
    #    if not d.has_key(v):
    #        d[v] = []
    #
    #    d[v].append(k)
    #d = sorted(d)
    #d.reverse()
    #
    #midIndex = (((len(d) / 2)) - 1 if len(d)%2==0 else (((len(d) + 1) / 2)) - 1)
    #mid = d[midIndex]
    #print d
    #print mid