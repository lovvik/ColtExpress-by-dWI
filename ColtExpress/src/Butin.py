from random import choice
import Player
import Game

class Butin :
    def __init__(self, type : str) :
        self.type = type
        self.value = 0

        if (self.type=='magot') : self.value = 1000
        elif (self.type=='bijoux') : self.value = 500
        elif (self.type=='bourse') : self.value = choice((100, 200))
        else : print("Wrong Butin Type\n")

        self.sprite = None
        self.xpos = 0
    
    def copier(self) :
        new = Butin(self.type)
        new.value = self.value
        return new





