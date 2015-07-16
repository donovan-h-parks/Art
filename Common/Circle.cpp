#include "Precompiled.hpp"

#include "Circle.hpp"

#include "Artist.hpp"

void Circle::setCircle(const Point& centre, int radius)
{
	m_centre = centre;
	m_radius = radius;
}

void Circle::draw(Image& image, const Colour& colour, bool bAntialiased)
{
	if(bAntialiased)
	{
		std::vector<Point> pts;
		std::vector<float> alpha;
		circleAA(m_centre, m_radius, pts, alpha);

		for(uint i = 0; i < pts.size(); ++i)
			image.draw_point(pts[i].xInt(), pts[i].yInt(), 0, colour.colour(), colour.alpha()*alpha[i]);
	}
	else
	{
		std::vector<Point> pts;
		circleBresenham(m_centre, m_radius, pts);

		for(uint i = 0; i < pts.size(); ++i)
			image.draw_point(pts[i].xInt(), pts[i].yInt(), 0, colour.colour());
	}
}

std::vector<Point> Circle::points()
{
	std::vector<Point> pts;
	circleBresenham(m_centre, m_radius, pts);

	return pts;
}

void Circle::circleBresenham(const Point& centre, int radius, std::vector<Point>& points)
{
   int x = -radius;
   int y = 0;
   int err = 2-2*radius;

   // calculate coordinates of circle using 4-fold symmetry
   std::vector<Point> symPoints;
   do 
   {
	   symPoints.push_back(Point(centre.x()-x, centre.y()+y));
	   symPoints.push_back(Point(centre.x()-y, centre.y()-x));
	   symPoints.push_back(Point(centre.x()+x, centre.y()-y));
	   symPoints.push_back(Point(centre.x()+y, centre.y()+x));

		radius = err;
		if (radius <= y) 
		{
			++y;
			err += y*2+1;
		}
		if (radius > x || err > y) 
		{
			++x;
			err += x*2+1;
		}
   } while (x < 0);

   // organize circle coordinates into a continuous list
   for(uint symIndex = 0; symIndex < 4; ++symIndex)
   {
	   for(uint i = symIndex; i < symPoints.size(); i += 4)
	   {
			points.push_back(symPoints[i]);
	   }
   }

   // pick random starting point for circle
   std::vector<Point>::iterator rndStart = points.begin() + randInt(0, points.size());
   std::rotate(points.begin(), rndStart, points.end());
}

/*
Linear-constraint circle anti-aliased algorithm.
Copyright (c) 2011 Konstantin Kirillov
License: MIT

Circle is a solution of constraint F=0 where 
function F(x,y)=R^2 - x^2 - y^2.
When moving from x=R, y=0 till y=R/2 we 

 1. change x-- when F becomes < 0
 2. we calculate intensities I1, I2 of neighbour pixels assuming
    that I1/I2 ~ DF1/DF2 at fixed y.

Following notations are used in program:

  E=R^2-y^2 ( "available excess" )
  x    - point on the left from circle
  xTop - x+1, point to the right from circle
  L    - "low difference", L=E-x^2         =DF1
  U    - "upper difference", U=(x+1)^2-E   =-DF2
  u    - intensity "contributed" by difference from upper node
  l    - intensity "contributed" by lower node  

(2) implies u/l=U/L

We must assign u to the left pixel and l to the right.
*/
void Circle::circleAA(const Point& centre, int radius, std::vector<Point>& points, std::vector<float>& alpha) 
{
	int R2 = radius*radius;
	int y = 0;
	int x = radius;

	int B = x*x;
	int xTop = x+1;
	int T = xTop*xTop;

	while(y < x) 
	{
		int E = R2-y*y;
		int L = E-B;
		int U = T-E;
		if(L<0)
		{ 
			xTop = x;
			x--;
			T = B;
			U = -L;
			B = x*x;
			L = E-B;
		}

		float u = float(U)/(U+L);
		points.push_back(Point(centre.x()+x, centre.y()+y));
		alpha.push_back(u);
		points.push_back(Point(centre.x()+xTop, centre.y()+y));
		alpha.push_back((1.0f-u));

		points.push_back(Point(centre.x()+x, centre.y()-y));
		alpha.push_back(u);
		points.push_back(Point(centre.x()+xTop, centre.y()-y));
		alpha.push_back((1.0f-u));

		points.push_back(Point(centre.x()-x, centre.y()+y));
		alpha.push_back(u);
		points.push_back(Point(centre.x()-xTop, centre.y()+y));
		alpha.push_back((1.0f-u));

		points.push_back(Point(centre.x()-x, centre.y()-y));
		alpha.push_back(u);
		points.push_back(Point(centre.x()-xTop, centre.y()-y));
		alpha.push_back((1.0f-u));

		points.push_back(Point(centre.x()+y, centre.y()+x));
		alpha.push_back(u);
		points.push_back(Point(centre.x()+y, centre.y()+xTop));
		alpha.push_back((1.0f-u));

		points.push_back(Point(centre.x()+y, centre.y()-x));
		alpha.push_back(u);
		points.push_back(Point(centre.x()+y, centre.y()-xTop));
		alpha.push_back((1.0f-u));

		points.push_back(Point(centre.x()-y, centre.y()+x));
		alpha.push_back(u);
		points.push_back(Point(centre.x()-y, centre.y()+xTop));
		alpha.push_back((1.0f-u));

		points.push_back(Point(centre.x()-y, centre.y()-x));
		alpha.push_back(u);
		points.push_back(Point(centre.x()-y, centre.y()-xTop));
		alpha.push_back((1.0f-u));
           
		y++;
	}    
}