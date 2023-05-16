# main.py
# pyInstaller
# pyinstaller --onefile your_script.py
import pygame
import sys
from pong_classes import Paddle, Ball, Game

game_instance = Game()
game_instance.init_pygame()
game_instance.load_assets()
game_instance.setup_game_objects()


def main_menu():
    while True:
        for game_instance.event in pygame.event.get():
            if game_instance.handle_events(game_instance.game_loop):
                return

        # Renderização do menu principal
        game_instance.screen.fill(game_instance.BLACK)
        title_font = pygame.font.Font(game_instance.font_file, 36)  # Escolha a fonte e o tamanho desejados
        title_text = title_font.render("Pong", True, game_instance.WHITE)
        title_rect = title_text.get_rect(center=(game_instance.SCREEN_WIDTH // 2, game_instance.SCREEN_HEIGHT // 4))

        game_instance.screen.blit(title_text, title_rect)

        title_font = pygame.font.Font(game_instance.font_file, 16)
        current_time = pygame.time.get_ticks()

        if current_time % 2000 < 1000:
            title_text1 = title_font.render("Pressione espaço para iniciar", True, game_instance.WHITE)
            title_rect1 = title_text1.get_rect(
                center=(game_instance.SCREEN_WIDTH // 2, game_instance.SCREEN_HEIGHT // 4 + 60))
            game_instance.screen.blit(title_text1, title_rect1)

        pygame.display.flip()


main_menu()