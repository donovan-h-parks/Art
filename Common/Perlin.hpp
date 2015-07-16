#ifndef PERLIN_HPP
#define PERLIN_HPP

#include <noise.h>

#include "Tools.hpp"

class Perlin
{
public:
	Perlin(float increment, float lowerBound, float upperBound,
			uint numOctaves = noise::module::DEFAULT_PERLIN_OCTAVE_COUNT, 
			double frequency =  noise::module::DEFAULT_PERLIN_FREQUENCY, 
			double persistence = noise::module::DEFAULT_PERLIN_PERSISTENCE);

	float nextValue();	// values are typically between -1.0 and 1.0 though this is not guaranteed

private:
	noise::module::Perlin m_perlin;

	float m_value;
	float m_increment;
	float m_lowerBound;
	float m_upperBound;
};

#endif