#include <math.h>
#include <iostream>
#include <iomanip>

#include "Brush.hpp"

using namespace std;

Brush::Brush(uint radius, const Colour& colour): m_radius(radius), m_colour(colour) 
{
	createKernel(radius);
}

float Brush::gaussian1d(float x, float mu, float sigma) 
{
  return exp( -(((x-mu)/(sigma))*((x-mu)/(sigma)))/2.0 );
}

void Brush::createKernel(uint radius) 
{
  // get kernel matrix
  vector< vector<float> > kernel (2*radius+1, vector<float>(2*radius+1));

  // determine sigma
  float sigma = radius/2.0f;

  // fill values
  float sum = 0;
  for (int row = 0; row < kernel.size(); row++)
  {
    for (int col = 0; col < kernel[row].size(); col++) 
	{
      kernel[row][col] = gaussian1d(row, radius, sigma) * gaussian1d(col, radius, sigma);
      sum += kernel[row][col];
    }
  }

  // normalize
  for (int row = 0; row < kernel.size(); row++)
    for (int col = 0; col < kernel[row].size(); col++)
      kernel[row][col] /= sum;

  m_kernel = kernel;
}