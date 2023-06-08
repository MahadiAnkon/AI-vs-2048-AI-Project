import pygame
import subprocess
import sys

pygame.init()

screen_width, screen_height = 400, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Menu")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
button_width, button_height = 200, 50

start_game_x = (screen_width - button_width) // 2
start_game_y = (screen_height - button_height) // 2 - 50
two_minutes_x = (screen_width - button_width) // 2
two_minutes_y = (screen_height - button_height) // 2 + 50

start_game_button = pygame.Rect(start_game_x, start_game_y, button_width, button_height)
two_minutes_button = pygame.Rect(two_minutes_x, two_minutes_y, button_width, button_height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_game_button.collidepoint(mouse_pos):
                subprocess.Popen(["python", "2048.py"])
                pygame.time.wait(2000)
                pygame.quit()
                sys.exit()
            elif two_minutes_button.collidepoint(mouse_pos):
                pass

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 0, 0), start_game_button)
    pygame.draw.rect(screen, (0, 255, 0), two_minutes_button)

    start_game_text = font.render("Start Game", True, (255, 255, 255))
    start_game_rect = start_game_text.get_rect(center=start_game_button.center)
    screen.blit(start_game_text, start_game_rect)

    two_minutes_text = font.render("2 Minutes", True, (255, 255, 255))
    two_minutes_rect = two_minutes_text.get_rect(center=two_minutes_button.center)
    screen.blit(two_minutes_text, two_minutes_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
