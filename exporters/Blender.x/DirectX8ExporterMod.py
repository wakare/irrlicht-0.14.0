#!BPY

""" Registration info for Blender menus:
Name: 'DirectX8 mod1.3.1 (.x)...'
Blender: 234
Group: 'Export'
Tip: 'Export to DirectX8 text file format format.'
"""


# DirectX8ExporterMod.py version 1.3.1
# Modification (c) 2004 by Jonas Petersen (jonas at mindfloaters dot de)
# http://development.mindfloaters.de/
MOD_VERSION = '1.3.1'
#
# DirectX8Exporter.py version 1.0
# Copyright (C) 2003  Arben OMARI -- omariarben@everyday.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# This script export meshes created with Blender in DirectX8 file format
# it exports meshes,armatures,materials,normals,texturecoords and animations

# Grab the latest version here :www.omariben.too.it


# ABOUT THIS MODIFICATION:
##########################
#
# This is a modified version by Jonas Petersen (jonas at mindfloaters dot de).
# It is based on the original version by Arben Omari from Jun-20-2004 for Blender 2.34.
#
# Btw. this is my local CVS, not the Blender CVS.
# $Id: DirectX8ExporterMod.py,v 1.21 2005/05/20 15:20:03 Jonas Exp $
#
# --
#
# Version history (of the modification):
#
# Version 1.3.1 - May 20th 2005
#   - Added check for SubSurf meshes. SubSurf meshes must be converted to
#     polygon meshes before exporting. I might add support for exporting
#     SubSurf meshes later.
#
# Version 1.3 - April 24th 2005
#   - Fixed problem with animations that have a modified pose at frame 1
#     (see Version 1.2.1). Fix provided by Ben Omari, thanks a lot!
#   - Fixed bug where error may occur with meshes that have no texture.
#     Fix also provided by Ben Omari, thanks another lot!
#   - Fixed bug where exception occurs when a mesh has uv coords and
#     contains vertices that does not belong to any face.
#     Thanks Trident from the Irrlicht forums for reporting!
#
# Version 1.2.1 - November 3rd 2004
#   - Again (This time really... :) ) fixed bug with the 'Flip Z axis'
#     switch (would internally sometimes not be set correctly).
#   - Fixed export of animations that have startframe > 1 ("Anim" buttons panel).
#   - Still working on the problem with animations that have a modified
#     pose at frame 1.
#
# Version 1.2 - October 5rd 2004
#   - Added a 'swap Y/Z axis' option which is active by default.
#     Now the conversion from Blender (right handed, z axis top/bottom)
#     to DirectX (left handed, z axis front/back) coordinate system
#     is complete and appropriate.
#   - Now all selected mesh objects get exported (selected objects of other
#     types will be ignored). Parented aramatures are detected and exported
#     with their objects (possibly including animations).
#   - Added a progess bar to the 'recalc vertex normals' and
#     'export animation' functions (because they can take some time).
#   - The script will fire a beep sound if the export took longer then
#     0.8 seconds (configurable) :)
#   - Fixed the indentation (tab spacing). The blocks of the exported .x file
#     are now properly formatted according to their hirarchy.
#   - Now a nice result message box with useful information is written to the
#     console after exporting.
#   - Added some warning popups where appropriate.
#   - Fixed MeshMaterialList export structure (one semi-colon too much
#     would get exported).
#   - Finally fixed export of the XSkinMeshHeader. In worst case
#     DirectX Mesh Viewer would crash if mesh had less SkinWeight
#     items than nBones in the XSkinMeshHeader.
#     Reimplemented calculation of all three values:
#     'nBones', 'nMaxSkinWeightsPerVertex' and 'nMaxSkinWeightsPerFace'.
#   - Added a comment with the Blender version and script version to the
#     exported file.
#   - Fixed bug with the 'Flip Z axis' switch (would internally sometimes
#     not be set correctly).
#   - Re-layouted the gui and gave all buttons tool tips (mouseover help).
#   - Added a 'Reset default' button to the gui
#   - The script now remembers the last filename and offers it in the submenu
#     and the in gui for direct saving to (overwriting) the last file.
#     (note: the gui part is disabled in this release because of a problem)
#
# Version 1.1 - September 23rd 2004
#   - Added proper right to left handed coordinate system
#     conversion by adjusting all exported matrices and coordinates
#     (as opposed to just scaling the root matrix by -1 in the Z axis).
#   - Added animation speed option. It can be chosen from
#     'DirectX speed' in frames per second (base is 4800 ticks
#     per second) or frame number based animation.
#   - Now periods (".") get replaced by underscores ("_")
#     also in the animation part of the export.
#   - Made file handling saver by always closing opened file
#     even when errors occur.
#   - Switched positions of buttons 'Export' and 'Exit'.
#   - Fixed bug in the armature hirarchy export.
#
# Version 1.0b - September 20th 2004
#   - Fixed typo that causes python error.
#
# Version 1.0a - September 20th 2004
#   - Meshes without an armature are now exported properly
#     (not writing one closing bracket too much anymore).
#   - Flip faces is now OFF by default.
#
# Version 1.0 - September 19th 2004
#   - Initial release of the modification.
#
# --
#
# Modification Version 1.0 changes:
#
# 1) Added a configure screen with the following options:
#
#     - Inverse Normals (inverts the direction
#       of the vertex normals).
#
#     - Flip Faces (flips the faces by reversing
#       the order of the face's vertices).
#
#     - 'Export XSkinMeshHeader' Turning it of helped me once loading
#       files into MView).
#
#     - Export animations or not.
#
#     - Flip Z Axis (of the mesh coordinates).
#
#     - Recalculate vertex normals (useful if Blender does not
#       generate proper vertex normals). Can be time consuming
#       on bigger meshes.
#
#     - Reset origin to (0,0,0).
#
#    The settings are remembered througout one Blender session.
#
# 2) Changed the format strings to use '%f' instead of '%s' to export floats
#    because it would sometimes write floats in some 'exponent mantissa' form
#    (like '1e-005' instead of '0.00001') that makes it impossible to load
#    it into the DirectX Mesh viewer. Also changed '%s' to '%d'
#    wherever integers get exported.
#
# 3) Periods (".") in names of materials and bones are converted automatically
#    into underscores ("_").
#
# 4) Meshes without an armature now get exported as well.
#
# 5) Texture mapping gets fixed by adding appropriate additional vertices.
#    Mesh coordinates, normals and weights are adjusted.
#
# Exported files have been tested with Microsoft DirectX Mesh Viewer (MView.exe)
# version 1.0 and version 5.4 and the Irrlicht 3D engine version 6.0, 7.0.1
# (http://irrlicht.sourceforge.net).
#
# The latest version of this modification can be found here:
# http://www.mindfloaters.de/blender/
#
#
#
# TODO:
# - Assign correct object and mesh names to Frame and Mesh blocks
# - Add material if it has none (if not mesh.materials: mesh.materials.append(Material.New()))
# - Write animation frames in info


####################################################################
#                                                                  #
#               Default configuration settings                     #
#                                                                  #
####################################################################

