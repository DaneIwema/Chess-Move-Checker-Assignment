# definitions for individual chess pieces
# Dane Iwema
# IT327

from chess_piece import ChessPiece
from chess_utils import BoardInfo
from chess_utils import PieceInfo

class Knight(ChessPiece):
    """class definition for a White Knight child of ChessPiece
    
    Attribues:
        _row(Integer): the row number
        _col(Integer): the column number
        _color(BoardInfo): a BoardInfo enumerator that represents Black or White
        _label(PieceInfo): a PieceInfo enumerator that represents the piece type
    """

    def __init__(self, row_num, col_num):
        """Knight initializer
        
        Arguments:
            c_row_num(Integer): the row number
            c_col_num(Integer): the column number
        """
        ChessPiece.__init__(self, row_num, col_num, BoardInfo.WHITE, PieceInfo.WHITE_KNIGHT)
        
    def is_legal_move(self, dest_row, dest_col, board):
        """Returns true if this piece can legally move to the specified
        location on the provide board
        
        Attribues:
            dest_row(Integer): the destination row to move the piece
            dest_col(Integer): the destination column to move the piece
            board(Board object): the current locations of every piece on the board
        
        Returns:
            type: boolean
        """

        # if the future row or column is in line with the current piece's 
        # row or column then early return as its impossible for that to be a move
        if (dest_row == self._row) or (dest_col == self._col):
            return False
        move = abs(self._row-dest_row) + abs(self._col-dest_col)
        is_legal = (move == 3) and self.check_take(board.get_square_info(dest_row, dest_col))
        return is_legal

    def generate_legal_moves(self, board_data, board):
        """Adds representation for the legal moves to the provided 
        board representation and returns a board object with all the possible spaces the piece can move
        
        Attribues:
            board_data(Board object): an empty board
            board(Board object): the current locations of every piece on the board
        
        Returns:
            type: Board object the passed in board object but now filled with all the possible moves of this piece
        """
        char_label = self._label.value
        board_data[self._row][self._col] = char_label

        pos_moves=[-1,1,-2,2] # set up the directions to move the piece

        #loop through all the move directions
        for move in pos_moves:

            #set up the indexes to use depeinding if the move is 1 or not
            index1 = 0
            index2 = 1
            if abs(move) == 1:
                index1 = 2
                index2 = 3

            # sets up row and column information and the square type from the given board
            row = move + self._row
            col = pos_moves[index1] + self._col
            # check if the move is legal and then set the board
            if self.check_take(board.get_square_info(row, col)):
                board_data[row][col] = char_label

            # reset the col
            col = pos_moves[index2] + self._col

            # check if the move is legal and then set the board
            if self.check_take(board.get_square_info(row, col)):
                board_data[row][col] = char_label
        return board_data

class Rook(ChessPiece):
    """class definition for a White Rook child of ChessPiece
    
    Attribues:
        _row(Integer): the row number
        _col(Integer): the column number
        _color(BoardInfo): a BoardInfo enumerator that represents Black or White
        _label(PieceInfo): a PieceInfo enumerator that represents the piece type
    """
    def __init__(self, row_num, col_num):
        """Rook initializer
        
        Arguments:
            c_row_num(Integer): the row number
            c_col_num(Integer): the column number
        """
        ChessPiece.__init__(self, row_num, col_num, BoardInfo.WHITE, PieceInfo.WHITE_ROOK)

    def is_legal_move(self, dest_row, dest_col, board):
        """Returns true if this piece can legally move to the specified
        location on the provide board
        
        Attribues:
            dest_row(Integer): the destination row to move the piece
            dest_col(Integer): the destination column to move the piece
            board(Board object): the current locations of every piece on the board
        
        Returns:
            type: boolean
        """
        return self.qbr_is_legal_move(dest_row, dest_col, board)

    def generate_legal_moves(self, board_data, board):
        """Adds representation for the legal moves to the provided 
        board representation and returns a board object with all the possible spaces the piece can move
        
        Attribues:
            board_data(Board object): an empty board
            board(Board object): the current locations of every piece on the board
        
        Returns:
            type: Board object the passed in board object but now filled with all the possible moves of this piece
        """
        return self.qbr_generate_legal_moves(board_data, board)

