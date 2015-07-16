#ifndef SAND_PAINTER_HPP
#define SAND_PAINTER_HPP

#include <CImg.h>

#include "Colour.hpp"

#include "Point.hpp"

using namespace cimg_library;

class SandPainter 
{
public:
	SandPainter(Image& image, const Colour& colour);

	void render(const Point& start, const Point& end);

	Colour colour() const { return m_colour; }

private:
	Image& m_image;

	Colour m_colour;
	float m_rand;
};

#endif