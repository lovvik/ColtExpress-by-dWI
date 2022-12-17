import pygame as pg
from random import randrange, choice
import Game
import pygame_gui as pgg

#voir var à la fin du fichier
pg.font.init()
img_x = [55, 128, 206, 284,362,440,518]
img_x_loco = [30, 108, 186, 264, 342, 420, 498]

def creation () :
    for wagon in Game.Game.wagons :
        if (wagon.type == 'Locomotive') : 
            wagon.sprite = pg.image.load(LOCO)
            wagon.sprite = rescale(wagon.sprite, 1.2)
        else :
            src = choice(WAGONS)
            wagon.sprite = pg.image.load(src)
            wagon.sprite = rescale(wagon.sprite, 1.5)

        for butin in wagon.butins :
            if (butin.value==100) :
                butin.sprite = pg.image.load(BOURSE100)
            elif (butin.value==200) : 
                butin.sprite = pg.image.load(BOURSE200)
            elif(butin.value==500) : 
                butin.sprite = pg.image.load(BIJOUX)
            elif (butin.value==1000) : 
                butin.sprite = pg.image.load(MAGOT)
            butin.sprite = rescale(butin.sprite, 0.7)
    
    skin_marsh = pg.image.load(MARSHALL)
    Game.Game.marsh.sprite = skin_marsh

    dispos = PERSOS_DISPO.copy()
    tt_dispos = HEADS.copy()
    for player in Game.Game.players :
        index = randrange(len(dispos))
        player.sprite = pg.image.load(dispos[index])
        player.icon = pg.image.load(tt_dispos[index])
        dispos.pop(index)
        tt_dispos.pop(index)
        player.sprite = rescale(player.sprite, 0.9)
        #print(f"{player.name} : {camino}")

def rescale (img, scale) :
    """il faut reassigner l'image remise a echelle :
        img = rescale(img, blabla)"""
    h = img.get_height()
    w = img.get_width()
    
    return pg.transform.scale(img, size=(w*scale, h*scale))


def draw_wagon (screen, wagon) :
    """screen : ecran principal du jeu"""
    w = wagon.sprite.get_width()
    h = wagon.sprite.get_height()
    x = (1280-w)/2
    y = 720-h
    
    nbi = nb100 = nb200 = nmag = 0
    
    wagon.sprite.blit(wagon.sprite, dest=(0,0))
    screen.blit(wagon.sprite, dest=(x,y))
    screen.blit(aff, dest=((1280-aff.get_width()),(720-aff.get_height())))

    i=0
    for individu in wagon.interior :
        if wagon.Id == 0 : n=img_x_loco[i]
        else : n=img_x[i]

        my_h = individu.sprite.get_height()
        
        screen.blit(individu.sprite, dest=(x+n, y+(h-my_h-50)))
        i+=1

    i=0
    for individu in wagon.exterior :
        if wagon.Id == 0 : n=img_x_loco[i]
        else : n=img_x[i]
        my_h = individu.sprite.get_height()
        screen.blit(individu.sprite, dest=((x+40) + n%(w-(150+40)), 720-(h+my_h-20)))
        i+=1

    for truc in wagon.butins :
        if (truc.type=='magot') : nmag +=1
        elif (truc.type=='bijoux') : nbi+=1
        else :
            if (truc.value==100) : nb100+=1
            else : nb200+=1

    #map des butins
    cooler =(222,181,117)
    aff.blit(b100, dest=(10,10))
    aff.blit(TpW.render(f"x {nb100}", True, (0,0,0), cooler), dest=(b100.get_width()+10,30))
    aff.blit(b200, dest=(190,10))
    aff.blit(TpW.render(f"{nb200} x", True, (0,0,0), cooler), dest=(aff.get_width()-b200.get_width()-30,30))
    if (wagon.Id==0) : screen.blit(TpW.render(f"Locomotive",True, (0,0,0), cooler), dest=(1280-170,720-110))
    else : screen.blit(TpW.render(f"Wagon {wagon.Id}",True, (0,0,0), cooler), dest=(1280-160,720-100))
    aff.blit(bij, dest=(10,100))
    aff.blit(TpW.render(f"x {nbi}", True, (0,0,0), cooler), dest=(bij.get_width()+10,130))
    aff.blit(mag, dest=(190,100))
    aff.blit(TpW.render(f"{nmag} x", True, (0,0,0), cooler), dest=(aff.get_width()-mag.get_width()-30,130))



def draw_stats (screen) :
    y = 30
    for player in Game.Game.players :
        screen.blit (player.icon, dest=(1200,y))
        name = Tyb18.render(f"{player.name}", True, (203,179,136),(0,0,0))
        screen.blit (name, dest=(1190-name.get_width(), y))
        stats = TpW16.render(f"({player.pos}) | {player.munitions} balles | {player.solde()}$", True, (0,0,0), None)
        screen.blit(stats, dest=(1190-stats.get_width(),y+30))
        y+=70


def draw_transition(screen) :
    token=0
    rayon=0
    #screen.fill((255,255,255))
    while(rayon<=800) :
        pg.draw.circle(screen, (token,token,token), (1280/2, 720/2), rayon)
        if (pg.time.get_ticks()%50)==0: rayon+=30
        pg.display.update()
    #print(rayon,'\n')

"""def draw_transition_reverse(screen) :
    token=0
    rayon=800
    #screen.fill((255,255,255))
    while(rayon>0) :
        pg.draw.circle(screen, (token,token,token), (1280/2, 720/2), rayon, 0)
        if (pg.time.get_ticks()%5)==0: rayon-=1
        pg.display.update()
    #print(rayon,'\n')"""


