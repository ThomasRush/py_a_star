
#from Utilities import Node_Property
from Node import Node
from SortedDictionary import SortedDictionary
from time import time


class AStar:
    """ Class determines the best path between a starting and ending point
    on a map of nodes.

    Uses the Manhattan implementation to determine distance between nodes.

    Keyword arguments:
    node_dict -- a dict of tuple / Node object pairs where tuple is a coordinate
    start_node -- a tuple representing the x/y coordinates of the path start
    end_node -- a tuple representing the x/y coordinates of the path end
    adjacency_function -- adjacency function takes a single tuple coordinate
    parameter and returns a dictionary of tuple / Node objects

    """

    def __init__(self):
        def sort_function(item):
            return item[1].f

        self.sort_function = sort_function


    def find_path(self, nodes, start_pos, end_pos, adjacency_function):
        """
        Applies the A* algorithm to determine a path, given the dictionary
        of nodes provided in the constructor.

        Returns a List of tuple coordinates that is the resulting path.
        If no path was found, returns an empty List
        """

        open = SortedDictionary(sort_function = self.sort_function)
        closed = SortedDictionary()

        # Shortened names
        get_adjacent_positions = adjacency_function

        #node_at = self.get_node_at
        p = Node.Property

        # Add the starting node to the open nodes
        # and mark it as the lowest score and the current node
        current_pos = start_pos
        current_node = nodes[current_pos] #node_at(current_pos)
        open[current_pos] = current_node

        # Loop ends when either a path is found (current node is the END node)
        # or if no path is found (open_dict becomes empty)
        # TODO: this looks like the loop runs an extra time since the
        # current_node is being checked and then reset.
        while not current_node.is_end():

            # If no path is found, exit
            if len(open) == 0:
                return {}
            else:

                # Get the lowest f-score position/node
                current_pos, current_node = open.pop()

                adjacent_positions = get_adjacent_positions(current_pos)

                # We're finished with the current node
                # mark it closed
                closed[current_pos] = None

                # Make sure they are not barriers, and not in the closed list
                for adjacent_pos in adjacent_positions:

                    adjacent_node = nodes[adjacent_pos]

                    # If it's not a wall and not closed
                    if (adjacent_node.get_property() <> p.BARRIER and
                        closed.has_key(adjacent_pos) == False):

                        # If it's already in the open list, see if this path
                        # is a better way of getting to the end. If so, make this
                        # path the way by setting it's parent
                        if open.has_key(adjacent_pos):

                            # If the adjacent node's "g" score is greater than
                            # the current node's "g" score plus the movement score,
                            # append the adjacent node to the open list
                            if (adjacent_node.g >
                                current_node.g + adjacent_node.terrain_score):

                                adjacent_node.set_parent_and_score(current_pos,
                                                                   current_node.g,
                                                                   end_pos)

                                # If the current node's f-score is lower than the
                                # current lowest f-score, set it
                                open[adjacent_pos] = adjacent_node


                        else: # If it's not open, make it so
                            # Set the parent and the score
                            nodes[adjacent_pos].set_parent_and_score(current_pos,
                                                               current_node.g,
                                                               end_pos)

                            open[adjacent_pos] = adjacent_node

        # If a path was found, return a list of tuple coordinates
        # by tracing it backwards.
        path_pos = nodes[end_pos].parent
        path = []
        while path_pos <> None:
            path.append(path_pos)
            path_pos = nodes[path_pos].parent

        # Remove the starting node
        path.pop()

        return path