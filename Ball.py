#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 Khachig Ainteblian <ainteblian99@gmail.com>
#
# Distributed under terms of the MIT license.

import pygame
from random import choice
from time import sleep

class Ball:

    height = 10
    width = 10
    colour = (240, 240, 240)
    increase = 0.025
    base_x = 2.5
    base_y = 2

    def __init__(self, scr, scr_height, scr_width):
        self.scr = scr
        self.scr_height = scr_height
        self.scr_width = scr_width
        self.x_pos = 0
        self.y_pos = 0
        # These two booleans are used to determine whether to
        # increase or decrease the x and y position on each frame
        self.going_up = bool
        self.going_right = bool
        # These two are the x and y speed of the ball, which are
        # slowly increased as the game goes on for added difficulty
        self.x_rate = Ball.base_x
        self.y_rate = Ball.base_y
        # Ball spawns at the center of the screen every time
        self.spawn_x = (scr_width // 2) - (self.width // 2)
        self.spawn_y = (scr_height // 2) - (self.height // 2)
        self.left_score = 0
        self.right_score = 0
        self.spawn()

    def change_position(self):
        # Increase or decrease the x and y position of the ball
        # based on the two booleans that keep track of the movement
        if self.going_up:
            self.y_pos -= self.y_rate
            if self.going_right:
                self.x_pos += self.x_rate
            else:
                self.x_pos -= self.x_rate
        else:
            self.y_pos += self.y_rate
            if self.going_right:
                self.x_pos += self.x_rate
            else:
                self.x_pos -= self.x_rate

    def change_direction(self, pegHeight, pegLeft_x, pegLeft_y, pegRight_x, pegRight_y):
        # Collision logic for the ball
        # Ball slightly speeds up after each bounce
        # Speed is reset when it hits left or right wall
        if self.y_pos <= 0: # Upper wall
            self.going_up = False
            self.x_rate += Ball.increase
            self.y_rate += Ball.increase
        if self.y_pos >= (self.scr_height - Ball.height): # Lower wall
            self.going_up = True
            self.x_rate += Ball.increase
            self.y_rate += Ball.increase
        if self.x_pos >= (self.scr_width - Ball.width): # Right wall
            self.left_score += 1
            self.spawn()
            sleep(1)
        if self.x_pos <= 0: # Left wall
            self.right_score += 1
            self.spawn()
            sleep(1)
        # If the ball is within the bounds of the peg, bounce back
        if pegLeft_x <= self.x_pos <= (pegLeft_x + self.width): 
            if pegLeft_y <= self.y_pos <= (pegLeft_y + pegHeight):
                self.going_right = True
                self.x_rate += Ball.increase
                self.y_rate += Ball.increase
        if pegRight_x <= self.x_pos <= (pegRight_x + self.width):
            if pegRight_y <= self.y_pos <= (pegRight_y + pegHeight):
                self.going_right = False
                self.x_rate += Ball.increase
                self.y_rate += Ball.increase

    def draw(self):
        pygame.draw.rect(self.scr, Ball.colour, pygame.Rect(self.x_pos, self.y_pos, Ball.width, Ball.height))

    def spawn(self):
        self.going_up = choice([True, False])
        self.going_right = choice([True, False])
        self.x_rate = Ball.base_x
        self.y_rate = Ball.base_y
        self.x_pos = self.spawn_x
        self.y_pos = self.spawn_y 
        self.draw()

