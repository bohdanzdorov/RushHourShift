from BoardPiece import BoardPiece
from Side import Side
class SideBoardPieces(BoardPiece):
    def __init__(self, margin, height, width, side):
        super().__init__(height, width)
        self.__margin = margin
        self.__side = side
    def getMargin(self):
        return self.__margin
    def getSide(self):
        return self.__side
