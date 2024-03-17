from BoardPiece import BoardPiece
from Side import Side
from Vehicle import Vehicle
from Orientation import Orientation
from ShiftTo import ShiftTo
from SideBoardPiece import SideBoardPieces
from Card import Card
from Player import Player

class Agent:
    def __init__(self, playerVehicle, startSide, card):
        self.__playerVehicle = playerVehicle
        self.__startSide = startSide
        self.__card = card:


