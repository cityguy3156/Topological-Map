#Converts gRelate strings into relation
getRelation = function(relation){
	a = gsub("F", "0", relation)
	DRM = gsub("2", "1", a)
	# 8 POSSIBLE TYPES OF RELATIONS
	if (DRM == "001001111"){		#Disjoint
		return("The objects are DISJOINTED from each other.")
	}else if (DRM == "001011111"){	#Meet
		return("The objects MEET each other.")
	}else if (DRM == "111111111"){	#Overlap
		return("The objects OVERLAP each other.")
	}else if (DRM == "100010001" ){	#Equals
		return("The objects are EQUAL to each other.")
	}else if (DRM == "111001001"){	#Contains
		return("The Reference Object CONTAINS the Target Object.")
	}else if (DRM == "111011001"){	#Covers
		return("The Target Object COVERS the Reference Object.")
	}else if (DRM == "100110111"){	#Covered By
		return("The Target Object is COVERED BY the Reference Object.")
	}else if (DRM == "100100111"){	#Inside
		return("The Reference Object is INSIDE the Target Object.")
	}else{ #ERROR MESSAGE
		return("ERROR = You got something different than intended.")
	}	
}
#IMPORT LIBRARIES
library(rgdal)
library(rgeos)
library(sp)

#DECLARE OBJECTS
map=readOGR("C:/Users/cityg/Downloads/cb_2017_23_place_500k","cb_2017_23_place_500k")
summary(map)$bbox[1,]				# Map Object
obj_ref = summary(map[2,])$bbox		# Reference Object
obj_tar = summary(map[3,])$bbox 	# Target Object

MIN_x = (summary(map)$bbox[1,1]-1)	# Smallest x bound of the map
MAX_x = (summary(map)$bbox[1,2]+1)	# Largest x Bound of the map
MIN_y = (summary(map)$bbox[2,1]-1)	# Smallest y bound of the map
MAX_y = (summary(map)$bbox[2,2]+1)	# Largest y bound of the map

xPoints = c(MIN_x, obj_ref[1,1], obj_ref[1,2], MAX_x)	# Each distinct point on the X-Axis. Sorted from left to right.
yPoints = c(MAX_y, obj_ref[2,2], obj_ref[2,1], MIN_y)	# Each distinct point on the Y-Axis. Sorted from top to bottom.

# 2D loop cycles through xPoints & yPoints to draw the 9 tile objects.
# Starts with the Top-Left (NW) tile. Ends with the Bottom-Right (SE) tile.
for (y in 1:3){
	for (x in 1:3){		
		coords = matrix(c(xPoints[x], yPoints[y],	# TL CORNER
						xPoints[x+1], yPoints[y],	# TR CORNER
						xPoints[x+1], yPoints[y+1], # BR CORNER
						xPoints[x], yPoints[y+1],	# BL CORNER
						xPoints[x], yPoints[y]), 	# TL CORNER - Closes the polygon.
						ncol = 2, byrow = TRUE)
		tile = Polygon(coords)	# Creates a rectangular "tile" polygon at the set coordinates.
		DRM = SpatialPolygons(list(Polygons(list(tile), ID = "a")), proj4string=CRS("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"))# Stores the tile object in a list.
	}
}
relation = gRelate(map[3],DRM)	# Finds relationship between Target Object and each tile within DRM
getRelation(relation)