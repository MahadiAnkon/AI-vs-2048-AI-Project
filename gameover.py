import pygame
import subprocess
import sys

pygame.init()

screen_width, screen_height = 400, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Over")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
button_width, button_height = 200, 50

game_over_x = (screen_width - button_width) // 2
game_over_y = (screen_height - button_height) // 2 - 50
main_menu_x = (screen_width - button_width) // 2
main_menu_y = (screen_height - button_height) // 2 + 50

game_over_text = font.render("Game Over", True, (255, 255, 255))
game_over_rect = game_over_text.get_rect(center=(screen_width // 2, game_over_y))

game_over_button = pygame.Rect(main_menu_x, main_menu_y, button_width, button_height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_over_button.collidepoint(mouse_pos):
                subprocess.Popen(["python", "main.py"])
                pygame.quit()
                sys.exit()

    screen.fill((0, 0, 0))
    
    screen.blit(game_over_text, game_over_rect)

    pygame.draw.rect(screen, (255, 0, 0), game_over_button)

    main_menu_text = font.render("Go to Main Menu", True, (255, 255, 255))
    main_menu_rect = main_menu_text.get_rect(center=game_over_button.center)
    screen.blit(main_menu_text, main_menu_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
