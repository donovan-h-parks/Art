#ifndef CIRCLE_HPP
#define CIRCLE_HPP

#include <vector>

#include "Tools.hpp"
#include "Colour.hpp"
#include "Point.hpp"

class Circle 
{
public:
	Circle(): m_centre(Point(0,0)) {}
	Circle(const Point& centre, int radius) { setCircle(centre, radius); }

	void setCircle(const Point& centre, int radius);

	const Point& centre() const { return m_centre; }
	int radius() const { return m_radius; }

	void draw(Image& image, const Colour& colour, bool bAntialiased = true);

	std::vector<Point> points();

private:
	void circleBresenham(const Point& centre, int radius, std::vector<Point>& points);
	void circleAA(const Point& centre, int radius, std::vector<Point>& points, std::vector<float>& alpha);

private:
	Point m_centre;
	int m_radius;
};

#endif