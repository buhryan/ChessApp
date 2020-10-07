"""
This class contains the chess board and pieces.
It contains all the rules that constrain the movements of the pieces.
A log of all moves made is also stored.
"""


class GameState:
    """
    The chess board is an 8x8 2d list. Each entry in the list has two characters. The first character indicates if the
     piece is black ('b') or white ('w'). The second character indicates the piece that it is.
     Pawn ('P'), Knight ('N'), Bishop ('B'), Rook ('R), Queen ('Q'), King ('K).
     '__' indicates an empty space on the board.
    """
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.move_functions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                               'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False

    '''
    Takes a Move as a parameter and executes it (doesn't work with special moves)
    '''

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '--'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # log the move so we can undo it later
        self.white_to_move = not self.white_to_move  # swap players
        # update the king's location if moved
        if move.piece_moved == 'wK':
            self.white_king_location == (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location == (move.end_row, move.end_col)

    '''
    Undo the last move made
    '''

    def undo_move(self):
        if len(self.move_log) != 0:  # make sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move  # switch turns back
            # update king's position if needed
            if move.piece_moved == 'wK':
                self.white_king_location == (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_location == (move.start_row, move.start_col)

    '''
    All moves considering checks
    '''

    def get_valid_moves(self):
        # 1. Generate all possible moves
        moves = self.get_all_possible_moves()
        # 2. For each move, make the move.
        for i in range(len(moves) - 1, -1, -1):  # when removing from a list go backwards through that list
            self.make_move(moves[i])
            # 3. Generate all opponent's moves
            # 4. For each of your opponent's moves, see if they attack your king
            self.white_to_move = not self.white_to_move
            if self.in_check():  # 5. If they do attack your king, not a valid move
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()
        if len(moves) == 0:  # either checkmate or stalemate
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

    '''
    Determine if the current player is in check
    '''

    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    '''
    Determine if the enemy can attack the square r, c
    '''

    def square_under_attack(self, r, c):
        self.white_to_move = not self.white_to_move  # switch to opponent's turn
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move  # switch turns back
        for move in opp_moves:
            if move.end_row == r and move.end_col == c:  # square is under attack
                return True
        return False

    '''
    All moves without considering checks
    '''

    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)  # calls the appropriate move function based on piece type

        return moves

    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''

    def get_pawn_moves(self, r, c, moves):

        if self.white_to_move:  # white pawn moves
            if self.board[r - 1][c] == '--':  # 1 square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == '--':  # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            # captures
            if c - 1 >= 0:  # captures to the left
                if self.board[r - 1][c - 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # captures to the right
                if self.board[r - 1][c + 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # black pawn moves
            if self.board[r + 1][c] == '--':  # 1 square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == '--':  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            # captures
            if c - 1 >= 0:  # captures to left
                if self.board[r + 1][c - 1][0] == 'w':  # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # captures to right
                if self.board[r + 1][c + 1][0] == 'w':  # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
        # pawn promotions later

    '''
    Get all the rook moves for the rook located at row, col and add these moves to the list
    '''

    def get_rook_moves(self, r, c, moves):  # check edge of board or until another piece
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':  # empty square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # valid enemy piece
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:  # friendly piece
                        break
                else:  # end of the board
                    break

    '''
    Get all the bishop moves for the bishop located at row, col and add these moves to the list
    '''

    def get_bishop_moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':  # empty square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # valid enemy piece
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:  # friendly piece
                        break
                else:  # end of board
                    break

    '''
    Get all the knight moves for the knight located at row, col and add these moves to the list
    '''

    def get_knight_moves(self, r, c, moves):
        knight_moves = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2))
        ally_color = 'w' if self.white_to_move else 'b'
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # valid square
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    '''
    Get all the queen moves for the queen located at row, col and add these moves to the list
    '''

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    '''
    Get all the king moves for the king located at row, col and add these moves to the list
    '''

    def get_king_moves(self, r, c, moves):
        king_moves = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row = r + king_moves[i][0]
            end_col = c + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # valid square
                    moves.append(Move((r, c), (end_row, end_col), self.board))


'''
This class defines one move on the chessboard for a piece. It will also display the required 
'''


class Move:
    # maps keys to values
    # key : value
    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
                   '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCol = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                  'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: k for k, v in filesToCol.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    '''
    Displays the moves made in standard algebraic notation.
    Refer to pg18 https://www.fide.com/FIDE/handbook/LawsOfChess.pdf. 
    '''

    def get_chess_notation(self):
        piece = self.piece_moved[1]
        if self.piece_moved[1] == 'P':  # pawns have no character indicator in chess notation
            piece = ''
        if self.piece_captured != '--':  # if a piece is captured on the move, pawns will have the file it departed from
            if piece == '':
                piece = self.get_rank_file(self.start_row, self.start_col)[0]
            piece += 'x'
        return piece + self.get_rank_file(self.end_row, self.end_col)

    '''
    Returns the position of the chess piece in standard rank file notation.
    '''

    def get_rank_file(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
