class Vehicle:
    def __init__(self,id,length,orientation,positions):
        self.__id=id
        self.__length=length
        self.__orientation=orientation
        self.__positions = positions

    def getId(self):
        return self.__id
    def getPositions(self):
        return self.__positions
    def getOrientation(self):
        return self.__orientation

    def getLength(self):
        return self.__length