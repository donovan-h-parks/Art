#ifndef COLOUR_HPP
#define COLOUR_HPP

#include "Tools.hpp"

class Colour
{
public:
	Colour(unsigned char red, unsigned char green, unsigned char blue, unsigned char alpha = 255);
	Colour(const std::vector<unsigned char>& colour, unsigned char alpha = 255);
	Colour(const unsigned char colour[], unsigned char alpha = 255);
	Colour(const Colour& colour);

	const unsigned char* const colour() const { return &m_colour[0]; }
	const std::vector<unsigned char>& colourVector() const { return m_colour; }

	unsigned char red() const { return m_colour[0]; }
	unsigned char green() const { return m_colour[1]; }
	unsigned char blue() const { return m_colour[2]; }
	float alpha() const { return m_colour[3]/255.0f; }
	
	unsigned char spectrum(uint index) const { return m_colour[index]; }

	void red(unsigned char value) { m_colour[0] = value; }
	void green(unsigned char value) { m_colour[1] = value; }
	void blue(unsigned char value) { m_colour[2] = value; }
	void alpha(unsigned char value) { m_colour[3] = value; }

	void darken(float factor);
	void lighten(float factor);

	inline bool operator==(const Colour& rhs) const { return colourVector() == rhs.colourVector(); }
	inline bool operator!=(const Colour& rhs) const { return !operator==(rhs); } 
	inline bool operator< (const Colour& rhs) const { return colourVector() < rhs.colourVector(); }
	inline bool operator> (const Colour& rhs) const { return colourVector() > rhs.colourVector(); } 
	inline bool operator<=(const Colour& rhs) const { return !operator> (rhs); } 
	inline bool operator>=(const Colour& rhs) const { return !operator< (rhs); }
	 
private:
	std::vector<unsigned char> m_colour;
};

#endif
