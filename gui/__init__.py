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

SPN_BX_RANGE = {
                'drsm_spnbx_min': (21, 28),
                'drsm_spnbx_max': (279, 322),
                'dgsm_spnbx_min': (21, 28),
                'dgsm_spnbx_max': (63, 70),
               }


DEF_SETTING = {
                'drsmMin' : (125, 140),
                'drsmMax' : (170, 210),
                'dgsmMin' : (38, 38),
                'dgsmMax' : (60, 60),
                'nbEvens' : ([2, 3, 4], [3, 4, 5]),
                'nbLows' : ([3], [4]),
              }


NO_PATH_STRING = '        < using no path >'

NO_NUM_STRING = '    < no numbers selected >'

RADIO_BTN = ['Last Six Months', 'All Months', 'Both']


DEF_RULES = {
                'drsmRule': True,
                'dgsmRule' : False,
                'evensRule': True,
                'lowsRule': False
            }