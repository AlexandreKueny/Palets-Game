# -*- coding: utf-8 -*-

from load_json import *

settings = readSettings()

screen_size = [settings["screen"]["screen_size_x"], settings["screen"]["screen_size_y"]]
music_state = settings["sounds"]["music"]["state"]
music_vol = settings["sounds"]["music"]["volume"]
but = 0
