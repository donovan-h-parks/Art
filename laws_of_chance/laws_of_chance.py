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
Draw imperfect squares as inspired by Arp's 'Collage arranged according to the laws of chance'.
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
 
class LawsOfChance:
    def __init__(self, outputFile):    
        self.canvasWidth = 10 * 300
        self.canvasHeight = 14 * 300
        self.border = int(self.canvasWidth * 0.05)
        
        self.numPolygons = 15
        self.minLength = self.canvasWidth * 0.1
        self.maxLength = self.canvasWidth * 0.35
        
        self.warm = [(254,224,210),(252,146,114),(222,45,38)]
        self.cold = [(222,235,247), (158,202,225), (49,130,189)]
        self.greyscale = [(240,240,240), (189,189,189), (99,99,99)]
        
        self.palette = self.warm

        self.background = "rgb(" + str(self.palette[0][0]) + "," + str(self.palette[0][1]) + "," + str(self.palette[0][2]) + ")"

        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='tiny')
        self.dwg.set_desc(title='Laws of Chance, DHP 2015', desc='Generative art inspired by Jean Arp.')
        
    def fractalLine(self, iterations=8):
        """Generate points along a fractal line."""

        minRatio = 0.33
        minY = 1
        maxY = 1

        pointList = []
        pointList.append(Point(0.0, 1.0))
        pointList.append(Point(1.0, 1.0))
        for i in xrange(0, iterations):
            newPointList = []
            for j in xrange(0, len(pointList)-1):
                pt = pointList[j]
                nextPt = pointList[j+1]
                
                newPointList.append(pt)
                
                ratio = random.uniform(minRatio, 2 * minRatio)

                newX = pt.x + ratio*(nextPt.x - pt.x)

                # find distance to closest point
                dx = min(newX - pt.x, nextPt.x - newX)

                # create new point
                newY = pt.y + ratio*(nextPt.y - pt.y);
                newY += dx * random.uniform(-1, 1);

                # track upper and lower bounds
                maxY = max(newY, maxY)
                minY = min(minY, newY)

                # add new point
                newPointList.append(Point(newX, newY))
                
            pointList = newPointList
            pointList.append(Point(1.0, 1.0))

        # normalize to values between 0 and 1
        if maxY != minY:
            normalizeRate = 1.0 / (maxY - minY)
            for pt in pointList:
                pt.y = normalizeRate * (pt.y - minY)
        else:
            # max = min, so set all points equal to 1
            for pt in pointList:
                pt.y = 1

        return pointList
                
    def drawImperfectPolygon(self, x0, y0, 
                                    w, h, 
                                    r, g, b, 
                                    cornerDrift=3,
                                    drawDriftX=3,
                                    drawDriftY=3,
                                    rotation=0,
                                    iterations=8):
        """Draw imperfect polygon with fractal fill."""
        
        # generate imperfect polygon
        corner = []
        corner.append(Point(x0 + cornerDrift*random.uniform(-1, 1), y0 + cornerDrift*random.uniform(-1, 1)))
        corner.append(Point(x0 + w + cornerDrift*random.uniform(-1, 1), y0 + cornerDrift*random.uniform(-1, 1)))
        corner.append(Point(x0 + w + cornerDrift*random.uniform(-1, 1), y0 + h + cornerDrift*random.uniform(-1, 1)))
        corner.append(Point(x0 + cornerDrift*random.uniform(-1, 1), y0 + h + cornerDrift*random.uniform(-1, 1)))

        driftVector = []
        driftVector.append(Point(0, drawDriftY))
        driftVector.append(Point(drawDriftX, 0))
        driftVector.append(Point(0, drawDriftY))
        driftVector.append(Point(drawDriftX, 0))
        
        points = [corner[0].list()]
        for i in xrange(0, 4):
            nextCorner = corner[(i + 1) % 4]
            pointList = self.fractalLine()
            endpointY = pointList[0].y

            for pt in pointList:
                nextX = corner[i].x + pt.x*(nextCorner.x - corner[i].x)
                nextY = corner[i].y + pt.x*(nextCorner.y - corner[i].y)
                nextX += driftVector[i].x*(pt.y - endpointY)
                nextY += driftVector[i].y*(pt.y - endpointY)
                points.append((nextX, nextY))

        polygon = self.dwg.add(self.dwg.polygon())
        polygon.points.extend(points)
        polygon.stroke(color='none')
            
        if rotation != 0:
            polygon.rotate(rotation, (x0+w/2.0, y0+h/2.0))

        fillColor = "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"
        polygon.fill(color=fillColor, opacity=1.0)
        
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
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=self.background, stroke='none'))

        boundingBoxes = []
        for i in xrange(self.numPolygons): 
            r = self.palette[1][0]
            g = self.palette[1][1]
            b = self.palette[1][2]
            if random.randint(0,1):
                r = self.palette[2][0]
                g = self.palette[2][1]
                b = self.palette[2][2]
   
            while True:
                w = random.randint(self.minLength, self.maxLength)
                h = random.randint(self.minLength, self.maxLength)
                x0 = random.randint(self.border, self.canvasWidth - self.border - w)
                y0 = random.randint(self.border, self.canvasHeight - self.border - h)
                
                cornerDrift = random.randint(0, int(min(w, h)*0.1))
                drawDrift = random.randint(int(min(w, h)*0.05), int(min(w, h)*0.1))
                rotationDrift = 0
                
                offset = cornerDrift + drawDrift
                boundingBox = (x0-offset, y0-offset, x0 + w + offset, y0 + h + offset)
            
                #if not self.boundingBoxCollision(boundingBox, boundingBoxes):
                break
            
            print 'boundingBoxes', len(boundingBoxes)
            boundingBoxes.append(boundingBox)
 
            self.drawImperfectPolygon(x0, y0, w, h, 
                                        r, g, b,
                                        cornerDrift=cornerDrift,
                                        drawDriftX=drawDrift,
                                        drawDriftY=drawDrift,
                                        rotation=rotationDrift,
                                        iterations=8)
            
        self.dwg.save()
        
if __name__ == "__main__":
    for i in xrange(10):
        print i
        output_file = './images/laws_of_chance.still_%d.svg' % (i+1)
        lawsOfChance = LawsOfChance(output_file)
        lawsOfChance.generate()
        
        os.system('"C:\Program Files\Inkscape\inkscape.exe" -z -e %s -w %d -h %d %s' % ('./images/laws_of_chance.still_%d.png' % (i+1), lawsOfChance.canvasWidth, lawsOfChance.canvasHeight, output_file))
        