#ifndef ARTIST_HPP
#define ARTIST_HPP

#include "Tools.hpp"
#include "Colour.hpp"

#include "CImg.h"
using namespace cimg_library;

class Artist
{
public:
	// common colours
	static const Colour white;
	static const Colour black;
	static const Colour grey;
	static const Colour darkGrey;

	static const Colour red;
	static const Colour green;
	static const Colour blue;

public:
	// common functions
	static void saveFrame(Image& image, const std::string& filename, unsigned int seed = 0);
	static void save(Image& image, const std::string& filename, unsigned int seed = 0, bool bSigInImage = false);

	static void extractPalette(const std::string& filename, std::vector<Colour>& palette);
	static void savePalette(const std::string& filename, const std::vector<Colour>& palette);
};

#endif