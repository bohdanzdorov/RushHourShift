class State():
    def __init__(self, curAgentVehicle, opponentVehicle, vehicles, sideBoards):
        self.__curAgentVehicle= curAgentVehicle
        self.__opponentVehicle = opponentVehicle
        self.__vehicles = vehicles
        self.__sideBoards = sideBoards

    def getCurAgentVehicle(self):
        return self.__curAgentVehicle
    def getOpponentVehicle(self):
        return self.__opponentVehicle
    def getVehicles(self):
        return self.__vehicles
    def getSideBoards(self):
        return self.__sideBoards
