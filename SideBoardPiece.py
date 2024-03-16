from BoardPiece import BoardPiece
from Side import Side
from Vehicle import Vehicle
from Orientation import Orientation
from ShiftTo import ShiftTo


class SideBoardPieces(BoardPiece):
    # margin - the number of shifted blocks
    # +margin  - shift up
    # -margin - shift down
    __margin = 0

    def __init__(self, height, width, side):
        super().__init__(height, width)
        self.__side = side

    def getSide(self):
        return self.__side

    def getMargin(self):
        return self.__margin

    def changeVehiclePositionsOnBoard(self, vehicle, numberToShift):
        # If (the Board Side is LEFT and vehicle on it) OR (the Board Side is RIGHT and vehicle on it)
        # Then change coordinates of vehicle
        if (
                (self.__side == Side.RIGHT and (
                        vehicle.getPositions()[0][0] >= 9 and vehicle.getPositions()[0][0] < 14))
                or ((self.__side) == Side.LEFT and (
                vehicle.getPositions[0][0] >= 0 and vehicle.getPositions[0][0] < 5))
        ):
            for coordinates in vehicle.getPositions():
                coordinates[1] += numberToShift


    def isShiftable(self, numberToShift, directionToShift, Vehicles):
        for vehicle in Vehicles:
            # Checks vehicles only in horizontal position
            if vehicle.getOrientation() is Orientation.HORIZONTAL:
                # Checks for LEFT Board Piece
                if self.__side is Side.LEFT:
                    # Checks whether x-coordinates of vehicle crosses the boarder of Board Pieces
                    if (vehicle.getLength() == 2 and
                            (-1 <= (vehicle.getPositions()[0][0] - self._width) <= 0) and
                            (-1 <= (vehicle.getPositions()[1][0] - self._width) <= 0)):
                        print("It's not impossible to shift LEFT Board, because vehicle is on the boarder.")
                        return False

                    if vehicle.getLength() == 3 and (-1 <= (vehicle.getPositions()[1][0] - self._width) <= 0):
                        print("It's not impossible to shift LEFT Board, because vehicle is on the boarder.")
                        return False
                # Checks for right Board Piece
                if self.__side is Side.RIGHT:
                    if (vehicle.getLength() == 2 and
                            (-1 <= (vehicle.getPositions()[0][0] - self._width - 4) <= 0) and
                            (-1 <= (vehicle.getPositions()[1][0] - self._width - 4) <= 0)):
                        print("It's not impossible to shift RIGHT Board, because vehicle is on the boarder.")
                        return False

                    if vehicle.getLength() == 3 and (-1 <= (vehicle.getPositions()[1][0] - self._width - 4) <= 0):
                        print("It's not impossible to shift RIGHT Board, because vehicle is on the boarder.")
                        return False
        # Checks whether the shifting is out of boundaries
        if (directionToShift is ShiftTo.UP) and (self.__margin - numberToShift > -6):
            return True
        if (directionToShift is ShiftTo.DOWN) and (self.__margin + numberToShift < 6):
            return True
        else:
            print("It's not possible to shift this Board, because it's already MAXIMUM shifted.")
            return False

    def shift(self, numberToShift, directionToShift, Vehicles, playersVehicles):
        if self.isShiftable(numberToShift, directionToShift, Vehicles) and self.isShiftable(numberToShift, directionToShift, playersVehicles):
            # If the Side to Shift Board is UP(PLUS)
            # Then find the vehicles on it
            if directionToShift is ShiftTo.UP:
                self.__margin -= numberToShift
                for vehicle in Vehicles:
                    self.changeVehiclePositionsOnBoard(vehicle, -numberToShift)
                for playerVehicle in playersVehicles:
                    self.changeVehiclePositionsOnBoard(playerVehicle, -numberToShift)


            # If the Side to Shift Board is DOWN(MINUS), find the vehicles on it
            if directionToShift is ShiftTo.DOWN:
                self.__margin += numberToShift
                # If (the Board Side is LEFT(PLUS) and vehicle on it) OR (the Board Side is RIGHT(MINUS) and vehicle on it)
                # Then change coordinates of vehicle
                for vehicle in Vehicles:
                    self.changeVehiclePositionsOnBoard(vehicle, numberToShift)
                for playerVehicle in playersVehicles:
                    self.changeVehiclePositionsOnBoard(playerVehicle, numberToShift)