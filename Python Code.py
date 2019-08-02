import arcpy
from arcpy import env  
from arcpy import mapping  

# list layers  
mxd = mapping.MapDocument("CURRENT") # will work even if your project is unsaved  
layer_list = mapping.ListLayers(mxd) # lists everything in the ToC window  
sr = arcpy.SpatialReference(4283) # GDA_94  

# Set environment settings
env.workspace = "C:/data"


# GETTING THE REFERENCE OBJECT
REF_OBJ = "REF_OBJ.shp" 	# Get the Reference Object (possibly as shape file.)
REF_MBR = ''				# Create a MBR for Reference Object 
extent_REF = REF_MBR.extent	# Get the extent of REF_MBR

# GETTING THE TARGET OBJECT
TAR_OBJ = "TAR_OBJ.shp" 	# Get the Reference Object (possibly as shape file.)
TAR_MBR = ''				# Create a MBR for Reference Object 
extent_TAR = TAR_MBR.extent	# Get the extent of REF_MBR

# CALULATE DISTANCE BETWEEN REF_OBJ & TAR_OBJ
dis_x = abs(abs(extent_TAR.XMin - extent_REF.XMin) + extent_TAR.width)
dis_y = abs(abs(extent_TAR.YMin - extent_REF.YMin) + extent_TAR.height)


# CALULATE BOUNDS OF THE TOTAL SPACE
MIN_x = extent_REF.XMin - dis_x
MAX_x = extent_REF.XMax + dis_x
MIN_y = extent_REF.YMin - dis_y
MAX_y = extent_REF.YMax + dis_y


dir = []	# List for points.
tiles = []	# List for polygons.


# CREATING & STORING RECTANGULAR TILES
#	A Direction Relation Matrix can only have 4 distinct X values & 4 distinct Y values. 
#	As such, it should be possible to handle the placement/creation of each tile for the DRM using a 2D array.
xPoints = [MIN_x, extent_REF.XMin, extent_REF.XMax, MAX_x]	# List for each distinct x value. 
yPoints = [MAX_y, extent_REF.YMax, extent_REF.YMin, MIN_y]	# List for each distinct y value.
xPoints.sort()	# Sorted from lowest to highest (I.E, from left to right.)
yPoints.sort(reverse=True)	# Sorted from highest to lowest (I.E, from top to bottom.)
# USING 2D ARRAY TO HANDLE CREATION/PLACEMENT OF EACH TILE FOR THE DRM.
for y in range(0,2):
	for x in range(0,2):
		# CREATE BOUNDING BOX		
		boundPoly = "{}\\extent".format(env.scratchWorkspace) 
		dir.add(arcpy.Point(xPoints[x], yPoints[y]))		# START: Top-Left Corner
		dir.add(arcpy.Point(xPoints[x+1], yPoints[y]))		# Top-Right Corner
		dir.add(arcpy.Point(xPoints[x+1], yPoints[y+1])) 	# Bottom-Right Corner
		dir.add(arcpy.Point(xPoints[x], yPoints[y+1]))		# Bottom-Left Corner
		dir.add(arcpy.Point(xPoints[x], yPoints[y]))		# END:	 Top-Left Corner

		# CREATE POLYGON OBJECT
		polygon = arcpy.Polygon(dir, sr)
		tiles.append(polygon)		
		arcpy.CopyFeatures_management(polygon, boundPoly) 
		dir.removeAll()


# CREATE DIRECTION RELATION MATRIX
# 	Determine relationship between the TARGET OBJECT & the given tile. Use results to create DRN
DRM = []	# Initialize Direction Relation Matrix array
for t in tiles:
	# Return "d" if tile DOES NOT overlap with TARGET OBJECT.
	if OBJ_TAR.disjoint(tiles[t]) or OBJ_TAR.touches(tiles[t]):
		DRM[t] = "d"
	# Return "o" if tile DOES overlap with TARGET OBJECT.
	elif OBJ_TAR.overlap(tiles[t]):
		DRM[t] = "o"		# Setting an overlap relation


# TOPOLOGICAL AUGMENTATION
d  = ['d','d','o',
	 'd','d','o',
	 'o','o','o']
m  = ['d','d','o',
	 'd','o','o',
	 'o','o','o']
o  = ['o','o','o',
	 'o','o','o',
	 'o','o','o']
e  = ['o','d','d',
	 'd','o','d',
	 'd','d','o']
ct = ['o','o','o',
	  'd','d','o',
	  'd','d','o']
cv = ['o','o','o',
	  'd','o','o',
	  'd','d','o']
cB = ['o','d','d',
	  'o','o','d',
	  'o','o','o']
i  = ['o','d','d',
	 'o','d','d',
	 'O','o','o']
if DRM == d:
	print("Disjoint")
elif DRM == m:
	print("Meet")
elif DRM == o:
	print("Overlap")
elif DRM == e:
	print("Equal")
elif DRM == ct:
	print("Contains")
elif DRM == cv:
	print("Covers")
elif DRM == cB:
	print("Covered By")
elif DRM == i:
	print("Inside")
else:
	print("No")
	

