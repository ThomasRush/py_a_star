from random import randint
from Node import Node
from Utilities import *

class Node_Map:

    class Map_Type:
        GRID = 0
        HEX = 1

    # map is a dictionary of tuple/Node objects.
    # the tuple is an x/y coordinate
    node_map = {}

    start_pos = None
    end_pos = None
    map_type = None
    random_start = False
    random_end = False

    # size is a Size object
    # start and end are tuples
    # barrier_percent is a float
    def __init__(self,
                 size,
                 start,
                 end,
                 barrier_percent,
                 map_type):
        self.size = size

        assert (barrier_percent >= 0.0 and barrier_percent <= 1.0)
        #assert (terrain_min <= terrain_max)

        if start == None:
            self.random_start = True
        else:
            assert (self.is_within_bounds(start))

        if end == None:
            self.random_end = True
        else:
            assert (self.is_within_bounds(end))

        self.start_pos = start
        self.end_pos = end
        self.barrier_percent = barrier_percent
        self.map_type = map_type


        # Node_Map provides the adjacency function to
        # AStar. This allows us to use different types of maps
        # without changing the underlying AStar implementation
        if map_type == Node_Map.Map_Type.GRID:
            self.adjacency_function = self.get_adjacent_grid_positions

        if map_type == Node_Map.Map_Type.HEX:
            self.adjacency_function = self.get_adjacent_hex_positions

        self.generate_random_map()

    def get_node_dict(self):
        return self.node_map

    def get_node_at(self,position):
        return self.node_map[position]

    def get_property_at(self,position):
        node = self.node_map[position]
        return node.get_property()

    def reset_map(self):

        for pos,node in self.node_map.iteritems():
            node.set_parent(None)
            if node.node_property == Node.Property.PATH:
                node.node_property == Node.Property.NOTHING

    def get_random_position(self):
        w = self.size.width
        h = self.size.height
        return (randint(0,w-1),randint(0,h-1))

    def generate_random_map(self):

        # TODO: bug here. Start and end should never be the same
        # position. Make sure they're different
        if self.random_start == True:
            self.start_pos = self.get_random_position()
        if self.random_end == True:
            self.end_pos = self.get_random_position()

        p = Node.Property

        for y in range(0,self.size.height):
            for x in range(0,self.size.width):

                if self.start_pos == (x,y):
                    node = Node(p.START)
                    self.node_map[(x,y)] = node

                elif self.end_pos == (x,y):
                    node = Node(p.END)
                    self.node_map[(x,y)] = node

                else:
                    # Determine whether this hex
                    # is a barrier or not
                    if randint(0,100) < (self.barrier_percent * 100):
                        node = Node(p.BARRIER)
                        self.node_map[(x,y)] = node
                    else:
                        # If the node is not a barrier, determine
                        # whether it has a terrain value. If so,
                        # calculate and set the terrain value.

                        # TODO: fix terrain problems
                        terrain_val = 1
                        node = Node(p.NOTHING,terrain_val)

                        #if randint(0,100) < (self.terrain_percentage * 100):
                        #    terrain_val = randint(self.terrain_min * 100,self.terrain_max * 100)
                        #    terrain_val /= 100.0
                        #    node = Node(p.NOTHING,terrain_val)
                        #else:
                        #    node = Node(p.NOTHING)

                        self.node_map[(x,y)] = node

    def set_start(self,pos_tuple):
        # Remove previous start property
        node = self.node_map[self.start_pos]
        node.set_property(Node.Property.NOTHING)

        # New start
        node = self.node_map[pos_tuple]
        node.set_property(Node.Property.START)
        self.start_pos = pos_tuple

    def set_end(self,pos_tuple):

        # Remove previous end property
        node = self.node_map[self.end_pos]
        node.set_property(Node_Property.NOTHING)

        # New end
        node = self.node_map[pos.as_tuple()]
        node.set_property(Node.Property.END)
        self.end_pos = pos_tuple

    def move(self,direction):
        d = Direction # from Utilities module
        x = self.start_pos[0]
        y = self.start_pos[1]
        new_pos = None
        if (direction == d.UP):
            new_pos = (x,y-1)
        elif (direction == d.DOWN):
            new_pos = (x,y+1)
        elif (direction == d.LEFT):
            new_pos = (x-1,y)
        elif (direction == d.RIGHT):
            new_pos = (x+1,y)

        if self.is_valid_move(new_pos):
            self.set_start(new_pos)

    ''' Checks to see whether the new position is within
    the confines of the map and is not a barrier
    or the path end
    '''
    def is_valid_move(self,new_pos):

        # TODO: clean up this multiple-exit function

        np = Node.Property

        # Make sure the new position is within the
        # bounds of the map
        if not self.is_within_bounds(new_pos):
            return False

        # Check to see if the new position is a barrier
        node = self.node_map[new_pos]
        if node.get_property() in (np.BARRIER,np.END):
            return False

        return True

    ''' Checks to see whether the supplied position is
    within the confines of the map
    '''
    def is_within_bounds(self,pos_tuple):
        s = self.size
        x = pos_tuple[0]
        y = pos_tuple[1]
        return x >= 0 and y >= 0 and x < s.width and y < s.height

    def get_adjacent_hex_positions(self,current_pos):

        x = current_pos[0]
        y = current_pos[1]

        nodes = self.node_map

        # Four positions will be adjacent regardless of whether the
        # hex column is offset down or not. These happen to be the
        # cardinal directions (up,down,left,right) of a regular
        # coordinate grid, so we can use that function to get them.
        adjacent_positions = self.get_adjacent_grid_positions(current_pos)

        # If it's an even column, it's offset DOWN
        # (adding one because it's zero-based)
        if (x + 1) % 2 == 0:
            down_right = (x+1,y+1)
            if (self.is_within_bounds(down_right)):
                adjacent_positions.append(down_right)

            down_left = (x-1,y+1)
            if (self.is_within_bounds(down_left)):
                adjacent_positions.append(down_left)

        # Otherwise it's offset UP
        else:
            up_left = (x-1,y-1)
            if (self.is_within_bounds(up_left)):
                adjacent_positions.append(up_left)

            up_right = (x+1,y-1)
            if (self.is_within_bounds(up_right)):
                adjacent_positions.append(up_right)

        return adjacent_positions

    def get_adjacent_grid_positions(self,current_pos):

        adjacent_positions = []

        x = current_pos[0]
        y = current_pos[1]

        positions = [ (x-1,y),  # left
                      (x+1,y),  # right
                      (x,y-1),  # up
                      (x,y+1) ] # down

        for position in positions:
            if (self.is_within_bounds(position)):
                adjacent_positions.append(position)

        return adjacent_positions

