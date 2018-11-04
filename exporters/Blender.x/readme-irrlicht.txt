This directory contains the .X exporter for BLENDER created by Ben Omari and Jonas Petersen which
is hosted on http://development.mindfloaters.de/DirectX_Exporter_Mod.8.0.html.
For more information read the file readme.txt in the parent directory 
or the original readme file of this package:


DirectX Exporter Mod

This is a modification of the famous DirectX8Exporter by Ben Omari. Lots of credits go to him here. He has worked long and hard to get a fine exporter. Unfortunately it wasn't always bringing me the results I needed, especially in conjunction with the Irrlicht 3D Engine. So I began to modify it. The aim was to create a comfortabe, stable and configurable exporter that produces well formated and accurate DirectX files that ideally get loaded in any application.

It is based on the original version by Ben from Jun-20-2004 for Blender 2.34.

 

Here is the list of changes that I've made to it so far:

 
Version history (latest first)

Version 1.3.1 - May 20th 2005

    * Added check for SubSurf meshes. SubSurf meshes must be converted to polygon meshes before exporting. I might add support for exporting SubSurf meshes later.
 

Version 1.3 - April 24th 2005

    * Fixed problem with animations that have a modified pose at frame 1 (see Version 1.2.1). Fix provided by Ben Omari, thanks a lot!
    * Fixed bug where error may occur with meshes that have no texture. Fix also provided by Ben Omari, thanks another lot!
    * Fixed bug where exception occurs when a mesh has uv coords and contains vertices that does not belong to any face. Thanks Trident from the Irrlicht forums for reporting!


Version 1.2.1 - November 3rd 2004

    * Again (This time really... :) ) fixed bug with the 'Flip Z axis' switch (would internally sometimes not be set correctly).
    * Fixed export of animations that have startframe > 1 ("Anim" buttons panel).
    * Still working on the problem with animations that have a modified pose at frame 1.

 

Version 1.2 - October 5rd 2004

    * Added a 'swap Y/Z axis' option which is active by default. Now the conversion from Blender (right handed, z axis top/bottom) to DirectX (left handed, z axis front/back) coordinate system is complete and appropriate.
    * Now all selected mesh objects get exported (selected objects of other types will be ignored). Parented aramatures are detected and exported with their objects (possibly including animations).
    * Added a progess bar to the 'recalc vertex normals' and 'export animation' functions (because they can take some time).
    * The script will fire a beep sound if the export took longer then 0.8 seconds (configurable) :)
    * Fixed the indentation (tab spacing). The blocks of the exported .x file are now properly formatted according to their hirarchy.
    * Now a nice result message box with useful information is written to the console after exporting.
    * Added some warning popups where appropriate.
    * Fixed MeshMaterialList export structure (one semi-colon too much would get exported).
    * Finally fixed export of the XSkinMeshHeader. In worst case DirectX Mesh Viewer would crash if mesh had less SkinWeight items than nBones in the XSkinMeshHeader. Reimplemented calculation of all three values: 'nBones', 'nMaxSkinWeightsPerVertex' and 'nMaxSkinWeightsPerFace'.
    * Added a comment with the Blender version and script version to the exported file.
    * Fixed bug with the 'Flip Z axis' switch (would internally sometimes not be set correctly).
    * Re-layouted the gui and gave all buttons tool tips (mouseover help).
    * Added a 'Reset default' button to the gui
    * The script now remembers the last filename and offers it in the submenu and the in gui for direct saving to (overwriting) the last file. (note: the gui part is disabled in this release because of a problem)

 

Version 1.1 - September 23rd 2004

    * Added proper right to left handed coordinate system conversion by adjusting all exported matrices and coordinates (as opposed to just scaling the root matrix by -1 in the Z axis).
    * Added animation speed option. It can be chosen from 'DirectX speed' in frames per second (base is 4800 ticks per second) or frame number based animation.
    * Now periods (".") get replaced by underscores ("_") also in the animation part of the export.
    * Made file handling saver by always closing opened file even when errors occur.
    * Switched positions of buttons 'Export' and 'Exit'.
    * Fixed bug in the armature hirarchy export.

 

Version 1.0b - September 20th 2004

    * Fixed typo that causes python error.
    * Version 1.0a - September 20th 2004
    * Meshes without an armature are now exported properly (not writing one closing bracket too much anymore).
    * Flip faces is now OFF by default.
    * Version 1.0 - September 19th 2004
    * Initial release of the modification.

 

Version 1.0 - September 19th 2004 (initial release)

    * Added a configure screen with the following options:
         1. Inverse Normals (inverts the direction of the vertex normals).
         2. Flip Faces (flips the faces by reversing the order of the face's vertices).
         3. 'Export XSkinMeshHeader' Turning it of helped me once loading files into MView).
         4. Export animations or not.
         5. Flip Z Axis (of the mesh coordinates).
         6. Recalculate vertex normals (useful if Blender does not generate proper vertex normals). Can be time consuming on bigger meshes.
         7. Reset origin to (0,0,0).
         8. The settings are remembered througout one Blender session.
    * Changed the format strings to use '%f' instead of '%s' to export floats because it would sometimes write floats in some 'exponent mantissa' form (like '1e-005' instead of '0.00001') that makes it impossible to load it into the DirectX Mesh viewer. Also changed '%s' to '%d' wherever integers get exported.
    * Periods (".") in names of materials and bones are converted automatically into underscores ("_").
    * Meshes without an armature now get exported as well.
    * Texture mapping gets fixed by adding appropriate additional vertices. Mesh coordinates, normals and weights are adjusted.

 

Exported files have been tested with Microsoft DirectX Mesh Viewer (MView.exe) version 1.0 and version 5.4 and the Irrlicht 3D engine version 6.0, 7.0.1 (http://irrlicht.sourceforge.net). I also have reports that it works well with many other applications as well.
	
	
