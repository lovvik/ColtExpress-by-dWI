import random
import Game
import Butin

class Player :
    def __init__(self, name):
        self.name = name
        self.avoirs = []
        self.pos = 1
        self.munitions = 6
        self.sprite = None
        self.icon = None
        self.plan = None
        """random.randrange(len(Game.Game.players)) l'index du wagon"""

    

    def lacherButin(self) :
        mlost =0
        if (self.avoirs==[] or self in  Game.Game.wagons[self.pos].exterior) : return None
        index = random.randrange(len(self.avoirs))
        mlost = Game.Game.wagons[self.pos].butins[index]
        Game.Game.wagons[self.pos].butins.append(self.avoirs[index])
        self.avoirs.pop(index)
        Game.mixer.Channel(3).play(Game.drop_s)
        Game.Game.log.append_html_text(f"<FONT COLOR = '#b51414'>{self.name} a perdu {mlost}$</FONT>\n")




    def showAvoirs (self) :
        print(f"==={self.name}===")
        for thing in self.avoirs :
            print(f"{thing.type} : {thing.value} euros")
        print("=========")
    

    def bouger(self, direction : str) :
        # L W W W W
        #options direction
        # u : up | d : down | l : left | r : right
        #up ->  go le toit
        #down -> go l'intérieur du wagon
        # left ->  go to n-1 wagon
        # right -> go to n+1 wagon

        cwagonId = self.pos
        cwagon = Game.Game.wagons[cwagonId]

        if (direction=='u' or direction=='up') :
            #Going UP
            if (self in cwagon.interior) :
                index = cwagon.interior.index(self)
                cwagon.interior.pop(index)
                cwagon.exterior.append(self)
                #print(f"{self.name} went up\n")
                Game.mixer.Channel(4).play(Game.up_s)
                Game.Game.log.append_html_text(f"{self.name} est monté\n")
                #Game.Game.log.html_text+='\n kiss'

        elif (direction=='d' or direction=='down') :
            #Going DOWN
            if (self in cwagon.exterior) :
                index = cwagon.exterior.index(self)
                cwagon.exterior.pop(index)
                cwagon.interior.append(self)
                #print(f"{self.name} went down\n")
                Game.mixer.Channel(4).play(Game.down_s)
                Game.Game.log.append_html_text(f"{self.name} est descendu\n")



        elif (direction=='l' or direction=='left') :
            #Going LEFT
            if ((cwagonId-1)>=0) :
                pwagon =  Game.Game.wagons[cwagonId-1]
                if (self in cwagon.interior) :
                    index = cwagon.interior.index(self)
                    self.pos -=1
                    cwagon.interior.pop(index)
                    pwagon.interior.append(self)
                    #print(f"{self.name} went to the left <-\n")
                else :
                    index = cwagon.exterior.index(self)
                    self.pos -=1
                    cwagon.exterior.pop(index)
                    pwagon.exterior.append(self)
                    #print(f"{self.name} went to the left <-\n")
                Game.Game.log.append_html_text(f"{self.name} est parti à droite\n")
                #droite a cause de l'affichage

                    
        elif (direction=='r' or direction=='right') :
            #Going RIGHT
            if ((cwagonId+1)<len(Game.Game.wagons)) :
                pwagon =  Game.Game.wagons[cwagonId+1]
                if (self in cwagon.interior) :
                    index = cwagon.interior.index(self)
                    self.pos +=1
                    cwagon.interior.pop(index)
                    pwagon.interior.append(self)
                    #print(f"{self.name} went to the right ->\n")
                else :
                    index = cwagon.exterior.index(self)
                    self.pos +=1
                    cwagon.exterior.pop(index)
                    pwagon.exterior.append(self)
                    #print(f"{self.name} went to the right ->\n")
                Game.Game.log.append_html_text(f"{self.name} est parti à gauche\n")
                #gauche a cause de l'affichage


        else : return None


    def changer_niveau(self):
        cwagon = Game.Game.wagons[self.pos]
        if (self in cwagon.interior): self.bouger('u')
        elif (self in cwagon.exterior) : self.bouger('d')



    def braquer(self) :
        cwagon = Game.Game.wagons[self.pos]
        if (not (self in cwagon.interior)) : return None
        if (cwagon.butins==[]) : return None
        index = random.randrange(len(cwagon.butins))
        wvalue = cwagon.butins[index].value
        self.avoirs.append(cwagon.butins[index])
        cwagon.butins.pop(index)
        if wvalue==1000 : 
            Game.Game.log.append_html_text(f"<b><FONT COLOR='#650dbd'>{self.name} a ramassé 1000$</FONT></b>\n")
            if (Game.Game.SIG1000 == False) : Game.Game.SIG1000 = True
        else : Game.Game.log.append_html_text(f"<FONT COLOR='#14b531'>{self.name} a ramassé {wvalue}$</FONT>\n")
        Game.mixer.Channel(3).play(Game.coin_s)

        #print(f"> Braquage en wagon {cwagon.Id} : {self.name}")

    def fuire(self) :
        self.bouger('up')

    def shoot(self) :
        if (self.munitions<=0) : return None

        cwagon = Game.Game.wagons[self.pos]
        """if(cwagon.interior+cwagon.exterior == [self]) :
            #print("Nobody there\n") 
            return None"""

        Occupants = (cwagon.interior+cwagon.exterior)
        Occupants.remove(self)
        try : Occupants.remove(Game.Game.marsh)
        except : pass
        
        #print (f"Occupants : {Occupants}")
        if (Occupants==[]) :
            self.munitions -=1
            Game.Game.log.append_html_text(f"{self.name} a tiré dans le vide\n")
            Game.mixer.Channel(4).play(Game.shot2_s)
            return None
        victim = random.choice(Occupants)
        
        mlost = 0

        if (victim.avoirs!=[]) : 
            index = random.randrange(len(victim.avoirs))
            loss = victim.avoirs[index].copier()
            victim.avoirs.pop(index)
            mlost = loss.value

            if (victim in cwagon.interior) :
                cwagon.butins.append(loss)
            #else le colis est perdu et voila

        self.munitions -= 1
        Game.mixer.Channel(4).play(Game.shot2_s)
        #print(f"{self.name} ({self.munitions} balles) shooted {victim.name} who lost {mlost} euros\n")
        Game.Game.log.append_html_text(f"<b>{self.name} a tiré sur {victim.name}</b>\n")
        Game.mixer.Channel(3).play(Game.ugh_s)
        Game.Game.log.append_html_text(f"<FONT COLOR='#b51414'>{victim.name} a perdu {mlost}$</FONT>\n")



    def solde(self) :
        s=0
        for avoir in self.avoirs :
            s+=avoir.value
        return s


