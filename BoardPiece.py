class BoardPiece:
    def __init__(self, height, width):
        self._height = height
        self._width = width

    def getHeight(self):
        return self._height

    def getWidth(self):
        return self._width