#ifndef BRUSH
#define BRUSH

#include <vector>

#include "Tools.hpp"

#include "Colour.hpp"

class Brush 
{
public:
	Brush(uint radius, const Colour& colour);

private:
	float gaussian1d(float x, float mu, float sigma);
	void createKernel(uint radius);

private:
	uint m_radius;
	Colour m_colour;

	std::vector< std::vector<float> > m_kernel;
};

#endif