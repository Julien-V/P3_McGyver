#!/usr/bin/python3
# coding : utf-8

import os
import pygame
from game.core import Game


def load_image(path, filename):
    img = pygame.image.load(os.path.join(path, filename)).convert_alpha()
    return img


def resize(img):
    h = img.get_rect().height
    w = img.get_rect().width
    if h >= w:
        w = u_size*w/h
        h = u_size
    elif w >= h:
        h = u_size*h/w
        w = u_size
    img_resized = pygame.transform.scale(img, (int(h), int(w)))
    return img_resized


def slice_sprites(img, size, zoom=1):
    """Slice a surface of different sprite"""
    nb_elements_per_line = int(img.get_width()/size)
    nb_elements_per_column = int(img.get_height()/size)

    sliced_sprite_list = []
    for i in range(0, nb_elements_per_column):
        for j in range(0, nb_elements_per_line):
            square = pygame.Rect(j*size, i*size, size, size)
            sprite = img.subsurface(square)
            if zoom > 1:
                sprite = pygame.transform.scale(sprite, (u_size, u_size))
            sliced_sprite_list.append(sprite)
    return sliced_sprite_list


def main(zoom, u_size, nb_elements):
    pygame.init()
    pygame.font.init()
    screen_size = (nb_elements[0]*u_size, nb_elements[1]*u_size)
    screen = pygame.display.set_mode(screen_size)  # (15*20*zoom, 15*20*zoom)
    pygame.display.set_caption("Help McGyver")
    pygame.mouse.set_visible(False)
    # Img loading :
    img_dict = {}
    # ** Characters
    img_dict["player"] = resize(load_image("res", "MacGyver.png"))
    img_dict["boss"] = resize(load_image("res", "Gardien.png"))
    # ** Structures
    struct_img = load_image("res", "floor-tiles-20x20.png")
    struct_img_list = slice_sprites(struct_img, u_size/zoom, zoom)
    img_dict["0"] = struct_img_list[1]
    img_dict["1"] = struct_img_list[9]
    img_dict["2"] = struct_img_list[0]
    img_dict["3"] = struct_img_list[3]
    img_dict["struct_list"] = struct_img_list
    # ** Items
    needle_img = resize(load_image("res", "aiguille.png"))
    ether_img = resize(load_image("res", "ether.png"))
    pipe_img = resize(load_image("res", "tube_plastique.png"))
    img_dict["items_list"] = [needle_img, ether_img, pipe_img]

    # level management in future versions here :
    cfg = [zoom, u_size, nb_elements]
    level = Game("lvl/01.map", img_dict, cfg)
    while level.playing:
        level.events_manager()
        level.game(screen)
        level.render_game(screen)
    # exit
    pygame.quit()


if __name__ == "__main__":
    zoom = 3
    u_size = 20*zoom  # unit size (nb pixel*zoom)
    nb_elements = (15, 15)  # nb elements (nb_lines, nb_columns)
    main(zoom, u_size, nb_elements)
