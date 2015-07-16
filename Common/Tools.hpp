#ifndef TOOLS_HPP
#define TOOLS_HPP

#include <limits>
#include "CImg.h"

using namespace cimg_library;

// typedefs
typedef unsigned int uint;
typedef CImg<unsigned char> Image;

// common defines
const float PI = 3.14159265359f;
const float HALF_PI = PI/2.0f;
const float TWO_PI = 2.0f * PI;
const float PI_SQUARED = (PI*PI);

const float SQRT_2 = 1.41421356237f;

const float RAD_TO_DEG = 180.0f / PI;
const float DEG_TO_RAD = PI / 180.0f;

const float EPS = 2*std::numeric_limits<float>::epsilon();

// common functions
int randInt(int lowerBound, int upperBound);
float randFloat(float lowerBound, float upperBound);

int ipart(float x);
int round(float x);
float fpart(float x);
float rfpart(float x);

#endif