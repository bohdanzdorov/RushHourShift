class Vehicle:
    def __int__(self,id,length,orientation,positions):
        self.__id=id
        self.__length=length
        self.__orientation=orientation
        self.__positions = positions
    def getId(self):
        return self.__id
    def getPositions(self):
        return self.__positions

    def slide(self, map, direction=1):
        empty_blocks=self.getAvailableEmptyBlocks(map, direction)
        if empty_blocks>0:
            dx= 0
            dy= 0
            if self.__orientation == "H":
                dx = direction*empty_blocks
            else:
                dy = direction * empty_blocks
            self.__positions = [(x + dx, y + dy) for x, y in self.__positions]
        else:
            return ("Wrong")

    def move(self,direction=1):
        empty_blocks = self.getAvailableEmptyBlocks(map, direction)
        if empty_blocks>0:
            dx = 0
            dy = 0
            if self.__orientation == "H":
                dx = direction
            else:
                dy = direction
            self.__positions = [(x + dx, y + dy) for x, y in self.__positions]
        else:
            return ("Wrong")

    def getAvailableEmptyBlocks(self,map,direction=1):
        if direction==1:
            start_x,start_y=self.__positions[-1]
            if self.orientation == "H":
                empty_blocks = count_positive_consecutive_empty_in_row(map, start_y, start_x + 1)
            else:
                empty_blocks = count_positive_consecutive_empty_in_row(map.T, start_x, start_y + 1)
        else:
            start_x, start_y = self.position[0]
            if self.orientation == "H":
                empty_blocks = count_negetive_consecutive_empty_in_row(map, start_y, start_x + 1)
            else:
                empty_blocks = count_negetive_consecutive_empty_in_row(map.T, start_x, start_y + 1)

        return empty_blocks

    def count_positive_consecutive_empty_in_row(map, row, start_col):
        if row < 0 or row >= len(grid) or start_col < 0 or start_col >= len(grid[0]):
            return 0
        empty_count = 0
        for col in range(start_col, len(grid[row])):
            if grid[row][col] is None:
                empty_count += 1
            else:
                break

        return empty_count
    def count_negetive_consecutive_empty_in_row(map, row, start_col):
        if row < 0 or row >= len(grid) or start_col < 0 or start_col >= len(grid[0]):
            return 0
        empty_count = 0
        for col in range(start_col, -1, -1):
            if grid[row][col] is None:
                empty_count += 1
            else:
                break

        return empty_count






