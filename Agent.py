import copy
import random
import sys

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
        self.__probabilityMove = 0.4
        self.__probabilityShift = 0.2
        self.__probabilitySlide = 0.2
        self.__probabilityMoveAndShift = 0.2
        self.__maxDepth = 2 

    def getPlayerVehicle(self):
        return self.__agentVehicle

    def zeroDepth(self, curState):
        possibleActions = self.getPossibleActions(curState, 1)
        bestActionValue = -sys.maxsize
        bestAction = None
        for possibleAction in possibleActions:
            if(possibleAction.getCardType() == self.__card):
                newState = self.result(curState, 1, possibleAction)
                evaluationOfState = self.minLayer(newState, 1, 1)
                if (evaluationOfState > bestActionValue):
                    bestActionValue = evaluationOfState
                    bestAction = possibleAction
        return bestAction


    def minLayer(self, curState, curPlayer, depth):
        minMove = sys.maxsize
        minSlide = sys.maxsize
        minShift = sys.maxsize
        minMoveAndShift = sys.maxsize

        possibleActions = self.getPossibleActions(curState, curPlayer)
        for possibleAction in possibleActions:
            newState = self.result(curState, curPlayer, possibleAction)
            evaluationOfState = self.maxLayer(newState, 1, depth+1)
            if (possibleAction.getCardType() == Card.MOVE and evaluationOfState < minMove):
                minMove = evaluationOfState
            if (possibleAction.getCardType() == Card.SHIFT and evaluationOfState < minShift):
                minShift = evaluationOfState
            if (possibleAction.getCardType() == Card.SLIDE and evaluationOfState < minSlide):
                minSlide = evaluationOfState
            if (possibleAction.getCardType() == Card.MOVEANDSHIFT and evaluationOfState < minMoveAndShift):
                minMoveAndShift = evaluationOfState
        
        return minMove*self.__probabilityMove + minShift*self.__probabilityShift + minSlide*self.__probabilitySlide + minMoveAndShift*self.__probabilityMoveAndShift
        
    def maxLayer(self, curState, curPlayer, depth):
        possibleActions = self.getPossibleActions(curState, curPlayer)
        maxMove = -sys.maxsize
        maxSlide = -sys.maxsize
        maxShift = -sys.maxsize
        maxMoveAndShift = -sys.maxsize

        if(depth < self.__maxDepth):
            for possibleAction in possibleActions:
                newState = self.result(curState, curPlayer, possibleAction)
                evaluationOfState = self.minLayer(newState, 0, depth+1)
                if (possibleAction.getCardType() == Card.MOVE and evaluationOfState > maxMove):
                    maxMove = evaluationOfState
                if (possibleAction.getCardType() == Card.SHIFT and evaluationOfState > maxShift):
                    maxShift = evaluationOfState
                if (possibleAction.getCardType() == Card.SLIDE and evaluationOfState > maxSlide):
                    maxSlide = evaluationOfState
                if (possibleAction.getCardType() == Card.MOVEANDSHIFT and evaluationOfState > maxMoveAndShift):
                    maxMoveAndShift = evaluationOfState
            
            return round(maxMove*self.__probabilityMove + maxShift*self.__probabilityShift + maxSlide*self.__probabilitySlide + maxMoveAndShift*self.__probabilityMoveAndShift, 5)  
        
        else:
            for possibleAction in possibleActions:
                newState = self.result(curState, curPlayer, possibleAction)
                evaluationOfState = self.evaluateState(newState)
                if (possibleAction.getCardType() == Card.MOVE and evaluationOfState > maxMove):
                    maxMove = evaluationOfState
                if (possibleAction.getCardType() == Card.SHIFT and evaluationOfState > maxShift):
                    maxShift = evaluationOfState
                if (possibleAction.getCardType() == Card.SLIDE and evaluationOfState > maxSlide):
                    maxSlide = evaluationOfState
                if (possibleAction.getCardType() == Card.MOVEANDSHIFT and evaluationOfState > maxMoveAndShift):
                    maxMoveAndShift = evaluationOfState
            
            return round(maxMove*self.__probabilityMove + maxShift*self.__probabilityShift + maxSlide*self.__probabilitySlide + maxMoveAndShift*self.__probabilityMoveAndShift, 5)  

    def getPossibleActions(self, curState, curPlayer):
        possibleActions = []
        operatableVehicles = copy.deepcopy(curState.getVehicles())
        operatableVehicles.append(curState.getCurAgentVehicle())
        operatableVehicles.append(curState.getOpponentVehicle())
        for vehicle in operatableVehicles:
            if(curPlayer == 1 and vehicle.getId() != '1'):
                movesForVehicle = self.isMovable(operatableVehicles, vehicle, curState.getSideBoards())
                for moves in movesForVehicle:
                    possibleActions.append(moves)
                slidesForVehicle = self.isSlidable(operatableVehicles, vehicle, curState.getSideBoards())
                for slides in slidesForVehicle:
                    possibleActions.append(slides)
            elif(curPlayer == 0 and vehicle.getId() != '2'):
                movesForVehicle = self.isMovable(operatableVehicles, vehicle, curState.getSideBoards())
                for moves in movesForVehicle:
                    possibleActions.append(moves)
                slidesForVehicle = self.isSlidable(operatableVehicles, vehicle, curState.getSideBoards())
                for slides in slidesForVehicle:
                    possibleActions.append(slides)
        for board in curState.getSideBoards():
            boardActions = self.isShiftable(operatableVehicles, board)
            for boardAction in boardActions:
                possibleActions.append(boardAction)
        for action in possibleActions:
            if(action.getCardType() == Card.MOVE):
                newState = self.result(curState, curPlayer, action)  
                newOperatableVehicles = copy.deepcopy(newState.getVehicles())
                newOperatableVehicles.append(newState.getCurAgentVehicle())
                newOperatableVehicles.append(newState.getOpponentVehicle())         
                for board in newState.getSideBoards():
                    boardActions = self.isShiftable(newOperatableVehicles, board)
                    for boardAction in boardActions:
                        possibleActions.append(Action(Card.MOVEANDSHIFT, [action.getDirection(), boardAction.getDirection()], [action.getItem(), boardAction.getItem()]))
            if(action.getCardType() == Card.SHIFT):
                newState = self.result(curState, curPlayer, action)
                newOperatableVehicles = copy.deepcopy(newState.getVehicles())
                newOperatableVehicles.append(newState.getCurAgentVehicle())
                newOperatableVehicles.append(newState.getOpponentVehicle())
                for vehicle in newOperatableVehicles:
                    if(curPlayer == 1 and vehicle.getId() != '1'):
                        vehicleActions = self.isMovable(newOperatableVehicles, vehicle, newState.getSideBoards())
                        for vehicleAction in vehicleActions:
                            possibleActions.append(Action(Card.MOVEANDSHIFT, [action.getDirection(), vehicleAction.getDirection()], [action.getItem(), vehicleAction.getItem()]))
                    elif(curPlayer == 0 and vehicle.getId() != '2'):
                        vehicleActions = self.isMovable(newOperatableVehicles, vehicle, newState.getSideBoards())
                        for vehicleAction in vehicleActions:
                            possibleActions.append(Action(Card.MOVEANDSHIFT, [action.getDirection(), vehicleAction.getDirection()], [action.getItem(), vehicleAction.getItem()]))
        return possibleActions
    def result(self, curState, curPlayer, action):
        newState = copy.deepcopy(curState)
        if action.getCardType() == Card.SHIFT:
            if action.getItem() == Side.LEFT:
                newState.getSideBoards()[0].shift(1, action.getDirection(), newState.getVehicles(), [newState.getCurAgentVehicle(), newState.getOpponentVehicle()])
            elif action.getItem() == Side.RIGHT:
                newState.getSideBoards()[1].shift(1, action.getDirection(), newState.getVehicles(), [newState.getCurAgentVehicle(), newState.getOpponentVehicle()])
        elif action.getCardType() == Card.MOVE or action.getCardType() == Card.SLIDE:
            for i in range(len(newState.getVehicles())):
                if action.getItem() == newState.getVehicles()[i].getId():
                    if newState.getVehicles()[i].getOrientation() == Orientation.VERTICAL:
                        newPositions = copy.deepcopy(newState.getVehicles()[i].getPositions())
                        updatedPositions = []
                        for coordinates in newPositions:
                            newCoordinates = [coordinates[0], coordinates[1]+ action.getDirection()]
                            updatedPositions.append(newCoordinates)
                        newState.getVehicles()[i].setPositions(tuple(map(tuple, updatedPositions)))


                    elif newState.getVehicles()[i].getOrientation() == Orientation.HORIZONTAL:
                        newPositions = copy.deepcopy(newState.getVehicles()[i].getPositions())
                        updatedPositions = []
                        for coordinates in newPositions:
                            newCoordinates = [coordinates[0]+action.getDirection(), coordinates[1]]
                            updatedPositions.append(newCoordinates)
                        newState.getVehicles()[i].setPositions(tuple(map(tuple, updatedPositions)))
            if(action.getItem() == '1' and curPlayer == 0):
                newPositions = copy.deepcopy(newState.getOpponentVehicle().getPositions())
                updatedPositions = []
                for coordinates in newPositions:
                    newCoordinates = [coordinates[0]+action.getDirection(), coordinates[1]]
                    updatedPositions.append(newCoordinates)
                newState.getOpponentVehicle().setPositions(tuple(map(tuple, updatedPositions)))
            if(action.getItem() == '2' and curPlayer == 1):
                newPositions = copy.deepcopy(newState.getCurAgentVehicle().getPositions())
                updatedPositions = []
                for coordinates in newPositions:
                    newCoordinates = [coordinates[0]+action.getDirection(), coordinates[1]]
                    updatedPositions.append(newCoordinates)
                newState.getCurAgentVehicle().setPositions(tuple(map(tuple, updatedPositions)))
       
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

                if(action.getItem()[1] == '1' and curPlayer == 0):
                    newPositions = list(copy.deepcopy(newState2.getOpponentVehicle().getPositions()))
                    updatedPositions = []
                    for coordinates in newPositions:
                        newCoordinates = [coordinates[0]+ action.getDirection()[1], coordinates[1]]
                        updatedPositions.append(newCoordinates)
                    newState2.getOpponentVehicle().setPositions(tuple(map(tuple, updatedPositions)))

                if(action.getItem()[1] == '2' and curPlayer == 1):
                    newPositions = list(copy.deepcopy(newState2.getCurAgentVehicle().getPositions()))
                    updatedPositions = []
                    for coordinates in newPositions:
                        newCoordinates = [coordinates[0]+ action.getDirection()[1], coordinates[1]]
                        updatedPositions.append(newCoordinates)
                    newState2.getCurAgentVehicle().setPositions(tuple(map(tuple, updatedPositions)))
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
                if(action.getItem()[0] == '1' and curPlayer == 0):
                    newPositions = list(copy.deepcopy(newState.getOpponentVehicle().getPositions()))
                    updatedPositions = []
                    for coordinates in newPositions:
                        newCoordinates = [coordinates[0]+action.getDirection()[0], coordinates[1]]
                        updatedPositions.append(newCoordinates)
                    newState.getOpponentVehicle().setPositions(tuple(map(tuple, updatedPositions)))
                if(action.getItem()[0] == '2' and curPlayer == 1):
                    newPositions = list(copy.deepcopy(newState.getCurAgentVehicle().getPositions()))
                    updatedPositions = []
                    for coordinates in newPositions:
                        newCoordinates = [coordinates[0]+ action.getDirection()[0], coordinates[1]]
                        updatedPositions.append(newCoordinates)
                    newState.getCurAgentVehicle().setPositions(tuple(map(tuple, updatedPositions)))
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
                newPositions = list(copy.deepcopy(buffVehicle.getPositions()))
                updatedPositions = []
                for coordinates in newPositions:
                    newCoordinates = [coordinates[0] - 1, coordinates[1]]
                    updatedPositions.append(newCoordinates)
                buffVehicle.setPositions(tuple(map(tuple, updatedPositions)))

            buffVehicle = copy.deepcopy(checkVehicle)
            while self.containsAction(Action(Card.MOVE, 1, buffVehicle.getId()), self.isMovable(vehicles, buffVehicle, boards)):
                rightCount += 1
                newPositions = list(copy.deepcopy(buffVehicle.getPositions()))
                updatedPositions = []
                for coordinates in newPositions:
                    newCoordinates = [coordinates[0] + 1, coordinates[1]]
                    updatedPositions.append(newCoordinates)
                buffVehicle.setPositions(tuple(map(tuple, updatedPositions)))

            if(leftCount > 0):
                slideActions.append(Action(Card.SLIDE, -1 * leftCount, checkVehicle.getId()))
            if (rightCount > 0):
                slideActions.append(Action(Card.SLIDE, rightCount, checkVehicle.getId()))
        elif checkVehicle.getOrientation() == Orientation.VERTICAL:
            upCount = 0
            bottomCount = 0
            buffVehicle = copy.deepcopy(checkVehicle)

            while self.containsAction(Action(Card.MOVE, -1, buffVehicle.getId()), self.isMovable(vehicles, buffVehicle, boards)):
                upCount += 1
                newPositions = list(copy.deepcopy(buffVehicle.getPositions()))
                updatedPositions = []
                for coordinates in newPositions:
                    newCoordinates = [coordinates[0], coordinates[1]-1]
                    updatedPositions.append(newCoordinates)
                buffVehicle.setPositions(tuple(map(tuple, updatedPositions)))

            buffVehicle = copy.deepcopy(checkVehicle)
            while self.containsAction(Action(Card.MOVE, 1, buffVehicle.getId()), self.isMovable(vehicles, buffVehicle, boards)):
                bottomCount += 1
                newPositions = list(copy.deepcopy(buffVehicle.getPositions()))
                updatedPositions = []
                for coordinates in newPositions:
                    newCoordinates = [coordinates[0], coordinates[1]+1]
                    updatedPositions.append(newCoordinates)
                buffVehicle.setPositions(tuple(map(tuple, updatedPositions)))

            if (upCount > 0):
                slideActions.append(Action(Card.SLIDE, -1 * upCount, checkVehicle.getId()))
            if (bottomCount > 0):
                slideActions.append(Action(Card.SLIDE, bottomCount, checkVehicle.getId()))

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

    def playRandomCard(self, deck):
        # Assume 'deck' is a list of available cards, and only contains one-move cards
        if deck:
            self.__card = random.choice(deck) #deck should be a list of card
            print(f"Agent picked card: {self.__card}")
            return self.__card
        
    def checkWin(self):
        for i in range(2):
            if(self.__agentVehicle.getPositions()[i][0] < 1):
                return True
        return False
        
# player1 = Player(Vehicle('1', 2, Orientation.HORIZONTAL, [[0,8], [1,8]]), Side.LEFT, None)
# vehicles = [ Vehicle('B', 2, Orientation.VERTICAL, [[11,8], [11,9]]), Vehicle('A', 2, Orientation.HORIZONTAL, [[1, 6], [2, 6]])]
# sidePieces = [SideBoardPieces(6, 5, Side.LEFT), SideBoardPieces(6, 5, Side.RIGHT)]

# agentVehicle = Vehicle('2', 2, Orientation.HORIZONTAL, [[12,10], [13,10]])
# agent = Agent(agentVehicle, Side.RIGHT, None)

# currentState = State(agentVehicle, player1.getPlayerVehicle(), vehicles, sidePieces)
# possibleActions = agent.getPossibleActions(currentState, 1)
# bestAction = agent.zeroDepth(currentState, Card.SHIFT) 
# print(bestAction.getDirection(), bestAction.getItem())

# action = Action(Card.SLIDE, 1, 'B')
# newState = agent.result(currentState, action)
# print(newState.getVehicles()[0].getPositions())

# print(newState.getVehicles()[0].getPositions(), newState.getVehicles()[1].getPositions())