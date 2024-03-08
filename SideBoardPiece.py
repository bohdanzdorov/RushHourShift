from BoardPiece import BoardPiece
from Side import Side
from Vehicle import Vehicle
from Direction import Direction
class SideBoardPieces(BoardPiece):
    # margin - the number of shifted blocks
    # +margin  - shift up
    # -margin - shift down
    __margin = 0
    def __init__(self, height, width, side):
        super().__init__(height, width)
        self.__side = side
    def getSide(self):
        # self.__side = Side.PLUS => side - left
        # self.__side = Side.MINUS => side - right
        if self.__side == 0 or self.__side == Side.PLUS:
            return Side.PLUS
        if self.__side == 1 or self.__side == Side.MINUS:
            return Side.MINUS
    def getMargin(self):
        return self.__margin

    def isShiftable(self, numberToShift, sideToShift, Vehicles):
        for vehicle in Vehicles:
            #Checks vehicles only in horizontal possition
            if vehicle.getDirection() == Direction.HORIZONTAL:
                #Checks for left Board Piece
                if (self.getSide() == Side.PLUS):
                    #Checks whether x-coordinates of vehicle crosses the boarder of Board Pieces
                    if vehicle.getLength() == 2 and abs((vehicle.getPositions()[0][0] - self._width) and (vehicle.getPositions()[1][0] - self._width)) <= 1:
                        print("It's not impossible to shift this Board, because vehicle is on the boarder.")
                        return False
                    if vehicle.getLength() == 3 and abs(vehicle.getPositions()[2][0] - self._width) <= 1:
                        print("It's not impossible to shift this Board, because vehicle is on the boarder.")
                        return False
                #Checks for right Board Piece
                if (self.getSide() == Side.MINUS):
                    if vehicle.getLength() == 2 and abs((vehicle.getPositions()[0][0] - self._width - 4) and (vehicle.getPositions()[1][0] - self._width - 4)) <= 1:
                        print("It's not impossible to shift this Board, because vehicle is on the boarder.")
                        return False
                    if vehicle.getLength() == 3 and abs(vehicle.getPositions()[2][0] - self._width - 4) <= 1:
                        print("It's not impossible to shift this Board, because vehicle is on the boarder.")
                        return False

        #Checks whether the shifting is out of boundaries
        if (sideToShift == Side.PLUS.name or sideToShift == Side.PLUS.value) and (self.__margin + numberToShift < 6):
            return True
        if (sideToShift == Side.MINUS.name or sideToShift == Side.MINUS.value) and (self.__margin - numberToShift > -6):
            return True
        else:
            print("It's not impossible to shift this Board, because it's already MAXIMUM shifted.")
            return False



    def shift (self, numberToShift, sideToShift, Vehicles):
        if self.isShiftable(numberToShift, sideToShift, Vehicles):
            #If the Side to Shift Board is UP(PLUS)
            #Then find the vehicles on it
            if sideToShift == Side.PLUS.name or sideToShift == Side.PLUS.value:
                self.__margin += numberToShift
                for vehicle in Vehicles:
                    #If (the Board Side is LEFT(PLUS) and vehicle on it) OR (the Board Side is RIGHT(MINUS) and vehicle on it)
                    #Then change coordinates of vehicle
                    if(
                        (self.getSide() == Side.PLUS and (vehicle.getPositions()[0][0] >= 0 and vehicle.getPositions()[0][0] < 5))
                        or (self.getSide() == Side.MINUS and (vehicle.getPositions()[0][0] >= 9 and vehicle.getPositions()[0][0] < 14))
                    ):
                        for coordinates in vehicle.getPositions():
                            coordinates[1] -= numberToShift



            # If the Side to Shift Board is DOWN(MINUS), find the vehicles on it
            if sideToShift == Side.MINUS.name or sideToShift == Side.MINUS.value:
                self.__margin += -numberToShift
                # If (the Board Side is LEFT(PLUS) and vehicle on it) OR (the Board Side is RIGHT(MINUS) and vehicle on it)
                # Then change coordinates of vehicle
                for vehicle in Vehicles:
                    if (
                        (self.getSide() == Side.PLUS and (vehicle.getPositions()[0][0] >= 0 and vehicle.getPositions()[0][0] < 5))
                        or (self.getSide() == Side.MINUS and (vehicle.getPositions()[0][0] >= 9 and vehicle.getPositions()[0][0] < 14))
                    ):
                        for coordinates in vehicle.getPositions():
                            coordinates[1] += numberToShift






