#include "Precompiled.hpp"

#include <fstream>
#include <set>
#include <vector>

#include "Artist.hpp"

// common colours
const Colour Artist::white = Colour(255, 255, 255, 255);
const Colour Artist::black = Colour(0, 0, 0, 255);
const Colour Artist::grey = Colour(127, 127, 127, 255);
const Colour Artist::darkGrey = Colour(64, 64, 64, 255);

const Colour Artist::red = Colour(255, 0, 0, 255);
const Colour Artist::green = Colour(0, 255, 0, 255);
const Colour Artist::blue = Colour(0, 0, 255, 255);

void Artist::saveFrame(Image& image, const std::string& filename, unsigned int seed)
{
	static uint frameNum = 0;

	char frameBuffer[30];
	itoa(frameNum, frameBuffer, 10);
	std::string frameStr = filename.substr(0, filename.rfind('.')) + std::string(frameBuffer) + filename.substr(filename.rfind('.'));

	save(image, frameStr, seed);

	frameNum++;
}

void Artist::save(Image& image, const std::string& filename, unsigned int seed, bool bSigInImage)
{
	std::string signatureLine("DHP 2013");
	uint signatureOffset = 40;
	if(seed != 0)
	{
		char seedBuffer[30];
		itoa(seed, seedBuffer, 10);
		signatureLine += std::string(" - ") + std::string(seedBuffer);

		signatureOffset += 80;
	}

	if(bSigInImage)
		image.draw_text(image.width() - signatureOffset, image.height() - 15, signatureLine.c_str(), grey.colour(), 8);
	else
	{
		std::ofstream fout;
		std::string sigFile = filename + ".txt";
		fout.open(sigFile.c_str());

		fout << "DHP 2013";
		if(seed != 0)
			fout << " - " << seed;
		fout << std::endl;

		fout.close(); 
	}

	image.save_bmp(filename.c_str());
}

void Artist::extractPalette(const std::string& filename, std::vector<Colour>& palette)
{
	Image source(filename.c_str());

	// find unique colours in source image
	std::set< Colour > uniqueColours;
	for(int x = 0; x < source.width(); ++x)
	{
		for(int y = 0; y < source.height(); ++y)
		{
			std::vector<unsigned char> colour(source.spectrum());
			for(int c = 0; c < source.spectrum(); ++c)
				colour[c] = *source.data(x, y, 0, c);

			uniqueColours.insert(Colour(colour, 255));
		}
	}

	// filter to a set of distinct colours
	int colourThreshold = 25;
	std::set< Colour >::iterator it;
	for(it = uniqueColours.begin(); it != uniqueColours.end(); ++it)
	{
		Colour colour = *it;

		bool bUnique = true;
		for(unsigned int i = 0; i < palette.size(); ++i)
		{
			int similarityCount = 0;
			for(int c = 0; c < source.spectrum(); ++c)
			{
				if(abs(colour.spectrum(c) - palette[i].spectrum(c)) < colourThreshold)
					similarityCount++;
			}

			if(similarityCount == source.spectrum())
			{
				bUnique = false;
				break;
			}
		}

		if(bUnique)
			palette.push_back(colour);
	}
}

void Artist::savePalette(const std::string& filename, const std::vector<Colour>& palette)
{
	Image image(palette.size(), 1, 1, 3, 255);
	for(uint x = 0; x < palette.size(); ++x)
		image.draw_point(x, 0, 0, palette[x].colour());

	image.save(filename.c_str());
}