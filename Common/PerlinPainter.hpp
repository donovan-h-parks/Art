#ifndef PERLIN_PAINTER_HPP
#define PERLIN_PAINTER_HPP

#include <CImg.h>

#include "Colour.hpp"

#include "Perlin.hpp"

#include "Point.hpp"

using namespace cimg_library;

class PerlinPainter 
{
public:
	PerlinPainter(Image& image, const Colour& colour);

	void render(const Point& start, const Point& end);

	Colour GetColour() const { return m_colour; }

private:
	Image& m_image;

	Colour m_colour;
	Perlin m_perlin;
};

#endif