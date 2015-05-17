# -*- coding: utf-8 -*-

from zModule import *
from load_datas import *
import datas

game = zEngine(datas.screen_size[0], datas.screen_size[1], "Palets Game !!!", icon, (270, 70), 50, font, RED, background)

from Sounds import *
from Games_reseau import *
from Palet import *

music = Music(datas.music_state, datas.music_vol)
