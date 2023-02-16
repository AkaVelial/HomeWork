import pygame
from pygame. constants import QUIT

pygame.init()

screen = width, heigth = 800, 600

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
BLUE = 0, 0, 255
RED = 255, 0, 0
main_surface = pygame.display.set_mode(screen)

ball = pygame.Surface((20, 20))
ball.fill((WHITE))
ball_rect = ball.get_rect()
ball_speed = [1, 1]

is_working = True

while is_working:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

    ball_rect = ball_rect.move(ball_speed)

    if ball_rect.bottom >= heigth:
        ball_speed[1] = -ball_speed[1]
        ball.fill((BLUE))

    elif ball_rect.top <= 0:
        ball_speed[1] = -ball_speed[1]
        ball.fill((GREEN))

    elif ball_rect.right >= width:
        ball_speed[0] = -ball_speed[0]
        ball.fill((RED))

    elif ball_rect.left <0:
        ball_speed[0] = -ball_speed[0]
        ball.fill((WHITE))

    main_surface.fill((BLACK))

    main_surface.blit(ball, ball_rect)
    pygame.display.flip()
