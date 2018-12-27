#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Khachig Ainteblian <ainteblian99@gmail.com>
#
# Distributed under terms of the MIT license.

import pygame
from time import time, sleep
from random import choice


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


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pong")

    scr_height = 500
    scr_width = 750

    screen = pygame.display.set_mode((scr_width, scr_height))

    font = pygame.font.SysFont("monospace", 45)
    
    welcome_message = font.render("Press space to start!", True, (255, 255, 255))
    welcome_rect = welcome_message.get_rect(center=(scr_width // 2, scr_height // 4))
    game_over = font.render("Game Over!", True, (255, 255, 255))
    game_rect = game_over.get_rect(center=(scr_width // 2, scr_height // 3))
    play_again = font.render("Press P to play again.", True, (255, 255, 255))
    play_rect = play_again.get_rect(center=(scr_width // 2, scr_height // 2))
    quit_game = font.render("Press Q to quit game.", True, (255, 255, 255))
    quit_rect = quit_game.get_rect(center=(scr_width // 2, scr_height - (scr_height // 3)))

    clock = pygame.time.Clock()

    done = False
    freeze = True
    win_score = 5

    pegLeft = Peg(screen, scr_height, 30)
    pegRight = Peg(screen, scr_height, scr_width - 30 - Peg.width)
    ball = Ball(screen, scr_height, scr_width)
   
    screen.blit(welcome_message, welcome_rect)

    pygame.display.flip()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Game pauses/unpauses when space button is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                freeze = not freeze

        if freeze: continue

        screen.fill((0, 0, 0))

        pressed = pygame.key.get_pressed()

        if ball.left_score == win_score or ball.right_score == win_score:
            # Game over screen
            screen.blit(game_over, game_rect)
            screen.blit(play_again, play_rect)
            screen.blit(quit_game, quit_rect)
            # Q to quit, P to play again
            if pressed[pygame.K_q]: done = not done
            if pressed[pygame.K_p]:
                ball.left_score = 0
                ball.right_score = 0
                pegLeft.y_pos = (scr_height // 2) - (Peg.height // 2)  
                pegRight.y_pos = pegLeft.y_pos
                ball.spawn()
            pygame.display.flip()
            # Skip rest of while loop until a decision is made
            continue

        # Key bindings
        if pressed[pygame.K_w]: pegLeft.go_up()
        if pressed[pygame.K_s]: pegLeft.go_down()
        if pressed[pygame.K_UP]: pegRight.go_up()
        if pressed[pygame.K_DOWN]: pegRight.go_down()


        # Score board
        left_score = font.render(str(ball.left_score)  , True, (255, 255, 255))
        left_rect = left_score.get_rect(center=(scr_width // 4, scr_height // 2))
        right_score = font.render(str(ball.right_score), True, (255, 255, 255))
        right_rect = right_score.get_rect(center=(scr_width - (scr_width // 4), scr_height // 2))
        screen.blit(left_score, left_rect)
        screen.blit(right_score, right_rect)

        # Drawing everything onto the frame
        pegLeft.draw()
        pegRight.draw()
        ball.draw()
        ball.change_position()
        ball.change_direction(Peg.height, pegLeft.x_pos, pegLeft.y_pos, pegRight.x_pos, pegRight.y_pos)

        # Slowing things down a bit
        clock.tick(90)

        # Advance the frame
        pygame.display.flip()
