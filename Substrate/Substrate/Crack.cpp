#include "Precompiled.hpp"

#include "Crack.hpp"

#include "Tools.hpp"
#include "Artist.hpp"
#include "Substrate.hpp"

Crack::Crack(Image& image, Substrate& substrate, const Colour& colour)
	: m_image(image), 
		m_substrate(substrate), 
		m_sandPainter(image, colour)
{
	start();
}

void Crack::start() 
{
	m_objectId = m_substrate.uniqueId();

	// shift until crack is found
	bool bFound = false;
	int timeout = 0;
	Point crackPt;
	while ((!bFound) || (timeout++ > 100)) 
	{
		// pick random crack
		crackPt = m_substrate.randomCrackedPixel();

		if(m_substrate.cracksInRadius(crackPt.xInt(), crackPt.yInt(), 2) == 1)
		{
			// start new crack on an existing crack that isn't already too fractured
			bFound=true;
		}
	}
    
	if (bFound) 
	{
		if(randFloat(0.0f, 1.0f) < m_substrate.curvePercentage())
		{
			newCircle(crackPt);
		}
		else
		{
			newLine(crackPt);
		}
	}
}

void Crack::newCircle(const Point& pt)
{
	// draw circle	
	int minDim = std::min(m_image.width(), m_image.height());
	int radius = randInt(minDim/10, minDim/2);

	m_bCurved = true;
	m_circle.setCircle(pt, radius);
	m_pts = m_circle.points();	
	m_ptIndex = 0;

	m_objectId = m_substrate.uniqueId();
}

void Crack::newLine(const Point& pt)
{
	// draw line at an angle roughly perpendicular to the crack
	int angle = m_substrate.angle(pt.xInt(), pt.yInt());
	
	// cracking off a previous circle
	if(m_substrate.shape(pt.xInt(), pt.yInt()) == CIRCLE)
	{
		// draw line towards the centre of the circle
		angle += 90 + int(randFloat(-m_substrate.degreesFromPerpendicular(), m_substrate.degreesFromPerpendicular()));

		// draw line tangent to circle
		//angle += int(randFloat(-m_substrate.degreesFromPerpendicular(), m_substrate.degreesFromPerpendicular()));
	}
	else
	{
		if(randInt(0, 100) < 50)
			angle += 90 + int(randFloat(-m_substrate.degreesFromPerpendicular(), m_substrate.degreesFromPerpendicular()));
		else
			angle -= 90 + int(randFloat(-m_substrate.degreesFromPerpendicular(), m_substrate.degreesFromPerpendicular()));
	}

	m_bCurved = false;
	m_line.setLine(pt, angle, m_image.width(), m_image.height());
	m_pts = m_line.points();
	m_ptIndex = 0;

	m_objectId = m_substrate.uniqueId();
}

bool Crack::move() 
{
	// continue either circlular or linear crack
	if(m_bCurved)
		return circleMove();
	
	return linearMove();
}

bool Crack::circleMove()
{
	if(m_ptIndex < m_pts.size())
	{
		int ptX = m_pts[m_ptIndex].x();
		int ptY = m_pts[m_ptIndex].y();	

		m_sandPainter.render(m_pts[m_ptIndex], m_circle.centre());

		m_ptIndex++;

		if(m_substrate.isWithinImage(ptX, ptY))
		{
			// continue cracking, save tangent to circle as crack angle
			float angle = atan2(ptY - m_circle.centre().y(), ptX - m_circle.centre().x()) * RAD_TO_DEG + 90;
			m_substrate.setGridData(m_objectId, angle, CIRCLE, ptX, ptY);	
		}
	}
	else
	{
		// complete circle drawn, stop cracking
		//start();
		//return false;

		int rnd = randInt(0, m_pts.size());
		newLine(m_pts[rnd]);
	}

	return true;
}

bool Crack::linearMove()
{
	m_ptIndex++;

	if(m_ptIndex < m_pts.size()) 
	{
		int ptX = m_pts[m_ptIndex].x();
		int ptY = m_pts[m_ptIndex].y();
		m_image.draw_point(ptX, ptY, 0, m_sandPainter.colour().colour()); //Artist::black.colour());
		
		regionColor();

		// safe to check
		if(m_ptIndex > 1 && m_substrate.isNearbyCrack(m_objectId, ptX, ptY))
		{
			int rnd = randInt(0, m_pts.size());
			while(!m_substrate.isCracked(m_pts[rnd].xInt(), m_pts[rnd].yInt()))
				rnd = randInt(0, m_pts.size());
			newLine(m_pts[rnd]);
		} 
		else
		{
			// continue cracking
			m_substrate.setGridData(m_objectId, m_line.angle(), LINE, ptX, ptY);
		}
	} 
	else 
	{
		int rnd = randInt(0, m_pts.size());
		while(!m_substrate.isCracked(m_pts[rnd].xInt(), m_pts[rnd].yInt()))
			rnd = randInt(0, m_pts.size());
		newLine(m_pts[rnd]);
	}

	return true;
}

void Crack::regionColor() 
{
	// find extents of open space
	Line line(m_pts[m_ptIndex], m_line.angle()+90.0f, m_image.width(), m_image.height());
	std::vector<Point> pts = line.points();
	if(pts.size() <= 1)
		return;

	Point endPoint;
	for(uint i = 0; i < pts.size(); ++i)
	{
		endPoint = pts[i];

		int cx = int(pts[i].x());
		int cy = int(pts[i].y());
		if(m_substrate.isNearbyCrack(m_objectId, cx, cy))
			break;
	}

	// draw sand painter
	m_sandPainter.render(m_pts[m_ptIndex], endPoint);
	//m_perlinPainter.render(m_pts[m_ptIndex], endPoint);
}