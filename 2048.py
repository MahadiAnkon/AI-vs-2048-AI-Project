import sys
import pygame
import random
import math
import subprocess

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
score = 0
direction = ""

timer_duration = 2 * 60 + 30
start_time = pygame.time.get_ticks()
lives = 1
moves_without_change = 0
max_moves_without_change = 3
move_time_limit = 5
last_move_time = pygame.time.get_ticks()

def draw_score_board(remaining_time, move_time_limit, lives):
    pygame.draw.rect(sc, (230, 230, 230), [0, 0, wd, 100])

    avatar_img = pygame.image.load("image.png")
    avatar_img = pygame.transform.scale(avatar_img, (80, 80))
    border_rect = avatar_img.get_rect(left=20, centery=50).inflate(10, 10)
    pygame.draw.rect(sc, (0, 0, 0), border_rect)
    avatar_rect = avatar_img.get_rect(left=20, centery=50)
    sc.blit(avatar_img, avatar_rect)

    font = pygame.font.Font("freesansbold.ttf", 24)
    time_text = font.render("Time: {} sec".format(remaining_time), True, (0, 0, 0))
    time_rect = time_text.get_rect(right=wd - 20, centery=50, top=20)
    sc.blit(time_text, time_rect)

    score_text = font.render("Score: {}".format(score), True, (0, 0, 0))
    score_rect = score_text.get_rect(right=wd - 20, centery=80, top=40)
    sc.blit(score_text, score_rect)

    lives_text = font.render("Lives: {}".format(lives), True, (0, 0, 0))
    lives_rect = lives_text.get_rect(right=wd - 20, centery=110, top=60)
    sc.blit(lives_text, lives_rect)

    timeout_radius = 40
    timeout_center = (60, 50)
    timeout_thickness = 100
    timeout_angle = (2 * math.pi) * (move_time_limit / 5)

    progress_surface = pygame.Surface((2 * timeout_radius, 2 * timeout_radius), pygame.SRCALPHA)
    pygame.draw.circle(progress_surface, (0, 0, 0, 0), (timeout_radius, timeout_radius), timeout_radius)
    pygame.draw.arc(
        progress_surface,
        (0, 0, 0, 50),
        pygame.Rect(0, 0, 2 * timeout_radius, 2 * timeout_radius),
        math.pi / 2,
        math.pi / 2 + timeout_angle,
        timeout_thickness,
    )

    sc.blit(progress_surface, (timeout_center[0] - timeout_radius, timeout_center[1] - timeout_radius))


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
                sc.blit(val_txt, textc)


def draw_new(board):
    if any(0 in row for row in board):
        while True:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            if board[row][col] == 0:
                if random.randint(1, 10) == 5:
                    board[row][col] = 4
                else:
                    board[row][col] = 2
                break
    return board


def stack():
    global board
    new_matrix = [[0] * 4 for _ in range(4)]
    for i in range(4):
        fill_position = 0
        for j in range(4):
            if board[i][j] != 0:
                new_matrix[i][fill_position] = board[i][j]
                fill_position += 1
    board = new_matrix


def combine():
    global board
    global score
    for i in range(4):
        for j in range(3):
            if board[i][j] != 0 and board[i][j] == board[i][j + 1]:
                board[i][j] *= 2
                board[i][j + 1] = 0
                score += board[i][j]


def reverse():
    global board
    new_matrix = []
    for i in range(4):
        new_matrix.append([])
        for j in range(4):
            new_matrix[i].append(board[i][3 - j])
    board = new_matrix


def transpose():
    global board
    new_matrix = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            new_matrix[i][j] = board[j][i]
    board = new_matrix


def left():
    stack()
    combine()
    stack()


def right():
    reverse()
    stack()
    combine()
    stack()
    reverse()


def up():
    transpose()
    stack()
    combine()
    stack()
    transpose()


def down():
    transpose()
    reverse()
    stack()
    combine()
    stack()
    reverse()


def take_turn(direction):
    if direction == "left":
        left()
    elif direction == "right":
        right()
    elif direction == "up":
        up()
    elif direction == "down":
        down()
    print(score)


running = True
draw_new_board = True

while running:
    remaining_time = max(timer_duration - (pygame.time.get_ticks() - start_time) // 1000, 0)

    if moves_without_change >= max_moves_without_change or lives == 0 or remaining_time == 0:
        subprocess.Popen(["python", "gameover.py"])
        pygame.display.flip()
        pygame.time.wait(1000)
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                direction = "left"
            elif event.key == pygame.K_RIGHT:
                direction = "right"
            elif event.key == pygame.K_DOWN:
                direction = "down"
            elif event.key == pygame.K_UP:
                direction = "up"

    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - last_move_time) // 1000

    if draw_new_board or init_count < 2:
        board = draw_new(board)
        draw_new_board = False
        init_count += 1
    if direction != "":
        take_turn(direction=direction)
        draw_new_board = True
        direction = ""
        last_move_time = pygame.time.get_ticks()
        moves_without_change = 0
    if elapsed_time >= move_time_limit:
        lives -= 1
        last_move_time = pygame.time.get_ticks()
    draw_board()
    draw_score_board(remaining_time, elapsed_time, lives)
    draw_tiles(board)
    pygame.display.flip()
    timer.tick(fps)