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

import random
#649
#l = [   22, 37, 17, 20, 5, 8, 36, 1, 4, 14, 24, 29, 32,
##        35, 6, 7, 12, 15, 19, 21, 26, 34, 38, 40, 44,
#        45, 18, 27, 47, 2, 31, 43, 46, 41, 23, 42, 9, 39, 49, 3, 30, 33]
#
#rs = 135
#re = 165
#nbNumbers = 6

#max
l = [2, 27, 1, 20, 33, 47, 5, 22, 26, 37, 44, 3, 7, 8, 12, 13, 18, 30, 35, 46,
48, 9, 10, 11, 14, 19, 23, 28, 24, 39, 25, 29, 6, 17, 32, 4, 15]

rs = 140
re = 210

nbNumbers = 7

#random.shuffle(l)
f = False
while not f:
    d = []
    for i in range(nbNumbers):
        index = random.randint(0, len(l)- 1)
        n = l[index]

        while n in d:
            index = random.randint(0, len(l)- 1)
            n = l[index]

        d.append(l[index])

        s = sum(d)

        if rs < s < re:
            print s
            f = True

print sorted(d)
