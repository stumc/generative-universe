import io

import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image, ImageOps

from generate_universe_lib.pygame_windows.drop_down import show_shape_menu


class ShapeDraw:
    def __init__(self):
        self.vertices = ()
        self.edges = ()
        # self.initialize_cube()
        # self.initialize_pyramid()
        # self.initialize_sphere(24, 12)
        # self.initialize_2d_star(5)
        # self.initialize_3d_star(25, 13, 0.75)

    def initialize_none(self):
        self.vertices = ((1, 1, 1))
        self.edges = ()

    def initialize_point(self):
        self.vertices = (
            (0, 0, 0),
            (0.1, 0.1, 0.1),
        )

        self.edges = (
            (0,1),
        )
    def initialize_line(self):
        self.vertices = (
            (1, 1, 1),
            (-1, 1, -1)
        )

        self.edges = (
            (0,1),
        )

    def initialize_cube(self):
        self.vertices = (
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, -1, 1),
            (-1, 1, 1)
        )

        self.edges = (
            (0,1),
            (0,3),
            (0,4),
            (2,1),
            (2,3),
            (2,7),
            (6,3),
            (6,4),
            (6,7),
            (5,1),
            (5,4),
            (5,7)
        )

    def initialize_pyramid(self):
        self.vertices = (
            (0, 1, 0),  # top
            (1, -1, 1),  # front right
            (-1, -1, 1),  # front left
            (-1, -1, -1),  # back left
            (1, -1, -1)  # back right
        )

        self.edges = (
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 1)
        )

    def initialize_2d_star(self, n=5):
        self.vertices = []
        self.edges = []

        angle_step = 2 * math.pi / n
        outer_radius = 1
        inner_radius = 0.5

        # Generate vertices
        for i in range(n):
            angle = i * angle_step

            outer_x = outer_radius * math.cos(angle)
            outer_y = outer_radius * math.sin(angle)
            outer_z = 0
            self.vertices.append((outer_x, outer_y, outer_z))

            inner_x = inner_radius * math.cos(angle + angle_step / 2)
            inner_y = inner_radius * math.sin(angle + angle_step / 2)
            inner_z = 0
            self.vertices.append((inner_x, inner_y, inner_z))

        # Generate edges
        for i in range(n):
            outer_index = i * 2
            inner_index = i * 2 + 1

            self.edges.append((outer_index, inner_index))
            self.edges.append((inner_index, (outer_index + 2) % (n * 2)))

    def initialize_3d_star(self, num_longitude_segments=24, num_latitude_segments=12, inner_radius_ratio=0.5):
        self.vertices = []
        self.edges = []

        # Generate vertices
        for i in range(num_latitude_segments):
            phi = math.pi * (i / num_latitude_segments)
            radius = 1 if i % 2 == 0 else inner_radius_ratio  # Use outer radius for even lines, inner radius for odd lines
            for j in range(num_longitude_segments):
                theta = 2 * math.pi * (j / num_longitude_segments)
                x = radius * math.sin(phi) * math.cos(theta)
                y = radius * math.sin(phi) * math.sin(theta)
                z = radius * math.cos(phi)
                self.vertices.append((x, y, z))

        # Generate edges
        for i in range(num_latitude_segments - 1):
            for j in range(num_longitude_segments):
                # Horizontal edges
                self.edges.append(
                    (i * num_longitude_segments + j, i * num_longitude_segments + (j + 1) % num_longitude_segments))
                # Vertical edges
                self.edges.append((i * num_longitude_segments + j, (i + 1) * num_longitude_segments + j))

        # Horizontal edges for the last latitude line
        for j in range(num_longitude_segments):
            self.edges.append((len(self.vertices) - num_longitude_segments + j,
                               len(self.vertices) - num_longitude_segments + (j + 1) % num_longitude_segments))

    def initialize_sphere(self, num_longitude_segments=24, num_latitude_segments=12):
        self.vertices = []
        self.edges = []

        # Add the top pole
        self.vertices.append((0, 0, 1))

        # Generate vertices and edges for the sphere
        for i in range(1, num_latitude_segments):
            phi = math.pi * (i / num_latitude_segments)
            for j in range(num_longitude_segments):
                theta = 2 * math.pi * (j / num_longitude_segments)
                x = math.sin(phi) * math.cos(theta)
                y = math.sin(phi) * math.sin(theta)
                z = math.cos(phi)
                self.vertices.append((x, y, z))

        # Add the bottom pole
        self.vertices.append((0, 0, -1))

        # Generate edges
        for j in range(num_longitude_segments):
            # Edges from the top pole to the first latitude line
            if j + 1 < len(self.vertices):
                self.edges.append((0, j + 1))
            # Edges from the bottom pole to the last latitude line
            if len(self.vertices) - 1 - num_longitude_segments + j < len(self.vertices):
                self.edges.append((len(self.vertices) - 1, len(self.vertices) - 1 - num_longitude_segments + j))

        for i in range(num_latitude_segments - 1):
            for j in range(num_longitude_segments):
                # Horizontal edges
                if i * num_longitude_segments + (j + 1) % num_longitude_segments + 1 < len(self.vertices):
                    self.edges.append((i * num_longitude_segments + j + 1,
                                       i * num_longitude_segments + (j + 1) % num_longitude_segments + 1))
                # Vertical edges
                if (i + 1) * num_longitude_segments + j + 1 < len(self.vertices):
                    self.edges.append((i * num_longitude_segments + j + 1, (i + 1) * num_longitude_segments + j + 1))

        # Horizontal edges for the last latitude line
        for j in range(num_longitude_segments):
            if len(self.vertices) - 1 - num_longitude_segments + (j + 1) % num_longitude_segments < len(self.vertices):
                self.edges.append((len(self.vertices) - 1 - num_longitude_segments + j,
                                   len(self.vertices) - 1 - num_longitude_segments + (j + 1) % num_longitude_segments))


    def draw_shape(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def main(self):
        pygame.init()
        if not self.edges and not self.vertices:
            show_shape_menu(self)
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

        glTranslatef(0.0, 0.0, -5)

        glRotatef(0, 0, 0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glRotatef(1, 3, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw_shape()
            pygame.display.flip()
            pygame.time.wait(10)

    def render_as_image_file(self, file_name=None):
        # Initialize Pygame
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        # Set up OpenGL
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        glRotatef(0, 0, 0, 0)

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.draw_shape()

        # Read the pixel data from the OpenGL buffer
        pygame.display.flip()
        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(0, 0, display[0], display[1], GL_RGB, GL_UNSIGNED_BYTE)

        # Convert the pixel data to an image
        image = Image.frombytes("RGB", (display[0], display[1]), pixels)
        image = ImageOps.flip(image)

        # optionally Save the image
        if file_name:
            image.save(file_name)

        # Close the Pygame window
        pygame.quit()

        # Create a BytesIO object
        img_byte_arr = io.BytesIO()

        # Save the image to the BytesIO object in PNG format
        image.save(img_byte_arr, format='PNG')

        # Get the byte array
        return img_byte_arr.getvalue()

if __name__ == "__main__":
    shape_to_draw = ShapeDraw()
    shape_to_draw.main()