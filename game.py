class Game:
    def __init__(self, map, vehicles, players, sidePieces, centralPiece):
        self.__currentPlayer = 0
        self.__map = map
        self.__vehicles = vehicles
        self.__players = players
        self.__sidePieces = sidePieces
        self.__centralPiece = centralPiece

    def updateMap(self):
        for y in range(len(self.__map)):
            for x in range(len(self.__map[0])):
                checkForVehicle = self.checkVehicleOnCoords(x, y)
                if(checkForVehicle):
                    self.__map[x][y] = checkForVehicle
                    break
                elif(self.checkBoardOnCoords(x, y)):
                    self.__map[x][y] = '_'
                else:
                    self.__map[x][y] = ' '
                                    
    
    def checkBoardOnCoords(self, xToCheck, yToCheck):
        alignLine = 5
        if(xToCheck < 5):
            if(alignLine + self.__sidePieces[0].getMargin() > yToCheck or alignLine - self.__sidePieces[0].getMargin() < yToCheck):
                return True
        if(xToCheck < 9):
            if(yToCheck < 5 or yToCheck > 10):
                return True
        else:
            if(alignLine + self.__sidePieces[1].getMargin() > yToCheck or alignLine - self.__sidePieces[1].getMargin() < yToCheck):
                return True
        return False    

    def checkVehicleOnCoords(self, xToCheck, yToCheck):
        #going through regular vehicles
        for i in range(len(self.__vehicles)):
            curVehiclePositions = self.__vehicles[i].getPositions()
            for j in range(len(curVehiclePositions)): #Go throught all the coordinates of a vehicle
                if(curVehiclePositions[j, 0] == xToCheck and curVehiclePositions[j, 1] == yToCheck):
                    return self.__vehicles[i].getVehicleChar()
                
        #going throught players' vehicles
        for i in range(len(self.__players)):
            curPositions = self.__players[i].getPlayerVehicle().getPositions()
            for j in range(len(curPositions)):
                if(curPositions[j, 0] == xToCheck and curPositions[j, 1] == yToCheck):
                    return self.__players[i].getPlayerVehicle().getVehicleChar()
        return None       

    def changePlayers(self):
         self.__currentPlayer = 1 if self.__currentPlayer == 0 else 0      

    def checkVehicleMovability(self, vehicle):
        vehiclePositions = vehicle.getPositions()

        if(vehicle.getDirection == 'Vertical'):
            isBlockedUp = False
            isBlockedDown = False
            for i in range(vehicle.getLength()):
                #Check upper block
                if(vehiclePositions[i][1]-1 < 0 or # vehicle out of upper world bounds
                   (map[vehiclePositions[i][0]][vehiclePositions[i][1]-1] != '_' and # upper block is ' ' or 'vehicle_char'
                    map[vehiclePositions[i][0]][vehiclePositions[i][1]-1] != vehicle.getVehicleChar()) # upper block is ' ' or 'OTHER_vehicle_char'
                ):
                    isBlockedUp = True
                #Check bottom block
                if(vehiclePositions[i][1]+1 > len(map)-1 or # vehicle out of bottom world bounds
                   (map[vehiclePositions[i][0]][vehiclePositions[i][1]+1] != '_' and # bottom block is ' ' or 'vehicle_char'
                    map[vehiclePositions[i][0]][vehiclePositions[i][1]+1] != vehicle.getVehicleChar()) # bottom block is ' ' or 'OTHER_vehicle_char'
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
                   (map[vehiclePositions[i][0]-1][vehiclePositions[i][1]] != '_' and # left block is 'vehicle_char'
                    map[vehiclePositions[i][0]-1][vehiclePositions[i][1]] != vehiclePositions.getVehicleChar()) # left block is 'OTHER_vehicle_char'
                ):
                    isBlockedLeft = True
                     
                if(vehiclePositions[i][0]+1 > len(map[0])-1 or # vehicle at the right side world bounds
                   (map[vehiclePositions[i][0]+1][vehiclePositions[i][1]] != '_' and # right block is 'vehicle_char'
                    map[vehiclePositions[i][0]+1][vehiclePositions[i][1]] != vehiclePositions.getVehicleChar()) # right block is 'OTHER_vehicle_char'
                ):
                    isBlockedLeft = True
            if(isBlockedLeft and isBlockedRight):
                return False 
            return True  

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

