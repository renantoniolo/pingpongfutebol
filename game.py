import pygame
import random
import sys

# Inicializa o pygame
pygame.init()

# Carrega o som
kick_sound = pygame.mixer.Sound("asset/sound-soccer.mp3")
kick_sound.set_volume(0.1)
kick_sound.play(-1)

# Configurações da tela
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Futebol")

# Cores
WHITE = (255, 255, 255)

import os
# Carregar imagem de fundo
background_img = pygame.image.load(os.path.join('asset', 'background.png'))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Objetos do jogo
ball = pygame.Rect(WIDTH//2 - 10, HEIGHT//2 - 10, 20, 20) # Bola
ball_img = pygame.image.load(os.path.join('asset', 'ball.png'))
ball_img = pygame.transform.scale(ball_img, (20, 20))

player = pygame.Rect(50, HEIGHT//2 - 60, 20, 120)   # Goleiro jogador
player_img = pygame.image.load(os.path.join('asset', 'goalkeeper2.png'))
player_img = pygame.transform.scale(player_img, (20, 120))
opponent = pygame.Rect(WIDTH - 70, HEIGHT//2 - 60, 20, 120)  # Goleiro CPU
opponent_img = pygame.image.load(os.path.join('asset', 'goalkeeper1.png'))
opponent_img = pygame.transform.scale(opponent_img, (20, 120))

ball_speed = [random.choice((4, -4)), random.choice((4, -4))]
player_speed = 0
opponent_speed = 5

# Pontuação
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 74)

show_goal = False
goal_timer = 0
goal_img = pygame.image.load(os.path.join('asset', 'goal.png'))
goal_img = pygame.transform.scale(goal_img, (400, 120))

clock = pygame.time.Clock()

def ball_animation():
    global ball_speed, player_score, opponent_score
    
    # Movimento da bola
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Colisão nas bordas superior/inferior
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] *= -1

    # Gol (bola passou pelos lados)
    global show_goal, goal_timer
    if ball.left <= 0:
        opponent_score += 1
        reset_ball()
        show_goal = True
        goal_timer = pygame.time.get_ticks()
    if ball.right >= WIDTH:
        player_score += 1
        reset_ball()
        show_goal = True
        goal_timer = pygame.time.get_ticks()

    # Colisão com jogador e oponente
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed[0] *= -1

def reset_ball():
    global ball_speed
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_speed = [random.choice((4, -4)), random.choice((4, -4))]

def opponent_ai():
    if opponent.centery < ball.centery:
        opponent.y += opponent_speed
    if opponent.centery > ball.centery:
        opponent.y -= opponent_speed

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Movimentação do jogador
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -6
            if event.key == pygame.K_DOWN:
                player_speed = 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_speed = 0

    # Atualiza posições
    player.y += player_speed
    ball_animation()
    opponent_ai()

    # Impede sair da tela
    if player.top < 0:
        player.top = 0
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
    if opponent.top < 0:
        opponent.top = 0
    if opponent.bottom > HEIGHT:
        opponent.bottom = HEIGHT

    # Desenho na tela
    screen.blit(background_img, (0, 0))  # Fundo do campo

    # Jogadores e bola
    screen.blit(player_img, player)
    screen.blit(opponent_img, opponent)
    screen.blit(ball_img, ball)

    # Mostrar mensagem de Goal como imagem
    if show_goal:
        if pygame.time.get_ticks() - goal_timer < 1500:
            kick_sound.stop()
            goal_sound = pygame.mixer.Sound("asset/sound-goal.mp3")
            goal_sound.set_volume(0.5)
            goal_sound.play()
            goal_rect = goal_img.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(goal_img, goal_rect)
        else:
            show_goal = False

    # Mostrar placar
    player_text = font.render(str(player_score), True, WHITE)
    screen.blit(player_text, (WIDTH//4, 30))
    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(opponent_text, (WIDTH*3//4, 30))

    # Atualiza tela
    pygame.display.flip()
    clock.tick(60)