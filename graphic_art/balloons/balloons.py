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
Balloons
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


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def list(self):
        return (self.x, self.y)
 
class Balloons:
    def __init__(self, outputFile):
        self.canvasWidth = 6 * 100
        self.canvasHeight = 8 * 100

        self.background = "rgb(" + str(53) + "," + str(53) + "," + str(53) + ")"

        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='tiny')
        self.dwg.set_desc(title='Balloons, DHP 2015', desc='')
            
    def generate(self):
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=self.background, stroke='none'))
        
        # draw base
        slope = 5

        x1 = 0.15*self.canvasWidth
        x2 = 0.55*self.canvasWidth
        dx = x2-x1
        
        y1 = 0.25*self.canvasHeight
        y2 = y1 + (1.0/slope)*dx
        
        b = self.dwg.add(self.dwg.line(start=(x1, y1), end=(x2, y2), fill='white', stroke_width=6))
        b.stroke(color='white')
        
        # draw large balloon
        ballon_height = 0.3*dx
        
        r = 0.08*dx
        
        xOffset = 0.1 * dx
        cx = x1 + xOffset
        cy = y1 + (1.0/slope) * xOffset - ballon_height

        b = self.dwg.add(self.dwg.line(start=(cx, cy), end=(cx, cy + ballon_height), fill='white', stroke_width=1))
        b.stroke(color='white')

        c = self.dwg.add(self.dwg.circle(center=(cx, cy), r=r))
        c.fill(color=self.background)
        c.stroke(color='white', width=1)
        
        # draw large balloon
        r = 0.05*dx
        
        xOffset = 0.9 * dx
        cx = x1 + xOffset
        cy = y1 + (1.0/slope) * xOffset - ballon_height
        
        b = self.dwg.add(self.dwg.line(start=(cx, cy), end=(cx, cy + ballon_height), fill='white', stroke_width=1))
        b.stroke(color='white')

        c = self.dwg.add(self.dwg.circle(center=(cx, cy), r=r))
        c.fill(color=self.background)
        c.stroke(color='white', width=1)
        
        # signature
        self.dwg.add(self.dwg.text("dhp 2015", x=[(self.canvasWidth-40)], y=[(self.canvasHeight-7)], font_size=7, fill='grey'))
            
        self.dwg.save()
        
if __name__ == "__main__":
    output_file = './images/balloons.svg'
    balloons = Balloons(output_file)
    balloons.generate()
    
    os.system('"C:\Program Files\Inkscape\inkscape.exe" -z -e %s -w %d -h %d %s' % ('./images/balloons.png', balloons.canvasWidth, balloons.canvasHeight, output_file))
        