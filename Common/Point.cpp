#include "Precompiled.hpp"

#include "Point.hpp"

const Point&  Point::normalize() 
{                     
	float len = length();
	if (len == 0) 
		return *this; 

	m_x /= len;
	m_y /= len;

	return *this;
}

Point Point::offset(const Point& pt) const
{
	return Point(x() + pt.x(), y() + pt.y());
}


Point Point::offset(float angle, float magnitude) const
{
	return Point(x() + magnitude*cos(angle*DEG_TO_RAD), y() + magnitude*sin(angle*DEG_TO_RAD));
}

float Point::angle(const Point& pt) const
{
	float len = length();
	float len2 = pt.length();

	if(len == 0 || len2 == 0)
		return 0.0;

	float dp = (x() * pt.x() + y() * pt.y()) / (len * len2);
	if (dp >= 1.0) 
		return 0.0f;
  
	if (dp <= -1.0f) 
		return 3.14159265f;

	return acos(dp);
}
