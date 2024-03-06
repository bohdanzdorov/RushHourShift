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

          
