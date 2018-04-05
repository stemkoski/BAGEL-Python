from Rectangle  import *
from Entity     import *

class Tile(Entity):

    def __init__(self, x=0, y=0, width=0, height=0, tileTextureIndex=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tileTextureIndex = tileTextureIndex

        # Full boundary of tile. Used for collision detection,
	#   but not for collision resolution, 
	#   due to "corner snag" or "internal edge" issues
	#   that interfere with Sprite movement
        self.boundary = Rectangle(x - width/2, y - height/2, width, height)

        # edges are represented by edges with width=0 or height=0
        #   set by corresponding Tilemap
        self.edgeLeft   = Rectangle()
        self.edgeRight  = Rectangle()
        self.edgeTop    = Rectangle()
        self.edgeBottom = Rectangle()


