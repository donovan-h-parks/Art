#include "Precompiled.hpp"

#include "CImg.h"

#include "Substrate.hpp"

int main(int argc, char* argv[])
{
	clock_t startTime = clock();

	uint seed = (unsigned int)time(NULL);
	srand(seed);
	
	// calculate pixel size
	float widthCM = 48; //120; 48
	float heightCM = 16; //40; 16
	int DPI = 96; //300; 96
	float cmToInches = 0.393700787f;
	int widthPixel = int(widthCM * cmToInches * DPI + 0.5);
	int heightPixel = int(heightCM * cmToInches * DPI + 0.5);

	Substrate substrate(widthPixel, heightPixel, 1, 32, 1.0f, 5.0f);
	//substrate.draw(10000, 100000, seed);
	substrate.drawToScreen();

	substrate.saveImage("./images/SubstrateFinal.png", seed);

	std::cout << double(clock() - startTime) / (double)CLOCKS_PER_SEC << " seconds." << std::endl;

	return 0;
}