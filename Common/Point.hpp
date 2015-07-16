#ifndef POINT_HPP
#define POINT_HPP

#include "Tools.hpp"

class Point
{
public:
	Point(float x = 0, float y = 0): m_x(x), m_y(y) {}

	float x() const { return m_x; }
	float y() const { return m_y; }

	int xInt() const { return int(m_x + 0.5f); }
	int yInt() const { return int(m_y + 0.5f); }

	void setX(float x) { m_x = x; }
	void setY(float y) { m_y = y; }

	// Calculate a point this is offset from this one.
	Point offset(const Point& pt) const;

	// Calculate a point offset by the specified angle and magnitude.
	Point offset(float angle, float magnitude = 1.0f) const;

	// Length of point (vector). 
	float length() const { return sqrt(squaredLength()); }

	// Squared length of point (vector). 
	float squaredLength() const { return (x()*x() + y()*y()); }

	// Normalize point (vector) to unit length. 
	const Point& normalize();

	// Dot product. Can also use * operator. 
	double dot(const Point& pt) const { return x() * pt.x() + y() * pt.y(); }

	// Calculate the smallest angle between two vectors. 
	float angle(const Point& pt) const;

	// Compound addition operator. 
	Point& operator+=(const Point& pt)
	{
		m_x += pt.x();
		m_y += pt.y();
		return *this;
	}

	// Compound subtraction operator. 
	Point& operator-=(const Point& pt)
	{
		m_x -= pt.x();
		m_y -= pt.y();
		return *this;
	}

	// Add two points. 
	const Point operator+(const Point& pt) const { return Point(x() + pt.x(), y() + pt.y()); }

	// Subtract two points. 
	const Point operator-(const Point& pt) const { return Point(x() - pt.x(), y() - pt.y()); }

	// Inner dot product. 
	const float operator*(const Point& pt) const { return x() * pt.x() + y() * pt.y(); }

	// Scalar multiplication. 
	friend Point operator*(float c, Point pt) { return Point(c*pt.x(), c*pt.y()); }

	// Scalar multiplication. 
	friend Point operator*(const Point& pt, float c) { return Point(c*pt.x(), c*pt.y()); }

	// Scalar division. 
	friend Point operator/(const Point& pt, float c) { return Point(pt.x()/c, pt.y()/c); }

	// Unary negation. 
	const Point operator-() const { return Point(-x(), -y()); }

	// Equality operator. 
	bool operator==(const Point& pt) const { return (x()==pt.x() && y()==pt.y()); }

	// Not equal operator. 
	bool operator!=(const Point& pt) const { return !(*this == pt); }

private:
	float m_x;
	float m_y;
};

#endif