def Welcome(screen) : 
    run = True
    mymanager = pgg.UIManager((1280, 720), "../mytheme.json")
    title = pg.image.load(LOGO)
    title = rescale(title, 0.5)
    Wlcm_bg = pg.image.load(WLCM)
    msg_txt= "Entrez les noms des joueurs séparés par des virgules (6 max)."
    msg = Avnit.render(msg_txt, False, (255,255,255), None)
    en_box = pgg.elements.UITextEntryLine((800, 300, 300, 35), mymanager)
    en_box.enable()

    while(run) :
        time_delta = pg.time.Clock().tick(60)/1000.0

        screen.blit(title, dest=(100, 10))
        screen.blit(Wlcm_bg, dest=(100 , ((720-Wlcm_bg.get_height())/2)+30))
        screen.blit(msg, dest=(750, 250))




        for Event in pg.event.get() :

            mymanager.process_events(Event)
            if Event.type == pgg.UI_TEXT_ENTRY_FINISHED:
                return traitement_text(en_box.get_text())

            if Event.type == pg.QUIT : quit()
            


        mymanager.update(time_delta)
        mymanager.draw_ui(screen)     
        pg.display.update()



def traitement_text (chaine) :
    liste =  chaine.split(',')
    if len(liste) > 6 :
        liste = liste[0:6]

    for el in liste :
        if el.isspace() or el=='' : liste.remove(el)

    #print(liste)
    return liste

def draw_r_turns(screen) :
    if (Game.Game.SIG1000==False) : return None
    text = Tyb60.render(f"{Game.Game.R_LAPS}", True, (0,0,0))
    screen.blit(text, (1200,470))


def TheEnd(screen) :
    run = True
    Game.mixer.Channel(0).play(Game.vic_s)
    screen.fill((0,0,0))
    thymanager = pgg.UIManager((1280, 720), "../mytheme.json")
    title = pg.image.load(LOGO)
    title = rescale(title, 0.5)
    Wlcm_bg = pg.image.load(WLCM)
    """msg_txt= "Fin."
    msg = Avnit.render(msg_txt, False, (255,255,255), None)"""
    geld = classement(Game.Game.players)


    while(run) :
        time_delta = pg.time.Clock().tick(60)/1000.0

        screen.blit(title, dest=(100, 10))
        screen.blit(Wlcm_bg, dest=(100 , ((720-Wlcm_bg.get_height())/2)+30))
        draw_stats_end(screen, geld)




        for Event in pg.event.get() :

            thymanager.process_events(Event)

            if Event.type == pg.QUIT : quit()
            


        thymanager.update(time_delta)
        thymanager.draw_ui(screen)     
        pg.display.update()


def classement(liste) :
        geld=[]
        for joueur in liste :
            geld.append([joueur, joueur.solde()])

        geld = sorted(geld, key=lambda x:x[1], reverse=True)
        #print(geld)
        return geld




def draw_stats_end (screen,liste) :
    y = 30
    couleur = (255,255,255)
    for couple in liste :
        if liste.index(couple) == 0 : couleur = (133, 33, 166)
        else : couleur = (255,255,255)
        player = couple[0]
        screen.blit (player.icon, dest=(1200,y))
        name = Tyb18.render(f"{player.name}", True, (203,179,136),(0,0,0))
        screen.blit (name, dest=(1190-name.get_width(), y))
        stats = Avnit.render(f"{player.solde()} $", True, couleur, None)
        screen.blit(stats, dest=(1190-stats.get_width(),y+30))
        y+=70




#*****************************FIXE*****************************#

MARSHALL = "../images/persos/Marshall.png"
PERSOS_DISPO = ["../images/persos/belle.png","../images/persos/cheyenne.png","../images/persos/django.png","../images/persos/doc.png","../images/persos/ghost.png","../images/persos/tuco.png"]
HEADS = ["../images/persos/belle_head.png","../images/persos/cheyenne_head.png","../images/persos/django_head.png","../images/persos/doc_head.png","../images/persos/ghost_head.png","../images/persos/tuco_head.png"]
SCALE_PERSOS = 0.9

LOCO = "../images/scene/new.png"
WAGONS = ["../images/scene/bar.png", "../images/scene/firstclass.png", "../images/scene/secondclass.png"]
SCALE_LOCO = 1.2
SCALE_WAGONS = 1.5

BIJOUX = "../images/utils/bijoux.png"
BOURSE100 = "../images/utils/bourse100.png"
BOURSE200 = "../images/utils/bourse200.png"
MAGOT = "../images/utils/magot.png"
bij = pg.image.load(BIJOUX)
b100 = pg.image.load(BOURSE100)
b200 = pg.image.load(BOURSE200)
mag = pg.image.load(MAGOT)
bij = rescale(bij, 0.6)
b100 = rescale(b100, 0.6)
b200 = rescale(b200, 0.6)
mag = rescale(mag, 0.6)




AFFICHE = "../images/utils/affiche.png"
aff = pg.image.load(AFFICHE)


TpW = pg.font.Font("../polices/TypeWriterjspquoi.otf",22)
Tyb18 = pg.font.Font("../polices/Toybox.otf",18)
Tyb60 = pg.font.Font("../polices/Toybox.otf", 60)
TpW16 = pg.font.Font("../polices/Old.ttf",16)
Avnit = pg.font.Font("../polices/AvenirNextCyr-Thin.ttf", 16)


WLCM = "../images/scene/welcome.png"
LOGO = "../images/scene/logo.png"



#*****************************FIXE*****************************#



    

