#include "Precompiled.hpp"

#include "CImg.h"

#include "SpacePartitioning.hpp"

int main(int argc, char* argv[])
{
	unsigned int seed = (unsigned int)time(NULL);
	srand(seed);
	
	// calculate pixel size
	int widthCM = 60; //120;
	int heightCM = 60; //40;
	int DPI = 96;
	float inchPerCM = 0.393700787f;
	int widthPixel = int(widthCM * inchPerCM * DPI + 0.5);
	int heightPixel = int(heightCM * inchPerCM * DPI + 0.5);

	int maxIterations = 7;
	float drawPrimativePercentage = 0.33f;
	bool bDisplay = false;

	for(uint i = 0; i < 100; ++i)
	{
		clock_t startTime = clock();

		SpacePartitioning sp(widthPixel, heightPixel, maxIterations, drawPrimativePercentage, 2, 2, bDisplay);
		sp.draw();

		std::string filename = "../images/SpacePartitioningFinal_";

		char version[30];
		itoa(i, version, 10);
		filename += std::string(version) + ".png";

		sp.saveImage(filename, seed, false);

		std::cout << i << ": " << double(clock() - startTime) / (double)CLOCKS_PER_SEC << " seconds." << std::endl;
	}

	

	return 0;
}