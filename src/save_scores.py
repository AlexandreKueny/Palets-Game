# -*- coding: utf-8 -*-

from Modified_json import *
import os

def save_scores(nameA, nameB, points,butA ,butB ,date, duration, mode):
    # on lis le fichier existant
    with open('scores_' + mode + '.json', 'r') as f:
        if os.stat('scores_' + mode + '.json').st_size > 0:
            dr = f.read()
            data = json_loads(dr)
        else:
            data = {}

    if data:
        size = len(data["games"])
    else:
        size = 0

    id = size + 1

    # on ajoute les nouvelles données
    scores = {}
    scores["stats"] = [0]
    scores["stats"][0] = {}
    if data:
        scores["games"] = {}
        scores["stats"][0]["points tot"] = data["stats"][0]["points tot"] + points
        scores["stats"][0]["games tot"] = data["stats"][0]["games tot"] + 1
        scores["stats"][0]["time tot"] = data["stats"][0]["time tot"] + duration

        scores["games"]["id"] = id
        scores["games"]["date"] = date
        scores["games"]["duree"] = duration
        scores["games"]["Joueur A"]=nameA
        scores["games"]["Joueur B"]=nameB
        scores["games"]["points"]=points
        scores["games"]["but A"]=butA
        scores["games"]["but B"]=butB
    else:
        scores["games"] = [0]
        scores["games"][0] = {}
        scores["stats"][0]["points tot"] = points
        scores["stats"][0]["games tot"] = 1
        scores["stats"][0]["time tot"] = duration

        scores["games"][0]["id"] = id
        scores["games"][0]["date"] = date
        scores["games"][0]["duree"] = duration
        scores["games"][0]["Joueur A"]=nameA
        scores["games"][0]["Joueur B"]=nameB
        scores["games"][0]["points"]=points
        scores["games"][0]["but A"]=butA
        scores["games"][0]["but B"]=butB

    if data:
        data["games"].append(scores["games"])
        data["stats"] = (scores["stats"])
    else:
        data.update(scores)
    dt = json_dumps(data, indent=4, sort_keys=True)
    # on sauvegarde le fichier
    with open('scores_' + mode + '.json', 'w') as f:
        f.write(dt)
