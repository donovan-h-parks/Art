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
Squares.
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

 
class Squares:
    def __init__(self, outputFile):    
        self.canvasWidth = 6 * 100
        self.canvasHeight = 8 * 100

        self.background = "rgb(" + str(53) + "," + str(53) + "," + str(53) + ")"
        #self.background = "rgb(" + str(255) + "," + str(255) + "," + str(255) + ")"
        
        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='tiny')
        self.dwg.set_desc(title='Squares, DHP 2015', desc='')
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=self.background, stroke='none'))
        
    def rand_bounded(self, mean, std, min, max):
        r = random.gauss(mean, std)
        if r > max:
            r = max
        elif r < min:
            r = min
            
        return r
        
    def getImageColors(self, image):
        """Get list of colors in image."""
        image = Image.open(image)
        pix = image.load()
        
        colors = []
        width, height = image.size
        for x in xrange(width):
            for y in xrange(height):
                r, g, b = pix[x,y]

                # filter out low saturation, dark colors
                if r < 100 and g < 100 and b < 100:
                    continue

                colors.append(pix[x,y])
                
        print 'Colors in palette: %d' % len(colors)
        return colors
            
    def generate(self):
        colors = self.getImageColors('../../data/palettes/aboriginal.palette.png')

        square_size = 20
        border = int(1.5*square_size)
        
        x_offset = int(0.5*square_size)
        x_std = 0.2*square_size
        y_offset = int(0.5*square_size)
        y_std = 0.2*square_size
        
        pts = []
        for y in xrange(border, self.canvasHeight-border+1, y_offset):
            for x in xrange(border, self.canvasWidth-border+1, x_offset):
                cur_x = x - 0.5*square_size + int(self.rand_bounded(0, x_std, -0.2*square_size, 0.2*square_size))
                cur_y = y - 0.5*square_size + int(self.rand_bounded(0, y_std, -0.2*square_size, 0.2*square_size))
                
                pt = (cur_x, cur_y)
                pts.append(pt)
                
        # shuffle points to randomize x-coordinate
        random.shuffle(pts)
        
        # sort by y-coordinate
        pts.sort(key=lambda pt: pt[1])

        for pt in pts:
            rect = self.dwg.add(self.dwg.rect(insert=(pt[0], pt[1]), size=(square_size, square_size), rx=None, ry=None))
            rect.stroke(color='black', width=1)
            
            #r = int(0.3*random.uniform(0,255) + 0.7*255)
            #g = int(0.3*random.uniform(0,255) + 0.7*128)
            #b = int(random.uniform(0,255))
            rndColor = random.choice(colors)
            
            c = "rgb(" + str(rndColor[0]) + "," + str(rndColor[1]) + "," + str(rndColor[2]) + ")"
            rect.fill(color=c)

        # signature
        self.dwg.add(self.dwg.text("dhp 2015", x=[(self.canvasWidth-40)], y=[(self.canvasHeight-7)], font_size=7, fill='grey'))
            
        self.dwg.save()
        
if __name__ == "__main__":
    output_file = './images/squares_color_aboriginal.svg'
    squares = Squares(output_file)
    squares.generate()
    
    os.system('"C:\Program Files\Inkscape\inkscape.exe" -z -e %s -w %d -h %d %s' % ('./images/squares_color_aboriginal.png', squares.canvasWidth, squares.canvasHeight, output_file))
        