DEF_SWAP_YZ_AXIS           = 1
DEF_FLIP_Z_AXIS            = 0
DEF_FLIP_FACES             = 1
DEF_INVERT_NORMALS         = 0
DEF_EXPORT_XSKINMESHHEADER = 1

DEF_RECALC_VERTEX_NORMALS  = 0
DEF_RESET_ORIGIN           = 0
DEF_EXPORT_ANIMATIONS      = 0
DEF_EXPORT_DX_SPEED        = 1
DEF_FRAMES_PER_SECOND      = 25

# BEEP_WHEN_FINISHED:
# set it to 0 to disable beeping.
# set it to -1 to beep always at finish.
# set it to a float value greater then 0.0 to beep only if
# the export took longer than then the given value in seconds. :)
BEEP_WHEN_FINISHED = 0.8

####################################################################
#                                                                  #
#            End of default configuration settings                 #
#                                                                  #
####################################################################



import Blender
from Blender import Types, Object, NMesh, Material,Armature
from Blender.Mathutils import *

import time, os, sys, mod_meshtools

import string
from string import replace

import math

SHOW_PROGRESS_BAR = 1
PROGRESS_BAR_STEPS = 20

global SWAP_YZ_AXIS, FLIP_Z_AXIS, FLIP_FACES, INVERT_NORMALS, EXPORT_XSKINMESHHEADER
global RECALC_VERTEX_NORMALS, RESET_ORIGIN, EXPORT_ANIMATIONS, EXPORT_DX_SPEED, FRAMES_PER_SECOND
global CURRENT_FILENAME

DIRECT_X_TICKS_PER_SECOND = 4800

CURRENT_FILENAME = ""

new_verts_uv = {}
new_verts = {}
new_faces = []
new_normals = []
duplicates = {}

def updateZMUL():
	global FLIP_Z_AXIS, ZMUL
	if FLIP_Z_AXIS: ZMUL = -1.0
	else: ZMUL = 1.0

def resetDefaultConfig():
	global SWAP_YZ_AXIS, FLIP_Z_AXIS, FLIP_FACES, INVERT_NORMALS, EXPORT_XSKINMESHHEADER
	global RECALC_VERTEX_NORMALS, RESET_ORIGIN, EXPORT_ANIMATIONS, EXPORT_DX_SPEED, FRAMES_PER_SECOND

	SWAP_YZ_AXIS           = DEF_SWAP_YZ_AXIS
	FLIP_Z_AXIS            = DEF_FLIP_Z_AXIS
	FLIP_FACES             = DEF_FLIP_FACES
	INVERT_NORMALS         = DEF_INVERT_NORMALS
	EXPORT_XSKINMESHHEADER = DEF_EXPORT_XSKINMESHHEADER
	RECALC_VERTEX_NORMALS  = DEF_RECALC_VERTEX_NORMALS
	RESET_ORIGIN           = DEF_RESET_ORIGIN
	EXPORT_ANIMATIONS      = DEF_EXPORT_ANIMATIONS
	EXPORT_DX_SPEED        = DEF_EXPORT_DX_SPEED
	FRAMES_PER_SECOND      = DEF_FRAMES_PER_SECOND



resetDefaultConfig()

# Looking for a saved key in Blender.Registry dict:
rd = Blender.Registry.GetKey('XExport')
if rd:
	try:
		INVERT_NORMALS = rd['INVERT_NORMALS']
		FLIP_FACES = rd['FLIP_FACES']
		EXPORT_XSKINMESHHEADER = rd['EXPORT_XSKINMESHHEADER']
		EXPORT_ANIMATIONS = rd['EXPORT_ANIMATIONS']
		FLIP_Z_AXIS = rd['FLIP_Z_AXIS']
		RECALC_VERTEX_NORMALS = rd['RECALC_VERTEX_NORMALS']
		RESET_ORIGIN = rd['RESET_ORIGIN']
		FRAMES_PER_SECOND = rd['FRAMES_PER_SECOND']
		EXPORT_DX_SPEED = rd['EXPORT_DX_SPEED']
		SWAP_YZ_AXIS = rd['SWAP_YZ_AXIS']
		CURRENT_FILENAME = rd['CURRENT_FILENAME']
	except:
		pass

updateZMUL()

def update_RegistryInfo():
	d = {}
	d['INVERT_NORMALS'] = INVERT_NORMALS
	d['FLIP_FACES'] = FLIP_FACES
	d['EXPORT_XSKINMESHHEADER'] = EXPORT_XSKINMESHHEADER
	d['EXPORT_ANIMATIONS'] = EXPORT_ANIMATIONS
	d['FLIP_Z_AXIS'] = FLIP_Z_AXIS
	d['RECALC_VERTEX_NORMALS'] = RECALC_VERTEX_NORMALS
	d['RESET_ORIGIN'] = RESET_ORIGIN
	d['FRAMES_PER_SECOND'] = FRAMES_PER_SECOND
	d['EXPORT_DX_SPEED'] = EXPORT_DX_SPEED
	d['SWAP_YZ_AXIS'] = SWAP_YZ_AXIS
	d['CURRENT_FILENAME'] = CURRENT_FILENAME
	Blender.Registry.SetKey('XExport', d)

