#!/usr/bin/python3
# coding : utf-8

import os
import pygame
from game.core import Game


class GameEngine(object):

    def __init__(self, zoom, u_size, nb_elements, maplvl="lvl/01.map"):
        self.maplvl = maplvl
        self.cfg = [zoom, u_size, nb_elements]
        pygame.init()
        pygame.font.init()
        self.screen_size = (nb_elements[0]*u_size, nb_elements[1]*u_size)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Help McGyver")
        pygame.mouse.set_visible(False)
        self.init_img()

    def init_img(self):
        # Img loading :
        self.img_dict = {}
        # ** Characters
        player_img = self.load_image("res", "MacGyver.png")
        boss_img = self.load_image("res", "Gardien.png")
        self.img_dict["player"] = self.resize(player_img)
        self.img_dict["boss"] = self.resize(boss_img)
        # ** Structures
        struct_img = self.load_image("res", "floor-tiles-20x20.png")
        struct_img_list = self.slice_sprites(struct_img)
        self.img_dict["0"] = struct_img_list[1]
        self.img_dict["1"] = struct_img_list[9]
        self.img_dict["2"] = struct_img_list[0]
        self.img_dict["3"] = struct_img_list[3]
        self.img_dict["struct_list"] = struct_img_list
        # ** Items
        needle_img = self.load_image("res", "aiguille.png")
        ether_img = self.load_image("res", "ether.png")
        pipe_img = self.load_image("res", "tube_plastique.png")
        items_img = [needle_img, ether_img, pipe_img]
        self.img_dict["items_list"] = [self.resize(img) for img in items_img]

    def load_image(self, path, filename):
        img = pygame.image.load(os.path.join(path, filename)).convert_alpha()
        return img

    def resize(self, img):
        u_size = self.cfg[1]
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

    def slice_sprites(self, img):
        """Slice a surface of different sprite"""
        size = self.cfg[1]/self.cfg[0]
        nb_elements_per_line = int(img.get_width()/size)
        nb_elements_per_column = int(img.get_height()/size)
        sliced_sprite_list = []
        for i in range(0, nb_elements_per_column):
            for j in range(0, nb_elements_per_line):
                square = pygame.Rect((j*size, i*size), (size, size))
                sprite = img.subsurface(square)
                if self.cfg[0] > 1:
                    uu_size = (self.cfg[1], self.cfg[1])  # u_size, u_size
                    sprite = pygame.transform.scale(sprite, uu_size)
                sliced_sprite_list.append(sprite)
        return sliced_sprite_list

    def run(self):
        # level management in future versions here :
        self.level = Game(self.maplvl, self.img_dict, self.cfg)
        while self.level.playing:
            self.level.events_manager()
            self.level.game(self.screen)
            self.level.render_game(self.screen)
        # exit
        pygame.quit()
