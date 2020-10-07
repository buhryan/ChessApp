"""
Main Driver that handles user inputs and the current GameState object.
"""
from typing import Tuple

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512  # square window
DIMENSION = 8  # dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialise a global dictionary of images. This will be called exactly once in the main.
'''


def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))
    # Note: we can access image by saying 'Images'['wP']'


'''
The main driver for our code. This will handle user input and updating the graphics
'''


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False  # flag variable for when a move is made

    load_images()  # only do this once, before the while loop
    running = True
    sq_selected: Tuple = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
    player_clicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)])

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):  # the user clicked the same square twice
                    sq_selected = ()  # unselect
                    player_clicks = []  # clear player clicks
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)  # append for both 1st and 2nd clicks
                if len(player_clicks) == 2:  # after 2nd click
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                    sq_selected = ()  # reset user clicks
                    player_clicks = []

            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Responsible for all graphics within a current GameState.
'''


def draw_game_state(screen, gs):
    draw_board(screen)  # draws the squares on the board\
    # add piece highlighting or move suggestion
    draw_pieces(screen, gs.board)  # draw pieces on top of those squares


'''
Draw the squares on the board. Top left square is always light.
'''


def draw_board(screen):
    colors = [p.Color('white'), p.Color('grey')]
    for r in range(DIMENSION):
        c: int
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Draw the pieces on the board using the current GameState.board
'''


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':  # not empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
