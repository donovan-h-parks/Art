#include "Precompiled.hpp"

#include "Ellipse.hpp"

#include "Artist.hpp"

Ellipse::Ellipse(Image& image, const Colour& colour)
	: m_image(image), m_colour(colour)
{

}

void Ellipse::ellipseBresenham(int x0, int y0, int x1, int y1)
{
   int a = abs(x1-x0);
   int b = abs(y1-y0);
   int b1 = b&1; 
   long dx = 4*(1-a)*b*b;
   int dy = 4*(b1+1)*a*a; 
   long err = dx+dy+b1*a*a;
   long e2; 

   if (x0 > x1) 
   { 
	   x0 = x1; 
	   x1 += a; 
   } 
   
   if (y0 > y1) 
	   y0 = y1;

   y0 += (b+1)/2; 
   y1 = y0-b1;
   a *= 8*a; 
   b1 = 8*b*b;

   do 
   {
	   m_image.draw_point(x1, y0, 0, m_colour.colour());
	   m_image.draw_point(x0, y0, 0, m_colour.colour());
	   m_image.draw_point(x0, y1, 0, m_colour.colour());
	   m_image.draw_point(x1, y1, 0, m_colour.colour());

       e2 = 2*err;
       if (e2 <= dy) 
	   { 
		   y0++; 
		   y1--; 
		   err += dy += a; 
	   }
       if (e2 >= dx || 2*err > dy) 
	   { 
		   x0++; 
		   x1--; 
		   err += dx += b1; 
	   }
   } while (x0 <= x1);
   
   while (y0-y1 < b) 
   {  
	   // finish top of ellipse
	   m_image.draw_point(x0-1, y0, 0, m_colour.colour());
	   m_image.draw_point(x1+1, y0++, 0, m_colour.colour());
	   m_image.draw_point(x0-1, y1, 0, m_colour.colour());
	   m_image.draw_point(x1+1, y1--, 0, m_colour.colour());
   }
}