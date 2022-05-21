import math
import random
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('icon.png')
background = pygame.image.load('background.png')
pygame.display.set_icon(icon)

mixer.music.load('background.mp3')
mixer.music.play(-1)

# player data
playerImg = pygame.image.load('ship3.png')
playerX = 368
playerY = 450
xChange = 0
yChange = 0

# enemy data
enemyImg = []
enemyX = []
enemyY = []
enemy_xChange = []
enemy_yChange = []
enemyLives = []
enemy_num = 15
lives = 8

for i in range(enemy_num):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 40))
    enemy_xChange.append(random.uniform(0.8, 2.0))
    enemy_yChange.append(random.randint(10, 30))
    enemyLives.append(lives)

# bullet data
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = playerY
bullet_xChange = 0
bullet_yChange = 5
fire = False

current_score = 0
kills = 0
end_game = False
win_game = False

font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 64)
font3 = pygame.font.Font('freesansbold.ttf', 40)


def showScore():
    score = font.render('SCORE: ' + str(current_score), True, (120, 200, 45))
    screen.blit(score, (10, 10))


def winGame():
    end = font2.render('GAME OVER', True, (150, 200, 145))
    screen.blit(end, (200, 230))

    win = font3.render('YOU WIN', True, (20, 250, 10))
    screen.blit(win, (295, 320))


def loseGame():
    global fire
    global enemy_num

    fire = False
    enemy_num = -1
    end = font2.render('GAME OVER', True, (150, 200, 145))
    screen.blit(end, (200, 230))

    lose = font3.render('YOU LOSE', True, (255, 10, 5))
    screen.blit(lose, (295, 320))


def player():
    screen.blit(playerImg, (playerX, playerY))


def enemy(x, y, j):
    screen.blit(enemyImg[j], (x, y))


def bullet():
    global fire

    fire = True
    screen.blit(bulletImg, (bulletX + 16, bulletY + 10))


def isCollision(y2, y1, x2, x1, collide):
    distance = math.sqrt(math.pow((y2 - y1), 2) + math.pow((x2 - x1), 2))
    if distance <= collide:
        return True


running = True
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xChange -= 2.5
            if event.key == pygame.K_RIGHT:
                xChange += 2.5
            if event.key == pygame.K_SPACE:
                if not fire:
                    shoot = mixer.Sound('fire.mp3')
                    shoot.play()
                    bullet()
                    bulletX = playerX
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                xChange = 0

    for i in range(enemy_num):
        enemyX[i] += enemy_xChange[i]

        if enemyX[i] <= 0:
            enemy_xChange[i] = (random.uniform(0.8, 2.0))
            enemyY[i] += random.randint(10, 40)
        elif enemyX[i] >= 736:
            enemy_xChange[i] = -(random.uniform(0.8, 2.0))
            enemyY[i] += random.randint(10, 30)
        elif enemyY[i] >= 600:
            enemyY[i] = random.randint(0, 40)
            enemyX[i] = random.randint(0, 736)

        collision = isCollision(enemyY[i], bulletY, enemyX[i], bulletX, 32)
        if collision and fire:
            fire = False
            bulletY = playerY
            current_score += 1
            enemyLives[i] -= 1
            kills += 1
            enemyY[i] = random.randint(0, 50)
            enemyX[i] = random.randint(0, 736)

        enemy(enemyX[i], enemyY[i], i)

        if enemyLives[i] == 0:
            enemyY[i] = 1000
            enemyX[i] = 1000

        gameOver = isCollision(playerY, enemyY[i], playerX, enemyX[i], 64)
        if gameOver:
            end_game = True
            dead = mixer.Sound('dead.mp3')
            dead.play()
        if (kills / lives) == enemy_num:
            win_game = True

    playerX += xChange
    if playerX <= 0:
        xChange = 0
    elif playerX >= 736:
        xChange = 0

    if fire:
        bullet()
        bulletY -= bullet_yChange

    if bulletY <= -32:
        fire = False
        bulletY = playerY

    showScore()
    player()
    if win_game:
        winGame()
    if end_game:
        loseGame()

    pygame.display.update()
