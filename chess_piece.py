# class definition of a chess piece
# Dane Iwema
# IT327

from chess_utils import BoardInfo
from chess_utils import PieceInfo

class ChessPiece():
    """Universal information and methods for every chess piece
    
    Attribues:
        _row(Integer): the row number
        _col(Integer): the column number
        _color(BoardInfo): a BoardInfo enumerator that represents Black or White
        _label(PieceInfo): a PieceInfo enumerator that represents the piece type
    """

    def __init__(self, c_row_num, c_col_num, c_color, c_label):
        """ChessPiece initializer
        
        Arguments:
            c_row_num(Integer): the row number
            c_col_num(Integer): the column number
            c_color(BoardInfo): a BoardInfo enumerator that represents Black or White
            c_label(PieceInfo): a PieceInfo enumerator that represents the piece type
        """
        self._row = c_row_num
        self._col = c_col_num
        self._color = c_color
        self._label = c_label

    def move(self, new_row, new_col):
        """Sets the Chess Piece's new location
        
        Arguments:
            new_row(Integer): the new row number to move to
            new_col(Integer): the new column number to move to
        """
        self._row = new_row
        self._col = new_col

    def get_color(self):
        """returns the color of the ChessPiece
        
        Returns:
            type: the color of the piece
        """
        return self._color

    def get_label(self):
        """returns the label of the ChessPiece
        
        Returns:
            type: the label of the piece
        """
        return self._label

    def is_legal_move(self, dest_row, dest_col, board):
        """definition for the is_legal_move function that each seperate piece
        will overrite

        Attribues:
            dest_row(Integer): the destination row to move the piece
            dest_col(Integer): the destination column to move the piece
            board(Board object): the current locations of every piece on the board
        
        Returns:
            type: boolean
        """
        return False
    
    def generate_legal_moves(self, pos_moves, board):
        """definition for the generate_legal_moves function that each seperate piece
        will overrite
        
        Attribues:
            pos_moves(Board object): an empty board
            board(Board object): the current locations of every piece on the board
        
        Returns:
            type: Board object the passed in board object but now filled with all the possible moves of this piece
        """
        return pos_moves
    
    def check_take(self, square_type):
        """Checks if a square is either empty or has a black piece, allowing a move there for pieces that can jump for the knight
        
        Arguments:
            square_type(BoardInfo enum): an enumerator from BoardInfo

            Returns:
                type: boolean
        """
        if square_type == BoardInfo.EMPTY or square_type == BoardInfo.BLACK:
            return True
        return False
    
    def search_direction(self, direction, board):
        """searches a given direction and returns a list of all the moves the piece can slide until another piece or the end of the board is reached
        
        Arguments:
            direction(integer): has to be an int 0-7, 0-3 for N, E, S, and W and 4-7 for NE, SE. SW. NW
            board(board Object): the current board object to test each space for another piece
        
            Returns:
                type: a dictionary where the keys are tuples of all the possible moves and the values to the keys are all True
        """
        # the 8 possible directions associated with the output from the determine_direction() method
        directions = [[-1, 0], [0, 1], [1, 0], [0, -1], [-1, 1], [1, 1], [1, -1], [-1, -1]]

        move_row = directions[direction][0] # finds the associated row movement from the given direction
        move_col = directions[direction][1] # finds the associated column movement from the given direction
        row = self._row
        col = self._col
        pos_moves = {}

        # while loop adding the move position to the current position and testing if the space can be moved to and adding the move as a key to the pos_moves dictionary with the value True
        while (-1 < row < 8) and (-1 < col < 8):
            row += move_row
            col += move_col
            square_info = board.get_square_info(row, col)
            if  square_info == BoardInfo.EMPTY:
                pos_moves[(row,col)] = True
            elif square_info == BoardInfo.BLACK:
                pos_moves[(row,col)] = True
                return pos_moves
            elif square_info == BoardInfo.WHITE:
                return pos_moves
        return pos_moves
    
    def determine_direction(self, dest_row, dest_col):
        """evaluates the direction you want to move the piece 
        
        Arguments:
            dest_row(Integer): the destination row to move the piece
            dest_col(Integer): the destination column to move the piece

        Returns:
            type: an single integer from numbers 0-8 representing the direction you want to move the piece
                0-3 are horizontal and vertical directions and 4-7 are diagonal directions, 8 if no movement, 
                does not test for direct diagonal sliding, it its not vertical or horizontal it will return diagonal
        """
        
        # gets the difference in positions and then normalizes the values to -1, 0, or 1
        row_diff = dest_row - self._row
        col_diff = dest_col - self._col
        row_sign = sign(row_diff)
        col_sign = sign(col_diff)

        direction_dict = {
            (-1, 0): 0, (0, 1): 1, (1, 0): 2, (0, -1): 3,  # north=0, east=1, south=2, west=3
            (-1, 1): 4, (1, 1): 5, (1, -1): 6, (-1, -1): 7, # north east=4, south east=5, south west=6, north west=7
            (0, 0): 8
        }

        return direction_dict.get((row_sign, col_sign), 8)
    
    def qbr_is_legal_move(self, dest_row, dest_col, board):
        """Legal move checker for Queen, Bishop, and Rook only
        
        Arguments:
            dest_row(Integer): the destination row to move the piece
            dest_col(Integer): the destination column to move the piece
            board(board Object): the current board object to test each space for another piece

        Returns:
            type: boolean repesting if its a legal move or not
        """
        # the rules for the possible directions the pieces can move in and then gets the bounds depending on the label
        # rook can only move in directions 0-3, the bishop 4-7 and the queen can use all 8
        dir_rules = {'Q':(0, 7), 'B':(4, 7), 'R':(0, 3)} 
        bounds = dir_rules[self._label.value]

        # gets the direction and checks its to the bounds of the posible directions for the piece type
        direction = self.determine_direction(dest_row, dest_col)
        if bounds[0] > direction or direction > bounds[1]:
            return False
        
        # searches the direction the piece wants to move to make sure there are no pieces in the way of the destination
        pos_moves = self.search_direction(direction, board)
        return pos_moves.get((dest_row, dest_col), False)
    
    def qbr_generate_legal_moves(self, board_data, board):
        """Legal move generator for Queen, Bishop, and Rook only
        
        Attribues:
            board_data(Board object): an empty board
            board(Board object): the current locations of every piece on the board
        
        Returns:
            type: Board object the passed in board object but now filled with all the possible moves of this piece
        """
        # adds staring position to the board
        char_label = self._label.value
        board_data[self._row][self._col] = char_label

        # dictionary for the ranges to generate the legal moves for each piece
        move_direction_ranges = {'Q':(8,0), 'B':(4,4), 'R':(4,0)}
        move_range = move_direction_ranges[self._label.value]

        # gets the possible moves from each direction and appends them to the dictionary of possible moves
        pos_moves = {}
        for direction in range(move_range[0]):
            offset = direction + move_range[1]
            pos_moves.update(self.search_direction(offset, board))

        # iterates through the dictionary of possible moves and adds them to the board    
        for move in pos_moves:
            board_data[move[0]][move[1]] = char_label
        return board_data
    
def sign(num):
    """used to normalize the given number
    
    Arguments:
        num(Integer): the number you want to normalize

    Returns:
        type: an integer number representing the normalized version of the number passed
    """
    if num > 0:
        return 1
    if num < 0:
        return -1
    return 0