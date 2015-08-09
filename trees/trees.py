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
Lines and red circles defined by a generative grammar.
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
 
class Trees:
    def __init__(self, outputFile):    
        self.canvasWidth = 20 * 300
        self.canvasHeight = 20 * 300
        
        self.lineHeight = self.canvasWidth / 3.0
        self.lineThickness = self.lineHeight / 5.0
        self.lineSpacing = self.lineThickness / 2.0

        self.background = "rgb(" + str(255) + "," + str(255) + "," + str(255) + ")"

        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='tiny')
        self.dwg.set_desc(title='Four lines, DHP 2015', desc='')
        
    def branch(self, x, y, length, angle, depth):
        if depth == self.maxDepth:
            return

        rad = math.radians(angle)
        dx = math.cos(rad)
        dy = math.sin(rad)
        
        b = self.dwg.line(start=(x, y), end=(x + dx*length, y + dy*length), fill='black', stroke_width=10)
        b.stroke(color='black')
        self.dwg.add(b)
            
        num_braches = 3 #random.randint(2,4)
        for b in xrange(num_braches):
            offset = random.uniform(0.1, 0.9) * length
            self.branch(x + dx*offset, 
                            y + dy*offset, 
                            length*0.7, 
                            angle + random.randint(-60, 60), 
                            depth+1)
            
    def generate(self):
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=self.background, stroke='none'))

        self.maxDepth = 5
        self.branch(self.canvasWidth / 2.0, self.canvasHeight / 2.0, self.canvasWidth * 0.10, 30.0, 0)
        self.branch(self.canvasWidth / 2.0, self.canvasHeight / 2.0, self.canvasWidth * 0.10, 150.0, 0)
        self.branch(self.canvasWidth / 2.0, self.canvasHeight / 2.0, self.canvasWidth * 0.10, 270.0, 0)

        self.dwg.save()
        
if __name__ == "__main__":
    for i in xrange(0, 1):
        output_file = './images/cherry_tree.still_%d.svg' % (i+1)
        trees = Trees(output_file)
        trees.generate()
        
        os.system('"C:\Program Files\Inkscape\inkscape.exe" -z -e %s -w %d -h %d %s' % ('./images/cherry_tree.still_%d.png' % (i+1), 
                                                                                            trees.canvasWidth, 
                                                                                            trees.canvasHeight, 
                                                                                            output_file))
