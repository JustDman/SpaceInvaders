import pygame
import random
import math

from pygame import mixer

pygame.init()

X = 800
Y = 600
SHIP_X = 64
SHIP_Y = 64

ALIEN_X = 64
ALIEN_Y = 64

BULLET_X = 32
BULLET_Y = 32

screen = pygame.display.set_mode((X, Y))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

background = pygame.image.load("background.png").convert_alpha()

mixer.music.load("background.wav")
mixer.music.play(-1)

playerImg = pygame.image.load("ship.png")
playerX = X / 2 - SHIP_X / 2
playerY = Y / 2 + Y / 3
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
modifier = 0
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, X - ALIEN_X))
    enemyY.append(random.randint(Y / 12, Y / 4))
    enemyX_change.append(0.3 + modifier)
    enemyY_change.append(40)

bulletImg = pygame.image.load("bullet.png")
bulletX = playerX + SHIP_X / 2 - BULLET_X / 2
bulletY = Y / 2 + Y / 3
bulletY_change = 2
bullet_state = "ready"

score_value = 0
hidden_score = score_value

font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

font_over = pygame.font.Font("freesansbold.ttf", 64)


def showScore(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (int(x), int(y)))


def player(x, y):
    screen.blit(playerImg, (int(x), int(y)))


def enemy(x, y, index):
    screen.blit(enemyImg[index], (int(x), int(y)))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (int(x), int(y)))


def isCollision(ex, ey, bx, by):
    distance = math.hypot(ex - bx, ey - by)
    if distance < 27:
        return True
    else:
        return False


def gameOverText():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (int(X / 2 - X / 12), int(Y / 2 - Y / 20)))


running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                playerX_change = -1

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                playerX_change = 1

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX + SHIP_X / 2 - BULLET_X / 2
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT or pygame.K_d or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > X - SHIP_X:
        playerX = X - SHIP_X

    for i in range(num_of_enemies):

        if enemyY[i] > Y * 11 / 15:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameOverText()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3 + modifier
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= X - ALIEN_X:
            enemyX_change[i] = -0.3 - modifier
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = Y / 2 + Y / 3
            bullet_state = "ready"
            score_value += 1
            hidden_score += 1
            enemyX[i] = random.randint(0, X - ALIEN_X)
            enemyY[i] = random.randint(Y / 12, Y / 4)
            enemyY_change[i] = 40
        enemy(enemyX[i], enemyY[i], i)

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY < 0:
            bullet_state = "ready"
            bulletY = Y / 2 + Y / 3

    if hidden_score == 5:
        hidden_score = 0
        modifier += 0.1

    player(playerX, playerY)
    showScore(textX, textY)

    pygame.display.update()
