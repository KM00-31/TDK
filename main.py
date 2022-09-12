import pygame
import random
from pygame import mixer

# initialise the pygame
pygame.init()

#
mixer.music.load('background.wav')
mixer.music.play(-1)

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('2124358.jpg')

# game over screen
game_state = "playing"
Over_screen = pygame.image.load('gameoverr.png')

# game won screen
game_state = "playing"
won_screen = pygame.image.load('winnn.png')

# caption and Icon
pygame.display.set_caption("The Dark Knight")
icon = pygame.image.load('001-spaceship.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('spaceship2.png')
playerX = 370
playerY = 480
playerX_change = 0




# enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 5

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('001-alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# bullet
# bullet not on screen
# bullet been fired currently mmovig
bulletImg = pygame.image.load('001-bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.7
bullet_state = "ready"
brect = bulletImg.get_rect()

#bulletcount
bullet_count = 5
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

# score
score_value = 0
bullet_font = pygame.font.Font('freesansbold.ttf',32)
text_X = 500
text_Y = 10




def show_score(x,y):
    score = font.render("Score:"+str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))

def show_bulletcount(x,y):
    bullets = font.render("batarangs:"+str(bullet_count),True, (255,255,255))
    screen.blit(bullets,(x,y))

def game_over(x,y):
    global game_state
    game_state = "over"
    screen.blit(Over_screen, (0, 0))

def game_won(x,y):
    global game_state
    game_state = "won"
    screen.blit(won_screen, (0, 0))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # IF KEYSTROKE PRESSED CHECK WHETHER R OR L
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.35
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.35
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    if bullet_count >= 1:
                        bullet_sound = mixer.Sound('batarang.wav')
                        bullet_sound.play()
                        bullet_count -= 1
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0



    # RGB - RED GREEN BLUE
    screen.fill((20, 0, 0))

    # background image
    screen.blit(background, (0,0))

    # player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    # enemy movement
    for i in range(no_of_enemies):
        if enemyImg[i].get_rect(x=enemyX[i], y=enemyY[i]).colliderect(playerImg.get_rect(x=playerX, y=playerY)):
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            text_Y = 2999
            textY = 2999
            playerY = 3000
            game_state = "over"


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            if score_value >= 0:
                enemyX_change[i] = 0.3
            if score_value >= 5:
                enemyX_change[i] = 0.35
            if score_value >= 10:
                enemyX_change[i] = 0.4
            if score_value >= 25:
                enemyX_change[i] = 0.45
            if score_value >= 20:
                enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            if score_value >= 0:
                enemyX_change[i] = -0.3
            if score_value >= 5:
                enemyX_change[i] = -0.35
            if score_value >= 10:
                enemyX_change[i] = -0.4
            if score_value >= 15:
                enemyX_change[i] = -0.45
            if score_value >= 20:
                enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]


        # collision
        if enemyImg[i].get_rect(x=enemyX[i], y=enemyY[i]).colliderect(bulletImg.get_rect(x=bulletX, y=bulletY)):
            if bullet_state is "fire":
                bulletY = 480
                bullet_count += 1
                score_value += 1
                bullet_state = "ready"
                if score_value % 5 == 0:
                    enemyY[i] = 30000
                else:
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = 50
                if score_value == 25:
                    text_Y = 2999
                    textY = 2999
                    playerY = 3000
                    game_state = "won"


        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    if game_state is "over":
        game_over(0,0)

    if game_state is "won":
        game_won(0,0)




    player(playerX, playerY)

    show_score(textX,textY)
    show_bulletcount(text_X, text_Y)
    pygame.display.update()
