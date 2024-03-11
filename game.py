class Game:
    def __init__(self, map, vehicles, players, sidePieces, centralPiece):
        self.__currentPlayer = 0
        self.__map = map
        self.__vehicles = vehicles
        self.__players = players
        self.__sidePieces = sidePieces
        self.__centralPiece = centralPiece

          ## Lummim Works From there 
    
    def getShiftableBoard(self,vehicles,map):
        #it return an array of shiftable boards
        shiftable_boards = []
        for i in range(len(vehicles)):
            if self.checkVehicleMovability(vehicles[i]):
                shifted_board = [row[:] for row in map]
                for position in vehicles[i].getPositions():
                    shifted_board[position[0]][position[1]] = '_'
                shiftable_boards.append(shifted_board)
        return shiftable_boards
    def getMovableVehicles(self,vehicles):
        #it should return an array of all the available vehicles that can be moved.  
        movable_vehicles = []
        for i in range(len(vehicles)):
            if self.checkVehicleMovability(vehicles[i]) and vehicles[i] != vehicle:
                movable_vehicles.append(vehicles[i])
        return movable_vehicles

    def playerTurn(self,currentPlayer,players):
        current_player = players[currentPlayer]
        print(f"Player {currentPlayer + 1}'s turn:")
        print("Available actions:")
        print("1. Move a vehicle")
        print("2. Shift the board")
        choice = int(input("Enter your choice (1 or 2): "))
        
        if choice == 1:
            movable_vehicles = self.getMovableVehicles(current_player.getPlayerVehicle())
            if not movable_vehicles:
                print("No movable vehicles available.")
                return

            print("Movable vehicles:")
            for i, vehicle in enumerate(movable_vehicles):
                print(f"{i + 1}. {vehicle.getVehicleChar()}")

            selected_vehicle_index = int(input("Select a vehicle to move (enter the corresponding number): ")) - 1
            selected_vehicle = movable_vehicles[selected_vehicle_index]

            new_positions = current_player.moveVehicle(selected_vehicle)
            if new_positions is not None:
                selected_vehicle.setPositions(new_positions)
                self.updateMap()
            else:
                print("Invalid move. Try again.")

        elif choice == 2:
            shiftable_boards = self.getShiftableBoard()
            if not shiftable_boards:
                print("No shiftable boards available.")
                return

            print("Shiftable boards:")
            for i, _ in enumerate(shiftable_boards):
                print(f"{i + 1}. Shift board")

            selected_board_index = int(input("Select a board to shift (enter the corresponding number): ")) - 1
            selected_board = shiftable_boards[selected_board_index]

            map = selected_board
            self.updateMap()

        else:
            print("Invalid choice. Try again.")


## WILL WORK ON TONIGHT - SORRY FOR THE DELAY

