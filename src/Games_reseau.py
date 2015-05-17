# -*- coding: utf-8 -*-

from zModule import *
from load_datas import *
from load_instances import *
from save_scores import *
from Palet import *
import datas as datas_
import socket
import Queue
import time
import json
from threading import *
import threading
import random
import datetime

clock = pygame.time.Clock()
screen = pygame.display.get_surface()

bg = pygame.image.load(terrain).convert()
palet_rouge_on = pygame.image.load(palet_rouge).convert_alpha()
palet_bleu_on = pygame.image.load(palet_bleu).convert_alpha()
palet_rouge_off = pygame.image.load(palet_rouge_2).convert_alpha()
palet_bleu_off = pygame.image.load(palet_bleu_2).convert_alpha()
ball = pygame.image.load(ball_path).convert_alpha()

palets_count = 10

def events():
    global click

    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            click = True
        elif e.type == pygame.MOUSEBUTTONUP:
            click = False


# on initialise les variables globales
def init_vars():
    global receive_queue
    global send_queue
    global palets
    global buts
    global time_start
    global click
    global i
    global last_received
    global hopper_internal_status
    global hopper_status
    global network_multiplayer
    global activate_IA
    global continue_game
    global in_loop
    global start_chrono
    global chrono_started
    global duration
    global global_names
    global one_time_1

    receive_queue = Queue.Queue()
    send_queue = Queue.Queue()
    palets = []
    buts = [0, 0]
    time_start = 0
    click = False
    i = 0
    last_received = 0
    hopper_internal_status = 0
    hopper_status = False
    network_multiplayer = False
    activate_IA = False
    continue_game = 1
    in_loop = True
    start_chrono = True
    chrono_started = False
    duration = "00:00"
    global_names = []
    one_time_1 = True


# on récupère les donnes stockées dans la Queue
def get_datas(role):
    global i
    global last_received
    global hopper_internal_status
    global hopper_status
    future = None
    try:
        if role == 'server':
            if receive_queue.qsize() == 0:  # pas de data, on freine le flux
                hopper_internal_status = 1
            if receive_queue.qsize() >= 20 or (
                            last_received > 150 and receive_queue.qsize() > 0):  # suffisament de data, on laisse partir
                hopper_internal_status = 0
            if not hopper_internal_status or not hopper_status:
                future = receive_queue.get_nowait()
                i += 1
                last_received = 0
            else:
                last_received += 1
        elif role == 'client':

            if receive_queue.qsize() == 0:  # pas de data, on freine le flux
                hopper_internal_status = 1
            if receive_queue.qsize() >= 20 or (
                            last_received > 150 and receive_queue.qsize() > 0):  # suffisament de data, on laisse partir
                hopper_internal_status = 0

            if not hopper_internal_status or not hopper_status:
                future = receive_queue.get_nowait()
                last_received = 0
            else:
                last_received += 1
    except Queue.Empty:
        pass
    return future


# renvoie notre IP locale
def get_local_address():
    return socket.gethostbyname(socket.gethostname())


# on initialise une connection et on écoute sur le port 1337
def start_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', 1337))
    server.listen(5)
    return server


# on initialise une connection et on se connecte au serveur ip
def connect_to_server(ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 1337))
    return client


