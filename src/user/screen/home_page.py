import sys
import numpy as np
from user.screen import pygame
from user.table import Sudoku
from sudoku_agent.sudoku_gen import generate_sudoku
from user.components.__init__ import create_cells, draw_board, \
    draw_button, visual_solve
from user.screen import buffer, screen, black, width, green, white, \
    height, button_height, button_border, button_width, inactive_btn, \
    active_btn


def check_sudoku(sudoku):
    '''
    Takes a complete instance of Soduku and 
    returns whether or not the solution is valid.
    '''
    # Ensure all cells are filled
    if sudoku.get_empty_cell():
        raise ValueError('Game is not complete')

    # Will hold values for each row, column, and box
    row_sets = [set() for _ in range(9)]
    col_sets = [set() for _ in range(9)]
    box_sets = [set() for _ in range(9)]

    # Check all rows, columns, and boxes contain no duplicates
    for row in range(9):
        for col in range(9):
            box = (row // 3) * 3 + col // 3
            value = sudoku.board[row][col].value

            # Check if number already encountered in row, column, or box
            if value in row_sets[row] or value in col_sets[col] or value in box_sets[box]:
                return False

            # Add value to corresponding set
            row_sets[row].add(value)
            col_sets[col].add(value)
            box_sets[box].add(value)

    # All rows, columns, and boxes are valid
    return True


def play():
    '''Contains all the functionality for playing a game of Sudoku.'''
    grid = np.array(generate_sudoku(3, 23), dtype=np.float32)
    grid[np.isnan(grid)] = 0
    grid = grid.astype(int)
    game = Sudoku(grid)
    cells = create_cells()
    active_cell = None
    solve_rect = pygame.Rect(
        buffer,
        height-button_height - button_border*2 - buffer,
        button_width + button_border*2,
        button_height + button_border*2
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Handle mouse click
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()

                # Reset button is pressed
                if reset_btn.collidepoint(mouse_pos):
                    game.reset()

                # Solve button is pressed
                if solve_btn.collidepoint(mouse_pos):
                    screen.fill(white)
                    active_cell = None
                    draw_board(active_cell, cells, game)
                    reset_btn = draw_button(
                        width - buffer - button_border*2 - button_width,
                        height - button_height - button_border*2 - buffer,
                        button_width,
                        button_height,
                        button_border,
                        inactive_btn,
                        black,
                        'Reset'
                    )
                    solve_btn = draw_button(
                        width - buffer*2 - button_border*4 - button_width*2,
                        height - button_height - button_border*2 - buffer,
                        button_width,
                        button_height,
                        button_border,
                        inactive_btn,
                        black,
                        'Visual Solve'
                    )
                    pygame.display.flip()
                    visual_solve(game, cells)

                # Test if point in any cell
                active_cell = None
                for row in cells:
                    for cell in row:
                        if cell.collidepoint(mouse_pos):
                            active_cell = cell

                # Test if active cell is empty
                if active_cell and not game.board[active_cell.row][active_cell.col].editable:
                    active_cell = None

            # Handle key press
            if event.type == pygame.KEYUP:
                if active_cell is not None:

                    # Input number based on key press
                    if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        game.board[active_cell.row][active_cell.col].value = 0
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        game.board[active_cell.row][active_cell.col].value = 1
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        game.board[active_cell.row][active_cell.col].value = 2
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        game.board[active_cell.row][active_cell.col].value = 3
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        game.board[active_cell.row][active_cell.col].value = 4
                    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        game.board[active_cell.row][active_cell.col].value = 5
                    if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        game.board[active_cell.row][active_cell.col].value = 6
                    if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        game.board[active_cell.row][active_cell.col].value = 7
                    if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        game.board[active_cell.row][active_cell.col].value = 8
                    if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        game.board[active_cell.row][active_cell.col].value = 9
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        game.board[active_cell.row][active_cell.col].value = None

        screen.fill(white)

        # Draw board
        draw_board(active_cell, cells, game)

        # Create buttons
        reset_btn = draw_button(
            width - buffer - button_border*2 - button_width,
            height - button_height - button_border*2 - buffer,
            button_width,
            button_height,
            button_border,
            inactive_btn,
            black,
            'Reset'
        )
        solve_btn = draw_button(
            width - buffer*2 - button_border*4 - button_width*2,
            height - button_height - button_border*2 - buffer,
            button_width,
            button_height,
            button_border,
            inactive_btn,
            black,
            'Visual Solve'
        )

        # Check if mouse over either button
        if reset_btn.collidepoint(pygame.mouse.get_pos()):
            reset_btn = draw_button(
                width - buffer - button_border*2 - button_width,
                height - button_height - button_border*2 - buffer,
                button_width,
                button_height,
                button_border,
                active_btn,
                black,
                'Reset'
            )
        if solve_btn.collidepoint(pygame.mouse.get_pos()):
            solve_btn = draw_button(
                width - buffer*2 - button_border*4 - button_width*2,
                height - button_height - button_border*2 - buffer,
                button_width,
                button_height,
                button_border,
                active_btn,
                black,
                'Visual Solve'
            )

        # Check if game is complete
        if not game.get_empty_cell():
            if check_sudoku(game):
                # Set the text
                font = pygame.font.Font(None, 36)
                text = font.render('Solved!', 1, green)
                textbox = text.get_rect(center=(solve_rect.center))
                screen.blit(text, textbox)

        # Update screen
        pygame.display.flip()