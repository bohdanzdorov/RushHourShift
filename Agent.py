import copy

from Action import Action
from Card import Card
from Orientation import Orientation
from Player import Player
from ShiftTo import ShiftTo
from Side import Side
from SideBoardPiece import SideBoardPieces
from State import State
from Vehicle import Vehicle


class Agent:
    def __init__(self, agentVehicle, startSide, card):
        self.__agentVehicle = agentVehicle
        self.__startSide = startSide
        self.__card = card
    def getAgentVehicle(self):
        return self.__agentVehicle

    def zeroDepth(self, card):
        #max, but card is known
        pass
    def oneDepth(self):
        pass
    def twoDepth(self):
        pass
    def result(self, curState, action):
        newState = copy.deepcopy(curState)
        if action.getCardType() == Card.SHIFT:
            if action.getItem() == Side.LEFT:
                newState.getSideBoards()[0].shift(1, action.getDirection(), newState.getVehicles(), [newState.getCurAgentVehicle(), newState.getOpponentVehicle()])
            elif action.getItem() == Side.RIGHT:
                newState.getSideBoards()[1].shift(1, action.getDirection(), newState.getVehicles(), [newState.getCurAgentVehicle(), newState.getOpponentVehicle()])
        elif action.getCardType() == Card.MOVE:
            for i in range(len(newState.getVehicles())):
                if action.getItem() == newState.getVehicles()[i].getId():
                    if newState.getVehicles()[i].getOrientation() == Orientation.VERTICAL:
                        newPositions = copy.deepcopy(newState.getVehicles()[i].getPositions())
                        for j in range(len(newPositions)):
                            newPositions[j][1] += action.getDirection()
                        newState.getVehicles()[i].setPositions(newPositions)
                    elif newState.getVehicles()[i].getOrientation() == Orientation.HORIZONTAL:
                        newPositions = copy.deepcopy(newState.getVehicles()[i].getPositions())
                        for j in range(len(newPositions)):
                            newPositions[j][0] += action.getDirection()
                        newState.getVehicles()[i].setPositions(newPositions)
        elif action.getCardType() == Card.SLIDE:
            for i in range(len(newState.getVehicles())):
                if action.getItem() == newState.getVehicles()[i].getId():
                    if newState.getVehicles()[i].getOrientation() == Orientation.VERTICAL:
                        newPositions = copy.deepcopy(newState.getVehicles()[i].getPositions())
                        for j in range(len(newPositions)):
                            newPositions[j][1] += action.getDirection()
                        newState.getVehicles()[i].setPositions(newPositions)
                    elif newState.getVehicles()[i].getOrientation() == Orientation.HORIZONTAL:
                        newPositions = copy.deepcopy(newState.getVehicles()[i].getPositions())
                        for j in range(len(newPositions)):
                            newPositions[j][0] += action.getDirection()
                        newState.getVehicles()[i].setPositions(newPositions)
        elif action.getCardType() == Card.MOVEANDSHIFT:
            if action.getItem()[0] == Side.LEFT or action.getItem()[0] == Side.RIGHT:
                newState.getSideBoards()[action.getItem()[0].value].shift(1, action.getDirection()[0], newState.getVehicles(), [newState.getCurAgentVehicle(), newState.getOpponentVehicle()])
                newState2 = copy.deepcopy(newState)
                for i in range(len(newState2.getVehicles())):
                    if action.getItem()[1] == newState2.getVehicles()[i].getId():
                        if newState2.getVehicles()[i].getOrientation() == Orientation.VERTICAL:
                            newPositions = list(copy.deepcopy(newState2.getVehicles()[i].getPositions()))
                            updatedPositions = []
                            for coordinates in newPositions:
                                newCoordinates = [coordinates[0], coordinates[1]+ action.getDirection()[1]]
                                updatedPositions.append(newCoordinates)
                            newState2.getVehicles()[i].setPositions(tuple(map(tuple, updatedPositions)))
                        elif newState2.getVehicles()[i].getOrientation() == Orientation.HORIZONTAL:
                            newPositions = list(copy.deepcopy(newState2.getVehicles()[i].getPositions()))
                            updatedPositions = []
                            for coordinates in newPositions:
                                newCoordinates = [coordinates[0]+ action.getDirection()[1], coordinates[1]]
                                updatedPositions.append(newCoordinates)
                            newState2.getVehicles()[i].setPositions(tuple(map(tuple, updatedPositions)))
                return newState2
            else:
                for i in range(len(newState.getVehicles())):
                    if action.getItem()[0] == newState.getVehicles()[i].getId():
                        if newState.getVehicles()[i].getOrientation() == Orientation.VERTICAL:
                            newPositions = list(copy.deepcopy(newState.getVehicles()[i].getPositions()))
                            updatedPositions = []
                            for coordinates in newPositions:
                                newCoordinates = [coordinates[0], coordinates[1] + action.getDirection()[0]]
                                updatedPositions.append(newCoordinates)
                            newState.getVehicles()[i].setPositions(tuple(map(tuple, updatedPositions)))
                        elif newState.getVehicles()[i].getOrientation() == Orientation.HORIZONTAL:
                            newPositions = list(copy.deepcopy(newState.getVehicles()[i].getPositions()))
                            updatedPositions = []
                            for coordinates in newPositions:
                                newCoordinates = [coordinates[0] + action.getDirection()[0], coordinates[1]]
                                updatedPositions.append(newCoordinates)
                            newState.getVehicles()[i].setPositions(tuple(map(tuple, updatedPositions)))
                newState2 = copy.deepcopy(newState)
                newState2.getSideBoards()[action.getItem()[1].value].shift(1, action.getDirection()[1], newState2.getVehicles(), [newState2.getCurAgentVehicle(), newState2.getOpponentVehicle()])
                return newState2
        return newState
    def isSlidable(self, vehicles, checkVehicle, boards):
        slideActions = []

        if checkVehicle.getOrientation() == Orientation.HORIZONTAL:
            leftCount = 0
            rightCount = 0

            buffVehicle = copy.deepcopy(checkVehicle)
            while self.containsAction(Action(Card.MOVE, -1, buffVehicle.getId()), self.isMovable(vehicles, buffVehicle, boards)):
                leftCount += 1
                newPositions = copy.deepcopy(buffVehicle.getPositions())
                for coordinates in newPositions:
                    coordinates[0] -= 1
                buffVehicle.setPositions(newPositions)

            buffVehicle = copy.deepcopy(checkVehicle)
            while self.containsAction(Action(Card.MOVE, 1, buffVehicle.getId()), self.isMovable(vehicles, buffVehicle, boards)):
                rightCount += 1
                newPositions = copy.deepcopy(buffVehicle.getPositions())
                for coordinates in newPositions:
                    coordinates[0] += 1
                buffVehicle.setPositions(newPositions)

            if(leftCount > 0):
                slideActions.append(Action(Card.SLIDE, -1 * leftCount, checkVehicle))
            if (rightCount > 0):
                slideActions.append(Action(Card.SLIDE, rightCount, checkVehicle))
        elif checkVehicle.getOrientation() == Orientation.VERTICAL:
            upCount = 0
            bottomCount = 0
            buffVehicle = copy.deepcopy(checkVehicle)

            while self.containsAction(Action(Card.MOVE, -1, buffVehicle.getId()), self.isMovable(vehicles, buffVehicle, boards)):
                upCount += 1
                newPositions = copy.deepcopy(buffVehicle.getPositions())
                for coordinates in newPositions:
                    coordinates[1] -= 1
                buffVehicle.setPositions(newPositions)

            print(checkVehicle.getPositions())
            buffVehicle = copy.deepcopy(checkVehicle)
            while self.containsAction(Action(Card.MOVE, 1, buffVehicle.getId()), self.isMovable(vehicles, buffVehicle, boards)):
                bottomCount += 1
                newPositions = copy.deepcopy(buffVehicle.getPositions())
                for coordinates in newPositions:
                    coordinates[1] += 1
                buffVehicle.setPositions(newPositions)

            if (upCount > 0):
                slideActions.append(Action(Card.SLIDE, -1 * upCount, checkVehicle))
            if (bottomCount > 0):
                slideActions.append(Action(Card.SLIDE, bottomCount, checkVehicle))

        return slideActions
    def containsAction(self, actionToCheck, actions):
        for action in actions:
            if actionToCheck.getItem() == action.getItem() and actionToCheck.getDirection() == action.getDirection():
                return True
        return False
    def isMovable(self, vehicles, checkVehicle, boards):
        alignLine = 5
        resultAction = []

        if(checkVehicle.getOrientation() == Orientation.HORIZONTAL):
            isBlockedLeft = False
            isBlockedRight = False
            #check map boundaries
            for position in checkVehicle.getPositions():
                if position[0] == 0:
                    isBlockedLeft = True
                if position[0] == 13:
                    isBlockedRight = True
            #check for road left/right
            #check for road if vehicle is on the Left Board
            for position in checkVehicle.getPositions():
                if position[0] == 4 and (position[1] < 5 or position[1] > 10):
                    isBlockedRight = True
                elif position[0] == 9 and (position[1] < 5 or position[1] > 10):
                    isBlockedLeft = True
                elif position[0] == 5 and (position[1] < alignLine+boards[0].getMargin() or position[1] > alignLine+boards[0].getMargin()+boards[0].getHeight()):
                    isBlockedLeft = True
                elif position[0] == 8 and (position[1] < alignLine+boards[1].getMargin() or position[1] > alignLine+boards[1].getMargin()+boards[1].getHeight()):
                    isBlockedRight = True
            #check for vehicles on left and right side
            for position in checkVehicle.getPositions():
                for vehicle in vehicles:
                    for vehiclePosition in vehicle.getPositions():
                        if position[0]+1 == vehiclePosition[0] and position[1] == vehiclePosition[1] and vehicle.getId() != checkVehicle.getId():
                            isBlockedRight = True
                        if position[0]-1 == vehiclePosition[0] and position[1] == vehiclePosition[1] and vehicle.getId() != checkVehicle.getId():
                            isBlockedLeft = True
            if not isBlockedLeft:
                resultAction.append(Action(Card.MOVE, -1, checkVehicle.getId()))
            if not isBlockedRight:
                resultAction.append(Action(Card.MOVE, 1, checkVehicle.getId()))

        if checkVehicle.getOrientation() == Orientation.VERTICAL:
            isBlockedUp = False
            isBlockedBottom = False
            # check map boundaries
            for position in checkVehicle.getPositions():
                if position[1] == 0:
                    isBlockedUp = True
                if position[1] == 13:
                    isBlockedBottom = True
            #check for road up and bottom
            for position in checkVehicle.getPositions():
                if position[0] < 5 and position[1] == alignLine+boards[0].getMargin():
                    isBlockedUp = True
                elif position[0] < 5 and position[1] == alignLine+boards[0].getMargin()+boards[0].getHeight()-1:
                    isBlockedBottom = True
                elif 4 < position[0] < 9 and position[1] == alignLine:
                    isBlockedUp = True
                elif 4 < position[0] < 9 and position[1] == alignLine+boards[0].getHeight()-1:
                    isBlockedBottom = True
                elif position[0] > 8 and position[1] == alignLine + boards[1].getMargin():
                    isBlockedUp = True
                elif position[0] > 8 and position[1] == alignLine + boards[1].getMargin() + boards[1].getHeight()-1:
                    isBlockedBottom = True
            # check for vehicles up and bottom
            for position in checkVehicle.getPositions():
                for vehicle in vehicles:
                    for vehiclePosition in vehicle.getPositions():
                        if position[1]+1 == vehiclePosition[1] and position[0] == vehiclePosition[0] and vehicle.getId() != checkVehicle.getId():
                            isBlockedBottom = True
                        if position[1]-1 == vehiclePosition[1] and position[0] == vehiclePosition[0] and vehicle.getId() != checkVehicle.getId():
                            isBlockedUp = True
            if not isBlockedBottom:
                resultAction.append(Action(Card.MOVE, 1, checkVehicle.getId()))
            if not isBlockedUp:
                resultAction.append(Action(Card.MOVE, -1, checkVehicle.getId()))

        return resultAction
    def isShiftable(self, Vehicles, board):
        numberToShift = 1
        for vehicle in Vehicles:
            # Checks vehicles only in horizontal position
            if vehicle.getOrientation() is Orientation.HORIZONTAL:
                # Checks for LEFT Board Piece
                if board.getSide() is Side.LEFT:
                    # Checks whether x-coordinates of vehicle crosses the boarder of Board Pieces
                    if (vehicle.getLength() == 2 and
                            (-1 <= (vehicle.getPositions()[0][0] - board.getWidth()) <= 0) and
                            (-1 <= (vehicle.getPositions()[1][0] - board.getWidth()) <= 0)):
                        return []
                    if vehicle.getLength() == 3 and (-1 <= (vehicle.getPositions()[1][0] - board.getWidth()) <= 0):
                        return []
                # Checks for right Board Piece
                if board.getSide() is Side.RIGHT:
                    if (vehicle.getLength() == 2 and
                            (-1 <= (vehicle.getPositions()[0][0] - board.getWidth() - 4) <= 0) and
                            (-1 <= (vehicle.getPositions()[1][0] - board.getWidth() - 4) <= 0)):
                        return []
                    if vehicle.getLength() == 3 and (-1 <= (vehicle.getPositions()[1][0] - board.getWidth() - 4) <= 0):
                        return []

        # Checks whether the shifting is out of boundaries
        if (board.getMargin() - numberToShift > -6) and (board.getMargin() + numberToShift < 6):
            return [Action(Card.SHIFT, ShiftTo.UP, board.getSide()), Action(Card.SHIFT, ShiftTo.DOWN, board.getSide())]
        elif board.getMargin() - numberToShift > -6:
            return [Action(Card.SHIFT, ShiftTo.UP, board.getSide())]
        elif board.getMargin() + numberToShift < 6:
            return [Action(Card.SHIFT, ShiftTo.DOWN, board.getSide())]
        else:
            return []
    def evaluateState(self, state):
        curAgentPositions = state.getCurAgentVehicle().getPositions()
        opponentPositions = state.getOpponentVehicle().getPositions()
        vehicles = state.getVehicles()
        sideBoards = state.getSideBoards()
        print(self.heuristicFunction(curAgentPositions, opponentPositions, vehicles, sideBoards))
        return self.progressFunction(curAgentPositions) - self.heuristicFunction(curAgentPositions, opponentPositions, vehicles, sideBoards)
    def progressFunction(self, curAgentPositions):
        return self.__agentVehicle.getPositions()[0][0] - curAgentPositions[0][0]
    def heuristicFunction(self, curAgentPositions, opponentPosition, vehicles, sideBoards):
        alignLine = 5
        penaltyPoints = 0
        if curAgentPositions[0][0] < 5 and curAgentPositions[1][0] < 5:
            penaltyPoints = self.givePenaltyForVehicles(vehicles, opponentPosition, curAgentPositions[0][1], 0, curAgentPositions[0][0])
        elif curAgentPositions[0][0] < 9 and curAgentPositions[1][0] < 9:
             yStartOfLeftBoard = alignLine + sideBoards[0].getMargin()
             yEndOfLeftBoard = alignLine + sideBoards[0].getMargin()+sideBoards[0].getHeight()
             if curAgentPositions[0][1] >= yStartOfLeftBoard and curAgentPositions[0][1] <= yEndOfLeftBoard:
                penaltyPoints = self.givePenaltyForVehicles(vehicles, opponentPosition, curAgentPositions[0][1], 0, curAgentPositions[0][0])
             else:
                penaltyPoints = self.givePenaltyForVehicles(vehicles, opponentPosition, curAgentPositions[0][1], 5, curAgentPositions[0][0])
                penaltyPoints += self.givePenaltyForBoards(curAgentPositions[0][1], yStartOfLeftBoard, yEndOfLeftBoard)
        else:
            yStartOfLeftBoard = alignLine + sideBoards[0].getMargin()
            yEndOfLeftBoard = alignLine + sideBoards[0].getMargin() + sideBoards[0].getHeight()
            yStartOfCentralBoard = alignLine
            yEndOfCentralBoard = alignLine+6
            if(curAgentPositions[0][1] >= yStartOfCentralBoard and curAgentPositions[0][1] <= yEndOfCentralBoard):
                if(curAgentPositions[0][1] >= yStartOfLeftBoard and curAgentPositions[0][1] <= yEndOfLeftBoard):
                    penaltyPoints = self.givePenaltyForVehicles(vehicles, opponentPosition, curAgentPositions[0][1], 0, curAgentPositions[0][0])
                else:
                    penaltyPoints = self.givePenaltyForVehicles(vehicles, opponentPosition, curAgentPositions[0][1], 5, curAgentPositions[0][0])
            else:
                penaltyPoints = self.givePenaltyForVehicles(vehicles, opponentPosition, curAgentPositions[0][1], 9, curAgentPositions[0][0])
                penaltyPoints += self.givePenaltyForBoards(curAgentPositions[0][1], yStartOfCentralBoard, yEndOfCentralBoard)

        return penaltyPoints
    def givePenaltyForVehicles(self, vehicles, opponentPositions, yToCheck, startXToCheck, endXToCheck):
        penaltyPoints = 0
        for vehicle in vehicles:
            for i in range(len(vehicle.getPositions())):
                if vehicle.getPositions()[i][1] == yToCheck and startXToCheck <= vehicle.getPositions()[i][0] <= endXToCheck:
                    penaltyPoints += 1.5
        for i in range(len(opponentPositions)):
            if opponentPositions[i][1] == yToCheck and startXToCheck <= opponentPositions[i][0] <= endXToCheck:
                penaltyPoints += 1.5
        return penaltyPoints
    def givePenaltyForBoards(self, agentY, startBoardY, endBoardY):
        penaltyPoints = 0
        if agentY < startBoardY:
            penaltyPoints = (startBoardY - agentY)*2
        elif agentY > endBoardY:
            penaltyPoints = (agentY - endBoardY)*2
        return penaltyPoints

player1 = Player(Vehicle('1', 2, Orientation.HORIZONTAL, [[0,8], [1,8]]), Side.LEFT, None)
vehicles = [ Vehicle('B', 2, Orientation.VERTICAL, [[3,5], [3,6]]), Vehicle('A', 2, Orientation.HORIZONTAL, [[1, 6], [2, 6]])]
sidePieces = [SideBoardPieces(6, 5, Side.LEFT), SideBoardPieces(6, 5, Side.RIGHT)]

agentVehicle = Vehicle('2', 2, Orientation.HORIZONTAL, [[12,8], [13,8]])
agent = Agent(agentVehicle, Side.RIGHT, None)

currentState = State(agentVehicle, player1.getPlayerVehicle(), vehicles, sidePieces)
action = Action(Card.SLIDE, 1, 'B')
newState = agent.result(currentState, action)
print(newState.getVehicles()[0].getPositions())

# print(newState.getVehicles()[0].getPositions(), newState.getVehicles()[1].getPositions())