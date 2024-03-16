import random
from Card import Card
from Side import Side
class Player:
    def __init__(self, playerVehicle, startSide, card):
        self.__playerVehicle = playerVehicle
        self.__startSide = startSide
        self.__card = card
        
    def getCard(self):
        return self.__card    
    def getStartSide(self):
        return self.__startSide
    def getPlayerVehicle(self):
        return self.__playerVehicle

    def playRandomCard(self, deck):
        # Assume 'deck' is a list of available cards, and only contains one-move cards
        if deck:
            self.__card = random.choice(deck) #deck should be a list of card
            print(f"Player picked card: {self.__card}")
            return self.__card
            
    def checkWin(self):
        if(self.__startSide == Side.LEFT):
            for i in range(2):
                if(self.__playerVehicle.getPositions()[i][0] > 12):
                    return True
            return False
        elif(self.__startSide == Side.RIGHT):
            for i in range(2):
                if(self.__playerVehicle.getPositions()[i][0] < 1):
                    return True
            return False

