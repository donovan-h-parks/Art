#ifndef CRACK
#define CRACK

#include "CImg.h"

#include "Tools.hpp"

#include "PerlinPainter.hpp"
#include "Line.hpp"
#include "Point.hpp"

using namespace cimg_library;

class Crack 
{
public:
	static const int UNCRACKED = 10001;

public:
	Crack(Image& image, std::vector<uint>& cgrid, const Colour& colour, float curvedPercentage = 0.0f, float degreesFromPerpendicular = 2.0f);

	Crack& operator=(Crack& other) { return *this; }

	bool move();

private:
	void findStart();
	void startCrack();
	void regionColor();

private:
	Image& m_image;
	std::vector<uint>& m_cgrid;

	Line m_line;
	std::vector<Point> m_pts;
	uint m_ptIndex;

	float m_degreesFromPerpendicular;

	float m_curvedPercentage;
	bool m_bCurved;
	float m_degreesDrawn;
	float m_angleStep;
	float m_xs;
	float m_ys;

	PerlinPainter m_perlinPainter;
};

#endif