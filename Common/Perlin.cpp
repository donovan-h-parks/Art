#include "Precompiled.hpp"

#include "Perlin.hpp"

Perlin::Perlin(float increment, float lowerBound, float upperBound, uint numOctaves, double frequency, double persistence)
	: m_increment(increment), m_lowerBound(lowerBound), m_upperBound(upperBound)
{
	int a = m_perlin.GetOctaveCount();
	double b = m_perlin.GetFrequency();
	double c = m_perlin.GetPersistence();

	m_perlin.SetSeed(randInt(0, INT_MAX));
	m_perlin.SetOctaveCount(6);
	m_perlin.SetFrequency(1.0);
	m_perlin.SetPersistence (0.5);

	m_value = randFloat(0.0f, 1000.0f);
}

float Perlin::nextValue()
{
	double perlinValue;
	do
	{
		perlinValue = m_lowerBound + (m_upperBound-m_lowerBound) * 0.5 *(m_perlin.GetValue(m_value, m_value, m_value) + 1);
		m_value += m_increment;
	} while(perlinValue < m_lowerBound || perlinValue > m_upperBound);

	return (float)perlinValue;
}