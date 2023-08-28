from random import choice
from node import Node
from game import Board
import math

class AI():
    def __init__(self,aiColor,type):
        self.color = aiColor
        self.type = type
        self.opponent = not aiColor
        self.root = None

    def chooseMove(self,game,moves):
        # random mode
        if self.type == 'random': return choice([move[1] for move in moves])
        # mcts mode
        if self.type == 'mcts': return self.monteCarlo(game)

    def monteCarlo(self,game,iterations=500,exploreConstant=0.7):
        #if self.root == None: 
        #    self.root = Node(None,game.copy())
        #else:
        #    for child in self.root.children:
        #        if child.board == game:
        #            self.root = child
        #            break
        self.root = Node(None,game.copy())
        for i in range(iterations):
            node = self.selection(self.root,exploreConstant)
            reward = self.simulation(node)
            self.backpropagation(node,reward)
        bestChild = self.bestChild(self.root,exploreConstant)
        self.root = bestChild
        #print(str(round(100*bestChild.wins/bestChild.games)) + ' % win probability')
        return bestChild.board.lastDisk

    def selection(self,node,exploreConstant):
        while not node.board.checkFinished():
            if not node.isExplored():
                return self.expansion(node)
            else:
                node = self.bestChild(node,exploreConstant)
        return node

    def expansion(self,node):
        board = node.board
        moves = board.validMoves()
        if moves == []:
            newBoard = board.copy()
            newBoard.changeTurn()
            moves = newBoard.validMoves()
            for disk in [move[1] for move in moves]:
                if disk not in node.childrenMoves:
                    newBoard.update(disk[0],disk[1],moves)
                    newBoard.changeTurn()
                    child = node.addChild(newBoard)
                    return child
        for disk in [move[1] for move in moves]:
            if disk not in node.childrenMoves:
                newBoard = board.copy()
                newBoard.update(disk[0],disk[1],moves)
                newBoard.changeTurn()
                child = node.addChild(newBoard)
                return child
        return None

    def simulation(self,node):
        board = node.board.copy()
        turn = board.getTurn()
        while not board.checkFinished():
            moves = board.validMoves()
            if moves == []:
                board.changeTurn()
                continue
            disk = choice([move[1] for move in moves])
            board.update(disk[0],disk[1],moves)
            board.changeTurn()
        board.count()
        if (board.count1 < board.count2) and not turn:
            return 1
        elif (board.count1 > board.count2) and turn:
            return 1
        elif (board.count1 == board.count2):
            return 1/2
        else:
            return 0

    def backpropagation(self,node,reward):
        if node == None:
            return
        turn = node.board.getTurn()
        while node != None:
            node.games += 1
            node.wins += reward if node.board.getTurn()==turn else 1-reward
            node = node.parent

    def bestChild(self,node,exploreConstant):
        bestChildren = []
        bestScore = -math.inf
        for child in node.children:
            exploitation = child.wins/child.games
            exploration = math.sqrt(math.log(node.games)/child.games)
            score = exploitation + exploreConstant*exploration
            if bestChildren == [] or score > bestScore:
                bestChildren = [child]
                bestScore = score
            elif score == bestScore:
                bestChildren.append(child)
        return choice(bestChildren)