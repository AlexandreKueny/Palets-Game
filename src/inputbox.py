# -*- coding: utf-8 -*-

# by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
import time
import sys


def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == QUIT:
            return event
        if event.type == KEYDOWN:
            # print event
            #print event.dict['unicode'].encode('windows-1252')
            return event
        else:
            pass
        time.sleep(0.01)


def display_box(screen, message):
    "Print a message in a box in the middle of the screen"
    fontobject = pygame.font.Font(None, 18)
    pygame.draw.rect(screen, (255, 255, 255),
                     ((screen.get_width() / 2) - 100,
                      (screen.get_height() / 2) - 10,
                      200, 20), 0)
    pygame.draw.rect(screen, (0, 0, 0),
                     ((screen.get_width() / 2) - 102,
                      (screen.get_height() / 2) - 12,
                      204, 24), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (0, 0, 0)),
                    ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
    pygame.display.flip()


def ask(screen, question, taille):
    "ask(screen, question) -> answer"
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": " + string.join(current_string, ""))
    while 1:
        inkey = get_key()
        if inkey.type == QUIT or inkey.key == K_ESCAPE:
            return ""
        if inkey.key == K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey.key == K_RETURN or inkey.key == K_KP_ENTER:
            break
        elif inkey.key == K_RSHIFT or inkey.key == K_LSHIFT:
            pass
        elif len(current_string) < taille:
            current_string.append(inkey.dict['unicode'].encode('windows-1252'))
        display_box(screen, question + ": " + string.join(current_string, ""))
    return string.join(current_string, "")


def main():
    screen = pygame.display.set_mode((320, 240))
    print ask(screen, "Name") + " was entered"


if __name__ == '__main__':
    main()
