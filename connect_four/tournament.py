import pygame
import sys
import random
import logging
from typing import Optional, Tuple

from .config import *
from .board import *
from .players import *
from .ui import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Connect-Four Tournament Visualizer")

    player1 = GPTAgentPlayer(PLAYER1_NAME)
    player2 = VLLMAgentPlayer(PLAYER2_NAME)
    tlog = logging.getLogger("connect_four.tournament")
    tlog.info(f"Starting tournament: {GAMES} games between {PLAYER1_NAME} and {PLAYER2_NAME}")

    stats = {"p1_wins": 0, "p2_wins": 0, "draws": 0}

    for game in range(GAMES):
        tlog.info(f"=== GAME {game + 1}/{GAMES} ===")
        board = create_board()
        last_move = None
        game_over = False
        p1_is_red = (game % 2 == 0)
        turn = 0 if p1_is_red else 1
        turn_counter = 1

        if p1_is_red:
            player1.symbol, player1.piece_code = "X", 1
            player2.symbol, player2.piece_code = "O", 2
        else:
            player1.symbol, player1.piece_code = "O", 2
            player2.symbol, player2.piece_code = "X", 1

        colours = {1: RED, 2: YELLOW}

        while not game_over:
            tlog.info(f"Game {game + 1}  •  Turn {turn_counter}  •  {'P1' if turn == 0 else 'P2'} to move")
            render(screen, board, colours, last_move, stats)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

            player = player1 if turn == 0 else player2
            piece_code = player.piece_code
            col = player.get_move(board)

            if player.last_error:
                banner(screen, f"Error by {player.name}\n{player.last_error}\nChoosing randomly", 1500)

            if 0 <= col < COLS and is_valid_location(board, col):
                row = get_next_open_row(board, col)
            else:
                player.fallbacks += 1
                banner(screen, f"Invalid move by {player.name}\nChoosing randomly", 1500)
                legal_cols = [c for c in range(COLS) if is_valid_location(board, c)]
                col = random.choice(legal_cols)
                row = get_next_open_row(board, col)

            animate_drop(screen, board, col, row, colours, piece_code, last_move, stats)
            drop_piece(board, row, col, piece_code)
            last_move = (row, col)

            if winning_move(board, piece_code):
                render(screen, board, colours, last_move, stats)
                banner(screen, f"{player.name} won!")
                if player is player1:
                    stats["p1_wins"] += 1
                else:
                    stats["p2_wins"] += 1
                game_over = True
            elif all(board[0][c] != 0 for c in range(COLS)):
                render(screen, board, colours, last_move, stats)
                banner(screen, "Draw!")
                stats["draws"] += 1
                game_over = True
            else:
                turn ^= 1
                turn_counter += 1

        pygame.time.delay(1500)
        tlog.info(f"End of game {game + 1}  •  Score: {stats['p1_wins']}–{stats['draws']}–{stats['p2_wins']}")

    render(screen, board, colours, last_move, stats)
    banner(screen, f"{stats['p1_wins']} : {stats['draws']} : {stats['p2_wins']}")
    banner(screen, f"{PLAYER1_NAME} fallbacks: {player1.fallbacks}  |  {PLAYER2_NAME} fallbacks: {player2.fallbacks}")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

