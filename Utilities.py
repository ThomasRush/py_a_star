
class Direction:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Size():
    def __init__(self,width,height):
        self.width = width
        self.height = height
    def as_tuple(self):
        return (self.width,self.height)

class Position():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def as_tuple(self):
        return (self.x,self.y)

    def same_as(self,pos):
        return pos.x == self.x and pos.y == self.y

    def is_positive(self):
        return self.x >= 0 and self.y >= 0

    def within_bounds(self,bounds_x,bounds_y):
        return (self.x <  bounds_x and self.y < bounds_y)

    def get_left(self):
        return Position(self.x-1,self.y)

    def get_right(self):
        return Position(self.x+1,self.y)

    def get_up(self):
        return Position(self.x,self.y-1)

    def get_down(self):
        return Position(self.x,self.y+1)



#\     /---\     /---\     /---\     /---\     /#
# \___/     \___/     \___/     \___/     \___/ #
# /---\     /---\     /---\     /---\     /---\ #
#/     \___/     \___/     \___/     \___/     \#
#\     /---\     /---\     /---\     /---\     /#
# \___/     \___/     \___/     \___/     \___/ #
# /---\     /---\     /---\     /---\     /---\ #
#/     \___/     \___/     \___/     \___/     \#
#\     /---\     /---\     /---\     /---\     /#
# \___/     \___/     \___/     \___/     \___/ #
# /---\     /---\     /---\     /---\     /---\ #
#/     \___/     \___/     \___/     \___/     \#
#\     /---\     /---\     /---\     /---\     /#
# \___/     \___/     \___/     \___/     \___/ #