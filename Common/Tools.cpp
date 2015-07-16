#include "Precompiled.hpp"

#include "Tools.hpp"

int randInt(int lowerBound, int upperBound)
{
	return lowerBound + rand()%(upperBound-lowerBound); 
}

float randFloat(float lowerBound, float upperBound)
{
	return lowerBound + (upperBound-lowerBound) * (rand()/(float)RAND_MAX);
}

int ipart(float x)
{
	float intX;
	modf(x, &intX);
	return int(intX);
}
 
int round(float x)
{
	return int(x + 0.5);
}
 
float fpart(float x)
{
	float intX;
	return modf(x, &intX);
}
 
float rfpart(float x)
{
     return 1.0f - fpart(x);
}