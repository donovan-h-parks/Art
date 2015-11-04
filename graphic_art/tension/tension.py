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
Graphic art capturing the notation of weight.
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
 
class Tension:
    def __init__(self, outputFile):    
        self.canvasWidth = 6 * 300
        self.canvasHeight = 8 * 300

        self.background = "rgb(" + str(53) + "," + str(53) + "," + str(53) + ")"

        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='tiny')
        self.dwg.set_desc(title='Tension, DHP 2015', desc='')
            
    def generate(self):
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=self.background, stroke='none'))
        
        # draw posts
        lineX1 = int(0.2*self.canvasWidth)
        lineX2 = int(0.5*self.canvasWidth)
        lineX3 = int(0.8*self.canvasWidth)
        lineY1 = int(0.6*self.canvasHeight)
        lineY2 = int(0.7*self.canvasHeight)
        
        thickness = 4
        for x in [lineX1, lineX2, lineX3]:
            p1 = self.dwg.line(start=(x, lineY1), end=(x, lineY2), fill='white', stroke_width=thickness)
            p1.stroke(color='white')
            self.dwg.add(p1)
        
        # draw trampoline lines
        p = self.dwg.path('m%d,%d' % (lineX2, lineY1))
        rX = 0.5*(lineX2-lineX1)
        rY = 0.8*(lineY2-lineY1)
        p.push_arc(target=(-(lineX2-lineX1), 0), rotation=0, r=(rX,rY))
        p.fill(color=self.background)
        p.stroke(color='white', width=thickness)
        self.dwg.add(p)
        
        t2 = self.dwg.line(start=(lineX2, lineY1+0.5*thickness), end=(lineX3, lineY1+0.5*thickness), fill='white', stroke_width=thickness)
        t2.stroke(color='white')
        self.dwg.add(t2)
        
        # draw circle
        circleR = int(0.02*self.canvasWidth)
        
        y = int(lineY1+0.5*(lineY2-lineY1))
        c1 = self.dwg.add(self.dwg.circle(center=(lineX1 + 0.5*(lineX2-lineX1), lineY1+rY-circleR-0.5*thickness), r=circleR))
        c1.fill(color='white')
        c1.stroke(color='white')
        
        c2 = self.dwg.add(self.dwg.circle(center=(lineX2 + 0.5*(lineX3-lineX2), lineY1-circleR-0.5*thickness), r=circleR))
        c2.fill(color='white')
        c2.stroke(color='white')
        
        # signature
        self.dwg.add(self.dwg.text("dhp 2015", x=[(self.canvasWidth-140)], y=[(self.canvasHeight-28)], font_size=24, fill='grey'))
            
        self.dwg.save()
        
if __name__ == "__main__":
    output_file = './images/tension.svg'
    tension = Tension(output_file)
    tension.generate()
    
    os.system('"C:\Program Files\Inkscape\inkscape.exe" -z -e %s -w %d -h %d %s' % ('./images/tension.png', tension.canvasWidth, tension.canvasHeight, output_file))
        