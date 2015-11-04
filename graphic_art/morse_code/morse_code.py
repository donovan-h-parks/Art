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
Visual representation of morse code.
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

 
class MorseCode:
    def __init__(self):
        # translate to morse code: http://www.unit-conversion.info/texttools/morse-code/
        self.text = "is this art?"
        self.morse_code = ".. ...\t- .... .. ...\t.- .-. - ..--.."
        
        self.background = "rgb(" + str(53) + "," + str(53) + "," + str(53) + ")"
            
    def generate(self, outputFile):
        boxSize = 60
        spacing = 9
        border = boxSize
        
        words = self.morse_code.split('\t')
        numWords = len(words)
        numLetters = sum([1 for word in words for letter in word.split()])
        longestLetter = max([len(letter) for word in words for letter in word.split()])

        self.canvasWidth = numLetters * (boxSize + spacing) + (numWords - 1) * (boxSize + spacing) + 2 * border
        self.canvasHeight = longestLetter * (boxSize + spacing) + 2 * border
        print self.canvasWidth, self.canvasHeight

        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='tiny')
        self.dwg.set_desc(title='Morse Code, DHP 2015', desc='')
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=self.background, stroke='none'))
        
        x = border
        y = self.canvasHeight - border - boxSize
        for word in words:
            for letter in word.split():
                for token in letter:
                    if token == '.':
                        r = self.dwg.add(self.dwg.rect(insert=(x,y), size=(boxSize,boxSize), fill='white'))
                        r.stroke(color='white',width=3,opacity=1.0)
                    else:
                        r = self.dwg.add(self.dwg.rect(insert=(x,y), size=(boxSize,boxSize), fill=self.background))
                        r.stroke(color='white',width=3,opacity=1.0)
                    
                    y -= (boxSize + spacing)
                    
                y = self.canvasHeight - border - boxSize
                x += boxSize + spacing
            x += boxSize + spacing
            
        # signature
        self.dwg.add(self.dwg.text("dhp 2015", x=[(self.canvasWidth-68)], y=[(self.canvasHeight-10)], font_size=12, fill='grey'))
            
        self.dwg.save()
        
if __name__ == "__main__":
    output_file = './images/morse_code.svg'
    morse_code = MorseCode()
    morse_code.generate(output_file)
    
    os.system('"C:\Program Files\Inkscape\inkscape.exe" -z -e %s -w %d -h %d %s' % ('./images/morse_code.png', morse_code.canvasWidth, morse_code.canvasHeight, output_file))
        