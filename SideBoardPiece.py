from BoardPiece import BoardPiece
from Side import Side
from Vehicle import Vehicle
from Direction import Orientation


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
        return self.__side

    def getMargin(self):
        return self.__margin

    def isShiftable(self, numberToShift, sideToShift, Vehicles):
        for vehicle in Vehicles:
            # Checks vehicles only in horizontal position
            if vehicle.getOrientation() is Orientation.HORIZONTAL:
                # Checks for LEFT Board Piece
                if self.getSide() is Side.PLUS:
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
                if self.getSide() is Side.MINUS:
                    if (vehicle.getLength() == 2 and
                            (-1 <= (vehicle.getPositions()[0][0] - self._width - 4) <= 0) and
                            (-1 <= (vehicle.getPositions()[1][0] - self._width - 4) <= 0)):
                        print("It's not impossible to shift RIGHT Board, because vehicle is on the boarder.")
                        return False

                    if vehicle.getLength() == 3 and (-1 <= (vehicle.getPositions()[1][0] - self._width - 4) <= 0):
                        print("It's not impossible to shift RIGHT Board, because vehicle is on the boarder.")
                        return False

        # Checks whether the shifting is out of boundaries
        if (sideToShift is Side.PLUS) and (self.__margin + numberToShift < 6):
            return True
        if (sideToShift is Side.MINUS) and (self.__margin - numberToShift > -6):
            return True
        else:
            print("It's not impossible to shift this Board, because it's already MAXIMUM shifted.")
            return False

    def shift(self, numberToShift, sideToShift, Vehicles):
        if self.isShiftable(numberToShift, sideToShift, Vehicles):
            # If the Side to Shift Board is UP(PLUS)
            # Then find the vehicles on it
            if sideToShift is Side.PLUS:
                self.__margin += numberToShift
                for vehicle in Vehicles:
                    # If (the Board Side is LEFT(PLUS) and vehicle on it) OR (the Board Side is RIGHT(MINUS) and vehicle on it)
                    # Then change coordinates of vehicle
                    if (
                            (self.getSide() == Side.PLUS and (
                                    vehicle.getPositions()[0][0] >= 0 and vehicle.getPositions()[0][0] < 5))
                            or (self.getSide() == Side.MINUS and (
                            vehicle.getPositions()[0][0] >= 9 and vehicle.getPositions()[0][0] < 14))
                    ):
                        for coordinates in vehicle.getPositions():
                            coordinates[1] -= numberToShift

            # If the Side to Shift Board is DOWN(MINUS), find the vehicles on it
            if sideToShift is Side.MINUS:
                self.__margin += -numberToShift
                # If (the Board Side is LEFT(PLUS) and vehicle on it) OR (the Board Side is RIGHT(MINUS) and vehicle on it)
                # Then change coordinates of vehicle
                for vehicle in Vehicles:
                    if (
                            (self.getSide() == Side.PLUS and (
                                    vehicle.getPositions()[0][0] >= 0 and vehicle.getPositions()[0][0] < 5))
                            or (self.getSide() == Side.MINUS and (
                            vehicle.getPositions()[0][0] >= 9 and vehicle.getPositions()[0][0] < 14))
                    ):
                        for coordinates in vehicle.getPositions():
                            coordinates[1] += numberToShift
