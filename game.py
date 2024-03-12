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
                return

            print("Movable vehicles:")
            #Just ask a user to write vehicle id that he wants to move
            # for i, vehicle in enumerate(movable_vehicles):
            #     print(f"{i + 1}. {vehicle.getVehicleChar()}")

            # selected_vehicle_index = int(input("Select a vehicle to move (enter the corresponding number): ")) - 1
            # selected_vehicle = movable_vehicles[selected_vehicle_index]

            new_positions = self.__players[self.__currentPlayer].moveVehicle(selected_vehicle)
            if new_positions is not None:
                selected_vehicle.setPositions(new_positions)
                self.updateMap()
            else:
                print("Invalid move. Try again.")
        elif(self.__players[self.__currentPlayer].playRandomCard() == Card.SHIFT):
            print("2. Shift the board")
            shiftable_boards = self.getShiftableBoard()
            if not shiftable_boards:
                print("No shiftable boards available.")
                return

            print("Shiftable boards:")
            #Just ask a user for a side to shift
            # for i, _ in enumerate(shiftable_boards):
            #     print(f"{i + 1}. Shift board")

            # selected_board_index = int(input("Select a board to shift (enter the corresponding number): ")) - 1
            # selected_board = shiftable_boards[selected_board_index]

            map = selected_board
            self.updateMap()
        elif(self.__players[self.__currentPlayer].playRandomCard() == Card.SLIDE):   
            pass
            #TODO: slide
        elif(self.__players[self.__currentPlayer].playRandomCard() == Card.MOVEANDSHIFT): 
            movable_vehicles = self.getMovableVehicles(self.__players[self.__currentPlayer].getPlayerVehicle())
            if not movable_vehicles:
                print("No movable vehicles available.")
                return

            print("Movable vehicles:")
            # for i, vehicle in enumerate(movable_vehicles):
            #     print(f"{i + 1}. {vehicle.getVehicleChar()}")

            # selected_vehicle_index = int(input("Select a vehicle to move (enter the corresponding number): ")) - 1
            # selected_vehicle = movable_vehicles[selected_vehicle_index]

            new_positions = self.__players[self.__currentPlayer].moveVehicle(selected_vehicle)
            if new_positions is not None:
                selected_vehicle.setPositions(new_positions)
            else:
                print("Invalid move. Try again.")
            
            print("2. Shift the board")
            shiftable_boards = self.getShiftableBoard()
            if not shiftable_boards:
                print("No shiftable boards available.")
                return

            # print("Shiftable boards:")
            # for i, _ in enumerate(shiftable_boards):
            #     print(f"{i + 1}. Shift board")

            # selected_board_index = int(input("Select a board to shift (enter the corresponding number): ")) - 1
            # selected_board = shiftable_boards[selected_board_index]

            map = selected_board
            self.updateMap()
            

        else:
            print("Invalid choice. Try again.")


## WILL WORK ON TONIGHT - SORRY FOR THE DELAY

