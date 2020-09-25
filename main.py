import pygame
import pygame.locals
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0, 0, 102)
TEXT_COLOR = (255, 255, 255)
SCORE_COORDS = (10, 10)
FONT_SIZE = 32

# Initialize pygame
pygame.display.init()
pygame.font.init()

# Create the scren
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Change Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('img/spaceship_logo.png')
pygame.display.set_icon(icon)

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)

def show_score():
    score_text = font.render("Score: {}".format(score), True, TEXT_COLOR)
    screen.blit(score_text, SCORE_COORDS)

def game_over_text():
    text = font.render("Game Over. 'q' to quit.", True, TEXT_COLOR)
    screen.blit(text, (225, 300))

def has_collided(x1, x2, y1, y2, collision_zone):
    distance = math.sqrt(((x2 - x1) ** 2) +
                         ((y2 - y1) ** 2))
    return distance < collision_zone

# Player
class Player():
    def __init__(self):
        self.img = pygame.image.load('img/spaceship_1.png')
        self.x = 368
        self.y = 480
        self.delta_x = 0
        self.captured = False
        self.collision_zone = 64

    def draw(self):
        screen.blit(self.img, (int(self.x), self.y))

    def update_x(self):
        self.x = (self.x + self.delta_x) % 736

    def check_collision(self, x, y):
        self.captured = has_collided(self.x, x, self.y, y,
                                     self.collision_zone)

# Enemy
class Enemy():
    def __init__(self):
        self.img = pygame.image.load('img/enemy_1.png')
        self.x = random.randint(64, 700)
        self.y = random.randint(50, 150)
        self.delta_x = random.randint(2, 9) / 10.0
        self.delta_y = 0
        self.shot = False
        self.collision_zone = 33

    def draw(self):
        screen.blit(self.img, (int(self.x), self.y))

    def check_collision(self, x, y):
        self.shot = has_collided(self.x+32, x, self.y+32, y, self.collision_zone)

    def reset(self):
        self.x = random.randint(64, 700)
        self.y = random.randint(25, 400)

    def descend(self):
        self.y += 10
        self.delta_x *= -1

    def update_x(self):
        self.x += self.delta_x

# Bullet
# Ready - Bullet is not on screen
# Fire - The bullet is moving
class Bullet():
    def __init__(self):
        self.img = pygame.image.load('img/bullet_1.png')
        self.x = 0
        self.y = 480
        self.delta_y = 0.5
        self.state = 'ready'

    def fire(self):
        self.state = 'fire'

    def show(self):
        screen.blit(self.img, (int(self.x+16), int(self.y+10)))

    def reset(self):
        self.y = 480
        self.state = 'ready'

    def update_y(self):
        self.y -= self.delta_y

num_enemies = 6
enemies = [Enemy() for _ in range(num_enemies)]
player = Player()
bullet = Bullet()

# Game Loop
running = True
while running:

    # RGB Color
    screen.fill(BG_COLOR)
    
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_LEFT:
                player.delta_x = -0.3
            if event.key == pygame.K_RIGHT:
                player.delta_x = 0.3
            if event.key == pygame.K_SPACE:
                if bullet.state == 'ready':
                    bullet.x = player.x
                    bullet.fire()
                    bullet.show()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.delta_x = 0

    player.update_x()

    for enemy in enemies:
        enemy.update_x()
        if not 0 <= enemy.x <= 736:
            enemy.descend()

    if bullet.state == 'fire':
        bullet.update_y()
        bullet.show()

    if bullet.y <= 0:
        bullet.reset()

    for enemy in enemies:
        enemy.check_collision(bullet.x, bullet.y)
        
        if enemy.shot:
            bullet.reset()
            score += 1
            enemy.reset()

        if not player.captured:
            player.check_collision(enemy.x, enemy.y)
        else:
            for bad_guy in enemies:
                bad_guy.y = 2000
            game_over_text()
        
        enemy.draw()

    show_score()
    player.draw()
    pygame.display.update()
