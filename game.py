from player import Player
from card import Card
class Game:
    def __init__(self, map, vehicles, players, sidePieces, centralPiece):
        self.__currentPlayer = 0
        self.__map = map
        self.__vehicles = vehicles
        self.__players = players
        self.__sidePieces = sidePieces
        self.__centralPiece = centralPiece


    ## Lummim Works From there 
    
    def getShiftableBoard(self):
        #it return an array of shiftable boards
        shiftable_boards=[]
        for i in range(len(self.__sidePieces)):
            if(self.__sidePieces[i]==True):
                shiftable_boards.append(self.__sidePieces[i])
        return shiftable_boards
    
    def getMovableVehicles(self):
        #it should return an array of all the available vehicles that can be moved.  
        movable_vehicles = []
        for i in range(len(self.__vehicles)):
            if(checkVehicleMovability(self.__vehicles)==True):
                movable_vehicles.append(self.__vehicles[i])
        return movable_vehicles

    def playerTurn(self):
        print(f"Player {self.__currentPlayer+1}'s turn:")
        selected_card = Player.playRandomCard()

        if(selected_card == Card.MOVE):
            print("Move a vehicle")
            movable_vehicles = self.getMovableVehicles()
         
            check_player_vehicle_movability=self.checkVehicleMovability(self.__players[self.__currentPlayer].getPlayerVehicle())
            if not movable_vehicles and not check_player_vehicle_movability:
                print("No movable vehicles available.")
                return 0
            else:
                for i in range(len(movable_vehicles)):
                        print(f"Movable vehicles:{movable_vehicles[i]} and the id = {movable_vehicles[i].getId()}.")
                if check_player_vehicle_movability:
                    #here should be a for loop for all the vehicles id printed so that player can select getVehicleID
                    print(f"the player vehicle is {self.__players[self.__currentPlayer].getPlayerVehicle().getId()}") 
                selected_vehicle_id= int(input("Select a vehicle to move (enter the corresponding number): "))
                move_direction = int(input("Press 1 to move forward and press -1 to move backward:"))
                for e in range(len(self.__vehicles)):
                    if(selected_vehicle_id==self.__vehicles[e]):
                        self.__vehicles[e].move(move_direction,self.__map)
            
                if(selected_vehicle_id== self.__players[self.__currentPlayer].getPlayerVehicle().getId()):
                        self.__players[self.__currentPlayer].getPlayerVehicle().move(move_direction,self.__map)
                else:
                    print("vehicle move command wrong")
                    return 0
            self.updateMap()
        elif(selected_card == Card.SHIFT):
            print("Shift the board")
            selected_board=0
            shiftable_boards = self.getShiftableBoard()
            if not shiftable_boards:
                print("No shiftable boards available.")
                return 0
            for i in range(len(shiftable_boards)):
                print(f"select sides of shiftable boards= {shiftable_boards[i].getSide().value}.")
            
            if len(shiftable_boards>1):
                selected_board= int(input(f"enter 0 to shift {shiftable_boards[0].getSide().value} and press 1 to shift {shiftable_boards[1].getSide().value}:"))
                selected_direction= int(input("enter 1 for up one block or -1 to down one block and 0 to pass the move:"))
                if(selected_direction==1):
                    self.__sidePieces[selected_board].shift(1,ShiftTo.UP,self.__vehicles)            
                else:
                    self.__sidePieces[selected_board].shift(1,ShiftTo.DOWN,self.__vehicles)            

            else:
                selected_direction= int(input("enter 1 for up one block or -1 to down one block and 0 to pass the move:"))
                if(selected_direction==1):
                    self.__sidePieces[selected_board[0].getSide().value].shift(1,ShiftTo.UP,self.__vehicles)            
                else:
                    self.__sidePieces[selected_board[0].getSide().value].shift(1,ShiftTo.DOWN,self.__vehicles) 
            self.updateMap()
        elif(selected_card == Card.SLIDE):   
            print("Slide a vehicle")
            movable_vehicles = self.getMovableVehicles()
            check_player_vehicle_movability=self.checkVehicleMovability(self.__players[self.__currentPlayer].getPlayerVehicle())
            if not movable_vehicles and not check_player_vehicle_movability:
                print("No movable vehicles available.")
                return 0
            else:
                for i in range(len(movable_vehicles)):
                        print(f"Shiftable vehicles id = {movable_vehicles[i].getId()}.")
                if check_player_vehicle_movability:
                    #here should be a for loop for all the vehicles id printed so that player can select getVehicleID
                    print(f"the player vehicle is {self.__players[self.__currentPlayer].getPlayerVehicle().getId()}") 
                selected_vehicle_id= int(input("Select a vehicle to Shift (enter the corresponding number): "))
                move_direction = int(input("Press 1 to shift forward and press -1 to move backward:"))
                for e in range(len(self.__vehicles)):
                    if(selected_vehicle_id==self.__vehicles[e]):
                        self.__vehicles[e].slide(move_direction,self.__map)
            
                if(selected_vehicle_id== self.__players[self.__currentPlayer].getPlayerVehicle().getId()):
                        self.__players[self.__currentPlayer].getPlayerVehicle().slide(move_direction,self.__map)
                else:
                    print("vehicle slide command wrong")
                    return 0
            self.updateMap()
        elif(selected_card == Card.MOVEANDSHIFT): 
            movable_vehicles = self.getMovableVehicles(self.__players[self.__currentPlayer].getPlayerVehicle())
            if not movable_vehicles:
                print("No movable vehicles available.")
                return

            print("Movable vehicles:")
            move_and_shift=int(input("Press 1 for shift or press 2 for move first:"))
            if(move_and_shift==1):
                print("Shift the board")
                selected_board=0
                shiftable_boards = self.getShiftableBoard()
                if not shiftable_boards:
                    print("No shiftable boards available.")
                    return 0
                for i in range(len(shiftable_boards)):
                    print(f"select sides of shiftable boards= {shiftable_boards[i].getSide().value}.")
                
                if len(shiftable_boards>1):
                    selected_board= int(input(f"enter 0 to shift {shiftable_boards[0].getSide().value} and press 1 to shift {shiftable_boards[1].getSide().value}:"))
                    selected_direction= int(input("enter 1 for up one block or -1 to down one block and 0 to pass the move:"))
                    if(selected_direction==1):
                        self.__sidePieces[selected_board].shift(1,ShiftTo.UP,self.__vehicles)            
                    else:
                        self.__sidePieces[selected_board].shift(1,ShiftTo.DOWN,self.__vehicles)            

                else:
                    selected_direction= int(input("enter 1 for up one block or -1 to down one block and 0 to pass the move:"))
                    if(selected_direction==1):
                        self.__sidePieces[selected_board[0].getSide().value].shift(1,ShiftTo.UP,self.__vehicles)            
                    else:
                        self.__sidePieces[selected_board[0].getSide().value].shift(1,ShiftTo.DOWN,self.__vehicles)
                self.updateMap()
                print("Move a vehicle")
                movable_vehicles = self.getMovableVehicles()
            
                check_player_vehicle_movability=self.checkVehicleMovability(self.__players[self.__currentPlayer].getPlayerVehicle())
                if not movable_vehicles and not check_player_vehicle_movability:
                    print("No movable vehicles available.")
                    return 0
                else:
                    for i in range(len(movable_vehicles)):
                            print(f"Movable vehicles:{movable_vehicles[i]} and the id = {movable_vehicles[i].getId()}.")
                    if check_player_vehicle_movability:
                        #here should be a for loop for all the vehicles id printed so that player can select getVehicleID
                        print(f"the player vehicle is {self.__players[self.__currentPlayer].getPlayerVehicle().getId()}") 
                    selected_vehicle_id= int(input("Select a vehicle to move (enter the corresponding number): "))
                    move_direction = int(input("Press 1 to move forward and press -1 to move backward:"))
                    for e in range(len(self.__vehicles)):
                        if(selected_vehicle_id==self.__vehicles[e]):
                            self.__vehicles[e].move(move_direction,self.__map)
                
                    if(selected_vehicle_id== self.__players[self.__currentPlayer].getPlayerVehicle().getId()):
                            self.__players[self.__currentPlayer].getPlayerVehicle().move(move_direction,self.__map)
                    else:
                        print("vehicle move command wrong")
                        return 0
                self.updateMap()
            elif(move_and_shift==2):
                print("Move a vehicle")
                movable_vehicles = self.getMovableVehicles()
            
                check_player_vehicle_movability=self.checkVehicleMovability(self.__players[self.__currentPlayer].getPlayerVehicle())
                if not movable_vehicles and not check_player_vehicle_movability:
                    print("No movable vehicles available.")
                    return 0
                else:
                    for i in range(len(movable_vehicles)):
                            print(f"Movable vehicles:{movable_vehicles[i]} and the id = {movable_vehicles[i].getId()}.")
                    if check_player_vehicle_movability:
                        #here should be a for loop for all the vehicles id printed so that player can select getVehicleID
                        print(f"the player vehicle is {self.__players[self.__currentPlayer].getPlayerVehicle().getId()}") 
                    selected_vehicle_id= int(input("Select a vehicle to move (enter the corresponding number): "))
                    move_direction = int(input("Press 1 to move forward and press -1 to move backward:"))
                    for e in range(len(self.__vehicles)):
                        if(selected_vehicle_id==self.__vehicles[e]):
                            self.__vehicles[e].move(move_direction,self.__map)
                
                    if(selected_vehicle_id== self.__players[self.__currentPlayer].getPlayerVehicle().getId()):
                            self.__players[self.__currentPlayer].getPlayerVehicle().move(move_direction,self.__map)
                    else:
                        print("vehicle move command wrong")
                        return 0
                self.updateMap()
                print("Shift the board")
                selected_board=0
                shiftable_boards = self.getShiftableBoard()
                if not shiftable_boards:
                    print("No shiftable boards available.")
                    return 0
                for i in range(len(shiftable_boards)):
                    print(f"select sides of shiftable boards= {shiftable_boards[i].getSide().value}.")
                
                if len(shiftable_boards>1):
                    selected_board= int(input(f"enter 0 to shift {shiftable_boards[0].getSide().value} and press 1 to shift {shiftable_boards[1].getSide().value}:"))
                    selected_direction= int(input("enter 1 for up one block or -1 to down one block and 0 to pass the move:"))
                    if(selected_direction==1):
                        self.__sidePieces[selected_board].shift(1,ShiftTo.UP,self.__vehicles)            
                    else:
                        self.__sidePieces[selected_board].shift(1,ShiftTo.DOWN,self.__vehicles)            

                else:
                    selected_direction= int(input("enter 1 for up one block or -1 to down one block and 0 to pass the move:"))
                    if(selected_direction==1):
                        self.__sidePieces[selected_board[0].getSide().value].shift(1,ShiftTo.UP,self.__vehicles)            
                    else:
                        self.__sidePieces[selected_board[0].getSide().value].shift(1,ShiftTo.DOWN,self.__vehicles)
                self.updateMap()

                
            else:
                print("invalid choice")
                return 0
            
            self.updateMap()
            

        else:
            print("Invalid choice. Try again.")
            return 0