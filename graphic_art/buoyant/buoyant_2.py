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
Visual representation of buoyancy #2.
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

 
class Buoyant2:
    def __init__(self, outputFile):
        self.canvasWidth = 6 * 300
        self.canvasHeight = 8 * 300
        
        self.background = "rgb(" + str(53) + "," + str(53) + "," + str(53) + ")"

        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='tiny')
        self.dwg.set_desc(title='Buoyant, DHP 2015', desc='')
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=self.background, stroke='none'))
     
    def boundingBoxCollision(self, boundingBox, boundingBoxes):
        # check if bounding box overlaps with any defined bounding boxes
        left = boundingBox[0]
        right = boundingBox[2]
        top = boundingBox[1]
        bottom = boundingBox[3]
        
        for bb in boundingBoxes:
            separate = (right < bb[0]) or (left > bb[2]) or (top > bb[3]) or (bottom < bb[1])
            if not separate:
                return True

        return False
        
    def generate(self):
    
        lineY = 0.8*self.canvasHeight

        # draw sitting circles
        circleRadius = 30
        numCircles = 10
        
        bounding_buffer = 5
        
        circlesDrawn = 0
        boundingBoxes = []
        while circlesDrawn < numCircles:
            rndCircleRadius = circleRadius + int(random.uniform(-15, 15))
            circleY = lineY - rndCircleRadius + int(random.uniform(0.05*rndCircleRadius, 0.5*rndCircleRadius))
            
            x, y = (int(random.uniform(0.15,0.85)*self.canvasWidth), circleY)
            bb = (x - rndCircleRadius - bounding_buffer, y - rndCircleRadius, x + rndCircleRadius + bounding_buffer, y + rndCircleRadius)
            if not self.boundingBoxCollision(bb, boundingBoxes): 
                self.dwg.add(self.dwg.circle(center=(x, y), r=rndCircleRadius, fill='none', stroke='white', stroke_width=4))
                
                boundingBoxes.append(bb)
                circlesDrawn += 1
        
        x, y = (int(random.uniform(0.3,0.7)*self.canvasWidth), lineY - int(random.uniform(0.3, 0.6)*self.canvasHeight))
        self.dwg.add(self.dwg.circle(center=(x, y), r=circleRadius, fill='none', stroke='white', stroke_width=4))

        # draw line
        b = self.dwg.line(start=(0.1*self.canvasWidth, lineY), end=(0.9*self.canvasWidth, lineY), fill='white', stroke_width=4)
        b.stroke(color='white')
        self.dwg.add(b)
            
        # signature
        self.dwg.add(self.dwg.text("dhp 2015", x=[(self.canvasWidth-140)], y=[(self.canvasHeight-28)], font_size=24, fill='grey'))
            
        self.dwg.save()
        
if __name__ == "__main__":
    output_file = './images/buoyant2.svg'
    buoyant2 = Buoyant2(output_file)
    buoyant2.generate()
    
    os.system('"C:\Program Files\Inkscape\inkscape.exe" -z -e %s -w %d -h %d %s' % ('./images/buoyant2.png', buoyant2.canvasWidth, buoyant2.canvasHeight, output_file))
        