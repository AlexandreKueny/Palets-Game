# -*- coding: utf-8 -*-

from zModule import *
from load_datas import *
from load_instances import *
from save_json import *
import datas
from show_scores import *
from names import *


def exit():
    global vexit
    vexit = True


def leave():
    pass


def show_local():
    show_scores("local")


def show_reseau():
    show_scores("reseau")


def ask_ip():
    screen = pygame.display.get_surface()
    name = None

    screen.fill(0xffffff)

    ip = inputbox.ask(screen, "Server ip", 15)

    return ip


def start_local():
    names = ask_names_local()
    if names[0] == "" or names[1] == "":
        return
    #Jeu_local().start([-1, 1], True, names, False)
    Jeu_reseau().init_local(names, False)

def heberge():
    name = ask_name_reseau()
    if name == "":
        return
    Jeu_reseau().init_server(name, False)
    Jeu_reseau().stop_game()

def rejoint():
    name = ask_name_reseau()
    if name == "":
        return
    ip = ask_ip()
    if ip == "":
        return
    Jeu_reseau().init_client(ip, name, False)
    Jeu_reseau().stop_game()

def choix_reseau():
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    while True:
        clock.tick(20)

        events = pygame.event.get()
        for e in events:
            if e.type == QUIT:
                return
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                return

        global vexit
        if vexit == True:
            vexit = False
            return

        screen.fill(0xffffff)

        reseau_menu.update(events)
        return_btn.update(events)
        reseau_menu.draw(screen)
        return_btn.draw(screen)
        pygame.display.flip()


music_btn = zCheckbutton("Musique", (307, 250), music.start, music.stop, 4, None, BLACK, BLACK, RED)
save_btn = zTextButton(saveSettings, [100, 600], "Save", 30, font, blue, red)
if datas.music_state == True:
    music_btn.select()
elif datas.music_state == False:
    music_btn.unselect()
txt = zAdvText("Options", (0, 0), 50, font, RED)
vol_select = zNumManager("Volume musique", (50, 350), datas.music_vol, 1, 10, 4, None, BLACK, RED, YELLOW)
# menu des scores
scores_menu = zMenu("Scores", (400, 70), 50, font, RED)
scores_menu.submenu("Local", show_local)
scores_menu.submenu("Reseau", show_reseau)
scores_menu.set_normal_color(GREEN)
scores_menu.set_highlight_color(RED)
scores_menu.set_dim(60)
scores_menu.center_at(200, 300)
# menu multijoueur
multi_menu = zMenu("Multijoueur", (400, 70), 50, font, RED)
multi_menu.submenu("Local", start_local)
multi_menu.submenu("Reseau", choix_reseau)
multi_menu.set_normal_color(GREEN)
multi_menu.set_highlight_color(RED)
multi_menu.set_dim(60)
multi_menu.center_at(200, 300)
# menu multijoueur reseau
reseau_menu = zMenu("Reseau", (400, 70), 50, font, RED)
reseau_menu.submenu("Heberger", heberge)
reseau_menu.submenu("Rejoindre", rejoint)
reseau_menu.set_normal_color(GREEN)
reseau_menu.set_highlight_color(RED)
reseau_menu.set_dim(60)
reseau_menu.center_at(200, 300)
return_btn = zImgButton(exit, (100, 65), retour, retour_2, 'alpha')


# lance le mode solo
def s1():
    Jeu_reseau().init_local(["Rouges", "Bleus"], False)


# affiche le menu multijoueur
def s2():
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    while True:
        clock.tick(20)

        events = pygame.event.get()
        for e in events:
            if e.type == QUIT:
                return
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                return

        global vexit
        if vexit == True:
            vexit = False
            return

        screen.fill(0xffffff)

        multi_menu.update(events)
        return_btn.update(events)
        multi_menu.draw(screen)
        return_btn.draw(screen)
        pygame.display.flip()


# affiche le menu scores
def s3():
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    while True:
        clock.tick(20)

        events = pygame.event.get()
        for e in events:
            if e.type == QUIT:
                return
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                return

        global vexit
        if vexit == True:
            vexit = False
            return

        screen.fill(0xffffff)

        scores_menu.update(events)
        return_btn.update(events)
        scores_menu.draw(screen)
        return_btn.draw(screen)
        pygame.display.flip()


# affiche la page des paramètres
def s4():
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    while True:
        clock.tick(20)

        events = pygame.event.get()
        for e in events:
            if e.type == QUIT:
                return
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                return

        global vexit
        if vexit == True:
            vexit = False
            return

        screen.fill(0xffffff)

        datas.music_vol = vol_select.value
        music.set_volume(datas.music_vol)

        music_btn.update(events)
        vol_select.update(events)
        return_btn.update(events)
        save_btn.update(events)
        # size_input.update(events)
        music_btn.draw(screen)
        return_btn.draw(screen)
        save_btn.draw(screen)
        # size_input.draw(screen)

        txt.center_at(512, 70)
        txt.draw(screen)

        vol_select.draw(screen)

        pygame.display.flip()
                            