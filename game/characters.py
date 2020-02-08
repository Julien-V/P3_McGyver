#!/usr/bin/python3
# coding : utf-8

import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
