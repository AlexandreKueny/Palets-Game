# -*- coding: utf-8 -*-

import os
from zModule import *
import datas

datadir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))

font = os.path.join(datadir,'cubicfive10.ttf')
background = os.path.join(datadir,'background_white.png')
terrain = os.path.join(datadir,'bg.png')
palet_rouge = os.path.join(datadir, 'palet rouge.png')
palet_bleu = os.path.join(datadir, 'palet bleu.png')
palet_rouge_2 = os.path.join(datadir, 'palet rouge 2.png')
palet_bleu_2 = os.path.join(datadir, 'palet bleu 2.png')
ball_path = os.path.join(datadir, 'ball.png')
icon = os.path.join(datadir,'icon.png')
music_file = os.path.join(datadir,'music.mp3')
b1 = os.path.join(datadir,"b1.png")
b2 = os.path.join(datadir,"b2.png")
retour = os.path.join(datadir,"return.png")
retour_2 = os.path.join(datadir,"return_2.png")
#palet = os.path.join(datadir,"palet.png")
player = os.path.join(datadir,"player.png")
vexit = False
red = (200, 50, 25)
blue = (25, 50, 200)
terrain_size = [(51, 973), (194, 720)]
buts_size = [ [(0, 45), (372, 542)], [(979, 1024), (372, 542)]]
ball_start = ((terrain_size[0][1] - terrain_size[0][0]) / 2 + terrain_size[0][0] + 3, (terrain_size[1][1] - terrain_size[1][0]) / 2 + terrain_size[1][0])
positions = [(200, 326), (80, 455), (200, 589), (300, 391), (300, 522), (824, 326), (944, 455), (824, 589), (724, 391), (724, 522)]
but = 0
modif_pos = []
for i in range(0, 800):
    if i % 2:
        modif_pos.append(i)
    else:
        modif_pos.append(-i)