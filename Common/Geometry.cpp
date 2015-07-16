//=======================================================================
// Author: Donovan Parks
//
// Copyright 2009 Donovan Parks
//
// This file is part of GenGIS.
//
// GenGIS is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// GenGIS is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with GenGIS.  If not, see <http://www.gnu.org/licenses/>.
//=======================================================================

#include "Precompiled.hpp"

#include "Geometry.hpp"

#include "Tools.hpp"

float Geometry::fastSin(float rad)
{
	// Code from: http://www.devmaster.net/forums/showthread.php?t=5784
	const float B = 4/PI;
	const float C = -4/(PI_SQUARED);

	float y = B * rad + C * rad * abs(rad);

	const float Q = 0.775f;
	const float P = 0.225f;

	y = Q * y + P * y * abs(y);

	return y;
}

Point Geometry::verticalIntersect(const Line& line, const double x)
{
	if(line.end().x()-line.start().x() == 0)
		return Point(std::numeric_limits<float>::max(), std::numeric_limits<float>::max());

	double slope = (line.end().y() - line.start().y()) / (line.end().x()-line.start().x());
	double run = x - line.start().x();

	double yInter = line.start().y()+slope*run;

	return Point((float)x, (float)yInter);
}

Point Geometry::horizontalIntersect(const Line& line, const double y)
{
	if(line.end().y()-line.start().y() == 0)
		return Point(std::numeric_limits<float>::max(), std::numeric_limits<float>::max());

	double vertSlope = (line.end().x()-line.start().x()) / (line.end().y() - line.start().y());
	double vertRun = y - line.start().y();

	double xInter = line.start().x()+vertSlope*vertRun;

	return Point((float)xInter, (float)y);
}

Point Geometry::intersect(const Line& line1, const Line& line2)
{
	// express line 1 in form: Ax+By=C
	double A1 = line1.end().y() - line1.start().y();
	double B1 = line1.start().x() - line1.end().x();
	double C1 = A1*line1.start().x() + B1*line1.start().y();

	// express line 2 in form: Ax+By=C
	double A2 = line2.end().y() - line2.start().y();
	double B2 = line2.start().x() - line2.end().x();
	double C2 = A2*line2.start().x() + B2*line2.start().y();

	double det = A1*B2 - A2*B1;
	if(det != 0)
	{
		double x = (B2*C1 - B1*C2)/det;
		double y = (A1*C2 - A2*C1)/det;

		return Point((float)x, (float)y);
	}

	return Point(0, 0);
}

bool Geometry::closestPointToLine(const Line& line, const Point& point, Point& closestPoint)
{
	/*
	[ Source unknown ]

	Subject 1.02: How do I find the distance from a point to a line?


			Let the point be C (Cx,Cy) and the line be AB (Ax,Ay) to (Bx,By).
			Let P be the point of perpendicular projection of C on AB.  The parameter
			r, which indicates P's position along AB, is computed by the dot product 
			of AC and AB divided by the square of the length of AB:
	    
			(1)     AC dot AB
					r = ---------  
							||AB||^2
	    
			r has the following meaning:
	    
					r=0      P = A
					r=1      P = B
					r<0      P is on the backward extension of AB
					r>1      P is on the forward extension of AB
					0<r<1    P is interior to AB
	*/

	double dx = line.end().x()-line.start().x();
	double dy = line.end().y()-line.start().y();

	double r_numerator = (point.x()-line.start().x())*dx + (point.y()-line.start().y())*dy;
	double r_denomenator = dx*dx + dy*dy;
	double r = r_numerator / r_denomenator;

	closestPoint.setX(line.start().x() + r*dx);
	closestPoint.setY(line.start().y() + r*dy);

	return (r >= 0 && r <= 1);
}

double Geometry::distance(const Point& pt1, const Point& pt2)
{
	double dx = pt1.x() - pt2.x();
	double dy = pt1.y() - pt2.y();

	return sqrt(dx*dx + dy*dy);
}

bool Geometry::isColinear(const Point& pt1, const Point& pt2, const Point& pt3)
{
	Point closestPoint;
	closestPointToLine(Line(pt1, pt2), pt3, closestPoint);

	double dx = pt3.x() - closestPoint.x();
	double dy = pt3.y() - closestPoint.y();

	return distance(pt3, closestPoint) < EPS;
}

