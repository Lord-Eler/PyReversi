class Node:
    def __init__(self, parent, board):
        self.parent = parent
        self.children = []
        self.childrenMoves = []
        self.wins = 0
        self.games = 0
        self.board = board

    def __str__(self):
        return "Node: "+str(self.wins)+"/"+str(self.games)

    def addChild(self,board):
        child = Node(self,board)
        self.children.append(child)
        self.childrenMoves.append(board.lastDisk)
        return child

    def update(self,wins,games):
        self.wins += wins
        self.games += games

    def isExplored(self):
        if self.board.validMoves() != []:
            disks = []
            for disk in [move[1] for move in self.board.validMoves()]:
                if not disk in disks:
                    disks.append(disk)
            return (len(self.children) == len(disks))
        elif self.board.checkFinished():
            return True
        elif self.board.validMoves() == []:
            board = self.board.copy()
            board.changeTurn()
            disks = []
            for disk in [move[1] for move in board.validMoves()]:
                if not disk in disks:
                    disks.append(disk)
            return (len(self.children) == len(disks))