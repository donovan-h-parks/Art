#include "Precompiled.hpp"

#include "Crack.hpp"

#include "Tools.hpp"
#include "Artist.hpp"

Crack::Crack(Image& image, std::vector<uint>& cgrid, const Colour& colour, float curvedPercentage, float degreesFromPerpendicular)
	: m_image(image), m_cgrid(cgrid), m_perlinPainter(image, colour),
		m_curvedPercentage(curvedPercentage), m_degreesFromPerpendicular(degreesFromPerpendicular)
{
	findStart();
}

void Crack::findStart() 
{
	// shift until crack is found
	bool bFound = false;
	int timeout = 0;
	uint px, py;
	while ((!bFound) || (timeout++>1000)) 
	{
		// pick random point
		px = randInt(0, m_image.width()-1);
		py = randInt(0, m_image.height()-1);

		if(m_cgrid[py*m_image.width() + px] < UNCRACKED)
			bFound=true;
	}
    
	if (bFound) 
	{
		// start crack
		int angle = m_cgrid[py*m_image.width() + px];
	
		if (randInt(0, 100) < 50)
			angle -= 90 + int(randFloat(-m_degreesFromPerpendicular, m_degreesFromPerpendicular));
		else
			angle += 90 + int(randFloat(-m_degreesFromPerpendicular, m_degreesFromPerpendicular));

		m_line.setLine(Point(px, py), angle, m_image.width(), m_image.height());
		m_pts = m_line.points();
		m_ptIndex = 0;

		startCrack();
	}
}

void Crack::startCrack() 
{
	m_bCurved = false;
	if(randFloat(0.0f, 1.0f) < m_curvedPercentage)
	{
		/*
		m_bCurved = true;
        m_degreesDrawn = 0;

        int r = randInt(10, int((m_image.width()+m_image.height()) / 10.0f));
        if(randInt(0, 10) < 50)
            r *= -1;

        // arc length = r * theta => theta = arc length / r
        float radianInc = 0.42f / r;
        m_angleStep = radianInc * 360 / 2 / PI;

        m_ys = r * sin(radianInc);
        m_xs = r * ( 1 - cos(radianInc));
		*/
	}
}

bool Crack::move() 
{
	m_ptIndex++;

	// continue cracking
	if(m_bCurved)
	{
		/*
        m_x += ((float) m_ys * cos(m_angle * DEG_TO_RAD));
        m_y += ((float) m_ys * sin(m_angle * DEG_TO_RAD));

        m_x += ((float) m_xs * cos(m_angle * DEG_TO_RAD - HALF_PI));
        m_y += ((float) m_xs * sin(m_angle* DEG_TO_RAD - HALF_PI));

        m_angle += m_angleStep;
        m_degreesDrawn += abs(m_angleStep);
		*/
    }
    
	// draw black crack
	if(m_ptIndex != m_pts.size()) 
	{
		int ptX = m_pts[m_ptIndex].x();
		int ptY = m_pts[m_ptIndex].y();
		m_image.draw_point(ptX, ptY, 0, Artist::black.colour());

		regionColor();

		// safe to check
		if(m_bCurved && (m_degreesDrawn > 360) )
		{
            findStart();
			return false;
        }
		else if(m_cgrid[ptY*m_image.width() + ptX] == UNCRACKED)
		{
			// continue cracking
			m_cgrid[ptY*m_image.width() + ptX] = m_line.angle();
		} 
		else
		{
			// crack encountered (not self), stop cracking
			findStart();
			return false;
		}
	} 
	else 
	{
		// out of bounds, stop cracking
		findStart();
		return false;
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

	Point endPoint = pts[1];
	for(uint i = 1; i < pts.size(); ++i)
	{
		endPoint = pts[i];

		int cx = int(pts[i].x());
		int cy = int(pts[i].y());
		if ((cx >= 0) && (cx < m_image.width()) && (cy >= 0) && (cy < m_image.height())) 
		{
			// safe to check
			if(m_cgrid[cy*m_image.width() + cx] < UNCRACKED) 
				break;
		} 
		else 
			break;
	}

	// draw sand painter
	m_perlinPainter.render(m_pts[m_ptIndex], endPoint);
}