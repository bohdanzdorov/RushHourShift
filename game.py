class Game:
    def __init__(self, map,vehicle,currentPlayer,players,sidePieces,centralPiece):
        pass

          ## Lummim Works From there 
    
    def getShiftableBoard(self):
        #it return an array of shiftable boards
        shiftable_boards = []
        for i in range(len(self.__vehicles)):
            if self.checkVehicleMovability(self.__vehicles[i]):
                shifted_board = [row[:] for row in self.__map]
                for position in self.__vehicles[i].getPositions():
                    shifted_board[position[0]][position[1]] = '_'
                shiftable_boards.append(shifted_board)
        return shiftable_boards
    def getMovableVehicles(self,vehicle):
        #it should return an array of all the available vehicles that can be moved.  
        movable_vehicles = []
        for i in range(len(self.__vehicles)):
            if self.checkVehicleMovability(self.__vehicles[i]) and self.__vehicles[i] != vehicle:
                movable_vehicles.append(self.__vehicles[i])
        return movable_vehicles

    def playerTurn(self):
        current_player = self.__players[self.__currentPlayer]
        print(f"Player {self.__currentPlayer + 1}'s turn:")
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

            self.__map = selected_board
            self.updateMap()

        else:
            print("Invalid choice. Try again.")


## WILL WORK ON TONIGHT - SORRY FOR THE DELAY

