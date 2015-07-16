#include "Precompiled.hpp"

#include "PerlinPainter.hpp"

#include "Tools.hpp"

#include "Point.hpp"
#include "Line.hpp"

PerlinPainter::PerlinPainter(Image& image, const Colour& colour)
	: m_image(image), m_colour(colour), m_perlin(0.1f, 0.0, 1.0f)
{

}

void PerlinPainter::render(const Point& start, const Point& end) 
{
	float perlinNoise = m_perlin.nextValue();

	Line line(start, perlinNoise*end);
	std::vector<Point> pts = line.points();
	for(uint i = 0; i < pts.size(); ++i)
	{
		float alpha = float(pts.size() - i) / pts.size();
		m_image.draw_point(pts[i].x(), pts[i].y(), 0, m_colour.colour(), alpha);
	}
}