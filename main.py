import os
import random
import math
import pygame

from pygame import mixer

pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)

# initialize the pygame
pygame.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = '50, 50'

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("background.png")

# background music
background_music = mixer.music.load("pacman_chomp.wav")
# mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("player.png")
pygame.display.set_icon(icon)


class Button:
    def __init__(self, color, x, y, width, height, text = ''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline = None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font_button = pygame.font.SysFont("comicsans", 60)
            text = font_button.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        # Pos is the mouse position of a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y * self.height:
                return True

        return False


class EnemyBullet:
    def __init__(self, img, x, y, x_change, y_change, state, fire_timer, max_fire_time):
        self.img = pygame.image.load(img)
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.state = state
        self.fire_timer = fire_timer
        self.max_fire_time = max_fire_time


class Enemy:
    def __init__(self, img, dead_img, dead, x, y, x_change, y_change, dead_pause_time):
        self.bullet = EnemyBullet("bullet_enemy.png", 350, 60, 4, 4, "ready", 0, random.randint(500, 2500))
        self.img = pygame.image.load(img)
        self.dead_img = pygame.image.load(dead_img)
        self.dead = dead
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.dead_pause_time = dead_pause_time


class PlayerBullet:
    def __init__(self, img, x, y, x_change, y_change, state):
        self.img = pygame.image.load(img)
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.state = state


class Player:
    def __init__(self, img, dead_img, x, y, x_change, dead):
        self.bullet = PlayerBullet("bullet.png", 370, 480, 0, 10, "ready")
        self.img = pygame.image.load(img)
        self.dead_img = pygame.image.load(dead_img)
        self.x = x
        self.y = y
        self.x_change = x_change
        self.dead = dead


def add_enemy():
    # new_bullet = EnemyBullet("bullet_enemy.png", 350, 60, 60, 4, "ready")
    new_enemy = Enemy("ghost.png", "dead_ghost.png", False, 350, 60, 4, 65, 1000)
    enemy_list.append(new_enemy)
    # enemy_bullet_list.append(new_bullet)


def remove_enemy(idx):
    enemy_list.pop(idx)


def show_score(x, y):
    score = font.render("score: " + str(score_value), True, (255, 255, 0))
    screen.blit(score, (x, y))


def show_game_over():
    game_over_text = font_game_over.render("GAME OVER", True, (255, 255, 0))
    screen.blit(game_over_text, (200, 200))
    play_button.draw(screen, (0, 0, 0))


def fire_bullet(x, y):
    screen.blit(player.bullet.img, (x + 16, y + 10))


def fire_enemy_bullet(idx, x, y):
    enemy_list[idx].bullet.state = "fire"
    screen.blit(enemy_list[idx].bullet.img, (x + 16, y + 10))


def move_player(x, y):
    if player.dead is False:
        screen.blit(player.img, (x, y))
    else:
        screen.blit(player.dead_img, (x, y))


def move_enemy(idx):
    if enemy_list[idx].dead is False:
        enemy_list[idx].x += enemy_list[idx].x_change
        if enemy_list[idx].x <= 0:
            enemy_list[idx].x_change = 4
            enemy_list[idx].y += enemy_list[idx].y_change
        elif enemy_list[idx].x >= 736:
            enemy_list[idx].x_change = -4
            enemy_list[idx].y += enemy_list[idx].y_change
    else:
        enemy_list[idx].x -= enemy_list[idx].x_change * 2
        if enemy_list[idx].x <= 0:
            enemy_list[idx].x_change = -4
            enemy_list[idx].y -= enemy_list[idx].y_change
        elif enemy_list[idx].x >= 736:
            enemy_list[idx].x_change = 4
            enemy_list[idx].y -= enemy_list[idx].y_change


def hit_enemy(idx):
    collision = is_collision(enemy_list[idx].x, enemy_list[idx].y, player.bullet.x, player.bullet.y)
    if collision:
        hit_sound = mixer.Sound("pacman_eatghost.wav")
        hit_sound.play()
        player.bullet.y = 480
        player.bullet.state = "ready"
        return True

    return False


def hit_player(idx):
    collision = is_collision(player.x, player.y, enemy_list[idx].bullet.x, enemy_list[idx].bullet.y)

    if collision:
        player_death_sound = mixer.Sound("pacman_death.wav")
        player_death_sound.play()
        return True

    return False


def render_enemy(idx):
    if enemy_list[idx].dead:
        screen.blit(enemy_list[idx].dead_img, (enemy_list[idx].x, enemy_list[idx].y))
    else:
        screen.blit(enemy_list[idx].img, (enemy_list[idx].x, enemy_list[idx].y))


def render_enemy_bullet(idx):
    if enemy_list[i].bullet.state is "fire":
        screen.blit(enemy_list[idx].bullet.img, (enemy_list[idx].bullet.x, enemy_list[idx].bullet.y))
        if game_over is False:
            enemy_list[i].bullet.y += enemy_list[i].bullet.y_change


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


player = Player("player.png", "player_dead.png", 370, 480, 0, False)

enemy_list = []
num_of_enemies = 0
max_enemies = 1
enemy_hit_pause_time = 0
all_enemies_deployed = False

score_value = 0

font = pygame.font.Font("freesansbold.ttf", 32)
font_game_over = pygame.font.Font("freesansbold.ttf", 64)
font_play_again = pygame.font.Font("freesansbold.ttf", 48)

textX = 10
textY = 10

clock = pygame.time.Clock()
minutes = 0
seconds = 0
milliseconds = 0
running = True
game_over = False
level = 1
play_button = Button((0, 255, 0), 325, 350, 150, 50, "Play")
pygame.mixer.music.play(-1)
# game loop
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    if level is 1 and num_of_enemies <= 0:
        max_enemies = 6

    """ add enemy every second until max enemies """
    if milliseconds > 1000:
        add_enemy()
        num_of_enemies += 1
        milliseconds = 0
        if num_of_enemies == max_enemies:
            all_enemies_deployed = True;

    tick = clock.tick_busy_loop(60)
    if num_of_enemies < max_enemies:
        milliseconds += tick

    for event in pygame.event.get():

        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            running = False

        if game_over is False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.x_change = -5
                if event.key == pygame.K_RIGHT:
                    player.x_change = 5
                if event.key == pygame.K_SPACE and player.bullet.state is "ready":
                    player.bullet.x = player.x
                    player.bullet.state = "fire"
                    bullet_sound = mixer.Sound("pacman_eatfruit.wav")
                    bullet_sound.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_change = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.is_over(pos):
                game_over = False
                player.dead = False
                num_of_enemies = 0
                milliseconds = 0
                player.x = 350
                all_enemies_deployed = False
                player.x_change = 0
                score = 0
                level = 1
                enemy_list.clear()
                pygame.mixer.music.play(-1)
                print("clicked")

        if event.type == pygame.MOUSEMOTION:
            if play_button.is_over(pos):
                play_button.color = (0, 255, 0)
            else:
                play_button.color = (255, 0, 0)

    if game_over is False:
        player.x += player.x_change
        # clamping bounds of player
        if player.x <= 0:
            player.x = 0
        elif player.x >= 736:
            player.x = 736

    enemy_num_to_remove = -1
    # clamping bounds of enemy
    for i in range(num_of_enemies):

        # game over
        if game_over is False:
            if enemy_list[i].y > 400 or hit_player(i):
                game_over = True
                player.dead = True
                # player_dead_sound = mixer.Sound("pacman_death.wav")
                # player_dead_sound.play()

        if game_over is False:
            move_enemy(i)
            enemy_list[i].bullet.fire_timer += tick

            if enemy_list[i].y <= 0:
                enemy_list[i].dead = True
                if enemy_num_to_remove == -1:
                    enemy_num_to_remove = i

            if enemy_list[i].dead is False:
                if hit_enemy(i):
                    score_value += 1
                    enemy_list[i].dead = True

            if num_of_enemies > 0 and enemy_list[i].bullet.state is "ready" and \
                    enemy_list[i].bullet.fire_timer > enemy_list[i].bullet.max_fire_time and enemy_list[i].dead is False:
                enemy_list[i].bullet.state = "fire"
                enemy_list[i].bullet.x = enemy_list[i].x + 16
                enemy_list[i].bullet.y = enemy_list[i].y + 48
                enemy_list[i].bullet.fire_timer = 0
                enemy_list[i].bullet.max_fire_time = random.randint(500, 2500)

            if enemy_list[i].bullet.y >= player.y + 128:
                enemy_list[i].bullet.state = "ready"

        if game_over:
            show_game_over()
            pygame.mixer.music.stop()

        render_enemy_bullet(i)
        render_enemy(i)

    if enemy_num_to_remove > -1:
        remove_enemy(enemy_num_to_remove)
        num_of_enemies -= 1

    if player.bullet.y <= 0:
        player.bullet.state = "ready"
        player.bullet.y = 480
    if player.bullet.state is "fire":
        fire_bullet(player.bullet.x, player.bullet.y)
        player.bullet.y -= player.bullet.y_change

    move_player(player.x, player.y)
    show_score(textX, textY)

    pygame.display.update()
