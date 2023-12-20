import sys
import time
from user.screen import pygame
from user.table import Sudoku
from user.components import draw_board
from user.components import screen, green, red, white

def solve_backtracking(game: Sudoku):
        '''
        Solves the game from it's current state with a backtracking algorithm.
        Returns True if successful and False if not solvable.
        '''
        cell = game.get_empty_cell()

        # Board is complete if cell is False
        if not cell:
            return True

        # Check each possible value in cell
        for val in range(1, 10):

            # Check if the value is a valid move
            if not game.check_move(cell, val):
                continue

            # Place value in board
            cell.value = val

            # If all recursive calls return True then board is solved
            if solve_backtracking():
                return True

            # Undo move is solve was unsuccessful
            cell.value = None

        # No moves were successful
        return False

def visual_solve(game, cells):
    '''Solves the game while giving a visual representation of what is being done.'''
    # Get first empty cell
    cell = game.get_empty_cell()

    # Solve is complete if cell is False
    if not cell:
        return True

    # Check each possible move
    for val in range(1, 10):
        # Allow game to quit when being solved
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Place value in board
        cell.value = val

        # Outline cell being changed in red
        screen.fill(white)
        draw_board(None, cells, game)
        cell_rect = cells[cell.row][cell.col]
        pygame.draw.rect(screen, red, cell_rect, 5)
        pygame.display.update([cell_rect])
        time.sleep(0.05)

        # Check if the value is a valid move
        if not game.check_move(cell, val):
            cell.value = None
            continue

        # If all recursive calls return True then board is solved
        screen.fill(white)
        pygame.draw.rect(screen, green, cell_rect, 5)
        draw_board(None, cells, game)
        pygame.display.update([cell_rect])
        if visual_solve(game, cells):
            return True

        # Undo move is solve was unsuccessful
        cell.value = None

    # No moves were successful
    screen.fill(white)
    pygame.draw.rect(screen, white, cell_rect, 5)
    draw_board(None, cells, game)
    pygame.display.update([cell_rect])
    return False