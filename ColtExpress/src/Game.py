import Player
import Butin
from random import randrange, choice
import apperance
import pygame_gui as pgg
from pygame import init, font, mixer


class Game :

    wagons = []
    players = []
    marsh = None
    SIG1000 = False
    R_LAPS = 4


    init()
    font.init()
    manager = pgg.UIManager((1280, 720), "../mytheme.json")
    log  = pgg.elements.UITextBox(html_text='<b>===Log===</b>\n',relative_rect=(0,720-470, 270, 470), manager=manager)


    def __init__(self, noms:list) :

        self.NB_JOUEURS = len(noms)
        self.NB_MAX_JOUEURS = 6
        self.NB_WAGONS = len(noms)
        self.NB_ACTIONS = 0
        self.NB_TOURS = 0
        self.NB_BALLES = 6
        self.marshall = Marshall()
        

        #phase de Creation
        Game.wagons.append(Wagon(self, 0)) #la locomotive
        Game.marsh = self.marshall
        Game.wagons[0].interior.append(self.marshall) #le Marshall
        #Game.wagons[0].butins.append(Butin.Butin('magot'))
        #resonne avec L70
        for i in range(self.NB_JOUEURS) :
            Game.wagons.append(Wagon(self, i+1))
            Game.players.append(Player.Player(noms[i]))
        
        #phase de Réglages
        for personne in Game.players :
            # Obligatoire
            #personne.pos = randrange(1, len(Game.players)+1)
            personne.pos = len(Game.players)
            personne.munitions = self.NB_BALLES
            Game.wagons[personne.pos].interior.append(personne)
            #fin Obligtoire
        
        apperance.creation()

        

        #personne.avoirs.append(Butin.Butin('bourse'))


            
        
        



class Wagon :
    def __init__(self,jeu : Game, id) :
        self.type = ''
        if (jeu.wagons == []) : self.type = 'Locomotive'
        else : self.type = 'Wagon'

        self.Id = id            #num de wagon (commence a 0 : locomotive)
        self.exterior = []           #liste des joueurs sur le toit
        self.interior = []           #liste des joueurs dans le wagon
        self.butins = []        #liste des butins dans le wagon
        self.sprite = None
        self.Remplir()

    
    def Remplir(self):
        if (self.type=='Locomotive') :
            self.butins.append(Butin.Butin('magot'))
        else :
            nombre = randrange(1,4)
            for g in range(nombre+1) :
                type_butin = choice(['bijoux','bourse','bourse','bourse','bourse'])
                self.butins.append(Butin.Butin(type_butin))





    def showContenu(self) :
        print(f"---Wagon {self.Id}---")
        for thing in self.butins :
            print(f"{thing.type} : {thing.value} euros")
        print("----------")

    def showOccupants(self) :
        print("> INT")
        for per in self.interior :
            print(f"{per.name}", end=' ')

        print("\n> EXT")
        for per in self.exterior :
            print(f"{per.name}", end=' ')



class Marshall :
    def __init__(self) :
        self.name = "Marshall"
        self.pos = 0
        self.sprite = None
        self.xpos = 0

    def bouger(self) :
        cwagonId = self.pos
        cwagon = Game.wagons[cwagonId]

        direction = choice(['left','right'])

        if(direction=='left' and (cwagonId-1)>=0) :
            pwagon =  Game.wagons[cwagonId-1]
            index = cwagon.interior.index(self)
            self.pos -=1
            cwagon.interior.pop(index)
            pwagon.interior.append(self)
            #print(f"{self.name} went to the left <-\n")
        elif (direction=='right' and (cwagonId+1)<len(Game.wagons)) :
            pwagon =  Game.wagons[cwagonId+1]
            index = cwagon.interior.index(self)
            self.pos +=1
            cwagon.interior.pop(index)
            pwagon.interior.append(self)
            #print(f"{self.name} went to the right ->\n")

    def shoot(self, player, cwagon) :
        #cwagonId = self.pos
        #cwagon = Game.wagons[cwagonId]
        mlost = 0

        if (player.avoirs!=[]) : 
            index = randrange(len(player.avoirs))
            loss = player.avoirs[index].copier()
            mlost = loss.value
            player.avoirs.pop(index)

            if (player in cwagon.interior) :
                cwagon.butins.append(loss)
            #else le colis est perdu et voila
        
        Game.log.append_html_text(f"<b>Le {self.name} a tiré sur {player.name}</b>\n")
        Game.log.append_html_text(f"<FONT COLOR = '#b51414'>{player.name} a perdu {mlost}$</FONT>\n")
        player.fuire()
        #print(f"{self.name} shooted {player.name} who lost {mlost} euros\n")

    
    def goberserk (self) :
        cwagonId = self.pos
        cwagon = Game.wagons[cwagonId]

        if (cwagon.interior==[self]) : return None

        copy_int = cwagon.interior.copy()
        copy_int.remove(self)

        for voyou in copy_int :
            #print(f"{voyou.name}")
            self.shoot(voyou, cwagon)
            mixer.Channel(1).play(shot1_s)
            mixer.Channel(3).play(ugh_s)


mixer.init(channels=10)
down_s = mixer.Sound("../music/down.wav")
shot1_s = mixer.Sound("../music/shot1.wav")
shot2_s = mixer.Sound("../music/shot2.wav")
trans_s = mixer.Sound("../music/transition.wav")
ugh_s = mixer.Sound("../music/ugh.wav")
up_s = mixer.Sound("../music/up.wav")
coin_s = mixer.Sound("../music/coin.wav")
drop_s = mixer.Sound("../music/drop.wav")
train_s = mixer.Sound("../music/train.wav")
bell_s = mixer.Sound("../music/bell.wav")
vic_s = mixer.Sound("../music/victory.wav")