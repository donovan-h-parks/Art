#!/usr/bin/env python

###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

"""
Draw a perfect polygon.
"""

__author__ = 'Donovan Parks'
__copyright__ = 'Copyright 2014'
__credits__ = ['Donovan Parks']
__license__ = 'GPL3'
__version__ = '1.0.0'
__maintainer__ = 'Donovan Parks'
__email__ = 'donovan.parks@gmail.com'
__status__ = 'Development'

import svgwrite
from svgwrite import cm, mm  

dwg = svgwrite.Drawing(filename='perfect_polygon.svg', size=(100, 100), profile='tiny')
polygon = dwg.add(dwg.polygon())
polygon.fill(color='blue', opacity=0.5)

lineColor = "rgb(" + str(255) + "," + str(0) + "," + str(0) + ")"
polygon.stroke(color=lineColor, width=3, opacity=0.2)
polygon.points.extend([(30,30),(50,20),(70,30),(80,50),(70,70),(50,80),(30,70),(20,50)])
dwg.save()