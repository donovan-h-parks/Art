#ifndef LINE_HPP
#define LINE_HPP

#include "Tools.hpp"

#include "Colour.hpp"
#include "Point.hpp"

class Line 
{
public:
	Line(): m_start(Point(0, 0)), m_end(Point(0, 0)) {}
	Line(const Point& start, const Point& end) { setLine(start, end); }
	Line(const Point& start, float angle, uint width, uint height) { setLine(start, angle, width, height); }

	void setLine(const Point& start, const Point& end) { m_start = start, m_end = end; }
	void setLine(const Point& start, float angle, uint width, uint height);

	const Point& start() const { return m_start; }
	const Point& end() const { return m_end; }

	float angle() const { return m_angle; }

	void draw(Image& image, const Colour& colour, bool bAntialiased = true);
	std::vector<Point> points();

	// Calculate the line offset from this one by a specified distance.
	Line offset(const Point& pt) const;

private:
	void lineBresenham(int x0, int y0, int x1, int y1, std::vector<Point>& points);
	void lineWu(int x0, int y0, int x1, int y1, std::vector<Point>& points, std::vector<float>& alpha);

private:
	Point m_start;
	Point m_end;

	float m_angle;
};

#endif