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
 
class FibSpaceFill:
    def __init__(self, outputFile):
        self.canvasWidth = 1000
        self.canvasHeight = 1000

        self.background = "rgb(" + str(53) + "," + str(53) + "," + str(53) + ")"
        
        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='tiny')
        self.dwg.set_desc(title='Fib Modulo, DHP 2015', desc='')
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=self.background, stroke='none'))
            
    def generate(self):
        border = 50
        
        imageWidth = self.canvasWidth - 2*border
        imageHeight = self.canvasHeight - 2*border

        while True:
            value = fib().next()
            
            row = value / imageWidth
            x = value - row*imageWidth + border
            y = row + border
            
            if row > imageHeight:
                break
            
            self.dwg.add(self.dwg.rect(insert=(x, y), size=(1, 1), fill='white', stroke='none'))

        # signature
        self.dwg.add(self.dwg.text("dhp 2015", x=[(self.canvasWidth-140)], y=[(self.canvasHeight-28)], font_size=24, fill='grey'))
            
        self.dwg.save()
        
if __name__ == "__main__":
    output_file = './images/fib_space_fill.svg'
    fib_space_fill = FibSpaceFill(output_file)
    fib_space_fill.generate()
    
    os.system('"C:\Program Files\Inkscape\inkscape.exe" -z -e %s -w %d -h %d %s' % ('./images/fib_space_fill.png', fib_space_fill.canvasWidth, fib_space_fill.canvasHeight, output_file))
        