def draw():
	global INVERT_NORMALS, FLIP_FACES, EXPORT_XSKINMESHHEADER, EXPORT_ANIMATIONS, FLIP_Z_AXIS, SWAP_YZ_AXIS
	global RECALC_VERTEX_NORMALS, RESET_ORIGIN, FPS_BUTTON, FRAMES_PER_SECOND, EXPORT_DX_SPEED

	# clearing screen
	Blender.BGL.glClearColor(0.5, 0.5, 0.5, 1)
	Blender.BGL.glColor3f(1.,1.,1.)
	Blender.BGL.glClear(Blender.BGL.GL_COLOR_BUFFER_BIT)

	#Text
	Blender.BGL.glColor3f(1, 1, 1)

	width, height = Blender.Window.GetAreaSize()

	x = width / 2 - 335 / 2
	y = height / 2 + 330 / 2
	if x < 10: x = 10
	if y < 350: y = 345

	#if False and CURRENT_FILENAME: y = 390
	#else: y = 350

	lh1 = 16
	lh2 = 12

	Blender.BGL.glRasterPos2d(x, y)
	Blender.Draw.Text("DirectX8ExportMod.py - mod version %s"%(MOD_VERSION))
	Blender.BGL.glRasterPos2d(x+1, y)
	Blender.Draw.Text("DirectX8ExportMod.py - mod version %s"%(MOD_VERSION))
	y -= 25
	Blender.BGL.glRasterPos2d(x+10, y)
	Blender.Draw.Text("1. All selected Mesh objects will be exported to one file",'small')
	y -= lh1
	Blender.BGL.glRasterPos2d(x+10, y)
	Blender.Draw.Text("2. Before parenting:",'small')

	y -= lh1
	Blender.BGL.glRasterPos2d(x+10, y)
	Blender.Draw.Text("     a) Make sure armature and mesh have the same origin location",'small')
	y -= lh2
	Blender.BGL.glRasterPos2d(x+10, y)
	Blender.Draw.Text("         (press N for both and set the same LocX, LocY and LocZ)",'small')
	y -= lh1
	Blender.BGL.glRasterPos2d(x+10, y)
	Blender.Draw.Text("     b) Armature and mesh must have the same size and rotation",'small')
	y -= lh2
	Blender.BGL.glRasterPos2d(x+10, y)
	Blender.Draw.Text("         (select them and press Ctrl+A)",'small')
	y -= lh1
	Blender.BGL.glRasterPos2d(x+10, y)
	Blender.Draw.Text("3. Check the number of the animation frames to export",'small')
	y -= lh1
	Blender.BGL.glRasterPos2d(x+10, y)
	Blender.Draw.Text("4. Read confirmation / warnings in the console",'small')

	y -= lh1
	Blender.BGL.glRasterPos2d(x+10, y)
	Blender.Draw.Text("Note: 'Swap Y and Z axis' together with 'Flip faces' is the appropriate", 'small')
	y -= lh2
	Blender.BGL.glRasterPos2d(x+40, y)
	Blender.Draw.Text("conversion from Blender to DirectX coordinate system.", 'small')

	# Buttons
	y -= 40
	col2x = x+170

	Blender.BGL.glRasterPos2d(x, y+10)
	Blender.Draw.Text("Export options:")
	Blender.Draw.Toggle("Flip faces", 4, col2x+80, y+4, 75, 14, FLIP_FACES, "Flips the faces by reversing the vertex order (default: ON). It is neccesary if one of the two options 'Swap Y and Z axis' or 'Flip Z axis' is selected.")
	y -= 22
	Blender.Draw.Toggle("Swap Y and Z axis", 11, col2x, y, 155, 20, SWAP_YZ_AXIS, "Convert from 'Z axis top/bottom' to 'Z axis front/back' (default: ON).")
	Blender.Draw.Toggle("Recalc vertex normals", 8, x, y, 155, 20, RECALC_VERTEX_NORMALS, "Recaculate the vertex normals, may take a while (default: OFF).")
	y -= 22
	Blender.Draw.Toggle("Flip Z axis", 7, col2x, y, 155, 20, FLIP_Z_AXIS, "Left to right hand coordinate system conversion (default: OFF).")
	Blender.Draw.Toggle("Invert vertex normals", 3, x, y, 155, 20, INVERT_NORMALS, "Inverts the vertex normals (default: OFF).")
	y -= 32
	Blender.Draw.Toggle("Export animations", 6, x, y, 155, 20, EXPORT_ANIMATIONS, "Export animations (default: OFF).")
	Blender.Draw.Toggle("Reset origin", 9, col2x, y, 155, 20, RESET_ORIGIN, "Resets the origin (absolute position) to (0,0,0) (default: OFF).")
	y -= 22
	Blender.Draw.Toggle("DX speed", 10, x, y, 95, 20, EXPORT_DX_SPEED, "Export animations in DirectX speed at specified framerate (default: ON). Otherwise animation is frame number based (e.g. for Irrlicht 3D engine).")
	fps = "%d" % (FRAMES_PER_SECOND)
	FPS_BUTTON = Blender.Draw.String("FPS: ", 20, x+100, y, 55, 20, fps, 3, "Animation speed in frames per second (default: 25).")
	Blender.Draw.Toggle("Export xSkinMeshHeader", 5, col2x, y, 155, 20, EXPORT_XSKINMESHHEADER, "Export the xSkinMeshHeader template (default: ON).")

	y -= 40
	Blender.Draw.Button("Export", 2, x, y, 107, 25)
	Blender.Draw.Button("Cancel", 1, x+109, y, 107, 25)
	Blender.Draw.Button("Reset defaults", 21, x+218, y, 107, 25)

	y -= 40
	if False and CURRENT_FILENAME:
		for i in range(2):
			Blender.BGL.glRasterPos2d(x+110+i, y+6)
			len = Blender.Draw.Text(os.path.basename(CURRENT_FILENAME))

		Blender.BGL.glRasterPos2d(x+120+len, y+6)
		current = "( %s )" % (CURRENT_FILENAME)
		Blender.Draw.Text(current)
		Blender.Draw.Button("Export current:", 22, x, y, 100, 25)

def event(evt, val):
	if evt == Blender.Draw.ESCKEY and not val:
		update_RegistryInfo()
		Blender.Draw.Exit()

def bevent(evt):
	global INVERT_NORMALS, FLIP_FACES, EXPORT_XSKINMESHHEADER, EXPORT_ANIMATIONS, FLIP_Z_AXIS, SWAP_YZ_AXIS
	global RECALC_VERTEX_NORMALS, RESET_ORIGIN, FPS_BUTTON, FRAMES_PER_SECOND, EXPORT_DX_SPEED, ZMUL

	if evt == 1: # Cancel
		#update_RegistryInfo()
		Blender.Draw.Exit()
	elif evt == 2: # Export
		update_RegistryInfo()
		Blender.Draw.Exit()
		Blender.Window.FileSelector(my_callback, "Export DirectX8")
	elif evt == 3:
		INVERT_NORMALS = 1 - INVERT_NORMALS
		Blender.Draw.Redraw(1)
	elif evt == 4:
		FLIP_FACES = 1 - FLIP_FACES
		Blender.Draw.Redraw(1)

	elif evt == 5:
		EXPORT_XSKINMESHHEADER = 1 - EXPORT_XSKINMESHHEADER
		Blender.Draw.Redraw(1)
	elif evt == 6:
		EXPORT_ANIMATIONS = 1 - EXPORT_ANIMATIONS
		Blender.Draw.Redraw(1)
	elif evt == 7:
		FLIP_Z_AXIS = 1 - FLIP_Z_AXIS
		if FLIP_Z_AXIS:
			SWAP_YZ_AXIS = 0
			FLIP_FACES = 1
		else: FLIP_FACES = 0
		updateZMUL()
		Blender.Draw.Redraw(1)
	elif evt == 8:
		RECALC_VERTEX_NORMALS = 1 - RECALC_VERTEX_NORMALS
		Blender.Draw.Redraw(1)
	elif evt == 9:
		RESET_ORIGIN = 1 - RESET_ORIGIN
		Blender.Draw.Redraw(1)
	elif evt == 10:
		EXPORT_DX_SPEED = 1 - EXPORT_DX_SPEED
		Blender.Draw.Redraw(1)
	elif evt == 11:
		SWAP_YZ_AXIS = 1 - SWAP_YZ_AXIS
		if SWAP_YZ_AXIS:
			FLIP_Z_AXIS = 0
			FLIP_FACES = 1
		else:
			FLIP_FACES = 0
		updateZMUL()
		Blender.Draw.Redraw(1)

	elif evt == 20:
		try: FRAMES_PER_SECOND = int(FPS_BUTTON.val)
		except: pass
		if FRAMES_PER_SECOND < 1: FRAMES_PER_SECOND = 1
		Blender.Draw.Redraw(1)

	elif evt == 21:
		resetDefaultConfig()
		updateZMUL()
		Blender.Draw.Redraw(1)




