#ifndef SPACE_PARTITIONING
#define SPACE_PARTITIONING

#include "CImg.h"

#include "Artist.hpp"
#include "Tools.hpp"

using namespace cimg_library;

class SpacePartitioning 
{
public:
	SpacePartitioning(uint width, uint height, int maxIterations, float drawPrimativePercentage, uint borderSize = 2, uint offset = 3, bool bDisplay = false);
	~SpacePartitioning() {}

	void draw();

	void saveImage(const std::string& filename, uint seed, bool bSigInImage) { Artist::save(m_image, filename, seed, bSigInImage); }

private:
	void initializeCanvas();

	bool sameColour(const Colour& colour, int x, int y);
	void partition(int x1, int y1, int x2, int y2, int iteration);

private:
	int m_maxIterations;
	float m_drawPrimativePercentage;
	uint m_borderSize;
	uint m_offset;
	bool m_bDisplay;

	Image m_image;
	std::vector<Colour> m_palette;

	CImgDisplay m_imageDisplay;
};

#endif