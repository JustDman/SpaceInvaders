import pygame

pygame.init()

X = 800
Y = 600

screen = pygame.display.set_mode((X, Y))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

playerImg = pygame.image.load("ship.png")
playerX = 370
playerY = 480


def player(x, y):
    screen.blit(playerImg, (x, y))


running = True
while running:

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                print("Left arrow is pressed")
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                print("Right arrow is pressed")

    player(playerX, playerY)
    pygame.display.update()
