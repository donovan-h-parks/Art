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
Draw an imperfect polygon with fractal fill.
"""

__author__ = 'Donovan Parks'
__copyright__ = 'Copyright 2014'
__credits__ = ['Donovan Parks']
__license__ = 'GPL3'
__version__ = '1.0.0'
__maintainer__ = 'Donovan Parks'
__email__ = 'donovan.parks@gmail.com'
__status__ = 'Development'

import random

import numpy as np

import svgwrite
from svgwrite import cm, mm  

def perpendicular(a):
	b = np.empty_like(a)
	b[0] = -a[1]
	b[1] = a[0]
	return b

def normalize(a):
	a = np.array(a)
	return a/np.linalg.norm(a)

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def list(self):
		return (self.x, self.y)

class ImperfectPolygon:
	def __init__(self):
		self.canvasWidth = 1000.0
		self.canvasHeight = 500.0
		
		self.canvasBorder = 5.0
		
		self.dwg = svgwrite.Drawing(filename='imperfect_polygon.svg', size=(self.canvasWidth, self.canvasHeight), profile='tiny')
		
	def fractalGradient(self, r, g, b, baseAlpha, alphaVariance):
		"""Fill object with a fractal gradient."""
		
		gradIterates = 8
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
			gradient.add_stop_color(float(i)/len(gradPoints), color = gradColor, opacity = alpha)
			
		self.dwg.defs.add(gradient)
		
		return gradient

	def fractalLine(self, iterations):
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
		
	def drawImperfectLine(self, x0, y0, x1, y1, lineColor):
		"""Draw an imperfect line."""
		
		iterates = 8
		
		polyline = self.dwg.add(self.dwg.polyline())
		polyline.fill(color='none')
		polyline.stroke(color=lineColor, width=1)
		
		pointList = self.fractalLine(iterates)
		
		width = x1 - x0
		height = y1 - y0
		for pt in pointList:
			polyline.points.append((x0 + width*pt.x, y0 + height*pt.y))

	def drawImperfectPolygon(self, points, cornerDrift, lineDrift, lineColor, fillColor, fillAlpha):
		"""Draw an imperfect polygon."""
		
		iterates = 8

		corners = []
		for pt in points:
			corners.append(Point(pt[0] + cornerDrift*random.uniform(-1, 1), pt[1] + cornerDrift*random.uniform(-1, 1)))

		polygon = self.dwg.add(self.dwg.polygon())
		polygon.fill(color=fillColor, opacity=fillAlpha)
		polygon.stroke(color=lineColor, width=1)
		
		polygon.points.append(corners[0].list())
		for i in xrange(0, len(corners)):
			nextCorner = corners[(i + 1) % len(corners)]
			pointList = self.fractalLine(iterates)
			endpointY = pointList[0].y
			
			# find perpendicular vector
			dX = corners[i].x - nextCorner.x
			dY = corners[i].y - nextCorner.y
			driftVec = perpendicular(normalize((dX, dY)))

			for pt in pointList:
				nextX = corners[i].x + pt.x*(nextCorner.x - corners[i].x)
				nextY = corners[i].y + pt.x*(nextCorner.y - corners[i].y)
				nextX += driftVec[0] * lineDrift * (pt.y - endpointY)
				nextY += driftVec[1] * lineDrift * (pt.y - endpointY)
				polygon.points.append((nextX, nextY))
				
	def drawImperfectPolygonWithFractalFill(self, points, r, g, b, colorSpread):
		"""Draw imperfect polygon with fractal fill."""
		
		layers = 8
		
		for i in xrange(0, layers):
			r = random.randint(max(0, r - colorSpread), min(255, r + colorSpread))
			g = random.randint(max(0, g - colorSpread), min(255, g + colorSpread))
			b = random.randint(max(0, b - colorSpread), min(255, b + colorSpread))
			
			lineColor = "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"
			
			gradient = self.fractalGradient(r, g, b, 0, 32.0/255)
			fillColor = gradient.get_paint_server()

			self.drawImperfectPolygon(points, 3, 3, fillColor, fillColor, 1.0)
			
		# draw stroke outline
		self.drawImperfectPolygon(points, 5, 3, fillColor, 'none', 1.0)

	def generate(self):
		
		points = [(50,150), (150, 50), (250, 75), (225, 225), (125, 300)]
		
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		colorSpread = 24
		
		self.drawImperfectPolygonWithFractalFill(points, r, g, b, colorSpread)
			
		self.dwg.save()
if __name__ == "__main__":
	imperfectPolygon = ImperfectPolygon()
	imperfectPolygon.generate()