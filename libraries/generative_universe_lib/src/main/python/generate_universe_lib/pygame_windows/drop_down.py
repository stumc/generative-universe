import pygame
import pygame_menu


def show_shape_menu(shape_rendered):
    pygame.init()
    surface = pygame.display.set_mode((600, 600))
    menu = None

    def set_shape(selected_shape, value):
        print(f'Selected shape: {value}')
        getattr(shape_rendered, value)()
        print(f"shape_rendered {shape_rendered}")
        print(f"getattr(shape_rendered, value) {getattr(shape_rendered, value)}")
        print(f"menu {menu}")
        menu.disable()


    menu = pygame_menu.Menu('Select Shape', 500, 400,
                            theme=pygame_menu.themes.THEME_BLUE)

    menu.add.dropselect('Shape :', [
        ('None', 'initialize_none'),
        ('Point', 'initialize_point'),
        ('Line', 'initialize_line'),
        ('Cube', 'initialize_cube'),
        ('Pyramid', 'initialize_pyramid'),
        ('Star 2d', 'initialize_2d_star'),
        ('Star 3d', 'initialize_3d_star'),
        ('Sphere', 'initialize_sphere')
    ],
                        onchange=set_shape)

    menu.mainloop(surface)
    print("Exit menu.mainloop(surface)")
