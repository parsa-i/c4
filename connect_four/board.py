from typing import List, Optional
from .config import ROWS, COLS

Board = List[List[int]]

def create_board() -> Board:
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def is_valid_location(board: Board, col: int) -> bool:
    return board[0][col] == 0

def get_next_open_row(board: Board, col: int) -> Optional[int]:
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r
    return None

def drop_piece(board: Board, row: int, col: int, piece: int) -> None:
    board[row][col] = piece

def winning_move(board: Board, piece: int) -> bool:
    for c in range(COLS - 3):
        for r in range(ROWS):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    return False
