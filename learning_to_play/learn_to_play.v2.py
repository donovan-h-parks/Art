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
 
class LearningToPlay:
    def __init__(self, outputFile):    
        self.gridWidth = 23
        self.gridHeight = 11
        
        self.squareSize = 100.0
        self.canvasBorder = 0.5 * self.squareSize
        
        self.canvasWidth = self.gridWidth * self.squareSize + 2*self.canvasBorder
        self.canvasHeight = self.gridHeight * self.squareSize + 2*self.canvasBorder
        
        # background color
        self.backgroundSpread = 0
        self.backgroundR = 255
        self.backgroundG = 255
        self.backgroundB = 255

        self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), profile='tiny')
        self.dwg.set_desc(title='Learn to Play, DHP 2015', desc='Generative art inspired by George Nees.')
        
    def fractalGradient(self, r, g, b, baseAlpha, alphaVariance, gradIterates=8):
        """Fill object with a fractal gradient."""
        
        # bound colors
        r = max(0, min(r, 255))
        g = max(0, min(g, 255))
        b = max(0, min(b, 255))
        
        gradColor = "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"

        if random.uniform(0.0, 1.0) < 0.5:
            # horizontal gradient
            gradient = self.dwg.linearGradient((0, 0), (1, 0))
        else:
            # vertical gradient
            gradient = self.dwg.linearGradient((0, 0), (0, 1))

        gradPoints = self.fractalLine(gradIterates)
        for i, pt in enumerate(gradPoints):
            alpha = baseAlpha + pt.y * alphaVariance
            gradient.add_stop_color(float(i)/(len(gradPoints)-1), color = gradColor, opacity = alpha)
            
        self.dwg.defs.add(gradient)
        
        return gradient

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
                
    def drawPolygonWithFractalFill(self, x0, y0, w, h, 
                                                r, g, b, 
                                                colorSpread,
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

        # perform fractal fill of polygon
        for i in xrange(0, iterations):
            r = random.randint(max(0, r - colorSpread), min(255, r + colorSpread))
            g = random.randint(max(0, g - colorSpread), min(255, g + colorSpread))
            b = random.randint(max(0, b - colorSpread), min(255, b + colorSpread))
            
            polygon = self.dwg.add(self.dwg.polygon())
            polygon.points.extend(points)
            
            #lineColor = "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"
            polygon.stroke(color='none') #, width=1, opacity=0.1)
            
            if rotation != 0:
                polygon.rotate(rotation, (x0+w/2.0, y0+h/2.0))

            gradient = self.fractalGradient(r, g, b, 0, 32.0/255)
            fillColor = gradient.get_paint_server()
            polygon.fill(color=fillColor, opacity=1.0)
            
    def background(self):
        """Setup background."""

        for i in xrange(8):
            r = random.randint(self.backgroundR - self.backgroundSpread, self.backgroundR + self.backgroundSpread)
            g = random.randint(self.backgroundG - self.backgroundSpread, self.backgroundG + self.backgroundSpread)
            b = random.randint(self.backgroundB - self.backgroundSpread, self.backgroundB + self.backgroundSpread)

            gradient = self.fractalGradient(r, g, b, 0, 24.0/255, gradIterates=8)
            fillColor = gradient.get_paint_server()
            
            self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=fillColor, stroke='none'))
            
    def _similarToBackground(self, r, g, b, spread):
        return (self.backgroundR - spread < r  and r < self.backgroundR + spread
                    and self.backgroundG - spread < g and g < self.backgroundG + spread
                    and self.backgroundB - spread < b and b < self.backgroundB + spread)
                    
    def getImageColors(self, image):
        """Get list of colors in image."""
        image = Image.open(image)
        pix = image.load()
        
        colors = []
        width, height = image.size
        for x in xrange(width):
            for y in xrange(height):
                r, g, b = pix[x,y]

                # filter out low saturation, very light colors
                if r > 200 and g > 200 and b > 200:
                    continue
                    
                # filter out colors similar to background
                if self._similarToBackground(r, g, b, 48):
                    continue

                colors.append(pix[x,y])
                
        print 'Colors in palette: %d' % len(colors)
        return colors

    def generate(self):
        #self.background()
        colors = self.getImageColors('../data/palettes/kandinsky.palette.png')

        for x in xrange(self.gridWidth):
            for y in xrange(self.gridHeight):
                rndColor = random.choice(colors)
                r = rndColor[0]
                g = rndColor[1]
                b = rndColor[2]
                colorSpread = 24
                
                cornerDrift = 7.0*(float(x)/(self.gridWidth-1)) + 7 * (float(y)/(self.gridHeight-1))
                drawDrift = 3.5*(float(x)/(self.gridWidth-1)) + 2.5 * (float(y)/(self.gridHeight-1))
                positionDrift = 20.0 * (float(x)**2 / ((self.gridWidth-1)**2)) + 5.0 * (float(y)**2 / ((self.gridHeight-1)**2))
                sizeDrift = 12.5 * (float(x)**2 / ((self.gridWidth-1)**2)) + 5.0 * (float(y)**2 / ((self.gridHeight-1)**2))
                rotationDrift = 20.0 * (float(x)**2 / ((self.gridWidth-1)**2)) + 5.0 * (float(y)**2 / ((self.gridHeight-1)**2))
                rotationDrift *= random.uniform(-1, 1)
                
                x0 = self.canvasBorder + x*self.squareSize + positionDrift*random.uniform(-1, 1)
                y0 = self.canvasBorder + y*self.squareSize + positionDrift*random.uniform(-1, 1)
                w = self.squareSize + sizeDrift*random.uniform(-1, 1)
                h = self.squareSize + sizeDrift*random.uniform(-1, 1)
                
                self.drawPolygonWithFractalFill(x0, y0, w, h, 
                                                        r, g, b, colorSpread,
                                                        cornerDrift=cornerDrift,
                                                        drawDriftX=drawDrift,
                                                        drawDriftY=drawDrift,
                                                        rotation=rotationDrift,
                                                        iterations=8)
            
        self.dwg.save()
        
if __name__ == "__main__":
    for i in xrange(10):
        print i
        learningToPlay = LearningToPlay('learn_to_play.kandinsky_%d.v2.svg' % (i+1))
        learningToPlay.generate()