# fonction asynchrone qui attend qu'un client se connecte
class wait_for_client(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        client, infos_client = self.server.accept()
        receive_queue.put([client, infos_client])


# fonction asynchrone qui reçoit les données du reseau et les stocke dans une Queue
class receive_datas(Thread):
    def __init__(self, client, role):
        Thread.__init__(self)
        self.stop_thread = threading.Event()
        self.client = client
        self.role = role
        self.count = 0
        self.continue_lopping = 1

    def stop(self):
        self.stop_thread.set()

    def run(self):
        global hopper_status

        while not self.stop_thread.is_set():
            datas = ""
            try:
                datas = self.client.recv(1024)
            except socket.error:
                datas = ""

            if len(datas) > 0:
                temp = ''
                for current_character in datas:
                    if current_character != '~':
                        temp += current_character
                    else:
                        if temp == "HIGH-FLUX-END":
                            hopper_status = False
                            continue
                        elif temp == "HIGH-FLUX-START":
                            hopper_status = True
                            continue

                        if self.role == 'server':
                            receive_queue.put(temp)
                        elif self.role == 'client':
                            receive_queue.put(temp)
                        self.count += 1
                        temp = ''
                #print datas
            time.sleep(0.001)


# fonction asynchrone qui récupère les données de la Queue et les envois sur le reseau
class send_datas(Thread):
    def __init__(self, client, role):
        Thread.__init__(self)
        self.stop_thread = threading.Event()
        self.client = client
        self.role = role
        self.count = 0

    def stop(self):
        self.stop_thread.set()


    def run(self):
        while not self.stop_thread.is_set():
            time.sleep(0.001)
            datas = None
            try:
                if self.role == 'server':
                    datas = send_queue.get_nowait()
                elif self.role == 'client':
                    datas = send_queue.get_nowait()
            except Queue.Empty:
                continue
            if datas is not None:
                #print datas
                self.count += 1
                self.client.send(datas + '~')


# rajoute des données à la Queue
def send(role, dts):
    if role == 'client':
        send_queue.put(dts)
    elif role == 'server':
        send_queue.put(dts)


# trouve une position éloignée de tous les palets
def check_space(palet, palets):
    min = 9999999
    for p in palets:
        dist = distance(palet.x, palet.y, p.x, p.y)
        if dist < min and p != palet:
            min = dist

    if min > palet.radius * 4:
        return True
    else:
        return False


# calcule les coordonnées du point d'intersection entre le cercle de puissance et la droite palet - souris
def maxPower(x, y, mouse_pos, circle_radius):
    d_x = 0
    d_y = 0
    m_x = mouse_pos[0]
    m_y = mouse_pos[1]
    scalaire = 0
    cos = 0
    angle = 0
    dist = distance(x, y, m_x, m_y)

    v = [m_x - x, m_y - y]

    scalaire = 50 * v[1]

    if dist == 0:
        dist = 0.0000001

    cos = scalaire / (50 * dist)

    angle = math.acos(cos)
    d_x = circle_radius * math.sin(angle)
    if m_x < x:
        d_x = -d_x

    scalaire = 50 * v[0]

    cos = scalaire / (50 * dist)

    angle = math.acos(cos)
    d_y = circle_radius * math.sin(angle)
    if m_y < y:
        d_y = -d_y

    return x + d_x, y + d_y


# initialise les palets et la balle
def init_game():
    global palets

    palets = []

    for i in range(palets_count):
        if i < 5:
            team = -1
        else:
            team = 1
        palets.append(Palet((positions[i][0], positions[i][1]), 20.5, 5, team, 'palet', 0.994, i, False, 0, False, False, False))

    palets.append(Palet((ball_start[0], ball_start[1]), 16.5, 1, 0, 'ball', 0.990, -1, False, 0, False, False, False))


class Jeu_reseau():
    # le jeu en lui-même
    def start(self, role):

        selected = None
        a_palet_selected = False
        draw_vector = False
        draw_circle = False
        force_send_message = False
        palet_in_move = 0
        tick = 0
        is_moving = False
        end_game = False
        network_modified = False

        global palets
        global buts
        global time_start
        global time_end
        global click
        global receive_thread
        global send_thread
        global network_multiplayer
        global activate_IA
        global continue_game
        global start_chrono
        global duration
        global global_names
        global chrono_started
        global one_time_1

        global_names = self.names

        init_game() # initialisation des palets et de la balle

        while continue_game:

            dt = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    continue_game = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    click = False

            if network_multiplayer == True: # si la partie est en reseau,
                future = None
                if tick % 2 == 0: # une fois sur deux,
                    future = get_datas(role) # on recupère les informations du reseau
                datas = None
                to_read = False
                if future is not None:
                    try:
                        datas = json.loads(future)
                        size = len(datas['palets'])
                        datas_.but = datas['but']
                        if datas_.but == -1 or datas_.but == 1:
                            network_modified = True
                        else:
                            network_modified = False
                        self.current_team = datas['team']
                        chrono_started = datas['start_chrono']
                        to_read = True
                    except ValueError:
                        pass

            m = '00'
            s = '00'
            if chrono_started:
                if one_time_1:
                    one_time_1 = False
                    time_start = datetime.datetime.now() # on définit l'heure de début de la partie
                duration = datetime.datetime.now() - time_start # et on calcule la durée de la partie
                # et on la converti sous la forme mm:ss
                s = duration.seconds % 60
                m = (duration.seconds - s) % 59
                if s < 10:
                    s = '0' + str(s)
                else:
                    s = str(s)
                if m < 10:
                    m = '0' + str(m)
                else:
                    m = str(m)


            screen.blit(bg, (0, 0))

            if activate_IA == False:
                if self.current_team == -1:
                    zTextDraw(screen, "Tour de " + self.names[0], 40, (50, 40), None, BLACK)
                else:
                    zTextDraw(screen, "Tour de " + self.names[1], 40, (50, 40), None, BLACK)
            else:
                if self.current_team == -1:
                    zTextDraw(screen, "Votre tour", 40, (400, 40), None, BLACK)
                else:
                    zTextDraw(screen, "Tour de l'IA", 40, (400, 40), None, BLACK)

            zTextDraw(screen, self.names[0] + " " + str(buts[0]) + "  -  " + str(buts[1]) + " " + self.names[1], 50, (337, 60), None, BLACK) # on affiche le nom des joueurs et leurs buts
            zTextDraw(screen, m + ':' + s, 40, (475, 120), None, BLACK)

            mouse_pos = pygame.mouse.get_pos()

            if network_multiplayer == False or self.team == self.current_team:

                for palet in palets:

                    palet.move(palets) # on déplace le palet (ou la balle) et on effectue les calculs de collision, etc

                    if activate_IA == False or self.team != self.current_team:

                        # si on clique sur le palet et qu'il n'est pas sélectionner, on le sélectionne
                        if palet.selected == True and palet.clicked == False and click == True:
                            palet.click_action_count += 1
                            palet.clicked = True

                        # si il est sélectionné mais qu'on ne clique pas dessus, on le désélectionne
                        if palet.selected == True and palet.clicked == True and click == False:
                            palet.click_action_count += 1
                            palet.clicked = False

                        # si le palet n'est pas sélectionné, on ne fait rien
                        if palet.selected == False:
                            palet.click_action_count = 0

                        # si on utilise Ctrl
                        if palet.using_distant_mode == True and palet.click_action_count == 3:
                            temp_pos = pygame.mouse.get_pos()
                            temp_x = temp_pos[0]
                            temp_y = temp_pos[1]
                            palet.click_action_count -= 2  # on remet au niveau du mode normal
                            palet.waiting_distant_mode = False

                        # si on clique sur le palet et qu'aucun autre n'est sélecionné
                        if click == True and a_palet_selected == False and distance(palet.x, palet.y, mouse_pos[0], mouse_pos[1]) < palet.radius and palet.team == self.current_team and is_moving == False:
                            # si on appuie sur Ctrl
                            if pygame.key.get_mods() == 4160:
                                palet.using_distant_mode = True
                                palet.waiting_distant_mode = True
                                palet.selected = True
                                a_palet_selected = True
                            else:
                                palet.using_distant_mode = False
                                palet.waiting_distant_mode = False
                                palet.selected = True
                                a_palet_selected = True
                                temp_x = palet.x
                                temp_y = palet.y

                        # si le palet est sélectionné et qu'on appuie pas sur Ctrl
                        if palet.selected == True and palet.waiting_distant_mode == False:
                            if palet.click_action_count == 1:
                                palet.circle_radius = int(distance(temp_x, temp_y, mouse_pos[0], mouse_pos[1])) # on calcule le rayon du cercle de puissance
                                if palet.circle_radius > 5 * palet.radius: # si il est suppérieur à 5 * celui du palet,
                                    palet.circle_radius = 5 * palet.radius # on le limite en taille
                                x, y = maxPower(temp_x, temp_y, mouse_pos, palet.circle_radius) # on calcule les coordonnées du point d'intersection
                            # on lance le palet
                            elif palet.click_action_count == 2:
                                # si le rayon du cercle de puissance est supérieur à celui du palet
                                if palet.circle_radius > palet.radius:
                                    dx = temp_x - x
                                    dy = temp_y - y
                                    palet.angle = 0.5 * math.pi + math.atan2(dy, dx)
                                    palet.speed = math.hypot(dx, dy) / 10
                                    is_moving = True
                                    palet.moving = True
                                    if network_multiplayer: # si c'est une partie reseau,
                                        send(role, "HIGH-FLUX-START") # on informe l'autre joueur que des données vont êtres envoyées
                                    if start_chrono == True:
                                        start_chrono = False
                                        chrono_started = True

                                # on réinitialise les variables de selection du palet
                                palet.selected = False
                                palet.click_action_count = 0
                                palet.using_distant_mode = False
                                a_palet_selected = False

                        if palet.selected == False or palet.waiting_distant_mode == True:
                            palet.circle_radius = 0

                        if palet.circle_radius > palet.radius:
                            draw_vector = True
                            draw_circle = True
                        else:
                            draw_vector = False
                            draw_circle = False

                        if draw_vector:
                            palet.drawVector(screen, temp_x, temp_y, x, y) # on dessine le vecteur direction
                        if draw_circle:
                            palet.drawCircle(screen, temp_x, temp_y) # on dessine le cercle de puissance

                    else:
                        if self.current_team == self.team and is_moving == False and palet.team == self.team and palet.type == 'palet':
                            # IA ICI

                            if random.randint(0, 50) == 25:
                                palet.angle = random.randint(0,int(2*math.pi*100)) / 100
                                palet.speed = random.randint(1,5)
                                is_moving = True
                                palet.moving = True

                    # si le palet s'arrête dans un but, on le décale de 50 px vers l'intérieur du terrain
                    # et on trouve la position y la plus éloignée des autres palets
                    if is_moving == False and palet.speed == 0 and palet.type == 'palet':

                        if palet.x - palet.radius < terrain_size[0][0]:
                            palet.x = terrain_size[0][0] + palet.radius + 50
                            palet.moving = True
                            i = 0
                            while not check_space(palet, palets):
                                if i < len(modif_pos):
                                    palet.y += modif_pos[i]
                                    i += 1
                                else:
                                    break

                        elif palet.x + palet.radius > terrain_size[0][1]:
                            palet.x = terrain_size[0][1] - palet.radius - 50
                            palet.moving = True
                            i = 0
                            while not check_space(palet, palets):
                                if i < len(modif_pos):
                                    palet.y += modif_pos[i]
                                    i += 1
                                else:
                                    break

                    # on compte le nombre de palets en mouvement
                    if palet.moving:
                        palet_in_move += 1

                # on vérifie si le palet vient juste de s'arrêter
                just_stopped_moving = False
                if is_moving and palet_in_move == 0:
                    self.current_team *= -1
                    is_moving = False
                    just_stopped_moving = True

                # on compte les buts
                if datas_.but == -1:
                    buts[0] += 1
                    self.current_team = 1
                    if not network_modified:
                        just_stopped_moving = True
                elif datas_.but == 1:
                    buts[1] += 1
                    self.current_team = -1
                    if not network_modified:
                        just_stopped_moving = True

                if network_multiplayer == True: # si c'est une partie reseau,
                    if palet_in_move > 0 or just_stopped_moving: # si des palets bougent ou si le palet vient de s'arrêter,

                        if (tick % 2 == 0 and palet_in_move > 0) or just_stopped_moving: # une fois sur deux si des palets bougent ou dans tous les cas s'il vient de s'arrêter
                            to_send = {}
                            to_send['team'] = self.current_team
                            to_send['but'] = datas_.but
                            to_send['start_chrono'] = chrono_started
                            to_send['palets'] = {}
                            z = 0
                            for p in palets:
                                if p.moving or just_stopped_moving:
                                    to_send['palets'][str(z)] = {}
                                    to_send['palets'][str(z)]['id'] = p.id
                                    to_send['palets'][str(z)]['x'] = p.x
                                    to_send['palets'][str(z)]['y'] = p.y
                                    z += 1
                            send(role, json.dumps(to_send)) # on envoie les données à l'autre joueur

                        if just_stopped_moving:
                            send(role, "HIGH-FLUX-END") # on prévient l'autre joueur que toutes les données ont été envoyées

                if datas_.but == -1 or datas_.but == 1:
                    datas_.but = 0
                    self.start(role) # si un but est marqué, on réinitialise le terrain

                palet_in_move = 0
            # si c'est une partie reseau et que ce n'est pas notre tour, on affiche les données recues
            elif network_multiplayer == True and self.current_team != self.team:
                if to_read:
                    for i in range(0, size):
                        id_ = datas['palets'][str(i)]['id']
                        if id_ == -1:
                            id_ = palets_count
                        palets[id_].x = datas['palets'][str(i)]['x']
                        palets[id_].y = datas['palets'][str(i)]['y']

            all_texture_off = False

            if (network_multiplayer == True or activate_IA == True) and self.team != self.current_team:
                all_texture_off = True

            # on choisi qulle image afficher pour les palets
            for palet in palets:
                if palet.type == 'palet':
                    if palet.team == -1:
                        if is_moving == False and all_texture_off == False and palet.team == self.current_team:
                            palet.draw(screen, palet_rouge_on) # en jeu
                        else:
                            palet.draw(screen, palet_rouge_off) # en attente
                    else:
                        if is_moving == False and all_texture_off == False and palet.team == self.current_team:
                            palet.draw(screen, palet_bleu_on)
                        else:
                            palet.draw(screen, palet_bleu_off)
                else:
                    palet.draw(screen, ball) # et on dessine la balle

            # si un joueur a marqué 2 buts, on termine la partie
            if buts[0] >= 2 or buts[1] >= 2:
                continue_game = 0
                if self.names != ["Rouges", "Bleus"]:
                    if network_multiplayer:
                        if self.name == self.names[1]:
                            self.names.reverse()
                            buts.reverse()
                    # on sauvegarde les scores
                    if network_multiplayer:
                        save_scores(self.names[0], self.names[1], buts[0] - buts[1], buts[0], buts[1], time.time(), duration, "reseau")
                    else:
                        save_scores(self.names[0], self.names[1], buts[0] - buts[1], buts[0], buts[1], time.time(), duration, "local")
                show_end_screen(self.names) # on affiche l'écran de fin
                buts = [0, 0]

            pygame.display.flip() #actualisation de l'affichage
            tick += 1

    # initialisation du serveur
    def init_server(self, name, IA):

        init_vars() # on initialise les variables

        global receive_thread
        global send_thread
        global network_multiplayer
        global activate_IA

        network_multiplayer = True
        activate_IA = IA

        self.team = -1
        self.name = name
        self.names = []
        self.names.append(name)
        self.local_socket = start_socket()
        accept_thread = wait_for_client(self.local_socket)
        accept_thread.start()

        local_ip = get_local_address() # on récupère notre IP locale

        screen.fill((255, 255, 255))

        zTextDraw(screen, "En attente d'un joueur. " + local_ip, 50, (50, 50), None, BLACK)
        pygame.display.flip()

        # on attend les inforamations du client
        future = None
        while future is None:
            time.sleep(0.001)
            events()
            future = get_datas('server')
        self.distant_socket, self.distant_socket_infos = future
        accept_thread._Thread__stop()

        self.distant_socket.setblocking(0)

        receive_thread = receive_datas(self.distant_socket, 'server')
        receive_thread.start()
        send_thread = send_datas(self.distant_socket, 'server')
        send_thread.start()

        # on attend le nom du client
        future = None
        while future is None:
            time.sleep(0.001)
            events()
            future = get_datas('server')
        self.names.append(future)

        send_queue.put(self.names[0] + ',' + self.names[1]) # on envoie les noms au client

        screen.fill((255, 255, 255))
        zTextDraw(screen, "Vous jouez avec " + self.names[1], 50, (50, 50), None, BLACK)

        pygame.display.flip()

        self.current_team = random.choice([-1, 1]) # on choisi au hazard le joueur qui commence
        send_queue.put(json.dumps(self.current_team)) # et on l'envoie à l'autre joueur

        self.start('server') # on lance la partie

        self.local_socket.close() # on ferme la connection avec le client

    # initialisation du client
    def init_client(self, server_ip, name, IA):

        init_vars() # on initialise les variables

        global receive_thread
        global send_thread
        global network_multiplayer
        global activate_IA

        network_multiplayer = True
        activate_IA = IA

        self.team = 1
        self.name = name
        self.distant_socket = connect_to_server(server_ip)

        self.distant_socket.setblocking(0)

        receive_thread = receive_datas(self.distant_socket, 'client')
        receive_thread.start()
        send_thread = send_datas(self.distant_socket, 'client')
        send_thread.start()

        send_queue.put(name) # on envoie ,otre nom au serveur

        # on attend les noms
        future = None
        while future is None:
            time.sleep(0.001)
            events()
            future = get_datas('client')
        self.names = future.split(',')

        # one attend le joueur qui commence
        future = None
        while future is None:
            time.sleep(0.001)
            events()
            future = get_datas('client')
        self.current_team = json.loads(future)

        screen.fill((255, 255, 255))
        zTextDraw(screen, "Vous jouez avec " + self.names[0], 50, (50, 50), None, BLACK)

        pygame.display.flip()

        self.start('client') # on lance la partie

        self.distant_socket.close() # on ferme la connection avec le serveur

    # initialisation de la partie locale
    def init_local(self, names, use_IA):

        init_vars() # on initialise les variables

        global network_multiplayer
        global activate_IA
        network_multiplayer = False
        if use_IA: # on utilise l'IA,
            activate_IA = True
            self.names = {}
            self.names[0] = "You"
            self.names[1] = "IA_DE_LA_MORT"
            self.team = -1
            self.current_team = random.choice([-1, 1])
            self.start('')
        else: # ou non
            self.names = names
            self.team = 1
            self.current_team = random.choice([-1, 1])
            self.start('')

    # on arrête les fonction asychrones
    def stop_game(self):
        global receive_thread
        global send_thread
        receive_thread.stop()
        send_thread.stop()


def quit():
    global in_loop
    in_loop = False


def replay():
    global continue_game
    continue_game = 1
    Jeu_reseau().init_local(global_names, activate_IA)


# écran de fin de partie
def show_end_screen(names):
    global in_loop
    in_loop = True
    winner = None
    equality = False

    if names != ["Rouges", "Bleus"]:
        solo = False
    else:
        solo = True

    quit_btn = zTextButton(quit, (50, 150), "Quitter", 50, None, GREEN, RED)
    replay_btn = zTextButton(replay, (350, 150), "Rejouer", 50, None, GREEN, RED)

    while in_loop:

        events = pygame.event.get()

        global buts

        # on détermine le gagnant
        if buts[0] > buts[1]:
            if solo == False:
                winner = names[0]
            else:
                winner = "Rouges"
        elif buts[0] < buts[1]:
            if solo == False:
                winner = names[1]
            else:
                winner = "Bleus"
        else:
            equality = True

        # on converti la durée en mm:ss
        s = duration.seconds % 60
        m = (duration.seconds - s) % 59
        if s < 10:
            s = '0' + str(s)
        else:
            s = str(s)
        if m < 10:
            m = '0' + str(m)
        else:
            m = str(m)

        for e in events:
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                in_loop = False

        screen.fill((255, 255, 255))

        if equality == False:
            if solo == False:
                zTextDraw(screen, "Victoire de " + winner, 50, (50, 50), None, BLACK)
            else:
                zTextDraw(screen, "Victoire des " + winner, 50, (50, 50), None, BLACK)
        else:
            zTextDraw(screen, "Egalitée", 50, (50, 50), None, BLACK)

        zTextDraw(screen, "Duree de la partie " + m + ':' + s, 50, (500, 400), None, BLACK)

        quit_btn.update(events)
        replay_btn.update(events)
        quit_btn.draw(screen)
        replay_btn.draw(screen)

        pygame.display.flip()