#***********************************************
#***********************************************
#                EXPORTER
#***********************************************
#***********************************************

class xExport:
	def __init__(self, filename):
		self.file = open(filename, "w")

#*********************************************************************************************************************************************
	#***********************************************
	#Export Animation
	#***********************************************
	def exportMesh(self, obj, amt_obj):
		global new_verts

		mesh = obj.getData()
		tex = []

		if type(mesh) == Types.NMeshType:
			if RECALC_VERTEX_NORMALS == 1: self.recalcVertexNormals(obj)
			self.findTextures(obj, tex)
			self.createNewVertices(obj, mesh)

			self.openMeshBlock(obj, amt_obj)

			self.writeMeshNormals(obj, mesh)
			self.writeMeshTextureCoords(obj, mesh)
			self.writeMeshMaterialList(obj, mesh, tex)
			if amt_obj: self.writeSkinWeights(amt_obj.getData(), mesh)

			self.closeMeshBlock()

			info = {'name': obj.getName(), 'verts1': len(mesh.verts), 'faces': len(mesh.faces), 'verts2': len(new_verts)}
			if mesh.hasFaceUV(): info['uv'] = "yes"
			else: info['uv'] = "no"
			info['face_types'] = self.face_types

			info['materials'] = len(mesh.materials)

			self.exported_objects.append(info)


	#***********************************************
	#Export Root Bone
	#***********************************************
	def writeRootBone(self):
		global  RESET_ORIGIN, EXPORT_ANIMATIONS
		self.level = 0
		tex = []
		armarture_found = 0
		#print "exporting ..."
		self.writeHeader()

		objects = []
		armatures = []
		self.exported_objects = []

		for obj in Object.GetSelected():
			if obj.getType() == 'Mesh':
				objects.append(obj)
				parent = obj.getParent()
				if parent and parent.getType() == 'Armature':
					armatures.append(parent)
				else:
					armatures.append(False)

		for i in range(len(objects)):
			if armatures[i]:
				obj = objects[i]
				mesh = obj.getData()
				amt = armatures[i].getData()
				Blender.Set('curframe',1)
				amt_mat = armatures[i].getMatrix()

				if RESET_ORIGIN == 1:
					translation = [0, 0, 0, 1]
				else:
					translation = [amt_mat[3][0],amt_mat[3][1],amt_mat[3][2],amt_mat[3][3]]

				mat_o = Matrix([amt_mat[0][0],amt_mat[0][1],amt_mat[0][2],amt_mat[0][3]],
								[amt_mat[1][0],amt_mat[1][1],amt_mat[1][2],amt_mat[1][3]],
								[amt_mat[2][0],amt_mat[2][1],amt_mat[2][2],amt_mat[2][3]],
								translation)

				self.openFrameBlock(mat_o, "RootFrame") # opens "Frame {"

				root_bon = amt.getBones()
				mat_r = self.getCombineMatrix(root_bon[0])
				name_r = root_bon[0].getName()

				self.openFrameBlock(mat_r, name_r) # opens "Frame {"

				self.writeListOfChildrens(root_bon[0])

				self.closeBlock()

				self.exportMesh(obj, armatures[i])

				self.closeBlock()

				if EXPORT_ANIMATIONS == 1:
					self.writeAnimation(amt)
			else:
				self.exportMesh(objects[i], 0)

	#***********************************************
	#Export Children Bones
	#***********************************************
	def writeListOfChildrens(self,bon):
		bon_c = bon.getChildren()
		Blender.Set('curframe',1)
		for n in range(len(bon_c)):
			name_h = bon_c[n].getName()
			chi_h = bon_c[n].getChildren()

		for nch in range(len(bon_c)):
			mat = self.getCombineMatrix(bon_c[nch])
			name_ch = bon_c[nch].getName()
			self.openFrameBlock(mat, name_ch)

			self.recurseChildren(bon_c[nch])

			self.closeBlock()


	#***********************************************
	#Create Children structure
	#***********************************************
	def recurseChildren(self,bon_c):
		bon_cc = bon_c
		self.writeListOfChildrens(bon_cc)


	#***********************************************
	#Offset Matrix
	#***********************************************
	def getMatrixOffset(self,bon):
		Blender.Set('curframe',1)
		mat_b = bon.getRestMatrix()
		mat_b.invert()
		return mat_b




	#***********************************************
	#Combine Matrix
	#***********************************************
	def getCombineMatrix(self,bon):
		Blender.Set('curframe',1)
		mat_b = bon.getRestMatrix()
		if bon.hasParent():
			pare = bon.getParent()
			mat_p = pare.getRestMatrix()
		else :
			mat_p = Matrix([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1])
		mat_p.invert()
		mat_rb = mat_b * mat_p
		return mat_rb

	#***********************************************
	#Combine Matrix
	#***********************************************
	def getCombineAnimMatrix(self,bon):

		mat_b = bon.getRestMatrix()
		if bon.hasParent():
			pare = bon.getParent()
			mat_p = pare.getRestMatrix()
		else :
			mat_p = Matrix([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1])
		mat_p.invert()
		mat_rb = mat_b * mat_p
		return mat_rb


#*********************************************************************************************************************************************
	#***********************************************
	#Write SkinWeights
	#***********************************************
	def writeSkinWeights(self, amt, mesh):
		global mat_dict, EXPORT_XSKINMESHHEADER, new_verts, duplicates
		Blender.Set('curframe',1)

		if EXPORT_XSKINMESHHEADER == 1:
			nMaxSkinWeightsPerVertex = 0
			nMaxSkinWeightsPerFace = 0
			nBones = 0

			vert_weight_count = {}

			# calculate nBones and nMaxSkinWeightsPerVertex

			for bo in amt.getBones() :
				name = bo.getName()

				vert_list = False
				try : vert_list = mesh.getVertsFromGroup(name)
				except: pass
				if vert_list:
					nBones += 1
					for inde in vert_list:
						if vert_weight_count.has_key(inde): vert_weight_count[inde].append(name)
						else: vert_weight_count[inde] = [name]

			for bonename_list in vert_weight_count.values():
				num = len(bonename_list)
				if num > nMaxSkinWeightsPerVertex:
					nMaxSkinWeightsPerVertex = num

