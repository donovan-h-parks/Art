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
Australian aboriginal pattern.
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
from scipy.spatial import Delaunay
from PIL import Image

 
class Pattern:
    def __init__(self, outputFile):    
        self.canvasWidth = 6 * 300
        self.canvasHeight = 8 * 300

        self.background = "rgb(" + str(255) + "," + str(128) + "," + str(0) + ")"

        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='tiny')
        self.dwg.set_desc(title='aboriginal pattern, DHP 2015', desc='')
        
    def rand_bounded(self, mean, std, min, max):
        r = random.gauss(mean, std)
        if r > max:
            r = max
        elif r < min:
            r = min
            
        return r
            
    def generate(self):
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=self.background, stroke='none'))
        
        bound_offset = 0.1*max(self.canvasWidth, self.canvasHeight)
        min_dist = 0.08*min(self.canvasWidth, self.canvasHeight)
        
        num_points = 100
        points = []
        while len(points) <= num_points:
            new_pt = (random.uniform(-bound_offset, self.canvasWidth+bound_offset), random.uniform(-bound_offset, self.canvasHeight+bound_offset))

            add_point = True
            for pt in points:
                x = pt[0] - new_pt[0]
                y = pt[1] - new_pt[1]
                d = math.sqrt(x*x + y*y)
                if d < min_dist:
                    add_point = False
                    break
               
            if add_point:
                points.append(new_pt)
  
        # plot triangles
        tri = Delaunay(points)
        for pts in tri.points[tri.simplices]:
            p = self.dwg.add(self.dwg.polygon())
            p.points.extend(pts)
            c = "rgb(" + str(int(random.uniform(0,255))) + "," + str(int(random.uniform(0,255))) + "," + str(int(random.uniform(0,255))) + ")"
            p.fill(color=c, opacity=0.3)
            p.stroke(color=None)

            
        # plot lines
        for pts in tri.points[tri.simplices]:
            pt1 = pts[0]
            pt2 = pts[1]
            pt3 = pts[2]
            for a, b in [(pt1, pt2), (pt2, pt3), (pt3, pt1)]:
                line = self.dwg.add(self.dwg.line(start=a, end=b, stroke_width=30))
                line.stroke(color='black', linecap="round")
                    
        # plot points
        for pts in tri.points[tri.simplices]:
            pt1 = pts[0]
            pt2 = pts[1]
            pt3 = pts[2]
            for a, b in [(pt1, pt2), (pt2, pt3), (pt3, pt1)]:
                run = b[0] - a[0]
                rise = b[1] - a[1]
                slope = rise / run
                
                length = math.sqrt(run*run + rise*rise)
                steps = int(length/40.0)
                for i in xrange(1, steps):
                    dx = i*(1.0/steps) * run
                    y = a[1] + slope*dx
                    x = a[0] + dx

                    r_rnd = self.rand_bounded(0, 1.5, -2, 2)
                    x_rnd = self.rand_bounded(0, 1.5, -2, 2)
                    y_rnd = self.rand_bounded(0, 1.5, -2, 2)

                    c = self.dwg.add(self.dwg.circle(center=(x+x_rnd, y+y_rnd), r=8+r_rnd))
                    c.fill(color='white')
                    c.stroke(color=None)
        
        # signature
        #self.dwg.add(self.dwg.text("dhp 2015", x=[(self.canvasWidth-140)], y=[(self.canvasHeight-28)], font_size=24, fill='grey'))
            
        self.dwg.save()
        
if __name__ == "__main__":
    output_file = './images/aboriginal_pattern.svg'
    pattern = Pattern(output_file)
    pattern.generate()
    
    os.system('"C:\Program Files\Inkscape\inkscape.exe" -z -e %s -w %d -h %d %s' % ('./images/aboriginal_pattern.png', pattern.canvasWidth, pattern.canvasHeight, output_file))
        