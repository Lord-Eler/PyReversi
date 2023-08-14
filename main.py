import pygame
from pyautogui import alert, confirm
from game import Board
from random import choice
from ai import AI

class GUI:
    def __init__(self):
        # game prompts
        translate = {'Yes':True,'No':False}
        self.aiOpponent = translate[confirm(text='Play against the computer ?', title='PyReversi', buttons=['Yes','No'])]
        if self.aiOpponent:
            self.aiColor = choice([True,False])
            temp = {True:'White',False:'Black'}
            alert(text=f'You play {temp[not self.aiColor]}', title='PyReversi', button='OK', timeout=3000)
            self.ai = AI(self.aiColor,'mcts')
        self.helper = translate[confirm(text='Play with the helper ?', title='PyReversi', buttons=['Yes','No'])]
        # pygame init
        pygame.init()
        self.size = 700
        self.SCREEN_SIZE = (self.size,self.size)
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.GREEN = (0,200,0)
        self.DARK_GREEN = (0,100,0)
        self.GRAY = (100,100,100)
        pygame.display.set_caption("PyReversi")
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.font = pygame.font.Font('freesansbold.ttf', self.size//20)
        self.game = Board()
        self.textCountWhite = self.font.render(f': {self.game.count2}', True, self.WHITE)
        self.textCountBlack = self.font.render(f': {self.game.count1}', True, self.WHITE)
        self.textCountWhiteRect = self.textCountWhite.get_rect()
        self.textCountBlackRect = self.textCountBlack.get_rect()
        self.screen.fill(self.GRAY)
        pygame.draw.rect(self.screen, self.GREEN, (self.size//10,self.size//10,8*self.size//10,8*self.size//10))
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(self.screen, self.BLACK, (self.size//10 + i*self.size//10,self.size//10 + j*self.size//10,self.size//10,self.size//10), 1)
        self.textTurn = self.font.render('Turn : ', True, self.WHITE)
        self.textTurnRect = self.textTurn.get_rect()
        self.textTurnRect.center = ((3/2)*self.size//10, (19/2)*self.size//10)
        self.screen.blit(self.textTurn, self.textTurnRect)
        pygame.draw.circle(self.screen,self.BLACK,(6*self.size//10, (37/4)*self.size//10), self.size//50)
        pygame.draw.circle(self.screen,self.WHITE,(6*self.size//10, (39/4)*self.size//10), self.size//50)
        self.textCountWhiteRect.center = (7*self.size//10, (39/4)*self.size//10)
        self.textCountBlackRect.center = (7*self.size//10, (37/4)*self.size//10)
        self.screen.blit(self.textCountWhite, self.textCountWhiteRect)
        self.screen.blit(self.textCountBlack, self.textCountBlackRect)
        pygame.display.flip()
        self.updateScreen()

    def updateScreen(self):
        for disk in self.game.board.keys():
            if self.game.board[disk] == True:
                pygame.draw.circle(self.screen, self.WHITE, (self.size//10 + disk[0]*self.size//10 + self.size//20, self.size//10 + disk[1]*self.size//10 + self.size//20), self.size//25)
            elif self.game.board[disk] == False:
                pygame.draw.circle(self.screen, self.BLACK, (self.size//10 + disk[0]*self.size//10 + self.size//20, self.size//10 + disk[1]*self.size//10 + self.size//20), self.size//25)
        if self.game.getTurn() == True:
            pygame.draw.circle(self.screen, self.WHITE, (3*self.size//10, (19/2)*self.size//10), self.size//25)
        elif self.game.getTurn() == False:
            pygame.draw.circle(self.screen, self.BLACK, (3*self.size//10, (19/2)*self.size//10), self.size//25)
        textCountWhite = self.font.render(f': {self.game.count2}', True, self.WHITE)
        textCountBlack = self.font.render(f': {self.game.count1}', True, self.WHITE)
        pygame.draw.rect(self.screen, self.GRAY, ((13/2)*self.size//10, 9*self.size//10,8*self.size//10,self.size))
        self.screen.blit(textCountWhite, self.textCountWhiteRect)
        self.screen.blit(textCountBlack, self.textCountBlackRect)
        pygame.display.flip()

    def previewMoves(self,moves):
        for disk in moves:
            pygame.draw.circle(self.screen, self.DARK_GREEN, (self.size//10 + disk[1][0]*self.size//10 + self.size//20, self.size//10 + disk[1][1]*self.size//10 + self.size//20), self.size//25)
        pygame.display.flip()
    def unpreviewMoves(self,moves):
        for disk in moves:
            pygame.draw.circle(self.screen, self.GREEN, (self.size//10 + disk[1][0]*self.size//10 + self.size//20, self.size//10 + disk[1][1]*self.size//10 + self.size//20), self.size//25)
        pygame.display.flip()

    def clickToCoords(self,coords):
        if self.size//10 < coords[0] < 9*self.size//10 and self.size//10 < coords[1] < 9*self.size//10:
            i = coords[0]//(self.size//10) - 1
            j = coords[1]//(self.size//10) - 1
            return (i,j)
        return None

    def run(self):
        while not self.game.checkFinished():
            moves = self.game.validMoves()
            if moves == []:
                self.game.changeTurn()
                self.updateScreen()
                if not self.aiOpponent or self.game.getTurn() != self.aiColor: alert(text='No moves available', title='PyReversi', button='OK', timeout=3000)
                continue
            diskToPlay = None
            
            # AI player
            if self.aiOpponent and self.game.getTurn() == self.aiColor:
                diskToPlay = self.ai.chooseMove(self.game,moves)
            
            # Human player
            else:
                if self.helper: self.previewMoves(moves)
                while diskToPlay == None:
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            coords = self.clickToCoords(pygame.mouse.get_pos())
                            if coords != None:
                                disks = [move[1] for move in moves]
                                if coords in disks:
                                    diskToPlay = coords
                                    if self.helper: self.unpreviewMoves(moves)
            
            # Update game
            self.game.update(diskToPlay[0],diskToPlay[1],moves)
            self.game.changeTurn()
            self.game.count()
            self.updateScreen()
        self.end()

    def end(self):
        self.game.count()
        if self.game.count2 != self.game.count1:
            translate = {self.game.count2: "White", self.game.count1: "Black"}
            winner = translate[max(self.game.count1,self.game.count2)]
            looser = translate[min(self.game.count1,self.game.count2)]
            alert(f"Game finished, {winner} won with {max(self.game.count1,self.game.count2)}, {looser} had {min(self.game.count1,self.game.count2)}", "PyReversi", "OK")
        else:
            alert("Draw !", "PyReversi", "OK")
        pygame.quit()


if __name__ == "__main__":
    gui = GUI()
    gui.run()