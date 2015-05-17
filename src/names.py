# -*- coding: utf-8 -*-

import inputbox
from zModule import *


def ask_names_local():
    screen = pygame.display.get_surface()
    names = [None, None]

    screen.fill(0xffffff)

    names[0] = inputbox.ask(screen, "Joueur 1", 6)
    if names[0] == "":
        return names
    names[1] = inputbox.ask(screen, "Joueur 2", 6)
            
    return names

def ask_name_reseau():
    screen = pygame.display.get_surface()
    name = None

    screen.fill(0xffffff)

    name = inputbox.ask(screen, "Nom", 6)

    return name