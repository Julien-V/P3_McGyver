#!/usr/bin/python3
# coding : utf-8

import random
import pygame

from game import chrono
from game import msprites
from game import characters


class Game(object):
    """Game core in a class, could be used for easier levels
    implementation"""
    def __init__(self, map_file, img_dict, cfg):
        self.map_file = map_file
        self.img_dict = img_dict
        # cfg == [zoom, u_size, nb_elements]
        self.cfg = cfg
        self.u_size = cfg[1]
        self.playing = True
        self.pause = False
        # sprites groups
        self.wall_group = pygame.sprite.Group()  # useless atm
        self.mazepath_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()
        self.all_sprites_group = pygame.sprite.Group()
        # map
        self.init_map()
        self.init_items()
        # player
        self.mcgyver = characters.Character(self.img_dict['player'])
        self.mcgyver.rect.x = self.start.rect.x
        self.mcgyver.rect.y = self.start.rect.y
        self.all_sprites_group.add(self.mcgyver)
        # boss
        self.boss = characters.Character(self.img_dict['boss'])
        self.boss.rect.x = self.end.rect.x
        self.boss.rect.y = self.end.rect.y
        self.all_sprites_group.add(self.boss)
        # timer
        self.chrono = chrono.Chrono()

    def init_map(self):
        # Load the maze
        with open(self.map_file, "r") as fileA:
            map_in_lines = fileA.read().splitlines()
        # Read the maze
        for id_line, line in enumerate(map_in_lines):
            line_splitted = line.split("/")
            for id_row, element in enumerate(line_splitted):
                # element[0] for future compatibility with "1tn"
                map_elem_img = self.img_dict[element[0]]
                map_elem = msprites.MazeSprite(map_elem_img, element[0])
                map_elem.rect.x = id_row*self.u_size  # x pos
                map_elem.rect.y = id_line*self.u_size  # y pos
                # Add map_elem (sprite) to groups
                if element[0] == "1":
                    self.wall_group.add(map_elem)
                else:
                    if element[0] == "2":
                        self.start = map_elem
                    elif element[0] == "3":
                        self.end = map_elem
                    self.mazepath_group.add(map_elem)
                self.all_sprites_group.add(map_elem)

    def init_items(self):
        # Random img list
        items_img_list = self.img_dict["items_list"]
        random.shuffle(items_img_list)
        # Random item list
        mazepath_list = self.mazepath_group.sprites()
        random.shuffle(mazepath_list)
        # Distribution
        for id_item, img in enumerate(items_img_list):
            new_item = msprites.MazeSprite(img, "4")
            location = mazepath_list[id_item]
            while location.state != "0":  # while not the floor
                # next item
                location = mazepath_list[id_item+1]
            # Just one img for one item
            mazepath_list.remove(location)
            new_item.rect = location.rect
            # Add item to groups
            self.item_group.add(new_item)
            self.all_sprites_group.add(new_item)

    def take_item(self, item):
        # remove item of all groups
        item.kill()
        if not len(self.item_group):
            # boss is going to sleep
            self.boss.isSleeping = True
            self.boss.kill()

    def checkPlayerPosition(self):
        autorisation = True
        if pygame.sprite.spritecollide(self.mcgyver, self.wall_group, 0):
            autorisation = False
        x = self.mcgyver.rect.x
        y = self.mcgyver.rect.y
        surf = pygame.display.get_surface().get_rect()
        if x >= 0 and x < surf.w and y >= 0 and y < surf.h:
            pass
        else:
            autorisation = False
        return autorisation

    def game(self, screen):
        self.all_sprites_group.update()
        item_list = self.item_group.sprites()
        for item in item_list:
            if pygame.sprite.collide_rect(self.mcgyver, item):
                self.take_item(item)
        collision = pygame.sprite.collide_rect(self.mcgyver, self.boss)
        if collision:
            # End Game
            self.chrono.pause()
            self.playing = False
            self.pause = False
            if self.boss.isSleeping:
                print("Victory : {}s".format(int(self.chrono.get_chrono())))
            else:
                print("Game Over : {}s".format(int(self.chrono.get_chrono())))

    def render_game(self, screen):
        if self.playing and not self.pause:
            self.all_sprites_group.draw(screen)
        pygame.display.flip()

    def events_manager(self):
        """Manage events"""
        keys = {
            pygame.K_UP: lambda: self.mcgyver.movement(0, -self.u_size),
            pygame.K_DOWN: lambda: self.mcgyver.movement(0, self.u_size),
            pygame.K_LEFT: lambda: self.mcgyver.movement(-self.u_size, 0),
            pygame.K_RIGHT: lambda: self.mcgyver.movement(self.u_size, 0)
        }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause
                # Movements
                #  = 0 + .. is my ugly way to create a new value
                # without referencing the old one
                # i'm totally open to suggestions for this one
                # since i can't remember how to do it properly
                sav_rect_x = 0 + self.mcgyver.rect.x
                sav_rect_y = 0 + self.mcgyver.rect.y
                if event.key in keys:
                    func = keys[event.key]
                    func()
                    # Test if position isn't possible
                    if not self.checkPlayerPosition():
                        # revert change
                        self.mcgyver.rect.x = sav_rect_x
                        self.mcgyver.rect.y = sav_rect_y
