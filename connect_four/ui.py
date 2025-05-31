import pygame
from typing import Optional, Tuple, Dict
from .config import *
from .board import Board

def draw_scoreboard(screen, colours, wins1, draws, wins2):
    rect = pygame.Rect(0, 0, WINDOW_WIDTH, SCOREBOARD_HEIGHT)
    pygame.draw.rect(screen, colours[1], (0, 0, WINDOW_WIDTH // 2, rect.height))
    pygame.draw.rect(screen, colours[2], (WINDOW_WIDTH // 2, 0, WINDOW_WIDTH // 2, rect.height))
    font_small = pygame.font.SysFont("arial", 24, bold=True)
    font_big = pygame.font.SysFont("arial", 30, bold=True)
    screen.blit(font_small.render(PLAYER1_NAME, True, BLACK), (12, rect.centery - 12))
    screen.blit(font_small.render(PLAYER2_NAME, True, BLACK), (rect.right - 120, rect.centery - 12))
    score_txt = font_big.render(f"{wins1} : {draws} : {wins2}", True, WHITE)
    screen.blit(score_txt, (rect.centerx - score_txt.get_width() // 2, rect.centery - 15))

def draw_board(screen, board, colours, last_pos):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SCOREBOARD_HEIGHT, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (c*SQUARESIZE+SQUARESIZE//2, r*SQUARESIZE+SCOREBOARD_HEIGHT+SQUARESIZE//2), RADIUS)
            piece = board[r][c]
            if piece:
                pygame.draw.circle(screen, colours[piece], (c*SQUARESIZE+SQUARESIZE//2, r*SQUARESIZE+SCOREBOARD_HEIGHT+SQUARESIZE//2), RADIUS)
    if last_pos:
        lr, lc = last_pos
        pygame.draw.circle(screen, GREEN, (lc*SQUARESIZE+SQUARESIZE//2, SCOREBOARD_HEIGHT+lr*SQUARESIZE+SQUARESIZE//2), RADIUS+4, 4)

def render(screen, board, colours, last_pos, stats):
    draw_scoreboard(screen, colours, stats['p1_wins'], stats['draws'], stats['p2_wins'])
    draw_board(screen, board, colours, last_pos)
    pygame.display.update()

def banner(screen, message, msec=2000):
    lines = message.split("\n")
    font = pygame.font.SysFont("arial", 32, bold=True)
    surfaces = [font.render(line, True, WHITE) for line in lines]
    width = max(s.get_width() for s in surfaces) + 30
    height = sum(s.get_height() for s in surfaces) + 20 + (len(lines) - 1) * 5
    backdrop = pygame.Surface((width, height))
    backdrop.fill(BLACK)
    backdrop.set_alpha(190)
    rect = backdrop.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(backdrop, rect)
    y = rect.top + 10
    for surf in surfaces:
        screen.blit(surf, (rect.centerx - surf.get_width() // 2, y))
        y += surf.get_height() + 5
    pygame.display.update()
    pygame.time.delay(msec)

def animate_drop(screen, board, col, row_dest, colours, piece_code, last_pos, stats):
    x = col * SQUARESIZE + SQUARESIZE // 2
    y = SCOREBOARD_HEIGHT - SQUARESIZE
    target_y = SCOREBOARD_HEIGHT + row_dest * SQUARESIZE + SQUARESIZE // 2
    clock = pygame.time.Clock()
    while y < target_y:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        y += DROP_SPEED
        render(screen, board, colours, last_pos, stats)
        pygame.draw.circle(screen, colours[piece_code], (x, int(y)), RADIUS)
        pygame.display.update()
        clock.tick(FPS)
