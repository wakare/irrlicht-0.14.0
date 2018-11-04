Irrlicht can natively read and import lots of common 3d formats of various 3d packages.
However, to make content creation even easier, this directory contains some exporters 
for Blender, Giles[s], 3DSMAX 5, 3DSMAX 6, and 3DSMAX 7 which export 3d data into
files irrlicht can read.

Exporters:

----------------------------------------------------------------------------------
Format               3D Package                      Notes
----------------------------------------------------------------------------------
.x                   Blender            Contains an .X file exporter for Blender 
                                        which was optimized for use with Irrlicht 
                                        because it can import .X files directly. 
                                        It is based on the exporter by Ben Omari 
                                        and was highly modified by Jonas Petersen.
                                        Thanks! Updates of this exporter can be 
                                        obtained from development.mindfloaters.de                                            

.my3d                Gile[s] 3.1,       Contains exporters for Zhuck Dimitry's 
                     3DSMAX 5,          my3D file format. He also wrote a loader for
                     3DSMAX 6,          Irrlicht for this format which was integrated
                     3DSMAX 7           since version 0.9, so Irrlicht is able to
                                        import these files directly. The original
                                        my3d package can be obtained from 
                                        my3dproject.nm.ru

.oct                 Blender, Fluid     Contains an OCT exporter for Blender which 
                     Radiosity Studios  was created by Murphy McCauley. Thanks to 
                     Processor          him, Irrlicht can also import .OCT files 
                                        directly. The OCT file format is used by the
                                        Radiosity Processor by Paul Nettle. New
                                        versions of this exporter and the full 
                                        OCTTOOLS package can be downloaded from
                                        www.constantthought.com

==================================================================================
Importers:

Irrlicht was originally written to work without exporters and is able to read 
3D data from various 3D packages directly. In this way, data is never 
needed to be converted for using it with the Irrlicht Engine, saving development 
time. The list of all supported formats is constantly growing. Currently Irrlicht 
supports meshes of the following formats directly:

----------------------------------------------------------------------------------
Importer                                  Notes
----------------------------------------------------------------------------------
3D Studio (.3ds)           Loader for 3D-Studio files which lots of 3D packages 
                           are able to export. Only static meshes are 
                           currently supported by this importer. 
                           
Cartography shop 4 (.csm)  Cartography Shop is a modeling program for creating 
                           architecture and calculating lighting. Irrlicht can directly
                           import .csm files thanks to the IrrCSM library created
                           by Saurav Mohapatra which is now integrated directly in 
                           Irrlicht. If you are using this loader, please note that
                           you'll have to set the path of the textures before loading
                           .csm files. You can do this using 
                           SceneManager->getStringParameters()->setParameter(
                           scene::CSM_TEXTURE_PATH, "path/to/your/textures");
                           
COLLADA (.dae, .xml)       COLLADA is an open Digital Asset Exchange Schema for the 
                           interactive 3D industry. There are exporters and importers for
                           this format available for most of the big 3d packages at 
                           http://collada.org. Irrlicht can import COLLADA files by 
                           using the ISceneManager::getMesh() method. As COLLADA need 
                           not contain only one single mesh but multiple meshes and a whole 
                           scene setup with lights, cameras and mesh instances, this loader 
                           sets up a scene as described by the COLLADA file instead of 
                           oading and returning one mesh. Created scene nodes will be 
                           named as the names of the nodes in the COLLADA file. The 
                           returned mesh is just a dummy object. However, if the COLLADA
                           file does not include any <instance> tags, only meshes will 
                           be loaded by the engine and no scene nodes should be created.
                           Meshes included in the scene will be added into the scene 
                           manager with the following naming scheme: 
                           path/to/file/file.dea#meshname. The loading of such meshes is
                           logged. Currently, this loader is able to create meshes (made of 
                           only polygons), lights, and cameras. Materials and animations 
                           are currently not supported but this will change with future 
                           releases. 
                           
Delgine DeleD (.dmf)       DeleD (delgine.com) is a 3D editor and level-editor combined 
                           into one and is specifically designed for 3D game-development. 
                           With this loader, it is possible to directly load all geometry 
                           is as well as textures and lightmaps from .dmf files. The loader 
                           is based on Salvatore Russo's .dmf loader, I just changed some 
                           parts of it. Thanks to Salvatore for his work and for allowing me 
                           to use his code in Irrlicht and put it under Irrlicht's license. 
                           For newer and more enchanced versions of the loader, take a look 
                           at delgine.com. 
                           
DirectX (.x)               Platform independent importer (so not D3D-only) for .x 
                           files. Most 3D packages can export these natively and 
                           there are several tools for them available. (e.g.
                           the Maya exporter included in the DX SDK) .x files can
                           include skeletal animations and Irrlicht is able to 
                           play and display them. Currently, Irrlicht only supports
                           text encoded .x files.
                           
Maya (.obj)                Most 3D software can create .obj files which contain
                           static geometry without material data. This importer 
                           for Irrlicht can load them directly. 
                           
Milkshape (.ms3d)          .MS3D files contain models and sometimes skeletal 
                           animations from the Milkshape 3D modeling and animation 
                           software. This importer for Irrlicht can display and/or 
                           animate these files. 
                           
My3D (.my3d)               .my3D is a flexible 3D file format. The My3DTools contains
                           plug-ins to export .my3D files from several 3D packages.
                           With this built-in importer, Irrlicht can read and display 
                           those files directly. This loader was written by Zhuck 
                           Dimitry who also created the whole My3DTools package.
                           If you are using this loader, please note that you can set
                           the path of the textures before loading .my3d files. You can 
                           do this using SceneManager->getStringParameters()->
                           setParameter(scene::MY3D_TEXTURE_PATH, "path/to/your/textures"); 
                           
OCT (.oct)                 The oct file format contains 3D geometry and lightmaps and 
                           can be loaded directly by Irrlicht. OCT files
                           can be created by FSRad, Paul Nette's radiosity processor or
                           exported from Blender using OCTTools which can be found in 
                           the exporters\OCTTools directory of the SDK. Thanks to 
                           Murphy McCauley for creating all this.
                           
Pulsar LMTools (.lmts)     LMTools is a set of tools (Windows & Linux) for creating 
                           lightmaps. Irrlicht can directly read .lmts files thanks to
                           the importer created by Jonas Petersen. 
                           If you are using this loader, please note that
                           you can set the path of the textures before loading
                           .lmts files. You can do this using 
                           SceneManager->getStringParameters()->setParameter(
                           scene::LMTS_TEXTURE_PATH, "path/to/your/textures"); Notes for
                           this version of the loader:
                           - It does not recognice/support user data in the *.lmts files.
			   - The TGAs generated by LMTools don't work in Irrlicht
			    for some reason (the textures are upside down). Opening and resaving 
			    them in a graphics app will solve the problem.
                           
Quake 3 levels (.bsp)      Quake 3 is a popular game by IDSoftware, and .pk3 files
                           contain .bsp files and textures/lightmaps describing huge
                           prelighted levels. Irrlicht can read .pk3 and .bsp files
                           directly and thus render Quake 3 levels directly. Written
                           by Nikolaus Gebhardt enhanced by Dean P. Macri with the 
                           curved surfaces feature.

Quake 2 models (.md2)      Quake 2 models are characters with morph target animation.
                           Irrlicht can read, display and animate them directly with
                           this importer. 
                           
                           
                           
                           
