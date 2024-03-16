from Orientation import Orientation
import numpy as np

class Vehicle:
    def __init__(self,id,length,orientation,positions):
        self.__id=id
        self.__length=length
        self.__orientation=orientation
        # Orientation represents the placement posture of the vehicle on the chessboard.
        # This value has only two states: "H" or "V"
        self.__positions = positions
    #     Positions store the coordinates of the blocks occupied by the vehicle.

    def setPositions(self, newPositions):
        self.__positions = newPositions
    
    def getId(self):
        return self.__id
    def getPositions(self):
        return self.__positions
    def getOrientation(self):
        return self.__orientation

    def getLength(self):
        return self.__length

    def slide(self, direction, map):
        # Direction means the direction of movement selected for the vehicle.
        # There are only two values, -1 for upwards or 1 for downwards.
        empty_blocks=self.getAvailableEmptyBlocks(map, direction)
        if empty_blocks>0:
            dx= 0
            dy= 0
            if self.__orientation == Orientation.HORIZONTAL:
                dx = direction*empty_blocks
            else:
                dy = direction * empty_blocks
            self.__positions = [(x + dx, y + dy) for x, y in self.__positions]
        else:
            return ("Wrong")

    def move(self,direction,map):
        empty_blocks = self.getAvailableEmptyBlocks(map, direction)
        if empty_blocks>0:
            dx = 0
            dy = 0
            if self.__orientation == Orientation.HORIZONTAL:
                dx = direction
            else:
                dy = direction
            self.__positions = [(x + dx, y + dy) for x, y in self.__positions]
        else:
            return ("Wrong")

    def getAvailableEmptyBlocks(self,map,direction):
        # If the vehicle's orientation is "H",
        # then check the blocks in the row where the vehicle is located
        # and detect the number of empty blocks corresponding to the direction.

        # For example: if you want to move a "H" vehicle to the right,
        # select direction=1,
        # and count the number of empty blocks to the right for the last coordinate (self.__positions[-1]) in the positions of the vehicle in this row.
        # Therefore, input start_y is the y where the vehicle is located, and start_x + 1 is the first blocks to the right of the vehicle.
        if direction==1:
            start_x,start_y=self.__positions[-1]
            if self.__orientation == Orientation.HORIZONTAL:
                empty_blocks = self.count_positive_consecutive_empty_in_row(map, start_y, start_x + 1)
            
            else:
                empty_blocks = self.count_positive_consecutive_empty_in_row(np.array(map).T, start_x, start_y + 1)
        #         Therefore, if we want to move the "V" car up or down,
        #         then we need to count the number of empty blocks up or down in the column where the vehicle is located.
        #         Therefore, we need to transpose the map first, and then calculate it according to the method function for calculating "H".

        else:
            start_x, start_y = self.__positions[0]
            # But if the vehicle's driving direction is "-1", then we need to take the first coordinate of the car's Position,
            # and then calculate the number of empty blocks forward or upward.
            if self.__orientation == Orientation.HORIZONTAL:
                empty_blocks = self.count_negetive_consecutive_empty_in_row(map, start_y, start_x - 1)
            else:
                empty_blocks = self.count_negetive_consecutive_empty_in_row(np.array(map).T, start_x, start_y - 1)
            
        return empty_blocks 

    def count_positive_consecutive_empty_in_row(self, map, row, start_col):
        grid=map
        if row < 0 or row >= len(grid) or start_col < 0 or start_col >= len(grid[0]):
            return 0
        empty_count = 0

        for col in range(start_col, len(grid[row])):
            if grid[row][col] == '_':
                empty_count += 1
            else:
                break

        return empty_count
    def count_negetive_consecutive_empty_in_row(self, map, row, start_col):
        grid = map
        if row < 0 or row >= len(grid) or start_col < 0 or start_col >= len(grid[0]):
            return 0
        empty_count = 0
        for col in range(start_col, -1, -1):

            if grid[row][col] == '_':
                empty_count += 1
            else:
                break
        print(empty_count)
        return empty_count

# map =[
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '_', 'b', 'b', '_'],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
#     ]


# #'_' = road, ' ' = void(carcannot move here), 'A' = car Id
#

# positions =  [[11,8], [12,8]]  #(col,row)
# v = Vehicle('b', 2, Orientation.HORIZONTAL, positions)
# v.move(-1,map)

# print(v.getPositions())