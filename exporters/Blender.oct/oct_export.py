#!BPY

"""
Name: 'FSRad OCT (.oct)...'
Blender: 236
Group: 'Export'
Tooltip: 'Export to an FSRad OCT File'
"""

__author__ = "Murphy McCauley"
__url__ = ["blender"]
__version__ = "1.0.2"

__bpydoc__ = """\
Exports all meshes and lights to an OCT file for use with the Fluid Studios Radiosity Processor

Usage:<br>
	Select RSRad OCT from the Export menu.
"""

# scaleFactor is for geometry scaling
scaleFactor = 100

# lightScale is for light intensity scaling
lightScale  = 10000000


from Blender import *
import struct


def Export(filename):
	print "Exporting OCT (oct_export v" + __version__ + " by Murphy McCauley)..."

	file = open(filename, "wb")

	# Output an empty header.  We'll come back and fill it in later.	
	file.write(struct.pack('<5i', 0, 0, 0, 0, 0))

	vertCount = 0
	faceCount = 0
	lightCount = 0
	textureCount = 0
	vertCountCheck = 0
	
	textures = list()
	
	# Output verts
	meshNum = 0	
	for ob in Object.Get():
		if ob.getType() != 'Mesh':
			continue
		
		m = NMesh.GetRawFromObject(ob.name)
  		worldTransform = ob.getMatrix("worldspace")
		location = ob.getLocation()

		for f in m.faces:
			if len(f.v) >= 3: # don't export faces with less than three verts
				if f.image:
					if f.image.name not in textures:
						textures.append(f.image.name)
				whichVert = len(f.v) - 1
				faceVerts = f.v
				faceVerts.reverse()		
				for vv in faceVerts:
					vert = m.verts[vv.index].co
					vert = Mathutils.VecMultMat(Mathutils.Vector([vert[0],vert[1],vert[2],0]), worldTransform)
					vert[0] += location[0]
					vert[1] += location[1]
					vert[2] += location[2]

					u = 0
					v = 0
					if f.uv:
						u = f.uv[whichVert][0]
						v = f.uv[whichVert][1]
					file.write(struct.pack('<2f2f3f', u, v, 0.0, 0.0, scaleFactor*vert[0], scaleFactor*vert[2], scaleFactor*vert[1]))
					vertCountCheck += 1
					whichVert -= 1


	# Output faces
	warned = False
	for ob in Object.Get():
		if ob.getType() != 'Mesh':
			continue

		m = NMesh.GetRawFromObject(ob.name)

		for f in m.faces:
			if len(f.v) >= 3:
				if f.image:
					textureID = textures.index(f.image.name)
				else:
					if warned == False:
						print "Warning: At least one face is not texture mapped"
						warned = True
					textureID = 0
				# I write the plane as four 0.0s.  It doesn't appear to be used anyway.
				file.write(struct.pack('<iiiiffff', vertCount, len(f.v), textureID, 0, 0.0, 0.0, 0.0, 0.0))							
				faceCount += 1
				vertCount += len(f.v)


	# Output textures
	textureCount = 0
	for t in textures:
		file.write(struct.pack('<i64s', textureCount, t))
		textureCount += 1

	
	# Output lights
	warned = False
	for ob in Object.Get():
		if ob.getType() == 'Lamp':
			#l = Lamp.Get(ob.name)
			l = ob.getData()
			
			if l.type != 0: # only point lights (0 = Lamp)
				if warned == False:
					print "Warning: At least one lamp was ignored (only point lamps are supported)"
					warned = True
				continue

			s = (l.energy / 10.0) * lightScale

			vert = ob.getLocation()
			file.write(struct.pack('<3f3fi', scaleFactor*vert[0], scaleFactor*vert[1], scaleFactor*vert[2], l.col[0], l.col[1], l.col[2], s))
			lightCount += 1
		else:
			pass
			#print ob.getType()


	# Output player position
	c = Camera.Get()
	if 0: #len(c):
		# Use the first camera's position as the player position
		# FIXME: Coords 1 and 2 may be swapped
		file.write(struct.pack('<3f', scaleFactor*c.getLocation()[0], scaleFactor*c.getLocation()[1], scaleFactor*c.getLocation()[2]))		
	else:
		# Just use 0,0,0
		file.write(struct.pack('<3f', 0, 0, 0))

		
	# Now output the real header
	file.seek(0)
	file.write(struct.pack('<5i', vertCount, faceCount, textureCount, 0, lightCount))
					

	#Done
	file.close()
	print "OCT exported.  %i vertices  %i faces  %i lights" % (vertCount, faceCount, lightCount)


Window.FileSelector(Export, 'Export FSRad OCT', Get('filename')[:-len(Get('filename').split('.', -1)[-1])] + 'oct')

