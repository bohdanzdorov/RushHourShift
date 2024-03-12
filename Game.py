import numpy as np

from Player import Player

from Orientation import Orientation
from Vehicle import Vehicle

from SideBoardPiece import SideBoardPieces
from BoardPiece import BoardPiece
from Side import Side
from ShiftTo import ShiftTo
class Game:
    def __init__(self, map, vehicles, players, sidePieces, centralPiece):
        self.__currentPlayer = 0
        self.__map = map
        self.__vehicles = vehicles
        self.__players = players
        self.__sidePieces = sidePieces
        self.__centralPiece = centralPiece

    def printMap(self):
        topBottomBounds = '-' * 46
        
        print("\033[94m" + topBottomBounds + "\033[00m")

        for i in range(len(self.__map)):
            s="\033[94m|  \033[00m"
            for j in range(len(self.__map[i])):
                if(self.__map[i][j] == '_'):
                    if(j < 5 or j > 8):
                        s += '\033[1;32m_  \033[00m'
                    else:
                        s += '\033[0;32m_  \033[00m'
                elif(self.__map[i][j] == '1'):
                    s += '\033[1;33m1  \033[00m'
                elif(self.__map[i][j] == '2'):
                    s += '\033[0;31m2  \033[00m'    
                else:    
                    s+= self.__map[i][j] + "  "

            print(s + "\033[94m| \033[00m")
        print("\033[94m" + topBottomBounds + "\033[00m")

    def updateMap(self):
        for y in range(len(self.__map)):
            for x in range(len(self.__map[y])):
                checkForVehicle = self.checkVehicleOnCoords(x, y)
                if(checkForVehicle):
                    self.__map[y][x] = checkForVehicle
                elif(self.checkBoardOnCoords(x, y)):    
                    self.__map[y][x] = '_'
                else:
                    self.__map[y][x] = ' '
                                    
    
    def checkBoardOnCoords(self, xToCheck, yToCheck):
        alignLine = 4
        if(xToCheck > -1 and xToCheck < 5): # we are checking the left board
            if(alignLine + self.__sidePieces[0].getMargin() < yToCheck and alignLine + self.__sidePieces[0].getMargin()+6 >= yToCheck): #or alignLine - self.__sidePieces[0].getMargin() < yToCheck):
                return True
        
        elif(xToCheck > 4 and xToCheck < 9):
            if(yToCheck > 4 and yToCheck < 11):
                return True
        else:
            if(alignLine + self.__sidePieces[1].getMargin() < yToCheck and alignLine + self.__sidePieces[1].getMargin()+6 >= yToCheck  ):
                return True
        return False    

    def checkVehicleOnCoords(self, xToCheck, yToCheck):
        #going through regular vehicles
        for i in range(len(self.__vehicles)):
            curVehiclePositions = self.__vehicles[i].getPositions()
            for j in range(len(curVehiclePositions)): #Go throught all the coordinates of a vehicle
                if(curVehiclePositions[j][0] == xToCheck and curVehiclePositions[j][1] == yToCheck):
                    return self.__vehicles[i].getId()
                
        #going throught players' vehicles
        for i in range(len(self.__players)):
            curPositions = self.__players[i].getPlayerVehicle().getPositions()
            for j in range(len(curPositions)):
                if(curPositions[j][0] == xToCheck and curPositions[j][1] == yToCheck):
                    return self.__players[i].getPlayerVehicle().getId()
        return None       

    def changePlayers(self):
         self.__currentPlayer = 1 if self.__currentPlayer == 0 else 0      

    def checkVehicleMovability(self, vehicle):
        vehiclePositions = vehicle.getPositions()
        if(vehicle.getOrientation() == Orientation.VERTICAL):
            isBlockedUp = False
            isBlockedDown = False
            for i in range(vehicle.getLength()):
                #Check upper block
                if(vehiclePositions[i][1]-1 < 0 or # vehicle out of upper world bounds
                   (map[vehiclePositions[i][1]-1][vehiclePositions[i][0]] != '_' and # upper block is ' ' or 'vehicle_char'
                    map[vehiclePositions[i][1]-1][vehiclePositions[i][0]] != vehicle.getId()) # upper block is ' ' or 'OTHER_vehicle_char'
                ):
                    isBlockedUp = True
                #Check bottom block
                if(vehiclePositions[i][1]+1 > len(map)-1 or # vehicle out of bottom world bounds
                   (map[vehiclePositions[i][1]+1][vehiclePositions[i][0]]!= '_' and # bottom block is ' ' or 'vehicle_char'
                    map[vehiclePositions[i][1]+1][vehiclePositions[i][0]] != vehicle.getId()) # bottom block is ' ' or 'OTHER_vehicle_char'
                ):
                    isBlockedDown = True
            #Decide if vehicle is fully blocked
            if(isBlockedUp and isBlockedDown):
                return False
            return True
        else: 
            isBlockedLeft = False
            isBlockedRight = False
            for i in range(vehicle.getLength()):
                if(vehiclePositions[i][0]-1 < 0 or # vehicle at the left side world bounds
                   (map[vehiclePositions[i][1]][vehiclePositions[i][0]-1] != '_' and # left block is 'vehicle_char'
                    map[vehiclePositions[i][1]][vehiclePositions[i][0]-1] != vehicle.getId()) # left block is 'OTHER_vehicle_char'
                ):
                    isBlockedLeft = True
                     
                if(vehiclePositions[i][0]+1 > len(map[0])-1 or # vehicle at the right side world bounds
                   (map[vehiclePositions[i][1]][vehiclePositions[i][0]+1] != '_' and # right block is 'vehicle_char'
                    map[vehiclePositions[i][1]][vehiclePositions[i][0]+1] != vehicle.getId()) # right block is 'OTHER_vehicle_char'
                ):
                    isBlockedRight = True
                
            if(isBlockedLeft and isBlockedRight):
                return False 
            return True  
        
vehicles = [Vehicle('A', 2, Orientation.HORIZONTAL, [[0,5], [1,5]]), Vehicle('B', 2, Orientation.VERTICAL, [[2,5], [2,6]])]

map = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    ]

player1 = Player(Vehicle('1', 2, Orientation.HORIZONTAL, [[1,7], [2,7]]), None, None, None)
player2 = Player(Vehicle('2', 2, Orientation.HORIZONTAL, [[13,8], [12,8]]), None, None, None)

players=[player1, player2]

sidePieces = [SideBoardPieces(6, 5, Side.LEFT), SideBoardPieces(6, 5, Side.RIGHT)]
centralPiece = BoardPiece(6, 4)

game = Game(map, vehicles, players, sidePieces, centralPiece)
game.updateMap()
game.printMap()

print(game.checkVehicleMovability(vehicles[0]))

