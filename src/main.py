# -*- coding: utf-8 -*-

from zModule import *
from load_datas import *
from load_instances import *
from screens import *

# on affiche le menu principal
def show_menu():

    game.MainMenu.submenu("Entrainement",s1)
    game.MainMenu.submenu("Multijoueur",s2)
    game.MainMenu.submenu("Scores",s3)
    game.MainMenu.submenu("Options",s4)
    game.MainMenu.submenu("Quitter",sys.exit)

    game.MainMenu.set_dim(60)
    game.MainMenu.center_at(200, 250)

    game.MainMenu.set_normal_color(GREEN)
    game.MainMenu.set_highlight_color(RED)


def loop():
    game.mainloop()

if __name__ == '__main__':

    show_menu()
    loop()
