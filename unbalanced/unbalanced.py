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
Experiments with 4 lines.
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
 
class Unbalanced:
    def __init__(self, outputFile):    
        self.canvasWidth = 6 * 300
        self.canvasHeight = 8 * 300

        self.background = "rgb(" + str(53) + "," + str(53) + "," + str(53) + ")"

        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='tiny')
        self.dwg.set_desc(title='Unbalanced, DHP 2015', desc='')
            
    def generate(self):
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=self.background, stroke='none'))
        
        # draw line
        lineWidth = 0.6*self.canvasWidth
        lineOffset = 0.3*self.canvasWidth
        lineX = lineOffset
        lineY = 0.7*self.canvasHeight
        
        b = self.dwg.line(start=(lineX, lineY), end=(lineX + lineWidth, lineY), fill='white', stroke_width=8)
        b.stroke(color='white')
        self.dwg.add(b)
        
        # draw triangle
        triOffset = 0.4*self.canvasWidth
        triHeight = 0.05*self.canvasHeight
        triY = lineY + 0.005*self.canvasHeight
        polygon = self.dwg.add(self.dwg.polygon())
        polygon.points.extend([(triOffset, triY), (triOffset + 0.5*triHeight, triY + triHeight), (triOffset -0.5*triHeight, triY + triHeight)])
        polygon.fill(color='white')
        polygon.stroke(color='white')
        
        # draw circle
        circleR = 0.125*triHeight
        circleX = lineX + lineWidth - 0.05*lineWidth
        circleY = lineY - circleR - 0.01*self.canvasHeight
        c = self.dwg.add(self.dwg.circle(center=(circleX, circleY), r=circleR))
        c.fill(color='white')
        c.stroke(color='white')
        
        # signature
        self.dwg.add(self.dwg.text("dhp 2015", x=[(self.canvasWidth-140)], y=[(self.canvasHeight-28)], font_size=24, fill='grey'))
            
        self.dwg.save()
        
if __name__ == "__main__":
    output_file = './images/unbalanced.svg'
    unbalanced = Unbalanced(output_file)
    unbalanced.generate()
    
    os.system('"C:\Program Files\Inkscape\inkscape.exe" -z -e %s -w %d -h %d %s' % ('./images/unbalanced.png', unbalanced.canvasWidth, unbalanced.canvasHeight, output_file))
        