# -*- coding: utf-8 -*-

from zModule import *
from load_datas import *
import datas

class Music():
    
    global music_state
    
    def __init__(self, state, volume):
        pygame.mixer.init()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(volume / 10.0)
        if state == False:
            pygame.mixer.music.stop()
        elif state == True:
            pygame.mixer.music.play(loops=-1)

    def start(self):
        datas.music_state = True
        pygame.mixer.music.play(loops=-1)
        
    def stop(self):
        datas.music_state = False
        pygame.mixer.music.stop()
        
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume/10.0)