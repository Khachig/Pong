#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 Khachig Ainteblian <ainteblian99@gmail.com>
#
# Distributed under terms of the MIT license.

import pygame

class Peg:

    height = 40
    width = 10
    colour = (240, 240, 240)
    speed = 6

    def __init__(self, scr, scr_height, x_pos):
        self.scr = scr
        self.scr_height = scr_height
        self.x_pos = x_pos
        # Center the peg in the y axis
        self.y_pos = (scr_height // 2) - (Peg.height // 2) 
        self.draw()

    def draw(self):
        pygame.draw.rect(self.scr, Peg.colour, pygame.Rect(self.x_pos, self.y_pos, Peg.width, Peg.height))

    # Basic collision logic for pegs
    def go_up(self):
        if not self.y_pos <= 0:
            self.y_pos -= Peg.speed

    def go_down(self):
        if not self.y_pos >= (self.scr_height - Peg.height):
            self.y_pos += Peg.speed

