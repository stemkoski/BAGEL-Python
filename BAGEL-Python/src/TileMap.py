import pygame
import math

from Entity     import *
from Texture    import *
from Rectangle  import *
from Physics    import *
from Tile       import *
from Vector2    import *

class TileMap(Entity):

    def __init__(self, mapRows=0, mapCols=0, tileWidth=32, tileHeight=32):
        self.mapRows    = mapRows
        self.mapCols    = mapCols
        self.tileWidth  = tileWidth
        self.tileHeight = tileHeight

        # a two-dimensional array storing all the text characters
        # used to specify this TileMap
        self.mapDataGrid = None # 2D list; initialize later

        # a two-dimensional array storing only the Tile objects
        # specified by this TileMap. used primarily to determine whether
        # a tile is adjacent to other tiles, and thereby which tile edges 
        # should be ignored when calculating collision resolution.
        self.mapTileGrid = None # 2D list; initialize later

        # a list containing all the Tile objects stored by this TileMap
        self.mapTileList = []

        # a list containing all the available Tile textures
        # loaded by the loadTilesetImage function
        self.tileTextureList = []
                          
    # Load a tileset - 
    # an image consisting of smaller rectangular images
    # that represent possible features of the game world environment. 
    def loadTilesetImage(self, imageFileName):
        image = pygame.image.load(imageFileName)
        tileImageRows = int(image.get_width()  / self.tileWidth)
        tileImageCols = int(image.get_height() / self.tileHeight)
        for y in range(tileImageRows):
            for x in range(tileImageCols):
                subimage = pygame.Surface( (self.tileWidth, self.tileHeight), pygame.SRCALPHA )
                subimage.blit(image, (0, 0),
                    (x*self.tileWidth, y*self.tileHeight, self.tileWidth, self.tileHeight))
                texture = Texture()
                texture.image  = subimage
                texture.width  = self.tileWidth
                texture.height = self.tileHeight
                self.tileTextureList.append(texture)
    
    def loadMapData(self, mapData, mapTileSymbolList, tileTextureIndexList):
        self.mapDataGrid = [[None for c in range(self.mapCols)] for r in range(self.mapRows)]
        self.mapTileGrid = [[None for c in range(self.mapCols)] for r in range(self.mapRows)]
        self.mapTileList = []
        
        for r in range(self.mapRows):
            for c in range(self.mapCols):
                
                # add all data to mapDataGrid
                data = mapData[r][c]
                self.mapDataGrid[r][c] = data
                
                # add Tile-specific data to mapTileGrid and list
                if (data in mapTileSymbolList):
                    i = mapTileSymbolList.index(data)
                    tileTextureIndex = tileTextureIndexList[i]
                    x = (c + 0.5) * self.tileWidth
                    y = (r + 0.5) * self.tileHeight
                    tile = Tile(x,y, self.tileWidth, self.tileHeight, tileTextureIndex)
                    self.mapTileGrid[r][c] = tile
                    self.mapTileList.append(tile)
                    
        # after all map data is loaded, use adjacency information to set Tile edge fields
        for r in range(self.mapRows):
            for c in range(self.mapCols):
                tile = self.mapTileGrid[r][c]
                if ( not(tile == None) ):
                    rect = tile.boundary;
                    if ( self.getTileAt(r,c-1) == None ):
                        tile.edgeLeft = Rectangle()
                        tile.edgeLeft.setValues(rect.left, rect.top, 0, self.tileHeight)
                    if ( self.getTileAt(r,c+1) == None ):
                        tile.edgeRight = Rectangle()
                        tile.edgeRight.setValues(rect.left + self.tileWidth, rect.top, 0, self.tileHeight)
                    if ( self.getTileAt(r-1,c) == None ):
                        tile.edgeTop = Rectangle()
                        tile.edgeTop.setValues(rect.left, rect.top, self.tileWidth, 0)
                    if ( self.getTileAt(r+1,c) == None ):
                        tile.edgeBottom = Rectangle()
                        tile.edgeBottom.setValues(rect.left, rect.top + self.tileHeight, self.tileWidth, 0)     
        
    def getTileAt(self, mapRow, mapCol):
        if (mapRow < 0 or mapRow >= self.mapRows or mapCol < 0 or mapCol >= self.mapCols):
            return None
        else:
            return self.mapTileGrid[mapRow][mapCol]

    def getSymbolPositionList(self, symbol):
        positionList = []
        for r in range(self.mapRows):
            for c in range(self.mapCols):
                if (self.mapDataGrid[r][c] == symbol):
                    x = (c + 0.5) * self.tileWidth
                    y = (r + 0.5) * self.tileHeight
                    positionList.append( Vector2(x,y) )
        return positionList

    def draw(self, displaySurface):
        for tile in self.mapTileList:
            texture = self.tileTextureList[ tile.tileTextureIndex ]
            rect  = texture.image.get_rect( center=(tile.x, tile.y) )    
            displaySurface.blit( texture.image, rect )

    def checkSpriteOverlap(self, sprite):
        spriteBoundary = sprite.getBoundary()
        for tile in self.mapTileList:
            if ( spriteBoundary.overlaps(tile.boundary) ):
                return True
        return False

    def preventSpriteOverlap(self, sprite):
        spriteBoundary = sprite.getBoundary()
        for tile in self.mapTileList:
            if ( spriteBoundary.overlaps( tile.boundary ) ):
                differences = []
		
                if ( tile.edgeLeft != None and spriteBoundary.overlaps(tile.edgeLeft) ):
                    differences.append( Vector2(tile.boundary.left - spriteBoundary.right, 0) )  # to the left
                if ( tile.edgeRight != None and spriteBoundary.overlaps(tile.edgeRight) ):
                    differences.append( Vector2(tile.boundary.right - spriteBoundary.left, 0) )  # how to displace this sprite to the right
                if ( tile.edgeTop != None and spriteBoundary.overlaps(tile.edgeTop) ):
                    differences.append( Vector2(0, tile.boundary.top - spriteBoundary.bottom) )  # to the bottom
                if ( tile.edgeBottom != None and spriteBoundary.overlaps(tile.edgeBottom) ):
                    differences.append( Vector2(0, tile.boundary.bottom - spriteBoundary.top) )  # to the top

                if ( len(differences) > 0 ):
                    # sort list in place (no returned list);
                    # requires key function that transforms object in comparable data
                    differences.sort( key=Vector2.getLength )
		
                    # get minimum (length) vector to translate by
                    mtv = differences[0]
                    sprite.moveBy(mtv.x, mtv.y)

		    # if sprite is using physics, come to a stop in appropriate direction
                    if ( sprite.physics != None ):
                        if ( abs(mtv.x) > 0 ):
                            sprite.physics.velocityVector.x = 0
                            sprite.physics.accelerationVector.x = 0
                        if ( abs(mtv.y) > 0 ):
                            sprite.physics.velocityVector.y = 0
                            sprite.physics.accelerationVector.y = 0

					
