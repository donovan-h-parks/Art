#ifndef ELLIPSE_HPP
#define ELLIPSE_HPP

#include "Tools.hpp"

#include "Colour.hpp"

class Ellipse 
{
public:
	Ellipse(Image& image, const Colour& colour);

	void draw(int x0, int y0, int x1, int y1) { ellipseBresenham(x0, y0, x1, y1); }

private:
	void ellipseBresenham(int x0, int y0, int x1, int y1);

private:
	Image& m_image;
	const Colour& m_colour;
};

#endif