#ifndef GEOMETRY_HPP
#define GEOMETRY_HPP

#include "Tools.hpp"
#include "Point.hpp"
#include "Line.hpp"

/**
* @brief Functions for calculating basic geometric relationships.
*/
class Geometry
{
public:
	/**
	* @brief Fast calculation of sine with adequate precision for most applications.
	* @return Sine of provided angle in radians.
	*/
	static float fastSin(float rad);

	/**
	* @brief Find intersection between a vertical and diagonal line.
	* @param line Diagonal line.
	* @param x X-coordinate of vertical line.
	* @return Point of intersections.
	*/
	static Point verticalIntersect(const Line& line, const double x);

	/**
	* @brief Find intersection between a horizontal and diagonal line.
	* @param line Diagonal line.
	* @param y Y-coordinate of horizontal line.
	* @return Point of intersections.
	*/
	static Point horizontalIntersect(const Line& line, const double y);

	/**
	* @brief Find intersection between two lines.
	* @param line Diagonal line 1.
	* @param line Diagonal line 2.
	* @return Point of intersections between lines.
	*/
	static Point intersect(const Line& line1, const Line& line2);

	/**
	* @brief Find the closest point on a line, L, to a given point, P. Note: the point and line are assumed to by in the (x,z) plane.
	* @param line Line L.
	* @param point Point P.
	* @param closestPoint Set to the closest point on L to P.
	* @return True if closest point on the line is on the line segment specified by L, otherwise false.
	*/
	static bool closestPointToLine(const Line& line, const Point& point, Point& closestPoint);

	/**
	* @brief Calculate the distance between two points.
	* @param pt1 First point.
	* @param pt2 Second point.
	* @return Distance between points.
	*/
	static double distance(const Point& pt1, const Point& pt2);

	/**
	* @brief Check if a set of 3 points are colinear. Note: the point and line are assumed to by in the (x,z) plane.
	* @param pt1 First point.
	* @param pt2 Second point.
	* @param pt3 Third point.
	* @return True if points are colinear
	*/
	static bool isColinear(const Point& pt1, const Point& pt2, const Point& pt3);

	/**
	* @brief Calculate length of line
	* @param line Line to calculate length of
	* @return Distance between end points of line.
	*/
	static double lineLength(const Line& line) { return distance(line.start(), line.end()); }

	/** 
	* @brief Find mid-point of a line.
	* @param line Line of interest.
	* @return Mid-point of line.
	*/
	static Point midPoint(const Line& line);

	/**
	* @brief Normal to line. The normal is on the RHS as one goes from the start to end points of the line.
	* @param line Line of interest. 
	* @return Normal to line.
	*/
	static Point normalToLine(const Line& line);

	/**
	* @brief Determine if a point is within a triangle.
	* @param pt Point to test.
	* @param x1 First vertex of triangle.
	* @param x2 Second vertex of triangle.
	* @param x3 Thrid vertex of triangle.
	* @return True if the point is contained in the triangle.
	*/
	static bool pointInTriangleXY(const Point& pt, const Point& v1, const Point& v2, const Point& v3);

	/** 
	* @brief Determine if the smallest angle between a start and stop angle is in the CW or CCW direction.
	* @param start First angle of interest.
	* @param end Second angle of interest.
	* @return -1/1 if the smallest angle going from start to end is in the CW/CCW direction.
	*/
	static int smallestAngleDir(double start, double end);

	/** 
	* @brief Find angle bisector of two angles.
	* @param angle1 First angle.
	* @param angle2 Second angle.
	* @return Angle halfway between angle1 and angle2.
	*/
	static double angleBisector(double angle1, double angle2);

	/**
	* @brief Find the angle bisector of a set of angles. For set with more
	*					than 2 angles, the largest angle between any two adjacent angles is identified.
	*					The angle bisector is than set half-way between these two angles such that it 
	*					is in the "middle" of the other angles.
	* @param angles Angles to find mid-point of (all angles must be between 0 and 2PI)
	* @param ccwAngles Order indices going in CCW order from the two angles used to calculate the bisector.
	* @return Angle bisector of set of angles.
	*/
	static double angleBisector(std::vector<double> angles, std::vector<uint>& ccwIndices);
};
#endif
