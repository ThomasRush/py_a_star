
import pygame
from Position import Position
from Node import Node
from Node_Map import Node_Map
from time import time

# TODO: pass in the map type and
# support rendering conventional grids
class Renderer:

    START_HEX_COLOR = pygame.Color(0,255,0)
    END_HEX_COLOR = pygame.Color(255,0,0)
    PATH_COLOR = pygame.Color(192,192,0)
    BARRIER_COLOR = pygame.Color(0,0,255)

    def __init__(self,graphic_size,map_type):
        self.graphic_size = graphic_size
        self.map_type = map_type

        if (map_type == Node_Map.Map_Type.GRID):
            create_graphic = self.create_square_gfx
            self.render = self.render_square_map
        elif (map_type == Node_Map.Map_Type.HEX):
            create_graphic = self.create_hex_gfx
            self.render = self.render_hex_map
        else:
            # TODO: raise map type not found error
            raise Exception("Map type not found")

        self.empty_node_gfx = create_graphic(None)
        self.start_node_gfx = create_graphic(self.START_HEX_COLOR)
        self.end_node_gfx = create_graphic(self.END_HEX_COLOR)
        self.path_node_gfx = create_graphic(self.PATH_COLOR)
        self.barrier_node_gfx = create_graphic(self.BARRIER_COLOR)

    def get_map_size_pixels(self,map_size):

        map_type = self.map_type
        g = self.graphic_size

        # Width and height in nodex across
        w = map_size.width
        h = map_size.height

        # Width and height in pixels
        w_pix = h_pix = 0

        if map_type == Node_Map.Map_Type.HEX:
            w_pix = int((w *  g * 0.75) - (0.25 * g))
            h_pix = int(((h+1) * g) - (0.5 * g))+1
        elif map_type == Node_Map.Map_Type.GRID:
            w_pix = map_size.width * g
            h_pix = map_size.height * g


        return w_pix,h_pix


    def create_square_gfx(self,color):

        square_size = self.graphic_size
        s = pygame.Surface((square_size,square_size))
        white = pygame.Color(255,255,255,0)
        magenta = pygame.Color(255,0,255)
        s.fill(magenta)

        top_left = (0,0)
        top_right = (square_size,0)
        bottom_right = (square_size,square_size)
        bottom_left = (0,square_size)

        # fill region
        if color != None:
            points = []
            points.append(top_left)
            points.append(top_right)
            points.append(bottom_right)
            points.append(bottom_left)

            pygame.draw.polygon(s, color, points)

        # Draw outlines
        pygame.draw.line(s, white, top_left, top_right, 1)
        pygame.draw.line(s, white, top_right, bottom_right,1)
        pygame.draw.line(s, white, bottom_right, bottom_left,1)
        pygame.draw.line(s, white, bottom_left, top_left,1)

        # Set color key to magenta for transparency
        s.set_colorkey(magenta)
        return s

    def create_hex_gfx(self,color):
        hex_size = self.graphic_size

        s = pygame.Surface((hex_size,hex_size))
        magenta = pygame.Color(255,0,255)
        s.fill(magenta)
        white = pygame.Color(255,255,255,0)

        half = hex_size / 2
        quarter = hex_size / 4

        # Hexagon points
        #
        #   1___2
        #   /   \
        # 6/     \3
        #  \     /
        #   \___/
        #   5   4

        # Color the hex region
        if color != None:
            points = []
            points.append((quarter,0)) #1
            points.append((3*quarter,0)) #2
            points.append((4*quarter-1,half)) #3
            points.append((3*quarter,4*quarter-1)) #4
            points.append((quarter,4*quarter-1)) #5
            points.append((0,half)) #6

            pygame.draw.polygon(s, color, points)

        # Draw outlines
        pygame.draw.line(s, white, (0,half), (quarter,0), 1)
        pygame.draw.line(s, white, (quarter,0), (3*quarter,0),1)
        pygame.draw.line(s, white, (3*quarter,0), (4*quarter-1,half),1)
        pygame.draw.line(s, white, (4*quarter-1,half), (3*quarter,2*half),1)
        pygame.draw.line(s, white, (3*quarter,2*half-1), (quarter,2*half-1),1)
        pygame.draw.line(s, white, (quarter, 2*half-1), (0,half),1)

        # Set color key to magenta for transparency
        s.set_colorkey(magenta)

        return s

    def render_square_map(self,node_map,path,screen):

        # Get some short names to work with
        m_width = node_map.size.width
        m_height = node_map.size.height
        g = self.graphic_size # hex size

        magenta = pygame.Color(255,0,255)

        p = Node.Property

        b = pygame.Surface((m_width * g, m_height * g))
        b.set_colorkey(magenta)

        for y in range(0,m_height):
            for x in range(0,m_width):
                x_blit = x * g
                y_blit = y * g

                node_property = node_map.get_property_at((x,y))

                if (x,y) in path:
                    b.blit(self.path_node_gfx, (x_blit,y_blit))
                elif node_property == p.START:
                    b.blit(self.start_node_gfx, (x_blit,y_blit))
                elif node_property == p.END:
                    b.blit(self.end_node_gfx, (x_blit,y_blit))
                elif node_property == p.BARRIER:
                    b.blit(self.barrier_node_gfx, (x_blit,y_blit))
                else:
                    b.blit(self.empty_node_gfx, (x_blit,y_blit))

        # Show the screen buffer
        screen.blit(b,(0,0))
        pygame.display.flip()

    def render_hex_map(self,node_map, path, screen):

        # Get some short names to work with
        m_width = node_map.size.width
        m_height = node_map.size.height
        g = self.graphic_size # hex size

        magenta = pygame.Color(255,0,255)

        p = Node.Property

        # Map graphics buffer; acount for extra
        # space required by staggered hexagons
        h = int(((m_height+1) * g) - (0.5 * g))+1
        w = int(m_width *  g * 0.75) - (0.25 * g)
        b = pygame.Surface((w, h))

        # Magenta is the transparency color
        b.set_colorkey(magenta)

        for y in range(0,m_height):
            for x in range(0,m_width):

                x_blit = (x * g)
                y_blit = (y * g)

                # Offset even rows downward
                if x % 2 != 0:
                    y_blit += (g/2)

                # Account for the fact that each
                # column will be "pulled back" by a
                # quarter of a hex so they interlock.
                if x > 0:
                    x_blit -= ((g/4)+1)*x

                node_property = node_map.get_property_at((x,y))

                if (x,y) in path:
                    b.blit(self.path_node_gfx, (x_blit,y_blit))
                elif node_property == p.START:
                    b.blit(self.start_node_gfx, (x_blit,y_blit))
                elif node_property == p.END:
                    b.blit(self.end_node_gfx, (x_blit,y_blit))
                elif node_property == p.BARRIER:
                    b.blit(self.barrier_node_gfx, (x_blit,y_blit))
                else:
                    b.blit(self.empty_node_gfx, (x_blit,y_blit))

        # Show the screen buffer
        screen.blit(b,(0,0))
        pygame.display.flip()