#						vert_infl = mesh.getVertexInfluences(inde)
#						ln_infl = len(vert_infl)
#						if ln_infl > max_infl :
#							max_infl = ln_infl

			# calculate nMaxSkinWeightsPerFace

			for face in mesh.faces:
				tmp_list = []
				for v in face.v:
					for bone_name in vert_weight_count[v.index]:
						if not bone_name in tmp_list:
							tmp_list.append(bone_name)
				if len(tmp_list) > nMaxSkinWeightsPerFace:
					nMaxSkinWeightsPerFace = len(tmp_list)


			self.file_indent()
			self.file.write("XSkinMeshHeader {\n")
			self.indent(1)
			self.file_indent()
			self.file.write("%d;\n" % (nMaxSkinWeightsPerVertex))
			self.file_indent()
			self.file.write("%d;\n" % (nMaxSkinWeightsPerFace))
			self.file_indent()
			self.file.write("%d;\n" % (nBones))
			self.closeBlock()

		for bo in amt.getBones() :
			name = bo.getName()

			fixed_name = replace(name, ".", "_")

			vert_list = False

			try :
				vert_list = mesh.getVertsFromGroup(name,1)
			except:
				pass

			if vert_list:
				# calc new list
				count = 0
				new_vert_list = []
				for ind in vert_list :
					new_vert_list.append(ind[0])
					if duplicates.has_key(ind[0]):
						for dup in duplicates[ind[0]]:
							new_vert_list.append(dup)

				#vert_list = mesh.getVertsFromGroup(name,1)

				# open SkinWeights

				self.file_indent()
				self.file.write("SkinWeights {\n")

				self.indent(1)
				self.file_indent()
				self.file.write("\"%s\";\n" % (fixed_name))
				self.file_indent()
				self.file.write("%d;\n" % (len(new_vert_list)))
				count = 0
				for ind in new_vert_list :
					count += 1
					self.file_indent()
					if count == len(new_vert_list):
						self.file.write("%d;\n" % (ind))
					else :
						self.file.write("%d,\n" % (ind))
				cou = 0
				for ind in new_vert_list :
					cou += 1
					ver_infl = mesh.getVertexInfluences(new_verts[ind])

					len_infl = float(len(ver_infl))
					if len_infl != 0.0:
						infl = 1 / len_infl
					else:
						infl = 0.0

					self.file_indent()
					if cou == len(new_vert_list):
						self.file.write("%f;\n" % (round(infl,6)))
					else :
						self.file.write("%f,\n" % (round(infl,6)))


				matx = self.getMatrixOffset(bo)

				self.writeOffsFrames(matx, name)

				# close SkinWeights
				self.closeBlock()



	#***********************************************
	# Write Matrices
	#***********************************************
	def openFrameBlock(self, matx, name):
		global ZMUL, SWAP_YZ_AXIS

		fixed_name = replace(name, ".", "_")

		self.file_indent()
		self.file.write("Frame ")
		self.file.write("%s {\n\n" % (fixed_name))

		self.indent(1)

		self.file_indent()
		self.file.write("FrameTransformMatrix {\n")

		self.indent(1)

		if SWAP_YZ_AXIS:
			self.file_indent()
			self.file.write("%f,%f,%f,%f,\n" % (round(matx[0][0],4),round(ZMUL*matx[0][2],4),round(matx[0][1],4),round(matx[0][3],4)))
			self.file_indent()
			self.file.write("%f,%f,%f,%f,\n" % (round(ZMUL*matx[2][0],4),round(matx[2][2],4),round(ZMUL*matx[2][1],4),round(ZMUL*matx[2][3],4)))
			self.file_indent()
			self.file.write("%f,%f,%f,%f,\n" % (round(matx[1][0],4),round(ZMUL*matx[1][2],4),round(matx[1][1],4),round(matx[1][3],4)))
			self.file_indent()
			self.file.write("%f,%f,%f,%f;;\n"% (round(matx[3][0],4),round(ZMUL*matx[3][2],4),round(matx[3][1],4),round(matx[3][3],6)))
		else:
			self.file_indent()
			self.file.write("%f,%f,%f,%f,\n" % (round(matx[0][0],4),round(matx[0][1],4),round(ZMUL*matx[0][2],4),round(matx[0][3],4)))
			self.file_indent()
			self.file.write("%f,%f,%f,%f,\n" % (round(matx[1][0],4),round(matx[1][1],4),round(ZMUL*matx[1][2],4),round(matx[1][3],4)))
			self.file_indent()
			self.file.write("%f,%f,%f,%f,\n" % (round(ZMUL*matx[2][0],4),round(ZMUL*matx[2][1],4),round(matx[2][2],4),round(ZMUL*matx[2][3],4)))
			self.file_indent()
			self.file.write("%f,%f,%f,%f;;\n"% (round(matx[3][0],4),round(matx[3][1],4),round(ZMUL*matx[3][2],4),round(matx[3][3],6)))

		self.closeBlock()

	#***********************************************
	# Write Matrices
	#***********************************************
	def writeOffsFrames(self, matx, name):
		global ZMUL, SWAP_YZ_AXIS

		self.file_indent()
		if SWAP_YZ_AXIS:
			self.file.write("%f,%f,%f,%f," % (round(matx[0][0],4),round(ZMUL*matx[0][2],4),round(matx[0][1],4),round(matx[0][3],4)))
			self.file.write("%f,%f,%f,%f," % (round(ZMUL*matx[2][0],4),round(matx[2][2],4),round(ZMUL*matx[2][1],4),round(ZMUL*matx[2][3],4)))
			self.file.write("%f,%f,%f,%f," % (round(matx[1][0],4),round(ZMUL*matx[1][2],4),round(matx[1][1],4),round(matx[1][3],4)))
			self.file.write("%f,%f,%f,%f;;\n"% (round(matx[3][0],4),round(ZMUL*matx[3][2],4),round(matx[3][1],4),round(matx[3][3],6)))
		else:
			self.file.write("%f,%f,%f,%f," % (round(matx[0][0],4),round(matx[0][1],4),round(ZMUL*matx[0][2],4),round(matx[0][3],4)))
			self.file.write("%f,%f,%f,%f," % (round(matx[1][0],4),round(matx[1][1],4),round(ZMUL*matx[1][2],4),round(matx[1][3],4)))
			self.file.write("%f,%f,%f,%f," % (round(ZMUL*matx[2][0],4),round(ZMUL*matx[2][1],4),round(matx[2][2],4),round(ZMUL*matx[2][3],4)))
			self.file.write("%f,%f,%f,%f;;\n"% (round(matx[3][0],4),round(matx[3][1],4),round(ZMUL*matx[3][2],4),round(matx[3][3],6)))


