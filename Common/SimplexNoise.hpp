// SimplexNoise1234
// Copyright © 2003-2011, Stefan Gustavson
//
// Contact: stegu@itn.liu.se
//
// This library is public domain software, released by the author
// into the public domain in February 2011. You may do anything
// you like with it. You may even remove all attributions,
// but of course I'd appreciate it if you kept my name somewhere.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// General Public License for more details.

/** \file
		\brief Declares the SimplexNoise1234 class for producing Perlin simplex noise.
		\author Stefan Gustavson (stegu@itn.liu.se)
*/

/*
 * This is a clean, fast, modern and free Perlin Simplex noise class in C++.
 * Being a stand-alone class with no external dependencies, it is
 * highly reusable without source code modifications.
 *
 *
 * Note:
 * Replacing the "float" type with "double" can actually make this run faster
 * on some platforms. A templatized version of SimplexNoise1234 could be useful.
 */

class SimplexNoise 
{
public:
	SimplexNoise() {}
	~SimplexNoise() {}

	/** Perlin noise */
	static float SimplexNoise::noise( float x );
	static float SimplexNoise::noise( float x, float y );

	/** Perlin noise, with a specified integer period */
    static float SimplexNoise::pnoise( float x, int px );
    static float SimplexNoise::pnoise( float x, float y, int px, int py );

private:
	static unsigned char SimplexNoise::perm[];
	static float  SimplexNoise::grad( int hash, float x );
	static float  SimplexNoise::grad( int hash, float x, float y );
};
