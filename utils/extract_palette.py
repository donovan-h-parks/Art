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
Draw an imperfect square.
"""

__author__ = 'Donovan Parks'
__copyright__ = 'Copyright 2015'
__credits__ = ['Donovan Parks']
__license__ = 'GPL3'
__version__ = '1.0.0'
__maintainer__ = 'Donovan Parks'
__email__ = 'donovan.parks@gmail.com'
__status__ = 'Development'

import random

import svgwrite
from svgwrite import cm, mm  

import numpy as np
from PIL import Image

class ExtractPalette:
    def __init__(self):
        pass
        
    def run(self, image, output):
        """Extract palette from image."""
        
        image = Image.open(image)
        pixels = image.load()
        
        # get unique colors in image
        uniqueColours = set()
        width, height = image.size
        for x in xrange(width):
            for y in xrange(height):
                uniqueColours.add(pixels[x,y])
                
        # filter highly similar colors
        palette = set()
        colourThreshold = 25
        for color in uniqueColours:
            r,g,b = color
            
            bUnique = True
            for pR,pG,pB in palette:
                if abs(pR-r) + abs(pG-g) + abs(pB-b) < colourThreshold:
                    bUnique = False
                    break
                    
            if bUnique:
                palette.add(color)
                
        print 'Unique colors: %d' % len(palette)
        
        # save image
        paletteImage = Image.new('RGB', (len(palette), 1))
        pixels = paletteImage.load()
        
        for i, c in enumerate(palette):
            pixels[i, 0] = c
            
        paletteImage.save(output)

if __name__ == "__main__":
    extractPalette = ExtractPalette()
    extractPalette.run("../data/src_images/HolgerLippmann_IterateIt.jpg","../data/palettes/lippmann.palette.png")