#include "Precompiled.hpp"

#include "IncrementalGeometry.hpp"
#include "Tools.hpp"

#include "Perlin.hpp"

#include "Line.hpp"

IncrementalGeometry::IncrementalGeometry(uint width, uint height, uint numInitialCracks, uint maxNumCracks, float curvedPercentage, float degreesFromPerpendicular)
	: m_image(width, height, 1, 3, 255), m_numInitialCracks(numInitialCracks), m_maxCracks(maxNumCracks), m_curvedPercentage(curvedPercentage), m_degreesFromPerpendicular(degreesFromPerpendicular)
{
	//extractPalette("../Data/pollockShimmering.jpg");
	Artist::extractPalette("../Data/RiopellePalette.png", m_palette);

	initializeCanvas();
}

void IncrementalGeometry::initializeCanvas()
{
	m_image.fill(255, 255, 255);

	m_cracks.clear();

	// make random crack seeds
	m_cgrid.clear();
	m_cgrid.resize(m_image.width()*m_image.height(), Crack::UNCRACKED);
	for(int k = 0; k < 16; k++) 
	{
		int c = randInt(0, m_image.width());
		int r = randInt(0, m_image.height());
		m_cgrid[r*m_image.width() + c] = randInt(0, 360);
	}

	// make initial cracks
	for(uint k = 0; k < m_numInitialCracks; ++k)
		makeCrack();
}

void IncrementalGeometry::draw()
{
	CImgDisplay imageDisplay(m_image,"Incremental Geometry", 0);
	uint saveNum = 0;
	while (!imageDisplay.is_closed()) 
	{
		for(unsigned int n = 0; n < m_cracks.size(); ++n)
		{
			if(!m_cracks[n].move())
				makeCrack();
		}

		if(imageDisplay.is_keyS())
			Artist::saveFrame(m_image, "IncrementalGeometry.png");
		else if(imageDisplay.is_keyR())
			initializeCanvas();

		imageDisplay.display(m_image);
	}
}

void IncrementalGeometry::makeCrack() 
{
	if (m_cracks.size() < m_maxCracks) 
	{
		Colour colour = m_palette[randInt(0, m_palette.size())];
		m_cracks.push_back(Crack(m_image, m_cgrid, colour, m_curvedPercentage, m_degreesFromPerpendicular));
	}
}