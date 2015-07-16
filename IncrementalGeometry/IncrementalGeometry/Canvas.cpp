// My C++ port of Jarad Tarbell's Substrate algorithm

#include "Precompiled.hpp"

#include "CImg.h"

#include "IncrementalGeometry.hpp"

int main(int argc, char* argv[])
{
	clock_t startTime = clock();

	unsigned int seed = (unsigned int)time(NULL);
	srand(seed);
	
	// calculate pixel size
	int widthCM = 9; //120;
	int heightCM = 3; //40;
	int DPI = 450;
	float inchPerCM = 0.393700787f;
	int widthPixel = int(widthCM * inchPerCM * DPI + 0.5);
	int heightPixel = int(heightCM * inchPerCM * DPI + 0.5);

	IncrementalGeometry incrementalGeometry(widthPixel, heightPixel, 3, 200, 0.0f, 0.0f);
	incrementalGeometry.draw();

	incrementalGeometry.saveImage("IncrementalGeometryFinal.png", seed);

	std::cout << double(clock() - startTime) / (double)CLOCKS_PER_SEC << " seconds." << std::endl;

	return 0;
}