#ifndef INCREMENTAL_GEOMETRY
#define INCREMENTAL_GEOMETRY

#include "CImg.h"

#include "Artist.hpp"
#include "Tools.hpp"

#include "Crack.hpp"

using namespace cimg_library;

class IncrementalGeometry 
{
public:
	IncrementalGeometry(uint width, uint height, uint numInitialCracks, uint maxNumCracks, float curvedPercentage, float degreesFromPerpendicular);
	~IncrementalGeometry() {}

	void draw();

	void saveImage(const std::string& filename, uint seed) { Artist::save(m_image, filename, seed); }

private:
	void initializeCanvas();
	void makeCrack();

private:
	uint m_maxCracks;
	uint m_numInitialCracks;
	float m_curvedPercentage;
	float m_degreesFromPerpendicular;

	Image m_image;
	std::vector<Colour> m_palette;

	std::vector<uint> m_cgrid;
	std::vector<Crack> m_cracks;
};

#endif