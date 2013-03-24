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

import random
from urllib import FancyURLopener

class WeightedRandomGenerator(object):
    def __init__(self, data=None):
        if data:
            self.data = data
            self.weightsData = {}
            self.weightsArray = []
            self._setWeightsData()
            self._setWeightsArray()

    def _setWeightsData(self):
        for k,v in self.data.iteritems():
            if not self.weightsData.has_key(v):
                self.weightsData[v] = []
            self.weightsData[v].append(k)

    def _setWeightsArray(self):
        self.weightsArray = sorted([k for k in self.weightsData])
        
    def _getWeightedRandom(self):
        rnd = random.random() * sum(self.weightsArray)
        for i, w in enumerate(self.weightsArray):
            rnd -= w
            if rnd < 0:
                return i

    def getRandomNumber(self):
        randomIndex = self._getWeightedRandom()
        nums = self.weightsData[self.weightsArray[randomIndex]]
        randomIndex = random.randint(0, len(nums) - 1)
        random.shuffle(nums)

        return nums[randomIndex]
        
    def getNonWeightedRandom(self):
        return random.randint(1, 49)
        
    def getNaturalRandom(self, min=1, max=49, nbNumbers=6):
        unique = False
        while not unique:
            url_opener = FancyURLopener()
            data = url_opener.open("http://www.random.org/integers/?num=%s&min=%s&max=%s&col=%s&base=10&format=plain&rnd=new" % (nbNumbers, min, max, nbNumbers))
            randList = data.readlines()[0].rstrip('\n').split('\t')
            unique = bool(len(randList) == len(list(set(randList))))
        return sorted([int(i) for i in randList]) 

        
if __name__ == '__main__':
    from scrap import ScrapLottoData
    url = r"http://diffusion.loto-quebec.com/sw3/stats/asp/stats.asp?cProduit=4&pRequest=3&l=1"
    ld = ScrapLottoData(url=url)
    data = ld.getLottoData()
    
    wr = WeightedRandomGenerator(data)
    print wr.weightsArray
    print wr.weightsData
    print wr.getRandomNumber()
    