#*********************************************************************************************************************************************

	#***********************************************
	#HEADER
	#***********************************************
	def writeHeader(self):
		global MOD_VERSION
		self.file.write("xof 0303txt 0032\n\n")
		self.file.write("// DirectX File - exported from Blender version %s using DirectX8ExporterMod.py - mod version %s\n\n"%(Blender.Get('version'), MOD_VERSION))

		self.file.write("template VertexDuplicationIndices { \n\
  <b8d65549-d7c9-4995-89cf-53a9a8b031e3>\n\
  DWORD nIndices;\n\
  DWORD nOriginalVertices;\n\
  array DWORD indices[nIndices];\n\
}\n\
template XSkinMeshHeader {\n\
  <3cf169ce-ff7c-44ab-93c0-f78f62d172e2>\n\
  WORD nMaxSkinWeightsPerVertex;\n\
  WORD nMaxSkinWeightsPerFace;\n\
  WORD nBones;\n\
}\n\
template SkinWeights {\n\
  <6f0d123b-bad2-4167-a0d0-80224f25fabb>\n\
  STRING transformNodeName;\n\
  DWORD nWeights;\n\
  array DWORD vertexIndices[nWeights];\n\
  array float weights[nWeights];\n\
  Matrix4x4 matrixOffset;\n\
}\n\n")

	#***********************************************
	#CLOSE FILE
	#***********************************************
	def writeEnd(self):
		self.file.close()
	##print "... finished"


	#***********************************************
	#EXPORT TEXTURES
	#***********************************************
	def findTextures(self, obj, tex):
		mesh = obj.data
		face_types = []
		for face in mesh.faces:
			if face.image and face.image.name not in tex:
				tex.append(face.image.name)
			if not len(face.v) in face_types: face_types.append(len(face.v))
		face_types.sort()
		self.face_types = face_types

	#***********************************************
	#EXPORT MESH DATA
	#***********************************************
	def openMeshBlock(self, obj, armat):
		global FLIP_FACES, ZMUL, new_verts, SWAP_YZ_AXIS

		mesh = NMesh.GetRawFromObject(obj.name)
		len_new_verts = len(new_verts)

		#ROTATION
		mat_obj = obj.getMatrix()
		if armat == 0:
			if RESET_ORIGIN:
				mat_reset = Matrix([mat_obj[0][0],mat_obj[0][1],mat_obj[0][2],mat_obj[0][3]],
				                   [mat_obj[1][0],mat_obj[1][1],mat_obj[1][2],mat_obj[1][3]],
				                   [mat_obj[2][0],mat_obj[2][1],mat_obj[2][2],mat_obj[2][3]],
				                   [0, 0, 0, 1])
				self.openFrameBlock(mat_reset, "body")
			else:
				self.openFrameBlock(mat_obj, "body")

		else:
			mat_ar = armat.getInverseMatrix()
			mat_f = mat_obj * mat_ar
			self.openFrameBlock(mat_f, "body")

		self.file_indent()
		self.file.write("Mesh object {\n")

		self.indent(1)

		self.file_indent()
		self.file.write("%d;\n" % (len_new_verts))

		# VERTEX COORDINATES

		for idx in new_verts.keys():
			vertex = mesh.verts[new_verts[idx]]
			self.file_indent()

			if SWAP_YZ_AXIS:
				self.file.write("%f;%f;%f;" % (round(vertex[0],6), ZMUL*round((vertex[2]),6), round(vertex[1],6)))
			else:
				self.file.write("%f;%f;%f;" % (round(vertex[0],6), round(vertex[1],6), ZMUL*round((vertex[2]),6)))

			if idx+1 == len_new_verts:
				self.file.write(";\n")
			else:
				self.file.write(",\n")

		# FACE COUNT

		numfaces=len(mesh.faces)
		self.file_indent()
		self.file.write("%d;\n" % (numfaces))

		# FACES INDICES

		if FLIP_FACES == 0:
			a3 = 0
			b3 = 1
			c3 = 2
			a4 = 0
			b4 = 1
			c4 = 2
			d4 = 3
		else:
			a3 = 2
			b3 = 1
			c3 = 0
			a4 = 3
			b4 = 2
			c4 = 1
			d4 = 0

		for counter in range(numfaces) :
			face = new_faces[counter]

			if len(face) == 3:
				self.file_indent()
				self.file.write("3;%d,%d,%d;" % (face[a3], face[b3], face[c3]))
			elif len(face) == 4:
				self.file_indent()
				self.file.write("4;%d,%d,%d,%d;" % (face[a4], face[b4], face[c4], face[d4]))
			elif len(face) == 2:
				print "WARNING:the mesh has faces with less then 3 vertices"
				continue

			if counter+1 == numfaces:
				self.file.write(";\n\n")
			else:
				self.file.write(",\n")






	#***********************************************
	#MESH MATERIAL LIST
	#***********************************************
	def writeMeshMaterialList(self, name, obj, tex):
		self.file_indent()
		self.file.write("MeshMaterialList {\n")

		self.indent(1)

		#HOW MANY MATERIALS ARE USED
		count = 0
		for mat in Material.Get():
			count+=1
		self.file_indent()
		self.file.write("%d;\n" % (len(tex) + count))
		#HOW MANY FACES IT HAS
		numfaces=len(obj.faces)
		self.file_indent()
		self.file.write("%d;\n" % (numfaces))
		##MATERIALS INDEX FOR EVERY FACE
		counter = 0
		for face in obj.faces :
			counter += 1
			mater = face.materialIndex

			if face.image and face.image.name in tex:
				self.file_indent()
				self.file.write("%d" % (tex.index(face.image.name) + count))
			else :
				self.file_indent()
				self.file.write("%d" % (mater))
			if counter == numfaces:
				self.file.write(";\n")
			else:
				self.file.write(",\n")

		##MATERIAL NAME
		for mat in Material.Get():
			self.file_indent()

			self.file.write("Material")

			fixed_name = replace(mat.name, ".", "_")

			self.file.write(" %s "%(fixed_name))
			self.file.write("{\n")

			self.indent(1)

			self.file_indent()
			self.file.write("%f; %f; %f;" % (mat.R, mat.G, mat.B))
			self.file.write("%f;;\n" % (mat.alpha))
			self.file_indent()
			self.file.write("%f;\n" % (mat.spec))
			self.file_indent()
			self.file.write("%f; %f; %f;;\n" % (mat.specR, mat.specG, mat.specB))
			self.file_indent()
			self.file.write("0.0; 0.0; 0.0;;\n")

			# close Material
			self.closeBlock()

		for mat in tex:
			self.file_indent()
			self.file.write("Material Mat")
			self.file.write("%s "% (len(tex)))
			self.file.write("{\n")

			self.indent(1)

			self.file_indent()
			self.file.write("1.0; 1.0; 1.0; 1.0;;\n")
			self.file_indent()
			self.file.write("1.0;\n")
			self.file_indent()
			self.file.write("1.0; 1.0; 1.0;;\n")
			self.file_indent()
			self.file.write("0.0; 0.0; 0.0;;\n")
			self.file_indent()
			self.file.write("TextureFilename {\n")
			self.indent(1)
			self.file_indent()
			self.file.write("\"%s\";\n" % (mat))

			# close TextureFilename
			self.closeBlock()

			# close Material
			self.closeBlock()

		# close MeshMaterialList
		self.closeBlock()

	#***********************************************
	#MESH NORMALS
	#***********************************************
	def writeMeshNormals(self,name,obj):
		global INVERT_NORMALS, FLIP_FACES, ZMUL, RECALC_VERTEX_NORMALS, new_verts, new_faces, new_normals, SWAP_YZ_AXIS

		len_new_verts = len(new_verts)
		mesh = name.data

		self.file_indent()
		self.file.write("MeshNormals {\n")

		self.indent(1)

		# VERTEX COUNT

		numvert=len(obj.verts)

		self.file_indent()
		self.file.write("%d;\n" % (len_new_verts))

		# VERTEX NORMALS

		counter = 0

		if INVERT_NORMALS == 0:
			mul = 1.0
		else:
			mul = -1.0


		for idx in new_verts.keys():
			vert = mesh.verts[new_verts[idx]]
			if RECALC_VERTEX_NORMALS == 1:
				no = new_normals[new_verts[idx]]
			else:
				no = mesh.verts[new_verts[idx]].no

			self.file_indent()

			if SWAP_YZ_AXIS:
				self.file.write("%f;%f;%f;" % ((mul*round(no[0],6)),(ZMUL*mul*round(no[2],6)),(mul*round(no[1],6))))
			else:
				self.file.write("%f;%f;%f;" % ((mul*round(no[0],6)),(mul*round(no[1],6)),(ZMUL*mul*round(no[2],6))))

			if idx+1 == len_new_verts:
				self.file.write(";\n")
			else:
				self.file.write(",\n")


		# FACE COUNT

		numfaces=len(obj.faces)
		self.file_indent()
		self.file.write("%d;\n" % (numfaces))

		# FACE INDICES

		counter = 0

		if FLIP_FACES == 0:
			a3 = 0
			b3 = 1
			c3 = 2
			a4 = 0
			b4 = 1
			c4 = 2
			d4 = 3
		else:
			a3 = 2
			b3 = 1
			c3 = 0
			a4 = 3
			b4 = 2
			c4 = 1
			d4 = 0

		for counter in range(numfaces) :
			face = new_faces[counter]
			if len(face) == 3:
				self.file_indent()
				self.file.write("3;%d,%d,%d;" % (face[a3], face[b3], face[c3]))
			elif len(face) == 4:
				self.file_indent()
				self.file.write("4;%d,%d,%d,%d;" % (face[a4], face[b4], face[c4], face[d4]))

			if counter+1 == numfaces:
				self.file.write(";\n")
			else:
				self.file.write(",\n")

		# close MeshNormals
		self.closeBlock()

	def vector_normalize(self, v):
		l = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
		if l == 0:
			return 0,0,0
		return v[0] / l, v[1] / l, v[2] / l

	def recalcVertexNormals(self, obj):
		global new_normals, SHOW_PROGRESS_BAR
		mesh = obj.data

		new_normals = []

		total_count = len(mesh.verts)
		count = 0
		mod = total_count / PROGRESS_BAR_STEPS

		for vert in mesh.verts:

			if SHOW_PROGRESS_BAR:
				if not mod or not count%mod:
					Blender.Window.DrawProgressBar(float(count)/total_count, "Recalc vnormals")
				count += 1

			sum = [0,0,0]
			vert.no[0] = 0
			vert.no[1] = 0
			vert.no[2] = 0
			for face in mesh.faces:
				for n in range(len(face.v)):
					if vert.index == face.v[n].index:
						sum[0] += face.no[0]
						sum[1] += face.no[1]
						sum[2] += face.no[2]
			sum = self.vector_normalize(sum)
			new_normals.append(sum)



	#***********************************************
	# CALCULATE NEW VERTICES
	#***********************************************
	def createNewVertices(self, obj, mesh):
		global new_verts_uv, new_verts, new_faces, duplicates

		new_verts_uv = {}
		new_verts = {}
		new_faces = []
		duplicates = {}

		mesh = obj.getData()

		numverts = len(mesh.verts)
		##		print "Faces: %d" % len(mesh.faces)##		print "Vertices: %d" % numverts

		if not mesh.hasFaceUV():
