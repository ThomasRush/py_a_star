
class Node:

    class Property:

        # Possible property values for a node
        NOTHING = 0
        BARRIER = 1
        START = 2
        END = 3
        PATH = 4

    """
        Represents a potentially traversable
        part of a map. Works for any 2D map.

        Contains variables used by AStar to determine
        the most ideal path.
    """
    node_property = None # is this node the start/end/barrier
    g = None # The current path score for this node
    h = None # The heuristic guess score for the rest of the path
    f = None # Combined g and f scores
    parent = None # Reference to the previous node's position (tuple)

    terrain_score = None # A number between 0.1 and 1.0 representing
    # how difficult it is to traverse the node
    # 0.1 is low difficulty, 1.0 is untraversable.

    def __init__(self,val,terrain_score = 1):

        # A node HAS to have some terrain score or
        # else A* will not work.
        assert (terrain_score >= 1)

        self.node_property = val
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.terrain_score = terrain_score

    def is_barrier(self):
        return self.node_property == self.Node_Property.BARRIER

    def is_end(self):
        return self.node_property == self.Property.END

    def is_start(self):
        return self.node_property == self.Property.START

    def set_property(self,node_property):
        self.node_property = node_property

    def set_parent_and_score(self,parent_pos,parent_g,end_pos):

        self.set_parent(parent_pos)

        # The cost of previous steps plus one more step
        self.g = parent_g + self.get_terrain_score()

        # Determine a guess of the remaining distance (H)
        # This is the "Manhattan" implementation
        self.h = abs(parent_pos[0] - end_pos[0])
        self.h += abs(parent_pos[1] - end_pos[1])

        # Set the new F score
        self.f = self.g + self.h

    def set_parent(self,parent_pos):
        self.parent = parent_pos

    def has_better_f_score(self,score):
        return self.get_f_score < score

    def get_property(self):
        return self.node_property

    def get_terrain_score(self):
        return self.terrain_score

    def get_f_score(self):
        return self.f

    def get_g_score(self):
        return self.g

    def __str__(self):
        return "Property: {0}, g: {1}, h: {2}, Terrain: {3}", (str(self._node_property), str(self.g), str(self.f),str(self.terrain_score))


