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
Parse output of QGIS shape file saved as a SVG and transform all paths into polygons.
"""

import xml.etree.ElementTree

__author__ = 'Donovan Parks'
__copyright__ = 'Copyright 2014'
__credits__ = ['Donovan Parks']
__license__ = 'GPL3'
__version__ = '1.0.0'
__maintainer__ = 'Donovan Parks'
__email__ = 'donovan.parks@gmail.com'
__status__ = 'Development'

import svgwrite
from svgwrite import cm, mm  

from xml.dom import minidom

class MapParser:
	def __init__(self):
		pass
		
	def convertToPolygon(self, path):
		"""Convert SVG path string to SVG polygon."""
		
		polygon = self.dwg.add(self.dwg.polygon())
		polygon.fill(color='none')
		polygon.stroke(color='black', width=1)
		
		for pt in path.split():
			pt = pt.replace("'", "")
			x, y = pt.split(',')
			x = float(x[1:]) # string starting character (M, L, ...)
			y = float(y)
			polygon.points.append((x,y))
		
	def parse(self, map):
		"""Parse SVG file."""
		doc = minidom.parse(map)
		
		# parse header information for SVG file
		self.canvasWidth = doc.getElementsByTagName('svg')[0].getAttribute('width')
		self.canvasHeight = doc.getElementsByTagName('svg')[0].getAttribute('height')
		
		self.dwg = svgwrite.Drawing(filename='output.svg', size=(self.canvasWidth, self.canvasHeight), profile='tiny')
		
		# parse all paths from SVG file and convert these to polygons
		paths = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
		for path in paths:
			self.convertToPolygon(path)

	def generate(self):
		self.parse('test.svg')
			
		self.dwg.save()
		
if __name__ == "__main__":
	mapParser = MapParser()
	mapParser.generate()