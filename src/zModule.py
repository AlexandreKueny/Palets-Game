# -*- coding: utf-8 -*-
# zModule
# Copyright (C) 2010  Davide Zagami

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import pygame, os, sys
from pygame.locals import *
# You don't need to include PyIgnition in your source if you don't use an effect.
# Otherwise you must include it in a folder named "PyIgnition", cases are important.
try:
    from PyIgnition.PyIgnition import *
except ImportError:
    print "zModule: warning, PyIgnition not found, will crash if you are trying to add an effect"


if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


WHITE = (255,255,255)
GRAY = (136,136,136)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)


def nothing():
    pass

class NoEffect:
    def Display(self,x):
        pass
    def Update(self):
        pass
    def Redraw(self):
        pass

class NoneSound:
    def play(self,x=0):
        pass
    def stop(self,x=0):
        pass
    def set_volume(self,x=0):
        pass



class zEngine:

    def __init__(self,x=800,y=600,title="pygame window",icon=None,titlepos=None,
                    titledim=60,titlefont=None,titlecolor=WHITE,background=None,effect=None,
                    music=None, move=None,select=None,volume=1.0, flags=0):

        pygame.init()
        self.Xscreen = x
        self.Yscreen = y
        self.screen = pygame.display.set_mode((x,y),flags)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.icon = icon
        if icon:
            self.icon = load_image(icon,'icon')[0]
            pygame.display.set_icon(self.icon)
        if not background:
            self.background = pygame.Surface((x,y))
            self.background.fill(0)
        else:
            self.background = load_image(background)[0]

        self.MainMenu = zMenu(title, (0,0), titledim, titlefont, titlecolor, music, move, select, volume)
        self.MainMenu.Title.create_image()
        if not titlepos:
            self.MainMenu.Title.center_at(x/2, self.MainMenu.Title.height)
        else:
            self.MainMenu.Title.set_pos(titlepos[0], titlepos[1])

        self.effect = NoEffect()
        try:
            ParticleEffect
        except NameError:
            pass
        else:
            if isinstance(effect,ParticleEffect):
                self.effect = effect
            else:
                print "Warning, the effect is not valid, defaulting to NoEffect"
        self.effect.Display(self.screen)



    def mainloop(self):
        self.MainMenu.music.play(-1)
        while True:
            self.clock.tick(20)

            #Handle Input Events
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    self.Quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.Quit()

            self.MainMenu.update(events)
            self.effect.Update()
            self.screen.blit(self.background, (0,0))
            self.effect.Redraw()
            self.MainMenu.draw(self.screen)
            pygame.display.flip()


    def Quit(self):

        print("AAA")
        pygame.quit()
        sys.exit()




#This function immediately blits a text on a surface
def zTextDraw(surface, text, dim, pos, font=None, color=WHITE):
    font = pygame.font.Font(font,dim)
    image = font.render(text, 1, color)
    surface.blit(image,pos)




class zAdvText:

    def __init__(self, text, pos, dim, font=None, color=WHITE):
        self.Font = pygame.font.Font(font,dim)
        self.font = font
        self.text = text
        self.color = color
        self.pos = pos
        self.dim = dim
        self.height = 1
        self.width = 1
        self.edit = True
        self.create_image()


    def collidepoint(self,point):
        if self.pos[0] <= point[0] <= self.pos[0]+self.image.get_width():
            if self.pos[1] <= point[1] <= self.pos[1]+self.Font.get_height():
                return True
        return False


    def set_text(self, newtext):
        self.text = newtext
        self.edit = True


    def set_color(self, newcolor):
        self.color = newcolor
        self.edit = True


    def set_pos(self,x,y):
        self.pos = (x,y)


    def center_at(self,x,y):
        x = x-(self.width/2)
        y = y-(self.height/2)
        self.pos = (x,y)


    def set_dim(self,newdim):
        self.dim = newdim
        self.edit = True


    def set_font(self,newfont):
        self.font = newfont
        self.edit = True


    def create_image(self):
        self.Font = pygame.font.Font(self.font,self.dim)
        self.image = self.Font.render(self.text, 1, self.color)
        self.height = self.Font.get_height()
        self.width = self.image.get_width()
        self.edit = False


    def draw(self,surface):
        if self.edit:
            self.create_image()
        surface.blit(self.image, self.pos)




