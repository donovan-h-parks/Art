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
Playing with the concept of 'unnatural' motion.
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
 
class UnnaturalMotion:
    def __init__(self, outputFile):    
        self.canvasWidth = 6 * 300
        self.canvasHeight = 8 * 300

        self.background = "rgb(" + str(53) + "," + str(53) + "," + str(53) + ")"

        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='tiny')
        self.dwg.set_desc(title='Motion, DHP 2015', desc='')
            
    def generate(self):
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=self.background, stroke='none'))
        
        # draw slope
        slope = 5
        border = 0.1*self.canvasWidth
        
        bottomSlope = 0.7*self.canvasHeight + (1.0/slope)*(self.canvasWidth-2*border)
        b = self.dwg.line(start=(border, 0.7*self.canvasHeight), end=(self.canvasWidth-border, bottomSlope), fill='white', stroke_width=8)
        b.stroke(color='white')
        self.dwg.add(b)
       
        # draw circles on ramp
        r = 0.01*self.canvasHeight
        
        xOffset = 0.03
        velocity = 0.03
        acceleration = 0.012
        while(xOffset < 0.9):
            xOffset += velocity
            velocity += acceleration
            
            run = xOffset * (self.canvasWidth - 2*border)
            x = border + run
            y = (0.7*self.canvasHeight - r - 10) + (1.0/slope) * run
        
            c = self.dwg.add(self.dwg.circle(center=(x, y), r=r))
            c.fill(color='white')
            c.stroke(color=self.background, width=3)
            
            rad = math.radians(random.uniform(0,90))
            dx = math.cos(rad)
            dy = math.sin(rad)
        
            b = self.dwg.line(start=(x - dx*r, y - dy*r), end=(x + dx*r, y + dy*r), fill=self.background, stroke_width=4)
            b.stroke(color=self.background)
            self.dwg.add(b)
            
        # draw single falling circle
        # x = position of circle at bottom of ramp
        y = bottomSlope+2*r
        c = self.dwg.add(self.dwg.circle(center=(x, y), r=r))
        c.fill(color='white')
        c.stroke(color=self.background, width=3)

        dx = 1
        dy = 0
        b = self.dwg.line(start=(x - dx*r, y - dy*r), end=(x + dx*r, y + dy*r), fill=self.background, stroke_width=4)
        b.stroke(color=self.background)
        self.dwg.add(b)
        
        # signature
        self.dwg.add(self.dwg.text("dhp 2015", x=[(self.canvasWidth-140)], y=[(self.canvasHeight-28)], font_size=24, fill='grey'))
            
        self.dwg.save()
        
if __name__ == "__main__":
    output_file = './images/unnatural_motion.svg'
    unnatural_motion = UnnaturalMotion(output_file)
    unnatural_motion.generate()
    
    os.system('"C:\Program Files\Inkscape\inkscape.exe" -z -e %s -w %d -h %d %s' % ('./images/unnatural_motion.png', unnatural_motion.canvasWidth, unnatural_motion.canvasHeight, output_file))
        