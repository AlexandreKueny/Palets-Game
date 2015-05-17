# -*- coding: utf-8 -*-

from zModule import *
from load_datas import *
import datetime
from Modified_json import *

screen = pygame.display.get_surface()
send_thread = pygame.time.Clock()

data = {}
games = []
end = False

page_index = 0


def exit():
    from main import *

    loop()


return_btn = zImgButton(exit, (50, 675), retour, retour_2, 'alpha')


# affiche l'historique des scores
def show_scores(mode):
    global data
    global games

    with open('scores_' + mode + '.json', "r") as f:
        if os.stat('scores_' + mode + '.json').st_size > 0:
            dr = f.read()
            data = json_loads(dr)
        else:
            data = {}

    if data:
        for g in (data["games"]):
            games.append(g)

        games.reverse()

        show_stats()
        show_historique()
        show_column_title(400)
        show_datas(450)

    else:
        zTextDraw(screen, "Aucune donnees", 50, (50, 50), None, BLACK)

    loop()


def loop():
    global games
    global end
    global page_index

    next = zTextButton(next_page, (900, 700), "Next", 50, None, BLACK)
    prev = zTextButton(prev_page, (800, 700), "Prev", 50, None, BLACK)

    while True:
        send_thread.tick(20)

        events = pygame.event.get()
        for e in events:
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                if page_index > 0:
                    prev_page()
                else:
                    exit()

        if len(games) > 5 and end == False:
            next.update(events)
            next.draw(screen)
        if page_index > 0:
            prev.update(events)
            prev.draw(screen)
        return_btn.update(events)
        return_btn.draw(screen)
        pygame.display.flip()


# affiche les statistiques généraux
def show_stats():
    global data

    s = data["stats"][0]["time tot"].seconds % 60
    m = (data["stats"][0]["time tot"].seconds - s) % 59
    if s < 10:
        s = '0' + str(s)
    else:
        s = str(s)
    if m < 10:
        m = '0' + str(m)
    else:
        m = str(m)

    zTextDraw(screen, "Stats", 50, (50, 50), None, BLACK)
    zTextDraw(screen, "Nombre de parties jouees : " + str(data["stats"][0]["games tot"]), 30, (50, 150), None, BLACK)
    zTextDraw(screen, "Temps de jeu total : " + m + ':' + s, 30, (50, 200), None, BLACK)
    zTextDraw(screen, "Nombre de points : " + str(data["stats"][0]["points tot"]), 30, (50, 250), None, BLACK)


def show_historique():
    zTextDraw(screen, "Historique des parties", 50, (50, 300), None, BLACK)


def show_column_title(y):
    zTextDraw(screen, "Id", 30, (50, y), None, BLACK)
    zTextDraw(screen, "Date", 30, (100, y), None, BLACK)
    zTextDraw(screen, "Duree", 30, (320, y), None, BLACK)
    zTextDraw(screen, "Buts", 30, (400, y), None, BLACK)
    zTextDraw(screen, "Points", 30, (470, y), None, BLACK)
    zTextDraw(screen, "Joueur 1", 30, (560, y), None, BLACK)
    zTextDraw(screen, "Joueur 2", 30, (690, y), None, BLACK)
    zTextDraw(screen, "Gagnant", 30, (820, y), None, BLACK)


# affiche les données
def show_datas(y):
    global games
    global page_index
    global end

    if page_index == 0:
        debut = 0
        fin = 4
    else:
        debut = 5 + ((page_index - 1) * 12)
        fin = debut + 11

    for i, g in enumerate(games):
        if i <= fin and i >= debut:
            zTextDraw(screen, str(g["id"]), 30, (50, y + (50 * (i - debut))), None, BLACK)
            zTextDraw(screen, datetime.datetime.fromtimestamp(g["date"]).strftime('%d/%m/%Y %H:%M:%S'), 30,
                      (100, y + (50 * (i - debut))), None, BLACK)
            s = g["duree"].seconds % 60
            m = (g["duree"].seconds - s) % 59
            if s < 10:
                s = '0' + str(s)
            else:
                s = str(s)
            if m < 10:
                m = '0' + str(m)
            else:
                m = str(m)
            zTextDraw(screen,m + ':' + s, 30, (320, y + (50 * (i - debut))), None, BLACK)
            zTextDraw(screen, str(g["but A"]) + "/" + str(g["but B"]), 30, (400, y + (50 * (i - debut))), None, BLACK)
            zTextDraw(screen, str(g["points"]), 30, (470, y + (50 * (i - debut))), None, BLACK)
            zTextDraw(screen, str(g["Joueur A"]), 30, (560, y + (50 * (i - debut))), None, BLACK)
            zTextDraw(screen, str(g["Joueur B"]), 30, (690, y + (50 * (i - debut))), None, BLACK)
            if g["points"] > 0:
                zTextDraw(screen, str(g["Joueur A"]), 30, (820, y + (50 * (i - debut))), None, BLACK)
            elif g["points"] < 0:
                zTextDraw(screen, str(g["Joueur B"]), 30, (820, y + (50 * (i - debut))), None, BLACK)
            else:
                zTextDraw(screen, "Egalit�", 30, (820, y + (50 * (i - debut))), None, BLACK)
            if g["id"] == 1:
                end = True


def next_page():
    global page_index
    page_index += 1

    screen.fill((255, 255, 255))

    show_column_title(50)
    show_datas(100)
    loop()


def prev_page():
    global page_index
    global end
    page_index -= 1
    end = False

    screen.fill((255, 255, 255))

    if page_index > 0:
        show_column_title(50)
        show_datas(100)
    else:
        show_stats()
        show_historique()
        show_column_title(400)
        show_datas(450)
    loop()
    
        
    