class Player:
    def __init__(self, playerVehicle, startSide,card, players_wining_position):
        self.__playerVehicle = playerVehicle
        self.__startSide = startSide
        self.__card = card
        self.__players_wining_position=players_wining_position

    def getPlayerVehicle(self):
        return self.__playerVehicle