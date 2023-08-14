class Board():
    def __init__(self):
        self.board = {}
        for i in range(8):
            for j in range(8):
                self.board[(i,j)] = None
        self.board[(3,3)] = True
        self.board[(4,4)] = True
        self.board[(3,4)] = False
        self.board[(4,3)] = False
        self.turn = False
        self.finished = False
        self.count1, self.count2 = 0, 0
        self.lastDisk = None

    def __eq__(self,other):
        return (self.board == other.board) and (self.turn == other.turn) and (self.finished == other.finished) and (self.lastDisk == other.lastDisk)

    def print(self):
            for i in range(8):
                print([self.board[(i,j)] for j in range(8)])

    def copy(self):
        newBoard = Board()
        newBoard.board = self.board.copy()
        newBoard.turn = self.turn
        newBoard.finished = self.finished
        newBoard.count1 = self.count1
        newBoard.count2 = self.count2
        newBoard.lastDisk = self.lastDisk
        return newBoard

    def update(self,i,j,validMoves):
        self.lastDisk = (i,j)
        for move in validMoves:
            if move[1] == (i,j):
                self.updateLine(move[0],move[1])

    def updateLine(self,disk1,disk2):
        i1,j1,i2,j2 = disk1[0],disk1[1],disk2[0],disk2[1]
        for delta in range(max(abs(i1-i2),abs(j1-j2)) + 1):
            self.board[(i1 + delta*int(i1!=i2)*((i1<i2)-(i2<i1)) , j1 + delta*int(j1!=j2)*((j1<j2)-(j2<j1)))] = self.turn

    def checkFinished(self):
        turn = self.getTurn()
        if self.validMoves() == []:
            self.changeTurn()
            if self.validMoves() == []:
                self.finished = True
                self.turn = turn
                return True
        self.turn = turn
        return False

    def getBoard(self):
        return self.board

    def getTurn(self):
        return self.turn

    def changeTurn(self):
        self.turn = not self.turn

    def validMoves(self):
        moves = []
        placedDisks = []
        for disk in self.board.keys():
            if self.board[disk] == self.turn:
                placedDisks.append(disk)
        for disk in placedDisks:
            movesFromDisk = self.validMovesFromDisk(disk)
            for move in movesFromDisk:
                moves.append((disk,move))
        return moves

    def validMovesFromDisk(self,coords):
        moves = []
        for dir in [(0,1),(1,0),(1,1),(1,-1),(-1,0),(0,-1),(-1,-1),(-1,1)]:
            temp = coords
            while (temp[0] + dir[0], temp[1] + dir[1]) in self.board.keys():
                if self.board[(temp[0] + dir[0], temp[1] + dir[1])] == (not self.turn):
                    temp = (temp[0] + dir[0], temp[1] + dir[1])
                elif self.board[(temp[0] + dir[0], temp[1] + dir[1])] == None and temp != coords:
                    moves.append((temp[0] + dir[0], temp[1] + dir[1]))
                    break
                else:
                    break
        return moves

    def count(self):
        self.count1, self.count2 = 0, 0
        for values in self.board.values():
            if values == True:
                self.count2 += 1
            elif values == False:
                self.count1 += 1

    def startGame(self):
        players = {True: "2", False: "1"}
        while not self.finished:
            self.print()
            if self.validMoves() == []:
                self.changeTurn()
                if self.validMoves() == []:
                    self.finished = True
                    count1,count2 = self.count()
                    print("Game finished, player %s wins (%s,%s)",(count1<count2),count1,count2)
                    return count1<count2
            validMoves = self.validMoves()
            validDisks = [move[1] for move in validMoves]
            print("Player " + players[self.turn] + "'s turn")
            print("Valid moves: " + str(validDisks))
            move = input("Enter your move: ")
            move = move.split(",")
            move = (int(move[0]),int(move[1]))
            while move not in validDisks:
                move = input("Invalid move. Enter your move: ")
                move = move.split(",")
                move = (int(move[0]),int(move[1]))
            self.update(move[0],move[1],validMoves)
            self.changeTurn()

if __name__ == "__main__":
    test = Board()
    test.startGame()