from Vector2 import *

class Rectangle(object):

    def __init__(self, x=0, y=0, w=0, h=0):
        self.setValues(x,y,w,h)

    def setValues(self, x, y, w, h):
        self.left   = x
        self.top    = y
        self.width  = w
        self.height = h
        self.right  = x + w
        self.bottom = y + h

    def overlaps(self, other):
        noOverlap = (other.right <= self.left) \
                 or (self.right <= other.left) \
                 or (other.bottom <= self.top) \
                 or (self.bottom <= other.top)
        return (not noOverlap)

    def contains(self, x, y):
        return (self.left <= x) \
               and (x <= self.right) \
               and (self.top <= y) \
               and (y <= self.bottom)

    def getMinTranslationVector(self, other):
        differences = [ Vector2(self.left - other.right, 0), # displacement to the left
			Vector2(self.right - other.left, 0), # right
			Vector2(0, self.top - other.bottom), # top
			Vector2(0, self.bottom - other.top)  # bottom
			]
        # sort list in place (no returned list);
        # requires key function that transforms object in comparable data
        differences.sort( key=Vector2.getLength )
        return differences[0]
