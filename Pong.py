#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Khachig Ainteblian <ainteblian99@gmail.com>
#
# Distributed under terms of the MIT license.

import pygame
from time import sleep
from random import choice
from Ball import Ball
from Peg import Peg

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
