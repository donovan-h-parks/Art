#ifndef CRACK_HPP
#define CRACK_HPP

#include "CImg.h"

#include "Tools.hpp"

#include "SandPainter.hpp"
#include "PerlinPainter.hpp"
#include "Line.hpp"
#include "Circle.hpp"

using namespace cimg_library;
class Substrate;

class Crack 
{
public:
	Crack(Image& image, Substrate& substrate, const Colour& colour);

	Crack& operator=(Crack& other) { return *this; }

	bool move();

private:
	void start();
	void regionColor();

	bool circleMove();
	bool linearMove();

	void newCircle(const Point& pt);
	void newLine(const Point& pt);

private:
	uint m_objectId;

	Image& m_image;
	Substrate& m_substrate;

	bool m_bCurved;
	Line m_line;
	Circle m_circle;

	std::vector<Point> m_pts;
	uint m_ptIndex;

	SandPainter m_sandPainter;
	//PerlinPainter m_perlinPainter;
};

#endif