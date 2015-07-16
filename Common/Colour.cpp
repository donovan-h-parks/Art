#include "Precompiled.hpp"

#include "Colour.hpp"

Colour::Colour(unsigned char red, unsigned char green, unsigned char blue, unsigned char alpha)
{
	m_colour.resize(4);
	m_colour[0] = red;
	m_colour[1] = green;
	m_colour[2] = blue;
	m_colour[3] = alpha;
}

Colour::Colour(const std::vector<unsigned char>& colour, unsigned char alpha)
{
	m_colour.resize(4);
	m_colour[0] = colour[0];
	m_colour[1] = colour[1];
	m_colour[2] = colour[2];
	m_colour[3] = alpha;
}

Colour::Colour(const unsigned char colour[], unsigned char alpha)
{
	m_colour.resize(4);
	m_colour[0] = colour[0];
	m_colour[1] = colour[1];
	m_colour[2] = colour[2];
	m_colour[3] = alpha;
}

Colour::Colour(const Colour& colour)
{
	m_colour.resize(4);
	m_colour[0] = colour.red();
	m_colour[1] = colour.green();
	m_colour[2] = colour.blue();
	m_colour[3] = uint(255 * colour.alpha() + 0.5f);
}

void Colour::darken(float factor)
{
	for(uint i = 0; i < 3; ++i)
	{
		int newColour = int(m_colour[i] - m_colour[i]*factor + 0.5f);
		if(newColour < 0)
			newColour = 0;

		m_colour[i] = newColour;
	}
}


void Colour::lighten(float factor)
{
	for(uint i = 0; i < 3; ++i)
	{
		int newColour = int(m_colour[i] + m_colour[i]*factor + 0.5f);
		if(newColour > 255)
			newColour = 255;

		m_colour[i] = newColour;
	}
}