Point Geometry::midPoint(const Line& line)
{	
	return line.start() + 0.5*(line.end()-line.start());
}

Point Geometry::normalToLine(const Line& line)
{
	Point normDir(line.start().y()-line.end().y(), line.end().x()-line.start().x());
	normDir.normalize();

	return normDir;
}

bool Geometry::pointInTriangleXY(const Point& pt, const Point& v1, const Point& v2, const Point& v3)
{
	Point vec1 = pt - v1;
	Point vec2 = pt - v2;
	Point vec3 = pt - v3;

	double angle1 = vec1.angle(vec2);
	double angle2 = vec2.angle(vec3);
	double angle3 = vec3.angle(vec1);

	double sum = angle1 + angle2 + angle3;

	return (sum > TWO_PI-EPS && sum < TWO_PI+EPS);
}

double Geometry::angleBisector(double angle1, double angle2)
{
	if(angle1 < 0) 
		angle1 = TWO_PI + angle1;
	
	if(angle2 < 0) 
		angle2 = TWO_PI + angle2;
	
	double midAngle;
	if(angle1 > angle2)
	{
		double deltaAngle = angle1 - angle2;
		if(deltaAngle > PI) 
			deltaAngle = deltaAngle - TWO_PI;
		midAngle = angle2 + deltaAngle * 0.5;
	}
	else
	{
		double deltaAngle = angle2 - angle1;
		if(deltaAngle > PI) 
			deltaAngle = deltaAngle - TWO_PI;
		midAngle = angle1 + deltaAngle * 0.5;
	}

	return midAngle;
}

int Geometry::smallestAngleDir(double start, double end)
{
	int dir = 1;
	double dAngle = start - end;
	if(dAngle > 0 && dAngle < PI)
			dir = -1;
	else if(dAngle > 0 && dAngle < -PI)
			dir = -1;

	return dir;
}

double Geometry::angleBisector(std::vector<double> angles, std::vector<uint>& ccwIndices)
{
	// Set angle bisector so it at the "middle angle" of the set of angles. For 
	// sets with 2 angles this is simple the angle bisector. For set with more
	// than 2 angles, the largest angle between any two adjacent angles is identified.
	// The angle bisector is than set half-way between these two angles such that it 
	// is in the "middle" of the other angles.

	assert(angles.size() > 1);

	if(angles.size() == 2)
	{
		int dir = smallestAngleDir(angles.at(0), angles.at(1));
		if(dir == 1)
		{
			ccwIndices.push_back(0);
			ccwIndices.push_back(1);
		}
		else
		{
			ccwIndices.push_back(1);
			ccwIndices.push_back(0);
		}

		return angleBisector(angles.at(0), angles.at(1));
	}
	else
	{
		// find largest angle between any two adjacent angles in the set
		std::sort(angles.begin(), angles.end());

		double maxAngle = 0;
		uint maxIndex;
		for(uint i = 1; i < angles.size(); ++i)
		{
			double angle = angles.at(i) - angles.at(i-1);
			if(angle > maxAngle)
			{
				maxAngle = angle;
				maxIndex = i;

			}
		}

		// check angle between first and last angle in set
		double angle = angles.at(angles.size()-1) - angles.at(0);
		angle = TWO_PI - angle;
		if(angle > maxAngle)
		{
			maxAngle = angle;
			maxIndex = 0;
		}
	
		// find bisector of angles with largest angle between them
		double dAngle;
		if(maxIndex > 0)
		{			
			dAngle = angles.at(maxIndex) - angles.at(maxIndex-1);
		}
		else
		{
			dAngle = angles.at(angles.size()-1) - angles.at(0);
			dAngle = TWO_PI - dAngle;
		}

		double bisector = angles.at(maxIndex) - dAngle * 0.5;
		
		// rotate bisector 180 degrees so it is in the "middle" of the angle set
		bisector += PI;
		if(bisector > TWO_PI)
			bisector -= TWO_PI;

		// create list of angles going in CCW direction between angles used to define the bisector
		for(uint i = maxIndex; i < angles.size(); ++i)
		{
			ccwIndices.push_back(i);
		}

		for(uint i = 0; i < maxIndex; ++i)
		{
			ccwIndices.push_back(i);
		}

		return bisector;
	}

	// the compiler has failed if this point is every reached!
	assert(false);
	return 0;
}