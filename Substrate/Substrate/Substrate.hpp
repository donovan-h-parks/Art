#ifndef SUBSTRATE_HPP
#define SUBSTRATE_HPP

#include "CImg.h"

#include "Artist.hpp"
#include "Tools.hpp"

#include "Crack.hpp"

using namespace cimg_library;

#undef CIRCLE
#undef LINE
enum ShapeType { NO_SHAPE, CIRCLE, LINE };

struct GridData {
	GridData(uint _objectId, float _angle, ShapeType _shape): objectId(_objectId), angle(_angle), shape(_shape) {}

	void setData(uint _objectId, float _angle, ShapeType _shape)
	{
		objectId = _objectId;
		angle = _angle;
		shape = _shape;
	}

	uint objectId;
	float angle;
	ShapeType shape;
};

class Substrate 
{
public:
	Substrate(uint width, uint height, uint numInitialCracks, uint maxNumCracks, float curvedPercentage, float degreesFromPerpendicular);
	~Substrate() {}

	void draw(uint framesPerImage, uint maxFrames, uint rndSeed);
	void drawToScreen();

	bool isWithinImage(int cx, int cy) const;

	void saveImage(const std::string& filename, uint seed) { Artist::save(m_image, filename, seed); }

	void setGridData(uint objectId, float angle, ShapeType shape, int px, int py) 
	{ 
		m_gridData[py*m_image.width() + px].setData(objectId, angle, shape);
		m_crackedPixels.push_back(py*m_image.width() + px);
	}

	bool isCracked(int px, int py) const { return m_gridData[py*m_image.width() + px].objectId != UNCRACKED; }
	bool isNearbyCrack(uint objectId, int px, int py) const;
	uint cracksInRadius(int px, int py, int radius) const;

	Point randomCrackedPixel() 
	{
		uint rnd = randInt(0, m_crackedPixels.size());
		uint py = m_crackedPixels[rnd]/m_image.width();
		uint px = m_crackedPixels[rnd] - py*m_image.width();

		return Point(px, py);
	}

	float angle(int px, int py) const { return m_gridData[py*m_image.width() + px].angle; }
	uint objectId(int px, int py) const { return m_gridData[py*m_image.width() + px].objectId; }
	ShapeType shape(int px, int py) const { return m_gridData[py*m_image.width() + px].shape; } 

	float curvePercentage() const { return m_curvedPercentage; }
	float degreesFromPerpendicular() const { return m_degreesFromPerpendicular; }

	uint uniqueId() { return ++m_uniqueId; }

private:
	static const int UNCRACKED = -1;

private:
	void initializeCanvas();
	void makeCrack();

private:
	uint m_uniqueId;

	uint m_maxCracks;
	uint m_numInitialCracks;
	float m_curvedPercentage;
	float m_degreesFromPerpendicular;

	Image m_image;
	std::vector<Colour> m_palette;

	std::vector<uint> m_crackedPixels;
	std::vector<GridData> m_gridData;
	std::vector<Crack> m_cracks;
};

#endif