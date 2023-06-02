import pygame
import random
from colors import *

pygame.init()

wd = 400
he = 500
sc = pygame.display.set_mode([wd, he])
init_count = 0
timer = pygame.time.Clock()
fps = 60
game_over = False
grid_size = 4
grid_padding = 8
board = [[0 for _ in range(4)] for _ in range(4)]


def draw_score_board():
    pygame.draw.rect(sc, SCORE_BOARD, [0, 0, wd, 100], 0, 0)


def draw_board():
    pygame.draw.rect(sc, GRID_COLOR, [0, 100, wd, he - 100], 0, 0)


def draw_tiles(board):
    for i in range(grid_size):
        for j in range(grid_size):
            val = board[i][j]
            if val <= 2048:
                color = CELL_COLORS[val]
            else:
                color = R
            pygame.draw.rect(sc, color, [j * 95 + 20, i * 95 + 120, 75, 75], 0, 5)
            if val > 0:
                vlen = len(str(val))
                font_size = 48 - (5 * vlen)
                font = pygame.font.Font("freesansbold.ttf", font_size)
                val_txt = font.render(str(val), True, CELL_NUMBER_COLORS[val])
                textc = val_txt.get_rect(center=(j * 95 + 57, i * 95 + 157))
                pygame.draw.rect(sc, color, [j * 95 + 20, i * 95 + 120, 75, 75], 0, 5)
                sc.blit(val_txt, textc)


def draw_new(board):
    if any(0 in row for row in board):
        while True:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            if board[row][col] == 0:
                if random.randint(1, 5) == 5:
                    board[row][col] = 4
                else:
                    board[row][col] = 2
                break
    return board


running = True
draw_new_board = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if draw_new_board or init_count < 2:
        board = draw_new(board)
        draw_new_board = False
        init_count += 1
    draw_board()
    draw_score_board()
    draw_tiles(board)
    pygame.display.flip()
    timer.tick(fps)

pygame.quit()