class WhitePawn(ChessPiece):
    """class definition for a White Pawn child of ChessPiece
    
    Attribues:
        _row(Integer): the row number
        _col(Integer): the column number
        _color(BoardInfo): a BoardInfo enumerator that represents Black or White
        _label(PieceInfo): a PieceInfo enumerator that represents the piece type
    """
    def __init__(self, row_num, col_num):
        """WhitePawn initializer
        
        Arguments:
            c_row_num(Integer): the row number
            c_col_num(Integer): the column number
        """
        ChessPiece.__init__(self, row_num, col_num, BoardInfo.WHITE, PieceInfo.WHITE_PAWN)

    def is_legal_move(self, dest_row, dest_col, board):
        """Returns true if this piece can legally move to the specified
        location on the provide board
        
        Attribues:
            dest_row(Integer): the destination row to move the piece
            dest_col(Integer): the destination column to move the piece
            board(Board object): the current locations of every piece on the board
        
        Returns:
            type: boolean
        """
        # check case for moving forward 2 spaces if not in starting position for early return False
        if dest_row-self._row==2 and self._row != 1:
            return False
        
        pos_moves = {5:1, 6:1, 2:0} # the possible directions for the pawn to move and the conditions to make the move

        direction = self.determine_direction(dest_row, dest_col) # gets the direction of the move to the destination
        
        isLegal = board.get_square_info(dest_row, dest_col).value == pos_moves[direction] # checks the move using the pos_moves for the direction and the condition

        return isLegal

    def generate_legal_moves(self, board_data, board):
        """Adds representation for the legal moves to the provided 
        board representation and returns a board object with all the possible spaces the piece can move
        
        Attribues:
            board_data(Board object): an empty board
            board(Board object): the current locations of every piece on the board
        
        Returns:
            type: Board object the passed in board object but now filled with all the possible moves of this piece
        """
        char_label = self._label.value
        board_data[self._row][self._col] = char_label

        # iterates through the 3 possible directions for the pawn to move and the conditions to make the move
        pos_moves = {(1, -1):1, (1, 1):1, (1, 0):0} 
        for move, condition in pos_moves.items():
            row = move[0] + self._row
            col = move[1] + self._col
            if board.get_square_info(row, col).value == condition:
                board_data[row][col] = char_label

        # case for moving 2 spaces forward
        if self._row==1 and board.get_square_info(self._row+2, self._col) == 0:
            board_data[self._row+2][self._col] = char_label

        return board_data

class Bishop(ChessPiece):
    """class definition for a White Bishop child of ChessPiece
    
    Attribues:
        _row(Integer): the row number
        _col(Integer): the column number
        _color(BoardInfo): a BoardInfo enumerator that represents Black or White
        _label(PieceInfo): a PieceInfo enumerator that represents the piece type
    """
    def __init__(self, row_num, col_num):
        """Bishop initializer
        
        Arguments:
            c_row_num(Integer): the row number
            c_col_num(Integer): the column number
        """
        ChessPiece.__init__(self, row_num, col_num, BoardInfo.WHITE, PieceInfo.WHITE_BISHOP)

    def is_legal_move(self, dest_row, dest_col, board):
        """Returns true if this piece can legally move to the specified
        location on the provide board
        
        Attribues:
            dest_row(Integer): the destination row to move the piece
            dest_col(Integer): the destination column to move the piece
            board(Board object): the current locations of every piece on the board
        
        Returns:
            type: boolean
        """
        return self.qbr_is_legal_move(dest_row, dest_col, board)
    
    def generate_legal_moves(self, board_data, board):
        """Adds representation for the legal moves to the provided 
        board representation and returns a board object with all the possible spaces the piece can move
        
        Attribues:
            board_data(Board object): an empty board
            board(Board object): the current locations of every piece on the board
        
        Returns:
            type: Board object the passed in board object but now filled with all the possible moves of this piece
        """
        return self.qbr_generate_legal_moves(board_data, board)

class Queen(ChessPiece):
    """class definition for a White Queen child of ChessPiece
    
    Attribues:
        _row(Integer): the row number
        _col(Integer): the column number
        _color(BoardInfo): a BoardInfo enumerator that represents Black or White
        _label(PieceInfo): a PieceInfo enumerator that represents the piece type
    """
    def __init__(self, row_num, col_num):
        """Queen initializer
        
        Arguments:
            c_row_num(Integer): the row number
            c_col_num(Integer): the column number
        """
        ChessPiece.__init__(self, row_num, col_num, BoardInfo.WHITE, PieceInfo.WHITE_QUEEN)
    
    def is_legal_move(self, dest_row, dest_col, board):
        """Returns true if this piece can legally move to the specified
        location on the provide board
        
        Attribues:
            dest_row(Integer): the destination row to move the piece
            dest_col(Integer): the destination column to move the piece
            board(Board object): the current locations of every piece on the board
        
        Returns:
            type: boolean
        """
        return self.qbr_is_legal_move(dest_row, dest_col, board)
    
    def generate_legal_moves(self, board_data, board):
        """Adds representation for the legal moves to the provided 
        board representation and returns a board object with all the possible spaces the piece can move
        
        Attribues:
            board_data(Board object): an empty board
            board(Board object): the current locations of every piece on the board
        
        Returns:
            type: Board object the passed in board object but now filled with all the possible moves of this piece
        """
        return self.qbr_generate_legal_moves(board_data, board)