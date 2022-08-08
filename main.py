# Importing Modules
from cmath import inf
import sys
import pygame
import numpy as np
import random
import copy
import math

from constants import *

# PyGame Setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE GAME - AI ENABLED')
screen.fill(BG_COLOR)

class Board:

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_squares = self.squares # List of Empty Squares
        self.marked_squares = 0

    def final_state(self, show=False):
        """
            return 0 if there is no win yet - Doesn't mean that match is draw
            return 1 if player 1 has won
            return 2 if player 2 has won
        """
        # Vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    STRIKE_COLOR = CIRCLE_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col*SQ_SIZE + SQ_SIZE // 2, 20)
                    fPos = (col*SQ_SIZE + SQ_SIZE // 2, HEIGHT-20)
                    pygame.draw.line(screen, STRIKE_COLOR, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # Horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    STRIKE_COLOR = CIRCLE_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row*SQ_SIZE + SQ_SIZE // 2)
                    fPos = (WIDTH-20, row*SQ_SIZE + SQ_SIZE // 2)
                    pygame.draw.line(screen, STRIKE_COLOR, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]
        
        # Descending Diagnol
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                STRIKE_COLOR = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH-20, HEIGHT-20)
                pygame.draw.line(screen, STRIKE_COLOR, iPos, fPos, LINE_WIDTH)
            
            return self.squares[1][1]

        # Ascending Diagnol 
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                STRIKE_COLOR = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT-20)
                fPos = (WIDTH-20, 20)
                pygame.draw.line(screen, STRIKE_COLOR, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]
        
        # No win yet
        return 0


    
    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    def is_empty_square(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_squares(self):
        empty_squares = []

        for row in range(ROWS):
            for col in range(COLS):
                if self.is_empty_square(row, col):
                    empty_squares.append((row, col))

        return empty_squares
    
    def is_full(self):
        return self.marked_squares == ROWS*COLS

    def is_empty(self):
        return self.marked_squares == 0

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def random_choice(self, board):
        empty_squares = board.get_empty_squares()
        idx = random.randrange(0, len(empty_squares))

        return empty_squares[idx] # Row, Col        
    
    def minimax(self, board, maximizing):
        # Terminal Case
        case = board.final_state()

        # Player 1 Wins
        if case == 1:
            return 1, None      # eval, move
        # Player 2 Wins
        if case == 2:
            return -1, None
        
        # Draw
        if board.is_full():
            return 0, None

        if maximizing:
            max_eval = -math.inf
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move
        
        elif not maximizing:
            min_eval = math.inf
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move


    def eval(self, main_board):
        if self.level == 0:
            # Random Choice
            eval = 'Random'
            move = self.random_choice(main_board)

        else:
            # Min Max Algorithm Choice
            eval, move = self.minimax(main_board, False)
        
        print(f"AI has made a move in position - {move} with an evaluation of {eval}")   

        return move # row, col


class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1         # 1 - Crosses and 0 - Circles
        self.gamemode = 'ai' # PvP or AI game modes available
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):
        # BG FILL
        screen.fill(BG_COLOR)

        # Horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQ_SIZE), (WIDTH, SQ_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQ_SIZE), (WIDTH, HEIGHT-SQ_SIZE), LINE_WIDTH)

        # Vertical
        pygame.draw.line(screen, LINE_COLOR, (SQ_SIZE, 0), (SQ_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH-SQ_SIZE, 0), (WIDTH-SQ_SIZE, HEIGHT), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross
            # descending line
            start_desc = (col*SQ_SIZE + OFFSET, row*SQ_SIZE + OFFSET)
            end_desc = (col*SQ_SIZE + SQ_SIZE - OFFSET, row*SQ_SIZE + SQ_SIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            # ascending line
            start_asc = (col*SQ_SIZE + OFFSET, row*SQ_SIZE + SQ_SIZE - OFFSET)
            end_asc = (col*SQ_SIZE + SQ_SIZE - OFFSET, row*SQ_SIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)


        elif self.player == 2:
            # draw circle
            center = (col*SQ_SIZE + SQ_SIZE // 2, row*SQ_SIZE + SQ_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)

    def next_turn(self):
        self.player = self.player%2 + 1
    
    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'
        
    def reset(self):
        self.__init__()

    def is_over(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()


def main():

    # Game Object Initialization
    game = Game()
    board = game.board
    ai = game.ai


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()      

                # r-restart
                if event.key == pygame.K_r:
                    game.reset() 
                    board = game.board
                    ai = game.ai
                
                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1 - random ai
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                col = pos[0] // SQ_SIZE
                row = pos[1] // SQ_SIZE
                
                if board.is_empty_square(row, col) and game.running:
                    game.make_move(row, col)

                    if game.is_over():
                        game.running = False

                elif not board.is_empty_square(row, col):
                    print("Square already filled")


            
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            # Update the Screen
            pygame.display.update()

            # ai methods
            row, col = ai.eval(board)

            game.make_move(row, col)        

            if game.is_over():
                game.running = False    

        pygame.display.update()


main()