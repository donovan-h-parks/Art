#include "Precompiled.hpp"

#include "SandPainter.hpp"

#include "Tools.hpp"

SandPainter::SandPainter(Image& image, const Colour& colour)
	: m_image(image), m_colour(colour)
{
	m_rand = randFloat(0.01f, 0.1f);
}

void SandPainter::render(const Point& start, const Point& end) 
{
	// modulate gain
	m_rand += randFloat(-0.05f, 0.05f);

	float modulationMax = 1.0f;
	if (m_rand < 0) 
		m_rand = 0;

	if (m_rand > modulationMax) 
		m_rand = modulationMax;
    
	// calculate grains by distance
	int grains = 64;

	// lay down grains of sand (transparent pixels)
	float w = m_rand/(grains-1);
	for(int i=0; i < grains; ++i) 
	{
		float a = 0.1f - i/(grains*10.0f);
		int cx = int(start.x()+(end.x()-start.x())*sin(sin(i*w)) + 0.5);
		int cy = int(start.y()+(end.y()-start.y())*sin(sin(i*w)) + 0.5);

		if ((cx >= 0) && (cx < m_image.width()) && (cy >= 0) && (cy < m_image.height())) 
			m_image.draw_point(cx, cy, 0, m_colour.colour(), a);
	}
}