#			print "Mesh has no uv coordinates."
			# do not calculate new vertices
			# stick to existing ones
			for idx in range(numverts):
				new_verts[idx] = idx
				new_verts_uv[idx] = 0.0, 0.0

			for face in mesh.faces:
				cur_new_face = []
				new_faces.append(cur_new_face)
				for n in range(len(face.v)):
					idx = face.v[n].index
					cur_new_face.append(idx)
			return

#		print "Calculating new vertices..."
		for face in mesh.faces:
			cur_new_face = []
			new_faces.append(cur_new_face)

			for n in range(len(face.v)):
				idx = face.v[n].index
				cur_new_face.append(idx)

				if new_verts.has_key(idx):
					# already exits

					# does it have different tx coords?
					if new_verts_uv[idx][0] != face.uv[n][0] or new_verts_uv[idx][1] != face.uv[n][1]:
						makenew = 1

						# other vert with same tx coords already?
						if duplicates.has_key(idx):
							for dup in duplicates[idx]:
								if new_verts_uv[dup][0] == face.uv[n][0] and new_verts_uv[dup][1] == face.uv[n][1]:
									makenew = 0
									cur_new_face[n] = dup # replace old vertex ref
									break
						else:
							duplicates[idx] = []

						if makenew == 1:
							# add new vertex
							new_verts_uv[numverts] = face.uv[n][0], face.uv[n][1]
							new_verts[numverts] = idx
							cur_new_face[n] = numverts # replace old vertex ref
							duplicates[idx].append(numverts)
							numverts += 1

				else:
					# new
					new_verts_uv[idx] = face.uv[n][0], face.uv[n][1]
					new_verts[idx] = idx

#		print "Vertices: %d" % len(new_verts)

	#***********************************************
	#MESH TEXTURE COORDS
	#***********************************************
	def writeMeshTextureCoords(self, name, obj):
		global new_verts, new_verts_uv

		len_new_verts = len(new_verts)
		uv_list = {}
		if obj.hasFaceUV():
			self.file_indent()
			self.file.write("MeshTextureCoords {\n")

			self.indent(1)

			# VERTEX COUNT

			mesh = name.data

			self.file_indent()
			self.file.write("%d;\n" % (len_new_verts))

			# UV COORDS

			counter = -1

			for idx in new_verts.keys():
				uv = new_verts_uv[idx]
				if idx+1 == len_new_verts:
					self.file_indent()
					self.file.write("%f;%f;;\n" % (uv[0],1 - (uv[1])))
				else:
					self.file_indent()
					self.file.write("%f;%f;,\n" % (uv[0],1 - (uv[1])))

			# close MeshTextureCoords
			self.closeBlock()

	#***********************************************
	#FRAMES
	#***********************************************
	def writeFrames(self, matx):
		global ZMUL, SWAP_YZ_AXIS

		if SWAP_YZ_AXIS:
			self.file.write("%f,%f,%f,%f," % (round(matx[0][0],4),round(ZMUL*matx[0][2],4),round(matx[0][1],4),round(matx[0][3],6)))
			self.file.write("%f,%f,%f,%f," % (round(ZMUL*matx[2][0],4),round(matx[2][2],4),round(ZMUL*matx[2][1],4),round(ZMUL*matx[2][3],6)))
			self.file.write("%f,%f,%f,%f," % (round(matx[1][0],4),round(ZMUL*matx[1][2],4),round(matx[1][1],4),round(matx[1][3],6)))
			self.file.write("%f,%f,%f,%f;;"% (round(matx[3][0],4),round(ZMUL*matx[3][2],4),round(matx[3][1],4),round(matx[3][3],6)))
		else:
			self.file.write("%f,%f,%f,%f," % (round(matx[0][0],4),round(matx[0][1],4),round(ZMUL*matx[0][2],4),round(matx[0][3],6)))
			self.file.write("%f,%f,%f,%f," % (round(matx[1][0],4),round(matx[1][1],4),round(ZMUL*matx[1][2],4),round(matx[1][3],6)))
			self.file.write("%f,%f,%f,%f," % (round(ZMUL*matx[2][0],4),round(ZMUL*matx[2][1],4),round(matx[2][2],4),round(ZMUL*matx[2][3],6)))
			self.file.write("%f,%f,%f,%f;;"% (round(matx[3][0],4),round(matx[3][1],4),round(ZMUL*matx[3][2],4),round(matx[3][3],6)))




	#***********************************************
	#WRITE ANIMATION KEYS
	#***********************************************
	def writeAnimation(self, amt):
		global EXPORT_DX_SPEED, DIRECT_X_TICKS_PER_SECOND

		self.file_indent()
		self.file.write("AnimationSet {\n")

		self.indent(1)

		startFr = Blender.Get('staframe')
		endFr = Blender.Get('endframe')

		if EXPORT_DX_SPEED:
			frame_ticks = DIRECT_X_TICKS_PER_SECOND / FRAMES_PER_SECOND
		else:
			frame_ticks = 1

		total_count = len(amt.getBones())
		count = 0
		mod = total_count / PROGRESS_BAR_STEPS

		for bon in amt.getBones() :

			if SHOW_PROGRESS_BAR:
				if not mod or not count%mod:
					Blender.Window.DrawProgressBar(float(count)/total_count, "Writing animation")
				count += 1

			fixed_name = replace(bon.getName(), ".", "_")
