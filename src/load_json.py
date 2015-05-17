# -*- coding: utf-8 -*-

import json

def readSettings():

    with open("settings.json", "r") as f:
        return json.load(f)