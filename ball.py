import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Catch the Ball')

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Переменные игры
clock = pygame.time.Clock()

# Платформа игрока
player_width = 100
player_height = 10
player_x = (WIDTH - player_width) // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Платформа ИИ
ai_width = 100
ai_height = 10
ai_x = (WIDTH - ai_width) // 2
ai_y = 10
ai_speed = 4

# Мяч
ball_radius = 15
ball_x = WIDTH / 2
ball_y = HEIGHT / 2
ball_speed_x = random.choice([-3, 3])  # Скорость мяча по оси X
ball_speed_y = 3  # Скорость мяча по оси Y

# Счет
score_player = 0
score_ai = 0
game_over = False
game_started = False  # Добавим переменную для отслеживания начала игры


# Функция завершения игры
def game_over_screen(winner):
    font = pygame.font.SysFont(None, 72)
    text = font.render(f"{winner} Wins!", True,
                       (0, 0, 0))
    screen.fill(WHITE)
    screen.blit(text, (WIDTH // 3, HEIGHT // 3))
    pygame.display.update()
    pygame.time.wait(3000)  # Пауза перед выходом из игры


# Главный игровой цикл
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if (event.type == pygame.KEYDOWN and
                event.key == pygame.K_SPACE and not
                game_started):
            game_started = True  # Начало игры при нажатии пробела

    if game_started:
        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Управление ИИ
        if ai_x + ai_width / 2 < ball_x:
            ai_x += ai_speed
        elif ai_x + ai_width / 2 > ball_x:
            ai_x -= ai_speed

        # Двигаем мяч
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Отскок мяча от стен
        if ball_x <= 0 or ball_x >= WIDTH - ball_radius:
            ball_speed_x = -ball_speed_x

        # Отскок мяча от платформы игрока
        if (player_y <= ball_y + ball_radius <= player_y + player_height and
                player_x <= ball_x <= player_x + player_width):
            ball_speed_y = -ball_speed_y

        # Отскок мяча от платформы ИИ
        if (ai_y <= ball_y - ball_radius <= ai_y + ai_height and
                ai_x <= ball_x <= ai_x + ai_width):
            ball_speed_y = -ball_speed_y
            # Мяч не должен проникать в платформу ИИ, если это происходит, исправляем его положение
            if ball_y - ball_radius < ai_y + ai_height:
                ball_y = ai_y + ai_height + ball_radius  # Мяч устанавливается выше платформы ИИ

        # Если мяч упал ниже экрана, проигрывает игрок
        if ball_y > HEIGHT:
            game_over = True
            game_over_screen("AI")  # ИИ выигрывает, если мяч не пойман

        # Если мяч упал выше экрана, проигрывает ИИ
        if ball_y < 0:
            game_over = True
            game_over_screen("Player")  # Игрок выигрывает, если мяч не пойман

        # Отображение объектов
        screen.fill(WHITE)  # Очищаем экран
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width,
                                        player_height))  # Платформа игрока
        pygame.draw.rect(screen, RED, (ai_x, ai_y, ai_width, ai_height))  # Платформа ИИ
        pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)  # Мяч

        # Отображение счета
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Player: {score_player}  AI: {score_ai}",
                                 True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

    else:
        # Если игра не началась, отображаем сообщение о старте
        font = pygame.font.SysFont(None, 72)
        text = font.render("Press Space to Start", True, (0, 0, 0))
        screen.fill(WHITE)
        screen.blit(text, (WIDTH // 4, HEIGHT // 3))

    pygame.display.update()  # Обновляем экран
    clock.tick(60)  # Ограничиваем кадры до 60 в секунду

# Закрытие Pygame
pygame.quit()