#			fixed_name = bon.getName()
			self.file_indent()
			self.file.write("Animation { \n")

			self.indent(1)

			self.file_indent()
			self.file.write("{%s}\n" %(fixed_name))
			self.file_indent()
			self.file.write("AnimationKey {\n")

			self.indent(1)

			self.file_indent()
			self.file.write("4;\n")
			self.file_indent()
			self.file.write("%d;\n" % ((endFr-startFr)+1))

			fcount = 0
			for fr in range(startFr,endFr + 1):
				self.file_indent()
				self.file.write("%d;" % (fcount*frame_ticks+1))
				self.file.write("16;")
				Blender.Set('curframe',fr)

				mat_new = self.getCombineAnimMatrix(bon)
				self.writeFrames(mat_new)

				if fr == endFr:
					self.file.write(";\n")
				else:
					self.file.write(",\n")
				fcount += 1

			# close Animation Key
			self.closeBlock()

			# close Animation
			self.closeBlock()

		# close AnimationSet
		self.closeBlock()

#***********************************************

	def file_indent(self):
		self.file.write("  " * self.level)

	def indent(self, factor):
		self.level += factor

	def closeBlock(self):
		self.indent(-1)
		self.file_indent()
		self.file.write("}\n")

	def closeMeshBlock(self):
		# close Frame block
		self.closeBlock()
		# close Mesh block
		self.closeBlock()

# copied here from mod_meshtools to remove beep
def print_boxed(text):
	lines = text.splitlines()
	maxlinelen = max(map(len, lines))
	if sys.platform[:3] == "win":
		print chr(218)+chr(196) + chr(196)*maxlinelen + chr(196)+chr(191)
		for line in lines:
			print chr(179) + ' ' + line.ljust(maxlinelen) + ' ' + chr(179)
		print chr(192)+chr(196) + chr(196)*maxlinelen + chr(196)+chr(217)
	else:
		print '+-' + '-'*maxlinelen + '-+'
		for line in lines: print '| ' + line.ljust(maxlinelen) + ' |'
		print '+-' + '-'*maxlinelen + '-+'


#***********************************************
# MAIN
#***********************************************

def my_callback(filename):
	global BEEP_WHEN_FINISHED, CURRENT_FILENAME

	CURRENT_FILENAME = filename
	update_RegistryInfo()

	start = time.clock()

	is_editmode = Blender.Window.EditMode()
	if is_editmode: Blender.Window.EditMode(0)

	if filename.find('.x', -2) <= 0: filename += '.x'
	xexport = xExport(filename)

	# make that file gets closed under all circumstances:
	try:
		xexport.writeRootBone()
	finally:
		xexport.writeEnd()
		if SHOW_PROGRESS_BAR: Blender.Window.DrawProgressBar(1.0, '')

	if xexport.level:
		Blender.Draw.PupMenu("DirectX Export error%%t|Identation Level: %d (must be zero)!"%(xexport.level))

	stop = time.clock()

	num = len(xexport.exported_objects)

	if num == 1: s = ""
	else: s = "s"
	duration = stop-start
	message = "DirectX8ExporterMod.py - mod version %s\n\n" % (MOD_VERSION)
	message += "Successfully exported %d object%s in %.2f seconds\n\n" % (num, s, duration)

	message += "filename  : " + os.path.basename(filename) + '\n'
	for info in xexport.exported_objects:
		message += "\nobject    : " + info['name'] + '\n'
		if info['verts2'] > info['verts1']: before = " (originally %d that's +%d)" % (info['verts1'], info['verts2']-info['verts1'])
		else: before = ""
		face_types = "";
		for type in info['face_types']:
			if face_types != "": face_types += " and "
			face_types += "%d"%(type)

		message += "verts     : %d%s\n" % (info['verts2'], before)
		message += "faces     : %d (with %s vertices)\n" % (info['faces'], face_types)
		message += "has uv    : %s\n" % (info['uv'])
		message += "materials : %d\n" % (info['materials'])

	print_boxed(message)
	if is_editmode: Blender.Window.EditMode(1)
	if BEEP_WHEN_FINISHED < 0 or duration > BEEP_WHEN_FINISHED: print("\a\n"),

# check if at least one mesh object is selected and none of it is in subsurf mode.
ok = False
subsurf = False

sel_objs = Object.GetSelected()
if len(sel_objs):
	for obj in sel_objs:
		if obj.getType() == 'Mesh':
			if obj.getData().getMode() & NMesh.Modes['SUBSURF']:
				subsurf = True
			ok = True
			break

if subsurf:
	Blender.Draw.PupMenu("DirectX Export error%t|At least one object is in \"SubSurf\" mode!|Please convert it using \"Convert Object Type\" in the Object menu.")

elif ok:
	if CURRENT_FILENAME: choose_file = "|%%l|Export as \"%s\" (%s)%%x3|" % (os.path.basename(CURRENT_FILENAME),CURRENT_FILENAME)
	else: choose_file = ""

	name = "Export: DirectX8 - mod"+MOD_VERSION+" (.x)...%t|"
	name += "Export to DX8 file format (choose filename)%x1|Help & Configuration%x2" + choose_file
	menu = Blender.Draw.PupMenu(name)

	if menu == 1:
		Blender.Window.FileSelector(my_callback, "Export DirectX8")
	elif menu == 2:
		Blender.Draw.Register(draw,event,bevent)
	elif menu == 3:
		my_callback(CURRENT_FILENAME)

else:
	Blender.Draw.PupMenu("DirectX Export error%t|Please select at least one Mesh object!")

