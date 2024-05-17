import pygame
import random
from pygame import mixer #to do music work we need it
# Creating first game window
# initialize the pygame
pygame.init()
# Create the screen
screen = pygame.display.set_mode((800, 600))  # Width,Height

# BACKGROUND
background = pygame.image.load('bg.png')

# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)


#  Title and Icon
pygame.display.set_caption("Space Invaders")  # For title
icon = pygame.image.load('ufo.png')  # to change the icon
pygame.display.set_icon(icon)  # to display the icon

# Player
PlayerImg = pygame.image.load("attacker.png")
# X and Y axis
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
# list are made inorder to make multiple enemies.
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []

num_of_ene = 7
for i in range(num_of_ene):
    EnemyImg.append(pygame.image.load("attacking.png"))
    # X and Y axis
    EnemyX.append(random.randint(0, 736))
    EnemyY.append(random.randint(0, 50))
    EnemyX_change.append(0.3)
    EnemyY_change.append(40)

# Bullet
BulletImg = pygame.image.load("bullet.png")
# X and Y axis
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 0.7
# ready-you can not see the bullet on the screen
# Fire - The bullet us currently moving
Bullet_state = "ready"

# SCORE
Score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10
# Game Over text
over_font=pygame.font.Font('freesansbold.ttf',64)

def show_score(x, y):
    score = font.render("Score :" + str(Score_value), True, (255, 255, 255)) #render is used to create a image then by using blit we can display it
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("YOU ARE DEAD" , True, (255, 255, 255))  # render is used to create a image then by using blit we can display it
    screen.blit(over_text, (190, 250))

def player(x, y):
    screen.blit(PlayerImg, (x, y))  # used for drawing the image of player on the screen


def Enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))  # used for drawing the image of player on the screen


def Fire_Bull(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))  # To make sure that the bullet is emerging from the center of player


# To detect collision
def isCollision(X1, Y1, X2, Y2):
    distance = ((X1 - X2) ** 2 + (Y1 - Y2) ** 2) ** 0.5
    if distance < 25:
        return True
    else:
        return False


# By doing this the screen will hang bcz we cant quit(not added function)
'''
while true:
    pass'''

# Now till we have not pressed the close window we will not exit the loop
running = True
while running:
    #   that we want to be persistently shown in window
    screen.fill((0, 0, 0))  # rgb-red,green,blue

    # BACKGROUND IMAGE
    screen.blit(background, (0, 0))
    # CLOSE FUNCTIONALITY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # IF keystroke is pressed check wether its right or left
        # Here we gave the commands of how the player will function when
        # specific keys are pressed and released
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.8
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.8
            #     TO Fire the bullets
            if event.key == pygame.K_SPACE:
                # this is to make sure that the bullet does not change its path whenever we press space bar
                if Bullet_state is "ready":
                    bullet_Sound=mixer.Sound('laser.wav')
                    # as the sound will be for an instant we have not used bullet_music and we have used bullet.sound
                    bullet_Sound.play()
                    # TO get the current x coordinate of the spaceship
                    BulletX = playerX  # To make sure that the bullet does not copys the path of the player
                    Fire_Bull(playerX, BulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # TO MAKE SURE THAT THE PLAYER and ENEMY MUST REMAIN INSIDE THE BOUNDARY
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > 736:  # 800- pixels of image
        playerX = 736
    # TO moving the enemy

    # we are declaring a for loop in order to keep track which enemyx is changed
    for i in range(num_of_ene):

        # Game Over
        if EnemyY[i]>450:
            for j in range(num_of_ene):
                EnemyY[j]==2000
            game_over_text()
            break
        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] < 0:
            EnemyX_change[i] = 0.5
            EnemyY[i] += EnemyY_change[i]  # Making sure enemy moves in Y too
        elif EnemyX[i] > 736:  # 800- pixels of image
            EnemyX_change[i] = -0.5
            EnemyY[i] += EnemyY_change[i]

        # TO check implimentation of collision
        collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            # as the sound will be for an instant we have not used bullet_music and we have used bullet.sound
            explosion_Sound.play()
            BulletY = 480
            Bullet_state = "ready"
            Score_value += 1
            print(Score_value)
            #     To make sure that enemy respawan after the bullet is hit.
            EnemyX[i] = random.randint(0, 736)
            EnemyY[i] = random.randint(0, 50)

        Enemy(EnemyX[i], EnemyY[i], i)

        #     Bullet Movement
        # This condition is used so that we can produce multiple bullets
    if BulletY <= 0:
        BulletY = 480
        Bullet_state = "ready"

    if Bullet_state is "fire":
        Fire_Bull(BulletX, BulletY)
        # TO move the bullet in upward direction
        BulletY -= BulletY_change

    # should be called after fill method
    player(playerX, playerY)
    show_score(textX,textY)
    # TO update the display
    pygame.display.update()
