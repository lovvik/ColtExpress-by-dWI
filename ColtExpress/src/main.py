#!/usr/bin/python3
from Game import *
from Player import *
from Butin import *
import pygame as pg
import apperance
import pygame_gui as pgg
def act(liste) :
    Game.Game.marsh.bouger()
    Game.Game.marsh.goberserk()    
    global i
    for j in range(3) :
        for player in liste :
                if player.plan[j] == 'wagon de gauche' : 
                    player.bouger('r')
                elif player.plan[j] == 'wagon de droite' : 
                    player.bouger('l')
                elif player.plan[j] == 'changer de niveau' : player.changer_niveau()
                elif player.plan[j] == 'tirer' : 
                    player.shoot()
                elif player.plan[j] == 'ramasser' : 
                    player.braquer()
                else : pass

pg.init()
pg.font.init()
pg.mixer.init(channels=4)
icon = pg.image.load("../images/utils/icon.png")
running = True
t_done = False
Action_list = ['rien', 'wagon de droite', 'wagon de gauche', 'changer de niveau', 'tirer', 'ramasser']
ecran = pg.display.set_mode(size=(1280,720))
pg.display.set_icon(icon)
pg.display.set_caption("Colt EXPRESS", "icon")

spieler = apperance.Welcome(ecran)
Game.mixer.Channel(7).play(bell_s)
apperance.draw_transition(ecran)
bg = pg.image.load("../images/scene/gauche.png")
clock = pg.time.Clock()

mon_jeu = Game.Game(spieler)
manager = Game.Game.manager


choixun = pgg.elements.UIDropDownMenu(options_list = Action_list,relative_rect=(10, 30, 170, 30), starting_option = Action_list[0],manager=manager, expand_on_option_click = False, object_id='choixun')
choixdeux = pgg.elements.UIDropDownMenu(options_list = Action_list,relative_rect=(10, 70, 170, 30), starting_option = Action_list[0],manager=manager, expand_on_option_click = False, object_id='choixdeux')
choixtrois = pgg.elements.UIDropDownMenu(options_list = Action_list,relative_rect=(10, 110, 170, 30), starting_option = Action_list[0],manager=manager, expand_on_option_click = False, object_id='choixtrois')
Action = pgg.elements.UIButton(relative_rect=(10, 160),text='ET...Action!', manager=manager, object_id='id_action')
log = Game.Game.log
temp = pg.Rect(1280-340,30,330,190)


Plan = ['','','']

#variables de tour
CPLAYER = None
SIGNAL = 'None'
Cindex = 0
NEXT = False
MUSIC = True




i=0
Game.mixer.Channel(0).play(Game.train_s, -1)
while running :

    time_delta = clock.tick(60)/1000.0

    ecran.blit(bg, dest=(0,0))
    apperance.draw_wagon(ecran,mon_jeu.wagons[i])
    apperance.draw_stats(ecran)   
    apperance.draw_r_turns(ecran)
    CPLAYER = mon_jeu.players[Cindex]
    Action.set_text(f"{CPLAYER.name} : Valider")

    if (Game.Game.R_LAPS==0) :
        apperance.draw_transition(ecran) 
        apperance.TheEnd(ecran)
    
    

    for Event in pg.event.get():

        if Event.type == pg.QUIT :
            running = False
        if Event.type == pg.KEYDOWN :
            if Event.key == pg.K_RIGHT :
                if (i-1>=0) : 
                    i-=1
                    Game.mixer.Channel(2).play(Game.trans_s)
            if Event.key == pg.K_LEFT :
                if (i<mon_jeu.NB_WAGONS) : 
                    i+=1
                    Game.mixer.Channel(2).play(Game.trans_s)
            if Event.key == pg.K_p :
                if MUSIC == True : 
                    Game.mixer.pause()
                    MUSIC = False
                else :
                    Game.mixer.unpause()
                    MUSIC = True 
        if Event.type == pgg.UI_DROP_DOWN_MENU_CHANGED :
            if Event.ui_element == choixun : Plan[0] = Event.text
            if Event.ui_element == choixdeux : Plan[1] = Event.text
            if Event.ui_element == choixtrois : Plan[2] = Event.text
        if Event.type == pgg.UI_BUTTON_PRESSED :
            if Event.ui_element == Action :
                CPLAYER.plan = Plan.copy()
                choixun.disable()
                choixdeux.disable()
                choixtrois.disable()
                Action.disable()
                NEXT = True

        manager.process_events(Event)



    if (NEXT==True) :
        #print(f"{mon_jeu.players[Cindex].name} : {mon_jeu.players[Cindex].plan}")
        Cindex+=1
        if (Cindex>=mon_jeu.NB_JOUEURS) :
            #print("Action Pour Tous!!!")
            act(mon_jeu.players)
            if (Game.Game.SIG1000==True) : Game.Game.R_LAPS-=1
            Cindex=0
        choixun.enable()
        choixdeux.enable()
        choixtrois.enable()
        Action.enable()
        NEXT = False
        #print(f"{mon_jeu.players[Cindex].name} fait son choix")

                
            
        

    manager.update(time_delta)
    manager.draw_ui(ecran)     
    pg.display.update()


"""for player in mon_jeu.players :
    print(f"{player.name} : {player.plan}")"""