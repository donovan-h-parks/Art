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
Experiments with Fibonacci series.
"""

__author__ = 'Donovan Parks'
__copyright__ = 'Copyright 2015'
__credits__ = ['Donovan Parks']
__license__ = 'GPL3'
__version__ = '1.0.0'
__maintainer__ = 'Donovan Parks'
__email__ = 'donovan.parks@gmail.com'
__status__ = 'Development'

import os
import math
import random

import svgwrite
from svgwrite import cm, mm  

import numpy as np
from PIL import Image

a,b = 0,1
def fib():
    global a,b
    while True:
        a,b = b, a+b
        yield a

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def list(self):
        return (self.x, self.y)
 
class FibModulo:
    def __init__(self):    
        self.canvasHeight = 8 * 300

        self.background = "rgb(" + str(53) + "," + str(53) + "," + str(53) + ")"
            
    def generate(self, outputFile):
        iterations = 100
        modulo = 6
        series = 1
        
        border = int(0.02*self.canvasHeight)
        spacing = 2
        boxHeight = int((self.canvasHeight - 2*border - (iterations-1)*spacing) / float(iterations))
        
        self.canvasWidth = 2*border + (series-1)*((boxHeight+spacing)*modulo*1.5) + (modulo-1)*boxHeight + (modulo-2)*spacing
        self.canvasWidth = int(2.0*self.canvasWidth)
        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='tiny')
        self.dwg.set_desc(title='Fib Modulo, DHP 2015', desc='')
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=self.background, stroke='none'))
        
        f = fib()
        for s in xrange(series):
            for r in xrange(iterations):
                y = border + boxHeight*r + spacing*r
            
                value = f.next() % modulo
                for c in xrange(0, value):
                    x = border + boxHeight*c + spacing*c + s*((boxHeight+spacing)*modulo*1.5)
                    self.dwg.add(self.dwg.rect(insert=(x,y), size=(boxHeight,boxHeight), fill='white'))
      
        # signature
        self.dwg.add(self.dwg.text("dhp 2015", x=[(self.canvasWidth-140)], y=[(self.canvasHeight-28)], font_size=24, fill='grey'))
            
        self.dwg.save()
        
if __name__ == "__main__":
    output_file = './images/fib_modulo.svg'
    fib_modulo = FibModulo()
    fib_modulo.generate(output_file)
    
    os.system('"C:\Program Files\Inkscape\inkscape.exe" -z -e %s -w %d -h %d %s' % ('./images/fib_modulo.png', fib_modulo.canvasWidth, fib_modulo.canvasHeight, output_file))
        