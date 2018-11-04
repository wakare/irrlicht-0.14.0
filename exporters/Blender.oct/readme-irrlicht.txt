This directory contains the OCT exporter for BLENDER from OCTTools by Murphy McCauley. 
The whole OCTTools package can be obtained from www.ConstantThought.com.
For more information, read the file readme.txt in the parent directory or 
the original file which references the full OCTTools package:

About
-----
This project contains items for working with OCT files, particularly in Irrlicht and Blender.

OCT is a 3D mesh file format used by the Fluid Studios Radiosity Processor (among other things), and it is well suited for game maps.

You can find out more at http://www.constantthought.com/project/OCTTools .



Redistribution
--------------
You may redistribute this software, but only the original, unmodified zip archive of it.  If you wish to redistribute pieces seperately, or a modified archive, please contact Murphy McCauley.



Contents
--------
oct_export.py - A Blender exporter for OCT files.  www.blender.org

FSRad - A custom build of a radiosity lightmap generator for OCT files by Paul Nettle.  www.FluidStudios.com

COCTLoader - An OCT file loading class for the Irrlicht 3D engine, with support for dynamic lights as well as lightmaps.  irrlicht.sf.net

OCT2OBJ - A commandline OCT to OBJ converter.  In lightmap mode, it will extract the lightmaps and save them as images and create a MTL (OBJ material) file that references them.



Requirements
------------
oct_exporter has been tested only with Blender version 2.36

The FSRad build requires a processor with SSE support.

COCTLoader was built for Irrlicht 0.7.

OCT2OBJ requires the Microsoft Visual Basic 6 Run-Time components, and the FreeImage DLL.  Both are free and should be easily available on www.ConstantThought.com (though they aren't at the moment) and elsewhere on the web.  Try:
http://support.microsoft.com/default.aspx?scid=kb;en-us;290887
http://prdownloads.sourceforge.net/freeimage/FreeImage.zip?download



FSRad
-----
For more information on FSRad (including how to get the original sourcecode), see "FSRad ReadMe.txt" and Paul Nettle's documents documents in the "FSRad Information" folder.



COCTLoader
----------
A bad example of how to load an OCT and enable dynamic lighting:

irr::scene::COCTLoader OCTLoader = irr::scene::COCTLoader(driver);
smgr->addExternalMeshLoader(&OCTLoader);

scene::IAnimatedMesh* mesh = smgr->getMesh(meshName);
smgr->addOctTreeSceneNode(mesh);

// Do this next part if you want dynamic lights
io::IReadFile* file = device->getFileSystem()->createAndOpenFile(meshName);
OCTLoader.OCTLoadLights(file, smgr);
file->drop();



Tips and Tweaking
-----------------
Blender exporter:
The blender exporter contains two values which you can tweak.  I plugged in two numbers which have given me decent results but which I haven't thought about two hard.  These variables are scaleFactor, which scales the geometry, and lightScale, which is multiplied by the the light intensity (0.0 to 1.0) before storing in the OCT.


FSRad:
A lot of it will depend on your source.  Feel free to send tips.
Some numbers that have worked well for me...
Area light multiplier 1000000
Point light multiplier .1
Convergence 1
Limit total iterations 40
Enable the use of the ambient term for estimation of unshot energy
-
Default surface reflectivity .78 .78 .78
-
Lightmap density 8x8
-
Gamma 1.8 - 2.0


COCTLoader:
OCTLoadLights() has two parameters to play around with -- the distance (radius) for lights, and a scale factor.  A scale factor of 0.0000001 would counteract the lightScale in the Blender exporter, but my experience has shown the results are too dark.  To arrive at the values I have, I just tweaked them until I got similar results as with the lightmaps.  Some experimentation or thinking on the subject is really required. :)


OCT2OBJ:
Run without arguments to see options.



Extended OCT Format Support
---------------------------
I've extended the OCT format slightly so that it can do two things it couldn't before.  It should be quite backwards comatible (things that could read the old format should be able to read the new format without using the new information).

First, it can store lightmaps of any size, not just 128x128.  This isn't that great of an advantage, but there it is.

Second, it can store vertex normals.

Of the things in this package, support is currently spotty.  This build of FSRad will write OCTs with any size lightmap, and OCT2OBJ will read OCTs with any size lightmap.  Nothing currently uses the vertex normals.

Note that you don't really get that much out of large lightmaps -- FSRad will just generate more smaller ones if you set the size smaller.  Also, beware of setting them too big.  If they are larger than the largest texture size supported by the video card, they will fail to load!

For more information, see "FSRad ReadMe.txt".



History
-------
1.0.2   Feb 18/2005
	FSRad: Color clamping preserves color correctly
	oct_export.py: Honors object origins
	oct_export.py: Reversed winding / flipped z axis
	COCTLoader.cpp: Swapped lighting axes (to make up for above fix)

1.0.1	Feb 14/2005
	COCTLoader.cpp was swapping red and blue.
	OCT2OBJ was outputting localized numbers.  In locales where a comma is the
        decimal seperator, this caused problems.
	New build of FSRad runs on Linux under WINE.
	oct_export.py now applies transformations to exported meshes.



Thanks
------
Many thanks to Vermeer from the Irrlicht messageboard for his invaluable help testing.



Murphy McCauley
www.ConstantThought.com
February 2005