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
Text fill.
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
 
class Repetition:
    def __init__(self, outputFile):    
        self.canvasHeight = 8 * 300
        self.canvasWidth = 8 * 300

        self.background = "rgb(" + str(53) + "," + str(53) + "," + str(53) + ")"
        
        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='full')
        self.dwg.set_desc(title='Repetition, DHP 2015', desc='')
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=self.background, stroke='none'))
            
    def check_surrounding(self, x, y, bVertical, index):
    
        if bVertical:
            if self.alpha_grid[x-1][y] != None:
                return False
            elif self.alpha_grid[x+1][y] != None:
                return False
            elif index == 0 and self.alpha_grid[x][y-1] != None:
                return False
            elif index == len(self.name)-1 and self.alpha_grid[x][y+1] != None:
                return False
        else:
            if self.alpha_grid[x][y-1] != None:
                return False
            elif self.alpha_grid[x][y+1] != None:
                return False
            elif index == 0 and self.alpha_grid[x-1][y] != None:
                return False
            elif index == len(self.name)-1 and self.alpha_grid[x+1][y] != None:
                return False
                
        return True
    
    def write_name(self, x, y, bVertical, box_size, border):
        offset = int(0.5 * (box_size + 2*border))
        
        start_x = x
        start_y = y
        
        # check if placement if valid
        bValid = True
        for i, ch in enumerate(self.name):
            # check if name overlaps perfectly with an existing name
            if bVertical and self.alpha_grid[x][y] == self.name[0] and self.alpha_grid[x][y+1] == self.name[1]:
                bValid = False
                break
            elif not bVertical and self.alpha_grid[x][y] == self.name[0] and self.alpha_grid[x+1][y] == self.name[1]:
                bValid = False
                break
            
            # check is name aligns properly with existing names
            if self.alpha_grid[x][y] != None and self.alpha_grid[x][y] != ch:
                bValid = False
                break
                
            if self.alpha_grid[x][y] == None:
                # check surrounding
                if not self.check_surrounding(x, y, bVertical, i):
                    bValid = False
                    break
        
            if bVertical:
                y += 1
            else:
                x += 1
                
        if not bValid:
            return False
        
        # write out name
        x = start_x
        y = start_y
        for index, ch in enumerate(self.name):
            x_pos = x * (box_size + 2*border)
            y_pos = y * (box_size + 2*border)
            
            self.dwg.add(self.dwg.rect(insert=(x_pos+border,y_pos+border), size=(box_size,box_size), fill=self.colors[index], stroke='none'))
            self.dwg.add(self.dwg.text(ch, insert=(x_pos+offset, y_pos+offset),
                                                    font_family="Geneva",
                                                    font_size=36,
                                                    font_weight="bold",
                                                    fill=self.background, 
                                                    text_anchor="middle", 
                                                    dominant_baseline="central"))
                                                    #dy=['0.3em'])) #
                                                    
            self.alpha_grid[x][y] = ch

            if bVertical:
                self.vertical_letters.append((x, y, index))
                y += 1
            else:
                self.horizontal_letters.append((x, y, index))
                x += 1
                
        return True
        
    def color_str(self, r, g, b):
        return "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"

    def generate(self):
        self.name = 'REPEAT'
        self.colors = [self.color_str(251,180,174)]
        self.colors.append(self.color_str(179,205,227))
        self.colors.append(self.color_str(204,235,197))
        self.colors.append(self.color_str(179,205,227))
        self.colors.append(self.color_str(222,203,228))
        self.colors.append(self.color_str(254,217,166))
        self.colors.append(self.color_str(222,203,228))
        self.colors.append(self.color_str(254,217,166))
        self.colors.append(self.color_str(255,242,174))
        self.colors.append(self.color_str(229,216,189))
        
        box_size = 48
        border = 1
        
        grid_size = self.canvasHeight / (box_size + border)
        
        self.alpha_grid = [[None]*grid_size for _ in range(grid_size)]
        self.vertical_letters = []
        self.horizontal_letters = []
        
        # draw initial name
        name_count = 0
        while name_count < 40:
            x = random.randint(1, grid_size-len(self.name)-1)
            y = random.randint(1, grid_size-len(self.name)-1)
            bVertical = random.randint(0,1)
            bValid = self.write_name(x, y, bVertical, box_size, border)
            
            if bValid:
                name_count += 1

        # draw names which cross existing names
        name_count = 0
        while name_count < 80:
            # switch orientation
            bVertical = not bVertical

            # pick a random square with a letter, followed by a 
            # random start square around the letter
            if bVertical:
                rand_x, rand_y, index = random.choice(self.horizontal_letters)
                x = rand_x
                y = rand_y - index
            else:
                rand_x, rand_y, index = random.choice(self.vertical_letters)
                x = rand_x - index
                y = rand_y
                
            if x >= 1 and y >= 1 and x < grid_size-len(self.name) and y < grid_size-len(self.name):
                bValid = self.write_name(x, y, bVertical, box_size, border)
            
                if bValid:
                    name_count += 1
      
        # signature
        self.dwg.add(self.dwg.text("dhp 2015", x=[(self.canvasWidth-20)], y=[(self.canvasHeight-20)], font_size=24, fill='grey', text_anchor="end",))
            
        self.dwg.save()
        
if __name__ == "__main__":
    output_file = './images/repetition.svg'
    repetition = Repetition(output_file)
    repetition.generate()
    
    os.system('"C:\Program Files\Inkscape\inkscape.exe" -z -e %s -w %d -h %d %s' % ('./images/repetition.png', repetition.canvasWidth, repetition.canvasHeight, output_file))
        