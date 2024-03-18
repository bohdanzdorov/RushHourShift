import numpy as np

from Agent import Agent
from Player import Player
from Card import Card

from Orientation import Orientation
from State import State
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
        self.__deck = [Card.SLIDE, Card.MOVE, Card.MOVE, Card.MOVE, Card.SHIFT, Card.SHIFT, Card.MOVEANDSHIFT]

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
              
    def getShiftableBoards(self):
        #it return an array of shiftable boards
        shiftable_boards=[]
        for i in range(len(self.__sidePieces)):
            if(self.__sidePieces[i].isShiftable(1, ShiftTo.UP, self.__vehicles)==True):
                shiftable_boards.append(self.__sidePieces[i])
        return shiftable_boards
    
    def getMovableVehicles(self):
        movable_vehicles = []
        for i in range(len(self.__vehicles)):
            if(self.checkVehicleMovability(self.__vehicles[i])==True):
                movable_vehicles.append(self.__vehicles[i])
        return movable_vehicles
    
    def makeMove(self):
        movable_vehicles = self.getMovableVehicles()
        
        check_player_vehicle_movability=self.checkVehicleMovability(self.__players[self.__currentPlayer].getPlayerVehicle())
        if not movable_vehicles and not check_player_vehicle_movability:
            print("No movable vehicles available.\nSorry, you need to skip your turn :(")
            return 0
        else:
            #Print out all movable vehicles
            i = 0
            print("Movable vehicles:")
            for i in range(len(movable_vehicles)):
                    print(f"- {movable_vehicles[i].getId()}")
            if check_player_vehicle_movability:
                print(f"- {self.__players[self.__currentPlayer].getPlayerVehicle().getId()}") 
            #Player selects vehicle and direction to move
            selected_vehicle_id= str(input("Select a vehicle to move (enter the corresponding id): \n>"))
            print(f"You chose {selected_vehicle_id}\n")

            move_direction = int(input("Select the movement direction:\n '1' - To move right/down\n '-1' - To move left/up\n\n>"))
            #Go through all movable vehicles and find
            for e in range(len(self.__vehicles)):
                if(selected_vehicle_id==self.__vehicles[e].getId()):
                    self.__vehicles[e].move(move_direction,self.__map)
            if(selected_vehicle_id == self.__players[self.__currentPlayer].getPlayerVehicle().getId()):
                    self.__players[self.__currentPlayer].getPlayerVehicle().move(move_direction,self.__map)
            #Update changes
            self.updateMap()

    def makeShift(self):
        selected_board=0
        shiftable_boards = self.getShiftableBoards()
        if not shiftable_boards:
            print("No shiftable boards available.\nSorry, you gonna skip this turn :(")
            return 0
        
        if len(shiftable_boards)>1:
            selected_board= int(input(f"Select board side to shift:\n 0. {shiftable_boards[0].getSide()}\n 1. {shiftable_boards[1].getSide()}\n\n>"))
            selected_direction= int(input("\nSelect the direction to shift:\n Enter 1 for 'up'\n Enter -1 for 'down'\n\n>"))
            if(selected_direction==1):
                self.__sidePieces[selected_board].shift(1,ShiftTo.UP,self.__vehicles, [self.__players[0].getPlayerVehicle(), self.__players[1].getPlayerVehicle()]) 
            else:
                self.__sidePieces[selected_board].shift(1,ShiftTo.DOWN,self.__vehicles, [self.__players[0].getPlayerVehicle(), self.__players[1].getPlayerVehicle()])
        else:
            selected_direction= int(input("Select the direction to shift:\n Enter 1 for 'up'\n Enter -1 for 'down'\n\n>"))
            if(selected_direction==1):
                self.__sidePieces[shiftable_boards[0].getSide().value].shift(1,ShiftTo.UP,self.__vehicles, [self.__players[0].getPlayerVehicle(), self.__players[1].getPlayerVehicle()])
            else:
                self.__sidePieces[shiftable_boards[0].getSide().value].shift(1,ShiftTo.DOWN,self.__vehicles, [self.__players[0].getPlayerVehicle(), self.__players[1].getPlayerVehicle()])
        self.updateMap()
    
    def makeSlide(self):
        movable_vehicles = self.getMovableVehicles()
        
        check_player_vehicle_movability=self.checkVehicleMovability(self.__players[self.__currentPlayer].getPlayerVehicle())
        if not movable_vehicles and not check_player_vehicle_movability:
            print("No movable vehicles available.\nSorry, you need to skip your turn :(")
            return 0
        else:
            #Print out all movable vehicles
            print("Movable vehicles: ")
            for i in range(len(movable_vehicles)):
                    print(f"- {movable_vehicles[i].getId()}")
            if check_player_vehicle_movability:
                print(f"- {self.__players[self.__currentPlayer].getPlayerVehicle().getId()}") 
            #Player selects vehicle and direction to slide
            selected_vehicle_id= str(input("Select a vehicle to slide (enter the corresponding id): "))
            print(f"You chose {selected_vehicle_id}\n")

            move_direction = int(input("Select the movement direction:\n '1' - To move right/down\n '-1' - To move left/up\n\n>"))
            #Go through all movable vehicles and find
            for e in range(len(self.__vehicles)):
                if(selected_vehicle_id==self.__vehicles[e].getId()):
                    self.__vehicles[e].slide(move_direction,self.__map)
            if(selected_vehicle_id == self.__players[self.__currentPlayer].getPlayerVehicle().getId()):
                    self.__players[self.__currentPlayer].getPlayerVehicle().slide(move_direction,self.__map)
            #Update changes
            self.updateMap()

    def makeTurn(self):
        print(f"Player {self.__currentPlayer+1}'s turn:")
        selected_card = self.__players[self.__currentPlayer].playRandomCard(self.__deck)

        self.printMap()
        if(selected_card == Card.MOVE):
            self.makeMove()
        elif(selected_card == Card.SHIFT):
            self.makeShift()
        elif(selected_card == Card.SLIDE):   
            self.makeSlide()
        elif(selected_card == Card.MOVEANDSHIFT): 
            move_and_shift=int(input("Choice the first action:\n1. Shift first, then move \n2. Move first, then shift:\n\n>"))
            if(move_and_shift==1):
                self.makeShift()
                self.printMap()
                self.makeMove()
            elif(move_and_shift==2):
                self.makeMove()
                self.printMap()
                self.makeShift()    
            else:
                print("invalid choice")
                return 0
        else:
            print("Invalid choice. Try again.")
            return 0
        
    def play(self):
        gameMode = int(input("Please, choose a play mode : \n1.Player vs. Player\n2.Player vs. AI\n\n>"))
        if(gameMode == 1):
            while(self.__players[0].checkWin() == False and self.__players[1].checkWin() == False):
                self.makeTurn()
                self.printMap()
                self.changePlayers()
            self.changePlayers()
            print(f"\n\nCongratulations!!!\nPlayer {self.__currentPlayer+1} won!!!")    
        elif(gameMode == 2):
            agent = Agent(Vehicle('2', 2, Orientation.HORIZONTAL, [[12,8], [13,8]]), Side.RIGHT, None)
            players[1] = agent
            self.__currentPlayer = 1 # agent always goes first
            
            while(self.__players[0].checkWin() == False and self.__players[1].checkWin() == False):
                if(self.__currentPlayer == 1):
                    self.__players[1].playRandomCard(self.__deck)
                    agentAction = self.__players[1].zeroDepth(State(self.__players[1].getPlayerVehicle(), self.__players[0].getPlayerVehicle(), self.__vehicles, self.__sidePieces))
                    
                    if(agentAction.getCardType() == Card.MOVE):
                        print("Agent moves vehicle '", agentAction.getItem(), "' to ", "right/down " if agentAction.getDirection() == 1 else "left/up ")
                        for e in range(len(self.__vehicles)):
                            if( agentAction.getItem()==self.__vehicles[e].getId()):
                                self.__vehicles[e].move(agentAction.getDirection(),self.__map)
                        if(agentAction.getItem() == self.__players[self.__currentPlayer].getPlayerVehicle().getId()):
                            self.__players[self.__currentPlayer].getPlayerVehicle().move(agentAction.getDirection(),self.__map)
                    
                    elif(agentAction.getCardType() == Card.SLIDE):
                        slideDirection = 0
                        if(agentAction.getDirection() > 0):
                            slideDirection = 1
                        elif(agentAction.getDirection() < 0):
                            slideDirection = -1
                        else:
                            slideDirection = 0
                        print("Agent slides vehicle '", agentAction.getItem(), "' to ", "right/down " if agentAction.getDirection() == 1 else "left/up ")
                        for e in range(len(self.__vehicles)):
                            if( agentAction.getItem()==self.__vehicles[e].getId()):
                                self.__vehicles[e].slide(slideDirection,self.__map)
                        if(agentAction.getItem() == self.__players[self.__currentPlayer].getPlayerVehicle().getId()):
                            self.__players[self.__currentPlayer].getPlayerVehicle().slide(slideDirection,self.__map)

                    elif(agentAction.getCardType() == Card.SHIFT):
                        print("Agent shifts board piece '", agentAction.getItem(), " up " if agentAction.getDirection() == ShiftTo.UP else " down ")
                        if(agentAction.getDirection()==ShiftTo.UP):
                            self.__sidePieces[agentAction.getItem().value].shift(1,ShiftTo.UP,self.__vehicles, [self.__players[0].getPlayerVehicle(), self.__players[1].getPlayerVehicle()])
                        else:
                            self.__sidePieces[agentAction.getItem().value].shift(1,ShiftTo.DOWN,self.__vehicles, [self.__players[0].getPlayerVehicle(), self.__players[1].getPlayerVehicle()])

                    elif(agentAction.getCardType() == Card.MOVEANDSHIFT):

                        if(agentAction.getItem()[0] == Side.LEFT or agentAction.getItem()[0] == Side.RIGHT):
                            print(f"Agents shifts the board {agentAction.getItem()[0]} {agentAction.getDirection()[0]}")
                            if(agentAction.getDirection()[0]==ShiftTo.UP):
                                self.__sidePieces[agentAction.getItem()[0].value].shift(1,ShiftTo.UP,self.__vehicles, [self.__players[0].getPlayerVehicle(), self.__players[1].getPlayerVehicle()])
                            else:
                                self.__sidePieces[agentAction.getItem()[0].value].shift(1,ShiftTo.DOWN,self.__vehicles, [self.__players[0].getPlayerVehicle(), self.__players[1].getPlayerVehicle()])
                            self.updateMap()
                            print(f"and then moves vehicle {agentAction.getItem()[1]} {"up/left" if agentAction.getDirection()[1] == -1 else " down/right"}")
                            for e in range(len(self.__vehicles)):
                                if( agentAction.getItem()[1]==self.__vehicles[e].getId()):
                                    self.__vehicles[e].move(agentAction.getDirection()[1],self.__map)
                            if(agentAction.getItem()[1] == self.__players[self.__currentPlayer].getPlayerVehicle().getId()):
                                self.__players[self.__currentPlayer].getPlayerVehicle().move(agentAction.getDirection()[1],self.__map)
                        else:
                            print(f"Agent moves vehicle {agentAction.getItem()[0]} {"up/left" if agentAction.getDirection()[0] == -1 else " down/right"}")
                            for e in range(len(self.__vehicles)):
                                if( agentAction.getItem()[0]==self.__vehicles[e].getId()):
                                    self.__vehicles[e].move(agentAction.getDirection()[0],self.__map)
                            if(agentAction.getItem()[0] == self.__players[self.__currentPlayer].getPlayerVehicle().getId()):
                                self.__players[self.__currentPlayer].getPlayerVehicle().move(agentAction.getDirection()[0],self.__map)
                            self.updateMap()
                            print(f"and then shifts the board {agentAction.getItem()[1]} {agentAction.getDirection()[1]}")
                            if(agentAction.getDirection()[1]==ShiftTo.UP):
                                self.__sidePieces[agentAction.getItem()[1].value].shift(1,ShiftTo.UP,self.__vehicles, [self.__players[0].getPlayerVehicle(), self.__players[1].getPlayerVehicle()])
                            else:
                                self.__sidePieces[agentAction.getItem()[1].value].shift(1,ShiftTo.DOWN,self.__vehicles, [self.__players[0].getPlayerVehicle(), self.__players[1].getPlayerVehicle()])
                    self.updateMap()
                    self.printMap()
                else:
                    self.makeTurn()
                    self.printMap()
                self.changePlayers()
            if(self.__currentPlayer == 1):
                print("Congratulations, YOU WON!!!")
            else:
                print("AI WON!!! Better luck next time, loser!!!")
        else:
            print("Incorrect option entered :(")
            return False        
map = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    ]

vehiclesSet6 = [ Vehicle('A', 2, Orientation.VERTICAL, [[4,7], [4,8]]), 
                 Vehicle('B', 3, Orientation.VERTICAL, [[5, 7], [5, 8], [5,9]]),
                 Vehicle('D', 2, Orientation.HORIZONTAL, [[5,6], [6,6]]),
                 Vehicle('E', 3, Orientation.VERTICAL, [[6,7], [6,8], [6,9]]),
                 Vehicle('F', 3, Orientation.VERTICAL, [[7,6], [7,7], [7, 8]]),
                 Vehicle('G', 3, Orientation.VERTICAL, [[8,6], [8,7], [8, 8]]),
                 Vehicle('H', 2, Orientation.HORIZONTAL, [[7,9], [8, 9]]),
                 Vehicle('I', 2, Orientation.VERTICAL, [[9,7], [9,8]]),


                ]
player1 = Player(Vehicle('1', 2, Orientation.HORIZONTAL, [[0,7], [1,7]]), Side.LEFT, None)
player2 = Player(Vehicle('2', 2, Orientation.HORIZONTAL, [[12,8], [13,8]]), Side.RIGHT, None)

players=[player1, player2]
sidePieces = [SideBoardPieces(6, 5, Side.LEFT), SideBoardPieces(6, 5, Side.RIGHT)]

centralPiece = BoardPiece(6, 4)

game = Game(map, vehiclesSet6, players, sidePieces, centralPiece)
game.updateMap()
game.printMap()

game.play()