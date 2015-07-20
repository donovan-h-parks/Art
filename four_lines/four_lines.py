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
 
class FourLines:
    def __init__(self, outputFile):    
        self.canvasWidth = 20 * 300
        self.canvasHeight = 20 * 300
        
        self.lineHeight = self.canvasWidth / 3.0
        self.lineThickness = self.lineHeight / 5.0
        self.lineSpacing = self.lineThickness / 2.0

        self.background = "rgb(" + str(255) + "," + str(255) + "," + str(0) + ")"

        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='tiny')
        self.dwg.set_desc(title='Four lines, DHP 2015', desc='')
            
    def generate(self):
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=self.background, stroke='none'))

        x0 = 0.5 * (self.canvasWidth - 4 * self.lineThickness  - 3 * self.lineSpacing)
        y0 = 0.5 * (self.canvasHeight - self.lineHeight)
        
        offset = self.lineThickness + self.lineSpacing

        self.dwg.add(self.dwg.rect(insert=(x0, y0), size=(self.lineThickness, self.lineHeight), fill='black'))
        self.dwg.add(self.dwg.rect(insert=(x0 + offset, y0), size=(self.lineThickness, self.lineHeight), fill='black'))
        #self.dwg.add(self.dwg.rect(insert=(x0 + 2*offset, y0 + self.lineHeight*0.15), size=(self.lineThickness, self.lineHeight), fill='black'))
        
        #rect = self.dwg.rect(insert=(x0 + 2*offset, y0), size=(self.lineThickness, self.lineHeight), fill='black')
        #rect.rotate(-7.5, (x0 + 2*offset + self.lineThickness/2.0, y0+self.lineHeight/2.0))
        #self.dwg.add(rect)
        
        #self.dwg.add(self.dwg.rect(insert=(x0 + 2*offset + 0.5 * self.lineSpacing, y0), size=(self.lineThickness, self.lineHeight), fill='black'))
        
        self.dwg.add(self.dwg.rect(insert=(x0 + 2*offset, y0), size=(self.lineThickness, self.lineHeight), fill='grey'))
        
        # still 3: self.dwg.add(self.dwg.rect(insert=(x0 + 2*offset, y0), size=(self.lineThickness, self.lineHeight), fill='black'))
        #self.dwg.add(self.dwg.rect(insert=(x0 + 2*offset - 0.25*self.lineThickness, y0), size=(self.lineThickness*1.5, self.lineHeight), fill='black'))
        self.dwg.add(self.dwg.rect(insert=(x0 + 3*offset, y0), size=(self.lineThickness, self.lineHeight), fill='black'))
            
        self.dwg.save()
        
if __name__ == "__main__":
    output_file = './images/four_lines.still_2_4.svg'
    fourLines = FourLines(output_file)
    fourLines.generate()
    
    os.system('"C:\Program Files\Inkscape\inkscape.exe" -z -e %s -w %d -h %d %s' % ('./images/four_lines.still_2_4.png', fourLines.canvasWidth, fourLines.canvasHeight, output_file))
    
    # create composite image
    border = 0 #int(fourLines.canvasWidth*0.02)
    blank_image = Image.new("RGB", (4*fourLines.canvasWidth + 5*border, fourLines.canvasHeight + 2*border), "white")
    
    img1 = Image.open('./images/four_lines.still_1_3.png')
    img2 = Image.open('./images/four_lines.still_1_1.png')
    img3 = Image.open('./images/four_lines.still_3_3.png')
    img4 = Image.open('./images/four_lines.still_1_4.png')
    
    blank_image.paste(img1, (border, border))
    blank_image.paste(img2, (fourLines.canvasWidth + 2*border, border))
    blank_image.paste(img3, (2*fourLines.canvasWidth + 3*border, border))
    blank_image.paste(img4, (3*fourLines.canvasWidth + 4*border, border))

    blank_image.save("./images/four_lines.composition.png")
        