class zMenu:

    def __init__(self, title, pos, dim, font=None, color=WHITE, music=None, move=None, select=None, volume=1.0):
        self.Title = zAdvText(title,pos,dim,font,color)
        self.submenus = []
        self.functions = []
        self.index = 0
        self.smdim = dim/2
        self.normal_color = WHITE
        self.highlight_color = GRAY
        self.counter = 0
        self.inc = 0
        self.cmp = 6
        self.key = 0
        self.music = NoneSound()
        self.move = NoneSound()
        self.select = NoneSound()
        self.volume = volume
        self.audio = True
        if music:
            self.music = load_sound(music)
        if move:
            self.move = load_sound(move)
        if select:
            self.select = load_sound(select)
        self.music.set_volume(volume)
        self.move.set_volume(1.0)
        self.select.set_volume(1.0)
        self.soundsOn = nothing
        self.soundsOff = nothing


    def submenu(self, text,func):
        self.submenus.append( zAdvText(text,0,self.smdim) )
        self.functions.append(func)
        self._reload()

    def collidepoint(self,point):
        for sm in self.submenus:
            if sm.collidepoint(point):
                return True
        return False

    def play_music(self):
        self.music.play(-1)

    def stop_music(self):
        self.music.stop()

    def sounds_player(self,f):
        self.soundsOn = f

    def sounds_stopper(self,f):
        self.soundsOff = f

    def _set_color(self,newcolor):
        for sm in self.submenus:
            sm.set_color(newcolor)


    def set_normal_color(self, newcolor):
        self.normal_color = newcolor
        self._set_color(newcolor)


    def set_highlight_color(self, newcolor):
        self.highlight_color = newcolor


    def set_pos(self,x,y):
        i=1
        h = self.submenus[0].height
        for sm in self.submenus:
            sm.set_pos(x,y+h*i)
            i+=1


    def center_at(self,x,y):
        i=1
        h = self.submenus[0].height
        for sm in self.submenus:
            sm.center_at(x,y+h*i)
            i+=1


    def set_dim(self,newdim):
        for sm in self.submenus:
            sm.set_dim(newdim)
        self._reload()


    def set_font(self,newfont):
        for sm in self.submenus:
            sm.set_font(newfont)
        self._reload()


    def _reload(self):
        self.Title.create_image()
        for sm in self.submenus:
            sm.create_image()

        x = self.Title.pos[0] + self.Title.width/2
        y = self.Title.pos[1] + self.Title.height*2
        self.center_at(x,y)


    def _selected(self):
        p = pygame.mouse.get_pos()
        i=0
        while i<len(self.submenus):
            if self.submenus[i].collidepoint(p):
                return i
            i+=1
        return -1


    def update(self, events):
        self.submenus[self.index].set_color(self.normal_color)
        i = self._selected()
        if i != -1:
            if self.index != i:
                self.move.play()
                self.index = i

        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_DOWN:
                    self.move.play()
                    self.inc = 1
                    self.index += 1
                    self.key = K_DOWN

                elif e.key == K_UP:
                    self.move.play()
                    self.inc = 1
                    self.index -= 1
                    self.key = K_UP

                elif e.key == K_RETURN:
                    self.select.play()
                    self.functions[self.index]()

                elif e.key == K_m:
                    if self.audio:
                        self.soundsOff()
                    else:
                        self.soundsOn()


            elif e.type == KEYUP:
                self.counter = 0
                self.inc = 0
                self.cmp = 6
                self.key = 0

            elif e.type == MOUSEBUTTONUP and e.button == 1 and i != -1:
                self.select.play()
                self.functions[self.index]()
                break

        self.counter += self.inc
        if self.counter == self.cmp:
            self.counter = 0
            self.cmp = 2
            if self.key == K_UP:
                self.move.play()
                self.index -= 1
            elif self.key == K_DOWN:
                self.move.play()
                self.index += 1

        if self.index > len(self.functions)-1:
            self.index = 0
        elif self.index < 0:
            self.index = len(self.functions)-1

        self.submenus[self.index].set_color(self.highlight_color)


    def draw(self,surface):
        self.Title.draw(surface)
        for sm in self.submenus:
            sm.draw(surface)



class zCheckbutton:

    def __init__(self, text, pos, activate, deactivate, m=2, font=None, textcolor=BLACK, rectcolor=WHITE, crosscolor=BLACK, state=False):
        if not (text and m):
            raise TypeError, "Invalid checkbutton"

        self.normal_image = pygame.Surface((10*m,10*m))
        self.normal_image.fill(1)
        pygame.draw.rect(self.normal_image,rectcolor,pygame.Rect(m,m,8*m,8*m),int(m))
        self.normal_image.set_colorkey(1)

        self.selected_image = self.normal_image.copy()
        pygame.draw.polygon( self.selected_image, crosscolor, ( (1.5*m,0),(0,1.5*m),(8.5*m,10*m),(10*m,8.5*m) ) )
        pygame.draw.polygon( self.selected_image, crosscolor, ( (8.5*m,0),(10*m,1.5*m),(1.5*m,10*m),(0,8.5*m) ) )

        self.state = state
        self.image = self.normal_image.copy()
        if self.state:
            self.image = self.selected_image.copy()
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.text = zAdvText(text, (0,0), 10*m, font, textcolor)
        self.text.create_image()
        self.text.center_at(self.rect.center[0]-self.text.width, self.rect.center[1])
        self.activate = activate
        self.deactivate = deactivate

    def collidepoint(self,point):
        return self.rect.collidepoint(point)

    def select(self):
        self.state = True
        self.image = self.selected_image.copy()
        self.activate()

    def unselect(self):
        self.state = False
        self.image = self.normal_image.copy()
        self.deactivate()

    def update(self,events):
        for e in events:
            if self.collidepoint(pygame.mouse.get_pos()) and e.type == MOUSEBUTTONUP and e.button == 1:
                if self.state:
                    self.unselect()
                else:
                    self.select()

    def draw(self,surface):
        self.text.draw(surface)
        surface.blit(self.image, self.pos)



