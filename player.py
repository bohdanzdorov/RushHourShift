import random
class Player:
    def __init__(self, playerVehicle, startSide,card, players_wining_position,player_position):
        self.__playerVehicle = playerVehicle
        self.__startSide = startSide
        self.__card = card
        self.__player_position=player_position
        self.__players_wining_position=players_wining_position

"""     def playRandomCard():
        #it will be take a random card which is basically the player will have the turn of his card in hand.
        #it will set the card of the class to a random card.
        pass
    def checkWin():
        #it will check whether the player or AI or other 2nd player wins or not.
        pass
    class Player:
    """
def playRandomCard(self, deck):
        # Assume 'deck' is a list of available cards, and only contains one-move cards
        if deck:
            player_card = random.choice(deck) #deck should be a list of card
            deck.remove(player_card)
            print(f"Player selected card: {card}")
            
            #ADD THE CARD AT THE END OF THE DECK
            deck.append(player_card)
        

def checkWin(self,player_position,players_wining_position):
        game_go_on=True
        if(player_position == players_wining_position):
            print("Players win")
        else:
            game_go_on = False
        return game_go_on