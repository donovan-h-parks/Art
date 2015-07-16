#include "Precompiled.hpp"

#include "Substrate.hpp"
#include "Tools.hpp"

#include "Perlin.hpp"

#include "Line.hpp"

Substrate::Substrate(uint width, uint height, uint numInitialCracks, uint maxNumCracks, float curvedPercentage, float degreesFromPerpendicular)
	: m_image(width, height, 1, 3, 255), 
		m_numInitialCracks(numInitialCracks), 
		m_maxCracks(maxNumCracks), 
		m_curvedPercentage(curvedPercentage), 
		m_degreesFromPerpendicular(degreesFromPerpendicular),
		m_uniqueId(0)
{
	//Artist::extractPalette("../Data/pollockShimmering.jpg", m_palette);
	Artist::extractPalette("../Data/RiopellePalette.png", m_palette);

	initializeCanvas();
}

void Substrate::initializeCanvas()
{
	m_image.fill(255, 255, 255);

	m_cracks.clear();

	// make random crack seeds
	m_gridData.clear();
	m_gridData.resize(m_image.width()*m_image.height(), GridData(UNCRACKED, UNCRACKED, NO_SHAPE));
	for(uint k = 0; k < m_numInitialCracks; k++) 
	{
		int c = m_image.width()/2; //randInt(0, m_image.width());
		int r = m_image.height()/2; //randInt(0, m_image.height());

		m_crackedPixels.push_back(r*m_image.width() + c);
		m_gridData[r*m_image.width() + c].angle = randInt(0, 360);
		m_gridData[r*m_image.width() + c].objectId = uniqueId();
	}

	// make initial cracks
	m_curvedPercentage = 1.0f;
	for(uint k = 0; k < m_numInitialCracks; ++k)
		makeCrack();

	// no more circles
	m_curvedPercentage = 0.0f;
}

void Substrate::draw(uint framesPerImage, uint maxFrames, uint rndSeed)
{
	static uint frameNum = 1;

	while(frameNum < maxFrames) 
	{
		for(unsigned int n = 0; n < m_cracks.size(); ++n)
		{
			if(!m_cracks[n].move())
				makeCrack();
		}

		if(frameNum % framesPerImage == 0)
			Artist::saveFrame(m_image, "./images/Substrate.png", rndSeed);

		std::cout << "Frame " << frameNum << " of " << maxFrames << '\xd';
		frameNum++;
	}
}

void Substrate::drawToScreen()
{
	CImgDisplay imageDisplay(m_image,"Substrate", 0);

	while(!imageDisplay.is_closed()) 
	{
		for(unsigned int n = 0; n < m_cracks.size(); ++n)
		{
			if(!m_cracks[n].move())
				makeCrack();
		}

		if(imageDisplay.is_keyS())
			Artist::saveFrame(m_image, "./images/Substrate.png");
		else if(imageDisplay.is_keyR())
			initializeCanvas();

		imageDisplay.display(m_image);
	}
}

void Substrate::makeCrack() 
{
	if (m_cracks.size() < m_maxCracks) 
	{
		Colour colour = m_palette[randInt(0, m_palette.size())];
		m_cracks.push_back(Crack(m_image, *this, colour));
	}
}

bool Substrate::isWithinImage(int px, int py) const
{
	return (px >= 0 && px < m_image.width() && py >= 0 && py < m_image.height());
}

// Check if there is a crack adjacent to the provided coordinates.
// This is useful for finding intersections with circles and lines where
// it can be possible to pass through them on the diagonal
bool Substrate::isNearbyCrack(uint objectId, int px, int py) const
{
	for(int dx = -1; dx < 2; ++dx)
	{
		for(int dy = -1; dy < 2; ++dy)
		{
			if(dx == 0 || dy == 0)	// check a cross pattern
			{
				int index = (py + dy)*m_image.width() + px + dx;

				if(isWithinImage(px + dx, py + dy) 
					&& m_gridData[index].angle != UNCRACKED 
					&& m_gridData[index].objectId != objectId)
				{
					return true;
				}
			}
		}
	}

	return false;
}

uint Substrate::cracksInRadius(int px, int py, int radius) const
{
	std::set<uint> objectIds;
	for(int dx = -radius; dx <= radius; ++dx)
	{
		for(int dy = -radius; dy <= radius; ++dy)
		{
			int index = (py + dy)*m_image.width() + px + dx;

			if(isWithinImage(px + dx, py + dy) && m_gridData[index].objectId != UNCRACKED)
			{
				objectIds.insert(m_gridData[index].objectId);
			}
		}
	}

	return objectIds.size();
}