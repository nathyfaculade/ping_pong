# pong_classes.py
import pygame
from pygame import mixer
import sys


class Paddle(pygame.Rect):
    def __init__(self, x, y, width, height, game_instance):
        super().__init__(x, y, width, height)
        self.screen = game_instance.screen

    def movey(self, dy):
        self.y += dy
        self.clamp_ip(self.screen.get_rect())

    def movex(self, dx):
        self.x += dx


class Ball(pygame.Rect):
    def __init__(self, x, y, size, dx, dy):
        super().__init__(x, y, size, size)
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def reverse_dx(self):
        self.dx = -self.dx

    def reverse_dy(self):
        self.dy = -self.dy


class Game:
    def __init__(self):
        self.mixer = mixer
        self.init_pygame()
        self.load_assets()
        self.setup_game_objects()

    def init_pygame(self):
        pygame.init()
        mixer.init()

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.PADDLE_WIDTH = 10
        self.PADDLE_HEIGHT = 60
        self.BALL_SIZE = 10
        self.PADDLE_SPEED = 4
        self.BALL_SPEED = 5

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.score_a = 0
        self.score_b = 0

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pong")

    def load_assets(self):
        self.font_file = "font/PressStart2P-Regular.ttf"
        self.font = pygame.font.Font(self.font_file, 36)

        self.mixer.music.load("audios/music_game.mp3")
        self.mixer.music.set_volume(0.3)
        self.mixer.music.play(-1)
        self.collision_sound_A = mixer.Sound("audios/Sound_A.wav")
        self.collision_sound_B = mixer.Sound("audios/Sound_B.wav")
        self.point_sound = mixer.Sound("audios/hoohooo.wav")

    def setup_game_objects(self):
        self.paddle_a = Paddle(20, self.SCREEN_HEIGHT // 2 - self.PADDLE_HEIGHT // 2, self.PADDLE_WIDTH,
                               self.PADDLE_HEIGHT, self)
        self.paddle_b = Paddle(self.SCREEN_WIDTH - 20 - self.PADDLE_WIDTH,
                               self.SCREEN_HEIGHT // 2 - self.PADDLE_HEIGHT // 2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT,
                               self)
        self.ball = Ball(self.SCREEN_WIDTH // 2 - self.BALL_SIZE // 2, self.SCREEN_HEIGHT // 2 - self.BALL_SIZE // 2,
                         self.BALL_SIZE, self.BALL_SPEED, self.BALL_SPEED)

    def handle_events(self, action_function=None):
        if self.event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif self.event.type == pygame.KEYDOWN:
            if self.event.key == pygame.K_ESCAPE:
                return True
            elif self.event.key == pygame.K_SPACE:
                if action_function:
                    action_function()
                return True
        return False

    def game_loop(self):
        while True:
            for self.event in pygame.event.get():
                if self.handle_events():
                    return

            self.screen.fill(self.BLACK)
            pygame.draw.rect(self.screen, self.WHITE, self.paddle_a)
            pygame.draw.rect(self.screen, self.WHITE, self.paddle_b)
            pygame.draw.ellipse(self.screen, self.WHITE, self.ball)
            pygame.draw.aaline(self.screen, self.WHITE, (self.SCREEN_WIDTH // 2, 0),
                               (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT))

            keys = pygame.key.get_pressed()

            # Movimento Vertical Paddle A
            if keys[pygame.K_w]:
                self.paddle_a.movey(-self.PADDLE_SPEED)
            if keys[pygame.K_s]:
                self.paddle_a.movey(self.PADDLE_SPEED)

            # Movimento Horizontal Paddle A
            if keys[pygame.K_a] and self.paddle_a.left > 0:
                self.paddle_a.movex(-self.PADDLE_SPEED)
            if keys[pygame.K_d] and self.paddle_a.right < self.SCREEN_WIDTH // 2 - 70:
                self.paddle_a.movex(self.PADDLE_SPEED)

            # Movimento Vertical Paddle B
            if keys[pygame.K_UP]:
                self.paddle_b.movey(-self.PADDLE_SPEED)
            if keys[pygame.K_DOWN]:
                self.paddle_b.movey(self.PADDLE_SPEED)

            # Movimento Horizontal Paddle B
            if keys[pygame.K_LEFT] and self.paddle_b.left > self.SCREEN_WIDTH // 2 + 70:
                self.paddle_b.movex(-self.PADDLE_SPEED)
            if keys[pygame.K_RIGHT] and self.paddle_b.right < self.SCREEN_WIDTH:
                self.paddle_b.movex(self.PADDLE_SPEED)

            # Atualize a posição da bola
            self.ball.move()

            if self.ball.colliderect(self.paddle_a):
                self.ball.left = self.paddle_a.right
                self.ball.reverse_dx()
                self.collision_sound_A.play()

            elif self.ball.colliderect(self.paddle_b):
                self.ball.right = self.paddle_b.left
                self.ball.reverse_dx()
                self.collision_sound_B.play()

            # Bola bater em cima e embaixo
            if self.ball.top <= 0 or self.ball.bottom >= self.SCREEN_HEIGHT:
                self.ball.reverse_dy()

            # Atualizar pontuação
            if self.ball.left <= 0:
                self.score_b += 1
                self.reset_ball()
                # print(f"Score B: {self.score_b}")
                self.point_sound.play()
                if self.score_b == 10:
                    self.end_game(False)

            elif self.ball.right >= self.SCREEN_WIDTH:
                self.score_a += 1
                self.reset_ball()
                # print(f"Score A: {self.score_a}")
                self.point_sound.play()
                if self.score_a == 10:
                    self.end_game(True)

            self.score_text = self.font.render(f"{self.score_a}  {self.score_b}", True, self.WHITE)
            self.score_rect = self.score_text.get_rect(center=(self.SCREEN_WIDTH // 2, 30))
            self.screen.blit(self.score_text, self.score_rect)

            # Atualizar a tela
            pygame.display.flip()

            # Controlar FPS
            clock = pygame.time.Clock()
            clock.tick(60)

    def reset_ball(self):
        self.ball.x = self.SCREEN_WIDTH // 2 - self.BALL_SIZE // 2
        self.ball.y = self.SCREEN_HEIGHT // 2 - self.BALL_SIZE // 2
        self.ball.reverse_dx()

    def reset_game(self):

        self.setup_game_objects()
        self.ball.move()
        self.score_a, self.score_b = 0, 0

    def end_game(self, winner):
        while True:
            for self.event in pygame.event.get():
                if self.handle_events(self.reset_game):
                    return

            # Renderização da tela de fim de jogo
            self.mixer.music.stop()
            self.screen.fill(self.BLACK)
            if winner:
                self.winner_text = "Player 2 Wins!"
            else:
                self.inner_text = "Player 1 Wins!"

            self.winner_font = pygame.font.Font(self.font_file, 36)
            self.winner_render = self.winner_font.render(self.winner_text, True, self.WHITE)
            self.winner_rect = self.winner_render.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 4))
            self.screen.blit(self.winner_render, self.winner_rect)
            pygame.display.flip()
