# -*- coding: utf-8 -*-

import json
import datas

def saveSettings():
    settings = {}
    settings["screen"] = {}
    settings["screen"]["screen_size_x"] = 1024
    settings["screen"]["screen_size_y"] = 768
    settings["sounds"] = {}
    settings["sounds"]["music"] = {}
    settings["sounds"]["music"]["state"] = datas.music_state
    settings["sounds"]["music"]["volume"] = datas.music_vol
    
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)