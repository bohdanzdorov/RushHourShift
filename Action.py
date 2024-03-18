class Action:
    def __init__(self, cardType, direction, item):
        self.__cardType = cardType
        self.__direction = direction
        self.__item = item
    def getCardType(self):
        return self.__cardType
    def getDirection(self):
        return self.__direction
    def getItem(self):
        return self.__item