#include "Precompiled.hpp"

#include "Line.hpp"

#include "Artist.hpp"

#include "Geometry.hpp"

void Line::setLine(const Point& start, float angle, uint width, uint height)
{
	m_start = start;
	m_angle = angle;

	// find where line intersects edge of canvas
	while(angle < 0) angle += 360;
	angle = int(angle + 0.5) % 360;

	Line lineVec(m_start, m_start.offset(angle));

	Point intersection;
	if(angle >= 0 && angle < 90)
	{
		intersection = Geometry::verticalIntersect(lineVec, width-1);
		Point test = Geometry::horizontalIntersect(lineVec, height-1);
		if(test.x() < intersection.x())
			intersection = test;
	}
	else if(angle >= 90 && angle < 180)
	{
		intersection = Geometry::verticalIntersect(lineVec, 0);
		Point test = Geometry::horizontalIntersect(lineVec, height-1);
		if(test.x() > intersection.x() || intersection.x() == std::numeric_limits<float>::max())
			intersection = test;
	}
	else if(angle >= 180 && angle < 270)
	{
		intersection = Geometry::verticalIntersect(lineVec, 0);
		Point test = Geometry::horizontalIntersect(lineVec, 0);
		if(test.x() > intersection.x() && test.x() != std::numeric_limits<float>::max())
			intersection = test;
	}
	else if(angle >= 270 && angle < 360)
	{
		intersection = Geometry::verticalIntersect(lineVec, width-1);
		Point test = Geometry::horizontalIntersect(lineVec, 0);
		if(test.x() < intersection.x())
			intersection = test;
	}

	m_start = start;
	m_end = intersection;
}

void Line::draw(Image& image, const Colour& colour, bool bAntialiased)
{
	if(bAntialiased)
	{
		std::vector<Point> pts;
		std::vector<float> alpha;
		lineWu(m_start.xInt(), m_start.yInt(), m_end.xInt(), m_end.yInt(), pts, alpha);

		for(uint i = 0; i < pts.size(); ++i)
			image.draw_point(pts[i].xInt(), pts[i].yInt(), 0, colour.colour(), colour.alpha()*alpha[i]);
	}
	else
	{
		std::vector<Point> pts = points();
		for(uint i = 0; i < pts.size(); ++i)
			image.draw_point(pts[i].xInt(), pts[i].yInt(), 0, colour.colour());
	}
}

std::vector<Point> Line::points()
{
	std::vector<Point> pts;
	lineBresenham(m_start.xInt(), m_start.yInt(), m_end.xInt(), m_end.yInt(), pts);

	return pts;
}

// Draw antialiased line using Wu's algorithm.
void Line::lineWu(int x0, int y0, int x1, int y1, std::vector<Point>& points, std::vector<float>& alpha)
{
	bool bSteep = abs(int(y1 - y0)) > abs(int(x1 - x0));
 
	if(bSteep)
	{
		std::swap(x0, y0);
		std::swap(x1, y1);
	}

	if(x0 > x1)
	{
		std::swap(x0, x1);
		std::swap(y0, y1);
	}
 
	float dx = float(x1 - x0);
	float dy = float(y1 - y0);
	float gradient = float(dy) / dx;
 
	// handle first endpoint
	uint xend = round(float(x0));
	float yend = y0 + gradient * (xend - x0);
	float xgap = rfpart(x0 + 0.5f);
	uint xpxl1 = xend;   //this will be used in the main loop
	uint ypxl1 = ipart(yend);

	if(bSteep)
	{
		points.push_back(Point(ypxl1, xpxl1));
		alpha.push_back(rfpart(yend) * xgap);

		points.push_back(Point(ypxl1+1, xpxl1));
		alpha.push_back(fpart(yend) * xgap);
	}
	else
	{
		points.push_back(Point(xpxl1, ypxl1));
		alpha.push_back(rfpart(yend) * xgap);

		points.push_back(Point(xpxl1, ypxl1+1));
		alpha.push_back(fpart(yend) * xgap);
	}

	float intery = yend + gradient; // first y-intersection for the main loop
 
     // handle second endpoint
	xend = round(float(x1));
	yend = y1 + gradient * (xend - x1);
	xgap = fpart(x1 + 0.5f);
	uint xpxl2 = xend; //this will be used in the main loop
	uint ypxl2 = ipart(yend);
	if(bSteep)
	{
		points.push_back(Point(ypxl2, xpxl2));
		alpha.push_back(rfpart(yend) * xgap);

		points.push_back(Point(ypxl2+1, xpxl2));
		alpha.push_back(fpart(yend) * xgap);
	}
	else
	{
		points.push_back(Point(xpxl2, ypxl2));
		alpha.push_back(rfpart(yend) * xgap);

		points.push_back(Point(xpxl2, ypxl2+1));
		alpha.push_back(fpart(yend) * xgap);
	}

	// main loop
	for(uint x = xpxl1 + 1; x < xpxl2; ++x)
	{
		if(bSteep)
		{
			points.push_back(Point(ipart(intery), x));
			alpha.push_back(rfpart(intery));

			points.push_back(Point(ipart(intery)+1, x));
			alpha.push_back(fpart(intery));
		}
		else
		{
			points.push_back(Point(x, ipart(intery)));
			alpha.push_back(rfpart(intery));

			points.push_back(Point(x, ipart(intery)+1));
			alpha.push_back(fpart(intery));
		}
		intery = intery + gradient;
	}
}

// Draw line using Bresenham's algorithm.
void Line::lineBresenham(int x0, int y0, int x1, int y1, std::vector<Point>& points)
{
	int dx = abs(int(x1-x0));
	int dy = abs(int(y1-y0));

	int sx = -1;
	if(x0 < x1)
		sx = 1;

	int sy = -1;
	if(y0 < y1)
		sy = 1;
   
	int err = dx-dy;
 
	while(true)
	{
		points.push_back(Point(x0, y0));

		if(x0 == x1 && y0 == y1)
			break;

		int e2 = 2*err;
		if(e2 > -dy)
		{
			err = err - dy;
			x0 = x0 + sx;
		}

		if(e2 <  dx)
		{
			err = err + dx;
			y0 = y0 + sy;
		}
	}
}

Line Line::offset(const Point& pt) const
{
	Point start =  m_start.offset(pt);
	Point end = m_end.offset(pt);		

	return Line(start, end);
}