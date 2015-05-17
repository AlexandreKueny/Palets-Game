# -*- coding: utf-8 -*-

from load_datas import *
from zModule import *
import math
import datas
import time

def addVectors((angle1, length1), (angle2, length2)):
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return angle, length


# calcule la distance entre deux points
def distance(x1, y1, x2, y2):
    return math.sqrt( pow(x2 - x1, 2) + pow(y2 - y1, 2) )


class Palet:
    
    def __init__(self, (x, y), radius, mass, team, type, drag, id, clicked, click_action_count, selected, using_distant_mode, waiting_distant_mode):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.speed = 0
        self.angle = 0
        self.drag = drag
        self.circle_radius = 0
        self.moving = False
        self.team = team
        self.type = type
        self.id = id
        self.clicked = clicked
        self.click_action_count = click_action_count
        self.selected = selected
        self.using_distant_mode = using_distant_mode
        self.waiting_distant_mode = waiting_distant_mode

    # dessine la palet
    def draw(self, screen, image):
        if self.type == 'palet':
            screen.blit(image, (self.x - 20.5, self.y - 20.5))
        else:
            screen.blit(image, (self.x - 16.5, self.y - 16.5))

    # dessine le cercle de puissance
    def drawCircle(self, screen, x, y):
        pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), int(self.circle_radius), 1)

    # dessine le vecteur direction
    def drawVector(self, screen, x2, y2, x, y):
        pygame.draw.line(screen, (0, 0, 0), (x2, y2), (x, y), 1)

    # calcule les mouvements du palet
    def move(self, palets):
        # déplace le palet en fonction de sa vitesse
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag # et on réduit ca vitesse à chaque tour

        # si la vitesse est inférieure à 0.5, on l'arrête
        if math.fabs(self.speed) < 0.5:
            self.speed = 0
            self.moving = False

        else:
            self.moving = True
        
        if self.x > terrain_size[0][1] - self.radius: # si le palet dépasse le bord droit du terrain
            if self.y < buts_size[1][1][0] or self.y > buts_size[1][1][1]: # si il n'est pas dans les buts
                self.x = terrain_size[0][1] - self.radius # on le place au bord du terrain
                self.angle = - self.angle # on inverse sa direction
                self.speed *= 0.95 # et on le ralenti
            elif self.x + self.radius > buts_size[1][0][0]: # si il est dans les buts
                if self.x > datas.screen_size[0] - self.radius: # si il est au bord droit de l'écran
                    if self.type == 'palet': # si c'est un palet, on le fait rebondir
                        self.x = datas.screen_size[0] - self.radius
                        self.angle = - self.angle
                        self.speed *= 0.95
                    else: # si c'est la balle
                        self.speed = 0 # on l'arrête
                        datas.but = -1 # on compte un but

        # même chose du côté gauche
        elif self.x < terrain_size[0][0] + self.radius:
            if self.y < buts_size[0][1][0] or self.y > buts_size[0][1][1]: 
                self.x = terrain_size[0][0] + self.radius
                self.angle = - self.angle
                self.speed *= 0.95
            elif self.x < self.radius:
                if self.type == 'palet':
                    self.x = self.radius
                    self.angle = - self.angle
                    self.speed *= 0.95
                else:
                    self.speed = 0
                    datas.but = 1

        # même chose avec le bord bas
        if self.y > terrain_size[1][1] - self.radius:
            self.y = terrain_size[1][1] - self.radius
            self.angle = math.pi - self.angle
            self.speed *= 0.95

        # même chose avec le bord haut
        elif self.y < terrain_size[1][0] + self.radius:
            self.y = terrain_size[1][0] + self.radius
            self.angle = math.pi - self.angle
            self.speed *= 0.95

        # même chose pour les bords intérieurs des buts
        if self.y < buts_size[0][1][0] + self.radius and (self.x < terrain_size[0][0] or self.x > terrain_size[0][1]):
            self.y = buts_size[0][1][0] + self.radius
            self.angle = math.pi - self.angle
            self.speed *= 0.95
        elif self.y > buts_size[0][1][1] - self.radius and (self.x < terrain_size[0][0] or self.x > terrain_size[0][1]):
            self.y = buts_size[0][1][1] - self.radius
            self.angle = math.pi - self.angle
            self.speed *= 0.95
        
        for palet in palets:
            
            if self != palet:
        
                dx = self.x - palet.x
                dy = self.y - palet.y

                dist = math.hypot(dx, dy) #on calcule la distance entre les 2 palets
                if dist < self.radius + palet.radius: # si les palets se superposent
                    angle = math.atan2(dy, dx) + 0.5 * math.pi
                    total_mass = self.mass + palet.mass
                    
                    #palet.speed = 1 * self.speed
                    if self.type == 'palet' and palet.type == 'palet':
                        # on alourdi le pelet qui se déplace
                        if self.moving == True:
                            self.mass += palet.mass / 1.5
                        elif palet.moving == True:
                            palet.mass += self.mass /1.5

                    # on calcule les nouvelles valeurs de l'angle de déplacement et de la vitesse des 2 palets
                    (self.angle, self.speed) = addVectors((self.angle, self.speed*(self.mass-palet.mass)/total_mass), (angle, 2*palet.speed*palet.mass/total_mass))
                    (palet.angle, palet.speed) = addVectors((palet.angle, palet.speed*(palet.mass-self.mass)/total_mass), (angle+math.pi, 2*self.speed*self.mass/total_mass))

                    #if distance(self.x, self.y, palet.x, palet.y) > self.radius + palet.radius + 5:
                    # et on les freine
                    self.speed *= 0.90
                    palet.speed *= 0.90

                    overlap = 0.5*(self.radius + palet.radius - dist+1) # on calcule la longueur de la superposition
                    # et on les déplace pour qu'ils ne se superposent plus
                    self.x += math.sin(angle)*overlap
                    self.y -= math.cos(angle)*overlap
                    palet.x -= math.sin(angle)*overlap
                    palet.y += math.cos(angle)*overlap