class zButton:

    def __init__(self, function, pos, image, primage=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.normal_image = image
        self.pressed_image = primage
        if not primage:
            self.pressed_image = self.normal_image.copy()
        self.function = function


    def collidepoint(self,point):
        return self.rect.collidepoint(point)


    def update(self,events):
        for e in events:
            if self.collidepoint(pygame.mouse.get_pos()):
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    self.image = self.pressed_image.copy()
                elif e.type == MOUSEBUTTONUP and e.button == 1:
                    self.image = self.normal_image.copy()
                    self.function()
            else:
                self.image = self.normal_image.copy()
                break

    def draw(self,surface):
        surface.blit(self.image, self.rect.topleft)



class zTextButton(zButton):

    def __init__(self, function, pos, text, dim, font=None, color=BLACK, prcolor=BLACK):
        font = pygame.font.Font(font,dim)
        image = font.render(text, 1, color)
        primage = font.render(text, 1, prcolor)
        zButton.__init__(self, function, pos, image, primage)



class zImgButton(zButton):

    def __init__(self, function, pos, image_path, primage_path=None, colorkey=None):
        image = load_image(image_path, colorkey)[0]
        primage = image.copy()
        if primage_path:
            primage = load_image(primage_path, colorkey)[0]
        zButton.__init__(self, function, pos, image, primage)



class zTextImgButton(zButton):

    def __init__(self, function, pos, image_path, text, dim, font=None, color=BLACK, prcolor=BLACK, primage_path=None, colorkey=None):
        font = pygame.font.Font(font,dim)
        textim = font.render(text, 1, color)
        prtextim = font.render(text, 1, prcolor)
        image = load_image(image_path, colorkey)[0]
        primage = image.copy()
        if primage_path:
            primage = load_image(primage_path, colorkey)[0]

        txtrect = textim.get_rect()
        imgrect = image.get_rect()
        txtrect.center = imgrect.center
        image.blit(textim, txtrect.topleft)
        primage.blit(prtextim, txtrect.topleft)

        zButton.__init__(self, function, pos, image, primage)



class zNumManager:

    def __init__(self, text, pos, defaultvalue=0, minvalue=None, maxvalue=None, dim=2, font=None, clr=BLACK, arrowclr=BLACK, prarrowclr=WHITE):
        self.value = defaultvalue
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.dim = 10*dim
        self.font = font
        self.color = clr
        self.text = zAdvText(text, pos, 10*dim, font, clr)
        self.pos = (self.text.pos[0]+self.text.width+self.dim, self.text.pos[1])

        img = pygame.Surface((5*dim,5*dim))
        img.fill(1)
        img.set_colorkey(1)
        normal_arrow = img.copy()
        pygame.draw.polygon(normal_arrow, arrowclr, [(0,5*dim), (5*dim,5*dim), (int(2.5*dim),0),])
        pygame.draw.polygon(img, prarrowclr, [(0,5*dim), (5*dim,5*dim), (int(2.5*dim),0),])
        pressed_arrow = img.copy()
        self.uparrow = zButton(self.valueup, (self.pos[0], self.pos[1]-self.dim*2/3), normal_arrow.copy(), pressed_arrow.copy())
        self.downarrow = zButton(self.valuedown, (self.pos[0], self.pos[1]+self.dim*2/3), pygame.transform.rotate(normal_arrow,180), pygame.transform.rotate(pressed_arrow,180))

    def valueup(self):
        self.value+=1
        if (self.maxvalue != None) and self.value > self.maxvalue:
            self.value = self.maxvalue

    def valuedown(self):
        self.value-=1
        if (self.minvalue != None) and self.value < self.minvalue:
            self.value = self.minvalue

    def update(self,events):
        self.uparrow.update(events)
        self.downarrow.update(events)

    def draw(self,surface):
        self.text.draw(surface)
        self.uparrow.draw(surface)
        self.downarrow.draw(surface)
        zTextDraw(surface, str(self.value), self.dim, self.pos, self.font, self.color)







#Load Images
def load_image(path, colorkey=None):
    try:
        image = pygame.image.load(path)
    except pygame.error:
        raise pygame.error, 'Cannot load ' + path
    if colorkey == 'alpha':
        image = image.convert_alpha()
    elif colorkey == 'icon':
        pass
    elif colorkey != None:
        image = image.convert()
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    else:
        image = image.convert()
    return image, image.get_rect()

#Load Sounds
def load_sound(path):
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    try:
        sound = pygame.mixer.Sound(path)
    except pygame.error:
        raise pygame.error, 'Cannot load ' + path
    return sound

