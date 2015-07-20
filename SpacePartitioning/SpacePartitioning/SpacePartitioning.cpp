#include "Precompiled.hpp"

#include "SpacePartitioning.hpp"

#include "Tools.hpp"

#include "Artist.hpp"
#include "Colour.hpp"

using namespace cimg_library;

SpacePartitioning::SpacePartitioning(uint width, uint height, int maxIterations, float drawPrimativePercentage, uint borderSize, uint offset, bool bDisplay)
	: m_image(width, height, 1, 3, 255), m_maxIterations(maxIterations), m_drawPrimativePercentage(drawPrimativePercentage), 
		m_borderSize(borderSize), m_offset(offset), m_bDisplay(bDisplay)
{
	Artist::extractPalette("../../data/palettes/modern_cubism.palette.png", m_palette);

	if(m_bDisplay)
		m_imageDisplay = CImgDisplay(m_image,"SpacePartition", 0);
}

void SpacePartitioning::initializeCanvas()
{
	m_image.fill(255, 255, 255);
}

void SpacePartitioning::draw()
{
	partition(0, 0, m_image.width(), m_image.height(), 0);

	while(m_bDisplay)
	{
		if(m_imageDisplay.is_closed())
			exit(0);

		if(m_imageDisplay.is_keyR())
		{
			initializeCanvas();
			partition(0, 0, m_image.width(), m_image.height(), 0);
		}
	}
}

bool SpacePartitioning::sameColour(const Colour& colour, int x, int y)
{
	for(int c = 0; c < m_image.spectrum(); ++c)
	{
		if(colour.spectrum(c) != *m_image.data(x, y, 0, c))
			return false;
	}
	return true;
}

void SpacePartitioning::partition(int x1, int y1, int x2, int y2, int iteration)
{
	x1 += m_offset;
	y1 += m_offset;
	x2 -= m_offset;
	y2 -= m_offset;

	int centreX = x1 + (x2-x1)/2;
	int centreY = y1 + (y2-y1)/2;
	int radius = (x2-x1)/2;

	if(randFloat(0, 1.0f) < m_drawPrimativePercentage)
	{
		float opacity = 1.0f; //randFloat(0.6f, 1.0f);

		// colour of primative must be different than primative below it
		Colour fillColour = m_palette[rand() % m_palette.size()];
		while(sameColour(fillColour, centreX, centreY))
			fillColour = m_palette.at(rand() % m_palette.size());

		Colour borderColour(fillColour);
		//borderColour.darken(0.2f);

		int randShape = randInt(0,2);
		if(randShape == 0)
		{
			m_image.draw_circle(centreX, centreY, radius, borderColour.colour(), opacity);
			m_image.draw_circle(centreX, centreY, radius-m_borderSize, fillColour.colour(), opacity);
		}
		else if(randShape == 1)
		{
			m_image.draw_rectangle(x1, y1, x2, y2, borderColour.colour(), opacity);
			m_image.draw_rectangle(x1+m_borderSize, y1+m_borderSize, x2-m_borderSize, y2-m_borderSize, fillColour.colour(), opacity);
			
		}
	}

	/*
	if(iteration == 0)
	{
		iteration++;
		partition(x1, y1, 0.25*(x2-x1), 0.25*(x2-x1), iteration);	// top-left
		partition(0.25*(x2-x1), y1, x2, 0.25*(x2-x1), iteration);	// top-right
		partition(x1, 0.25*(x2-x1), 0.25*(x2-x1), y2, iteration);	// bottom-left
		partition(0.25*(x2-x1), 0.25*(x2-x1), x2, y2, iteration);	// bottom-right
	}
	*/

	if(m_bDisplay)
	{
		if(m_imageDisplay.is_closed())
			exit(0);

		if(m_imageDisplay.is_keyS())
			Artist::saveFrame(m_image, "SpacePartition.png");

		m_imageDisplay.display(m_image);
	}

	if(iteration < m_maxIterations)
	{
		iteration++;
		partition(x1, y1, centreX, centreY, iteration);	// top-left
		partition(centreX, y1, x2, centreY, iteration);	// top-right
		partition(x1, centreY, centreX, y2, iteration);	// bottom-left
		partition(centreX, centreY, x2, y2, iteration);	// bottom-right
	}
}