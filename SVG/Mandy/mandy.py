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
Wedding present.
"""

__author__ = 'Donovan Parks'
__copyright__ = 'Copyright 2014'
__credits__ = ['Donovan Parks']
__license__ = 'GPL3'
__version__ = '1.0.0'
__maintainer__ = 'Donovan Parks'
__email__ = 'donovan.parks@gmail.com'
__status__ = 'Development'

import math
import colorsys
import random
from xml.dom import minidom

import svgwrite
from svgwrite import cm, mm  

import numpy as np
from PIL import Image

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

class Mandy:
	def __init__(self):
		self.rndSeed = '19-09-2014'
		
		self.fractalGradIterations = 4
		self.imperfectPolygonIterations = 2
		self.polygonFractalLayers = 3
		
		self.polygonCornerDrift = 15
		self.polygonLineDrift = 15
		
		self.polygonCornerDriftOutline = 10
		self.polygonLineDriftOutline = 10
		
		self.fractalGradientBaseAlpha = 0.05
		
		self.maxDistortionFromNeighbour = 0.15
		
		self.backgroundSpread = 48
		self.backgroundR = 190
		self.backgroundG = 135
		self.backgroundB = 100
		
	def fractalGradient(self, r, g, b, baseAlpha, alphaVariance, iterations):
		"""Fill object with a fractal gradient."""
		
		# bound colors
		r = max(0, min(r, 255))
		g = max(0, min(g, 255))
		b = max(0, min(b, 255))
		
		gradColor = "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"

		if random.uniform(0.0, 1.0) < 0.5:
			# horizontal gradient
			gradient = self.dwg.linearGradient((0, random.uniform(0, 1)), (1, random.uniform(0, 1)))
		else:
			# vertical gradient
			gradient = self.dwg.linearGradient((random.uniform(0, 1), 0), (random.uniform(0, 1), 1))

		gradPoints = self.fractalLine(iterations)
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
		
	def distToClosestNeighbours(self, points, index):
		"""Calculate distance to nearest neighbour."""
		if index == 0:
			prevPt = points[len(points)-1]
		else:
			prevPt = points[(index-1)]
		nextPt = points[(index+1) % len(points)]
		
		dist1 = abs(prevPt[0] - points[index][0])**2 + abs(prevPt[1] - points[index][1])**2
		dist2 = abs(nextPt[0] - points[index][0])**2 + abs(nextPt[1] - points[index][1])**2
		
		if dist1 < dist2:
			return math.sqrt(dist1)
			
		return math.sqrt(dist2)

	def drawImperfectPolygon(self, points, cornerDrift, lineDrift, lineColor, fillColor, fillAlpha):
		"""Draw an imperfect polygon."""
		
		corners = []
		for i, pt in enumerate(points):
			distClosestNeighbour = self.distToClosestNeighbours(points, i)
			
			# limit corner drift to ensure points still occur in a reasonable order
			# (otherwise, points can move such that crosses occur in the polygon
			# or points along a curve become very jagged)
			drift = min(cornerDrift, self.maxDistortionFromNeighbour*distClosestNeighbour)
			
			corners.append(Point(pt[0] + drift*random.uniform(-1, 1), pt[1] + drift*random.uniform(-1, 1)))

		polygon = self.dwg.add(self.dwg.polygon())
		polygon.fill(color=fillColor, opacity=fillAlpha)
		polygon.stroke(color=None, width=1)
		
		polygon.points.append(corners[0].list())
		for i in xrange(0, len(corners)):
			nextCorner = corners[(i + 1) % len(corners)]
			pointList = self.fractalLine(self.imperfectPolygonIterations)
			endpointY = pointList[0].y
			
			# find perpendicular vector
			dX = corners[i].x - nextCorner.x
			dY = corners[i].y - nextCorner.y
			if dX > 0 or dY > 0:
				driftVec = perpendicular(normalize((dX, dY)))
			else:
				driftVec = (0, 0)

			for pt in pointList:
				distClosestNeighbour = self.distToClosestNeighbours(points, i)
			
				# limit line drift to ensure points still occur in a reasonable order
				# (otherwise, points can move such that crosses occur in the polygon,
				# or points along a curve become very jagged)
				drift = min(lineDrift, self.maxDistortionFromNeighbour*distClosestNeighbour)
			
				nextX = corners[i].x + pt.x*(nextCorner.x - corners[i].x)
				nextY = corners[i].y + pt.x*(nextCorner.y - corners[i].y)
				nextX += driftVec[0] * drift * (pt.y - endpointY)
				nextY += driftVec[1] * drift * (pt.y - endpointY)
				polygon.points.append((nextX, nextY))
				
	def drawImperfectPolygonWithFractalFill(self, points, r, g, b, colorSpread):
		"""Draw imperfect polygon with fractal fill."""
		
		# draw white layer
		self.drawImperfectPolygon(points, self.polygonCornerDriftOutline, self.polygonLineDriftOutline, None, 'white', 1.0)
		
		for i in xrange(0, self.polygonFractalLayers):
			r = random.randint(max(0, r - colorSpread), min(255, r + colorSpread))
			g = random.randint(max(0, g - colorSpread), min(255, g + colorSpread))
			b = random.randint(max(0, b - colorSpread), min(255, b + colorSpread))

			gradient = self.fractalGradient(r, g, b, self.fractalGradientBaseAlpha, 32.0/255, self.fractalGradIterations)
			fillColor = gradient.get_paint_server()

			self.drawImperfectPolygon(points, self.polygonCornerDrift, self.polygonLineDrift, None, fillColor, 1.0)
			
	def convertToPolygon(self, path):
		"""Convert SVG path string to SVG polygon."""
		
		points = []
		for pt in path.split():
			pt = pt.replace("'", "")
			x, y = pt.split(',')
			
			x = float(x[1:]) # string starting character (M, L, ...)
			y = float(y)
			points.append((x,y))
			
		rndColor = random.choice(self.colors)
		r = rndColor[0]
		g = rndColor[1]
		b = rndColor[2]
		colorSpread = 24
		
		self.drawImperfectPolygonWithFractalFill(points, r, g, b, colorSpread)
		
	def background(self):
		"""Setup background."""

		for i in xrange(12):
			gradient = self.fractalGradient(random.randint(self.backgroundR - self.backgroundSpread, self.backgroundR + self.backgroundSpread), 
												random.randint(self.backgroundG - self.backgroundSpread, self.backgroundG + self.backgroundSpread), 
												random.randint(self.backgroundB - self.backgroundSpread, self.backgroundB + self.backgroundSpread), 
												0.0, 28.0/255, 9)
			fillColor = gradient.get_paint_server()
			self.dwg.add(self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=fillColor, stroke='none'))
		
	def parse(self, mapFile):
		"""Parse SVG file."""
		doc = minidom.parse(mapFile)
		
		# parse header information for SVG file
		width = doc.getElementsByTagName('svg')[0].getAttribute('width')
		height = doc.getElementsByTagName('svg')[0].getAttribute('height')
		viewBox = doc.getElementsByTagName('svg')[0].getAttribute('viewBox')

		# parse all paths from SVG file and convert these to polygons
		paths = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
		
		return width, height, viewBox, paths

	def __similarToBackground(self, r, g, b):
		backgroundSpread = 1.25 * self.backgroundSpread
		return (self.backgroundR - backgroundSpread < r  and r < self.backgroundR + backgroundSpread
					and self.backgroundG - backgroundSpread < g and g < self.backgroundG + backgroundSpread
					and self.backgroundB - backgroundSpread < b and b < self.backgroundB + backgroundSpread)
			
	def getImageColors(self, image):
		"""Get list of colors in image."""
		image = Image.open(image)
		pix = image.load()
		
		colors = []
		width, height = image.size
		for x in xrange(width):
			for y in xrange(height):
				r, g, b = pix[x,y]
				#h,s,v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
				
				# filter out low saturation, very light colors
				if r > 200 and g > 200 and b > 200:
					continue
					
				# filter out colors similar to background
				if self.__similarToBackground(r, g, b):
					continue

				colors.append(pix[x,y])
				
		print 'Num. colors: %d' % len(colors)
		return colors

	def generate(self):
		self.colors = self.getImageColors('./data/RiopellePalette.png')

		self.canvasWidth, self.canvasHeight, viewBox, paths = self.parse('kelowna_40x20.svg')

		for i in xrange(10):
			print i
			outputFile = 'output.' + str(i) + '.svg'
			random.seed(self.rndSeed)
			self.dwg = svgwrite.Drawing(filename=outputFile, size=(self.canvasWidth, self.canvasHeight), viewBox=viewBox, profile='tiny')
			self.dwg.set_desc(title='Home in Kelowna', desc='rnd=' + self.rndSeed)
			self.background()
			
			# cycle colors
			for j in xrange(0,10+i):
				tmp = random.randint(0, 100)
		
			for path in paths:
				self.convertToPolygon(path)

			self.dwg.save()

if __name__ == "__main__":
	mandy = Mandy()
	mandy.generate()