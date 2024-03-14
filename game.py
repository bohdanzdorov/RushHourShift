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
        print(f"Player {self.__currentPlayer + 1}'s turn:")

        if(self.__players[self.__currentPlayer].playRandomCard() == Card.MOVE):
            print("1. Move a vehicle")
            movable_vehicles = self.getMovableVehicles(self.__players[self.__currentPlayer].getPlayerVehicle())
            if not movable_vehicles:
                print("No movable vehicles available.")
                return 0

            print(f"Movable vehicles:{movable_vehicles}")
            selected_vehicle_index = int(input("Select a vehicle to move (enter the corresponding number): "))
            move_command = int(input("Press one to move:"))
            if(move_command==1):print("vehicle moved")
            else:
                print("vehicle move command wrong")
                return 0
        
            
            if new_positions is not None:
                selected_vehicle.setPositions(new_positions)
                self.updateMap()
            else:
                print("Invalid move. Try again.")
                return 0
        elif(self.__players[self.__currentPlayer].playRandomCard() == Card.SHIFT):
            print("2. Shift the board")
            shiftable_boards = self.getShiftableBoard()
            if not shiftable_boards:
                print("No shiftable boards available.")
                return 0

            print("Shiftable boards:")
            if len(shiftable_boards>1):
                selected_board= int(input(f"enter 1 to shift {shiftable_boards[0]} and press 2 to shift {shiftable_boards[1]}:"))
            else:
                selected_board= int(input(f"enter 1 to shift {shiftable_boards}:"))
            #we neeed to know how many time we ask user to prompt the same think to how much it wants to go up or down.
            selected_direction= int(input("enter 1 for up one block or 2 to down one block and 0 to pass the move:"))

            shift(selected_board,selected_direction)  #refactor this accordingly
        elif(self.__players[self.__currentPlayer].playRandomCard() == Card.SLIDE):   
            movable_vehicles = self.getMovableVehicles(self.__players[self.__currentPlayer].getPlayerVehicle())
            if not movable_vehicles:
                print("No movable vehicles available.")
                return
            selected_vehicle_to_slide= str(input(f"enter the vehicle you want to slide"))
            return
        elif(self.__players[self.__currentPlayer].playRandomCard() == Card.MOVEANDSHIFT): 
            movable_vehicles = self.getMovableVehicles(self.__players[self.__currentPlayer].getPlayerVehicle())
            if not movable_vehicles:
                print("No movable vehicles available.")
                return

            print("Movable vehicles:")
            move_or_slide=int(input("Press 1 for shift and move same only and 2 for shift and move different"))
            if(move_or_slide==1):
                selected_vehicle= select_vehicle()
                shift(selected_vehicle)
            elif(move_or_slide==2):
                selected_first_vehicle=()
                selected_second_vehicle=()
                shift(selected_first_vehicle)
                move(selected_second_vehicle)
            else:
                print("invalid choice")
                return 0
            
            map = selected_board
            self.updateMap()
            

        else:
            print("Invalid choice. Try again.")
            return 0