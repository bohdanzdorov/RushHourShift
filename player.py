import random
from card import Card

class Player:
    def __init__(self, playerVehicle, startSide,card, players_wining_position,player_position):
        self.__playerVehicle = playerVehicle
        self.__startSide = startSide
        self.__card = card
        self.__players_wining_position=players_wining_position

    #TODO: add getters

    def playRandomCard(self, deck):
        # Assume 'deck' is a list of available cards, and only contains one-move cards
        if deck:
            self.__card = random.choice(deck) #deck should be a list of card
            print(f"Player selected card: {self.__card}")
            return self.__card
            
        

    def checkWin(self,player_position,players_wining_position):
        game_go_on= True
        if(player_position == players_wining_position):
            print("Players win")
        else:
            game_go_on = False
        return game_go_on

deck = [Card.MOVE, Card.MOVE, Card.SLIDE, Card.SHIFT, Card.MOVEANDSLIDE]

p = Player(None, None, Card.MOVE, None, None)
p.playRandomCard(deck)
